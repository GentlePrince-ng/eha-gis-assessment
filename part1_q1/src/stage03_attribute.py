"""Stage 03 — attribute cleaned track points to planned settlements.

Method: buffered proximity with an **accuracy-scaled radius**. Each usable point
searches a radius of ``BASE_TOLERANCE_M + K_ACCURACY * accuracy_m``, so a fix the
logger reports as poor is given a correspondingly wider benefit of the doubt
rather than being excluded outright (DECISIONS.md D-004d, D-005).

Why scaled rather than fixed: at equivalent reach the scaled rule found 1,071
settlements with 253 ambiguous points, against 1,069 with 501 for a fixed 100 m
radius. Same coverage, half the ambiguity — it dominates rather than trades.

Why buffered proximity rather than a settlement micro-grid: the masterlist gives
settlements as *points*, not extents, so there is no footprint to grid. A micro
grid would require inventing settlement boundaries from a spacing heuristic,
which would embed a stronger assumption than the tolerance it replaced.

All geometry is computed in EPSG:32632 (WGS 84 / UTM zone 32N) — D-003.

Ambiguity
---------
Where a point falls inside more than one settlement's radius it is attributed to
the **nearest**, and the number of candidates is recorded. Attributing to all
candidates would double-count coverage; discarding the point would throw away a
real visit. The count is reported so the reader can judge the effect rather than
take the rule on trust.
"""

from __future__ import annotations

import sys
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd
from scipy.spatial import cKDTree

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config  # noqa: E402


PROJECTED_CRS = "EPSG:32632"   # D-003
BASE_TOLERANCE_M = 50.0        # D-005
K_ACCURACY = 2.0               # D-005

# Dwell thresholds reported side by side. "Visited" is a judgement about how much
# presence constitutes a visit, so the result is given at several values rather
# than at one silently chosen number.
DWELL_THRESHOLDS_MIN = [1, 3, 5, 10, 15]


def load_usable_points(con: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    """Points that survived the QA rule set, with the accuracy that scales their radius."""
    return con.execute(
        """
        SELECT q.point_id, q.team_id, q.ts, q.accuracy_m,
               t.longitude, t.latitude
        FROM track_qa q
        JOIN track_point t USING (point_id)
        WHERE q.use_for_coverage
        """
    ).df()


def project(lon: np.ndarray, lat: np.ndarray) -> np.ndarray:
    """Longitude/latitude in EPSG:4326 to projected metres in EPSG:32632."""
    from pyproj import Transformer

    transformer = Transformer.from_crs("EPSG:4326", PROJECTED_CRS, always_xy=True)
    x, y = transformer.transform(lon, lat)
    return np.column_stack([x, y])


def attribute_points(points: pd.DataFrame, settlements: pd.DataFrame) -> pd.DataFrame:
    """Nearest settlement within each point's own accuracy-scaled radius.

    Returns one row per *matched* point. Points matching nothing are absent by
    design — they are counted in the report, not silently dropped, and they are
    a real finding (a team was somewhere no planned settlement sits).
    """
    settlement_xy = project(settlements.longitude.values, settlements.latitude.values)
    point_xy = project(points.longitude.values, points.latitude.values)

    tree = cKDTree(settlement_xy)
    radii = BASE_TOLERANCE_M + K_ACCURACY * points.accuracy_m.values

    # One ball query per point, each with its own radius.
    candidates = tree.query_ball_point(point_xy, r=radii)

    matched_row, matched_settlement, distance_m, n_candidates = [], [], [], []
    for row_index, candidate_indices in enumerate(candidates):
        if not candidate_indices:
            continue
        candidate_indices = np.asarray(candidate_indices)
        d = np.linalg.norm(settlement_xy[candidate_indices] - point_xy[row_index], axis=1)
        nearest = int(np.argmin(d))
        matched_row.append(row_index)
        matched_settlement.append(int(candidate_indices[nearest]))
        distance_m.append(float(d[nearest]))
        n_candidates.append(len(candidate_indices))

    return pd.DataFrame(
        {
            "point_id": points.point_id.values[matched_row],
            "team_id": points.team_id.values[matched_row],
            "ts": points.ts.values[matched_row],
            "settlement_id": settlements.settlement_id.values[matched_settlement],
            "distance_m": distance_m,
            "n_candidates": n_candidates,
        }
    )


def write_tables(con: duckdb.DuckDBPyConnection, attribution: pd.DataFrame) -> None:
    """Persist the point-level attribution and the settlement-visit rollup."""
    con.register("attribution_df", attribution)
    con.execute("CREATE OR REPLACE TABLE point_attribution AS SELECT * FROM attribution_df")

    # Dwell is counted in DISTINCT minutes. Minutes in dispute carry more than
    # one fix, and counting fixes would inflate presence for exactly the teams
    # whose data is least trustworthy.
    con.execute(
        """
        CREATE OR REPLACE TABLE settlement_visit AS
        SELECT
            settlement_id,
            team_id,
            CAST(ts AS DATE)        AS campaign_date,
            count(*)                AS n_fixes,
            count(DISTINCT ts)      AS dwell_minutes,
            min(ts)                 AS first_fix,
            max(ts)                 AS last_fix,
            round(min(distance_m),1) AS nearest_fix_m,
            sum(CASE WHEN n_candidates > 1 THEN 1 ELSE 0 END) AS ambiguous_fixes
        FROM point_attribution
        GROUP BY settlement_id, team_id, CAST(ts AS DATE)
        """
    )


def coverage_by_dwell(con: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    """Settlements judged visited at each candidate dwell threshold."""
    total_settlements = con.execute("SELECT count(*) FROM settlement").fetchone()[0]
    etally_settlements = con.execute(
        "SELECT count(DISTINCT settlement_id) FROM etally"
    ).fetchone()[0]

    rows = []
    for minutes in DWELL_THRESHOLDS_MIN:
        visited, agree, tracks_only, etally_only = con.execute(
            f"""
            WITH v AS (
                SELECT settlement_id
                FROM settlement_visit
                GROUP BY settlement_id
                HAVING sum(dwell_minutes) >= {minutes}
            ),
            e AS (SELECT DISTINCT settlement_id FROM etally)
            SELECT
                (SELECT count(*) FROM v),
                (SELECT count(*) FROM v  WHERE settlement_id IN (SELECT settlement_id FROM e)),
                (SELECT count(*) FROM v  WHERE settlement_id NOT IN (SELECT settlement_id FROM e)),
                (SELECT count(*) FROM e  WHERE settlement_id NOT IN (SELECT settlement_id FROM v))
            """
        ).fetchone()
        rows.append(
            {
                "dwell_min": minutes,
                "settlements_visited": visited,
                "pct_of_masterlist": round(100 * visited / total_settlements, 1),
                "agree_with_etally": agree,
                "tracks_only": tracks_only,
                "etally_only": etally_only,
            }
        )
    return pd.DataFrame(rows).assign(etally_settlements=etally_settlements)


def main() -> None:
    con = duckdb.connect(str(config.DB_PATH))
    con.execute("INSTALL spatial; LOAD spatial;")

    points = load_usable_points(con)
    settlements = con.execute(
        "SELECT settlement_id, longitude, latitude FROM settlement"
    ).df()

    attribution = attribute_points(points, settlements)
    write_tables(con, attribution)

    matched = len(attribution)
    unmatched = len(points) - matched
    ambiguous = int((attribution.n_candidates > 1).sum())

    print("\nStage 03 - attribution")
    print("-" * 66)
    print(f"  CRS                              {PROJECTED_CRS}")
    print(f"  tolerance                        {BASE_TOLERANCE_M:.0f} m + "
          f"{K_ACCURACY:.0f} x reported accuracy")
    print(f"  usable points in                 {len(points):>10,}")
    print(f"  matched to a settlement          {matched:>10,}"
          f"   ({100*matched/len(points):.1f}%)")
    print(f"  matched nothing within tolerance {unmatched:>10,}"
          f"   ({100*unmatched/len(points):.1f}%)")
    print(f"  had more than one candidate      {ambiguous:>10,}"
          f"   ({100*ambiguous/max(matched,1):.2f}% of matched)")
    print(f"  median distance to settlement    "
          f"{attribution.distance_m.median():>10.1f} m")

    print("\n  Settlements judged visited, by dwell threshold")
    print("  " + "-" * 64)
    print(coverage_by_dwell(con).to_string(index=False))

    # Accounting: every matched point belongs to exactly one settlement-visit row.
    fixes_in_rollup = con.execute("SELECT sum(n_fixes) FROM settlement_visit").fetchone()[0]
    assert fixes_in_rollup == matched, "settlement_visit does not account for every match"
    print("\n  accounting reconciles: every matched fix appears in exactly one visit row")

    con.close()


if __name__ == "__main__":
    main()
