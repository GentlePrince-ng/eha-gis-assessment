"""Stage 02 — apply the documented quality assurance rule set to the track data.

Every rule **flags**. No rule deletes. The pack states twice that records must
not be silently dropped, and the question asks how many points each rule removed
or flagged — which is only answerable if nothing has already vanished.

The output is one row per stored point in ``track_qa``, carrying a boolean per
rule plus a single derived ``use_for_coverage`` column. Downstream stages filter
on that column, so the definition of "usable" lives in exactly one place and can
be changed and re-run.

Thresholds and their justification are in DECISIONS.md D-004; the rejected
alternatives and the measured distributions behind each choice are in
docs/qa_rule_options.md. Nothing here is a default.

A note on rule QA05
-------------------
There is deliberately no positional-accuracy exclusion. Every candidate cut
touches the same eight teams, and a 30 m cut would remove ~62% of each of their
tracks — a quality rule manufacturing a coverage finding. Accuracy is recorded
as a tier and carried into attribution instead, where tolerance scales with a
point's own reported error.
"""

from __future__ import annotations

import sys
from pathlib import Path

import duckdb

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config  # noqa: E402


# --- Thresholds. Every one traceable to DECISIONS.md D-004. ---------------
DUTY_START_HOUR = 7          # D-004b, inclusive
DUTY_END_HOUR = 17           # D-004b, exclusive -> 07:00-16:59
SPEED_LIMIT_KMH = 15.0       # D-004c
GAP_INTERRUPTION_S = 300     # D-004e, 5 minutes
GAP_OUTAGE_S = 900           # D-004e, 15 minutes
ACCURACY_TIER_BOUNDARY_M = 20.0   # D-004d: labels the two logger tiers, excludes nothing


def build_qa_table(con: duckdb.DuckDBPyConnection) -> None:
    """One row per point, one column per rule, plus the derived usability flag."""
    # Qualified with the alias: the SELECT joins two tables that both carry `ts`.
    window = (
        f"CAST(t.ts AS DATE) BETWEEN DATE '{config.CAMPAIGN_START}' "
        f"AND DATE '{config.CAMPAIGN_END}'"
    )

    con.execute(
        f"""
        CREATE OR REPLACE TABLE track_qa AS
        WITH
        -- Minutes carrying more than one fix for the same team. Their positions
        -- disagree, so any speed derived across them is meaningless.
        conflicted AS (
            SELECT team_id, ts
            FROM track_point
            GROUP BY team_id, ts
            HAVING count(*) > 1
        ),
        -- Implied speed is only evaluable on a conflict-free consecutive pair.
        -- Where it cannot be evaluated it stays NULL - recorded as unknown
        -- rather than quietly treated as passing.
        clean_seq AS (
            SELECT
                t.point_id, t.team_id, t.ts,
                st_point(t.longitude, t.latitude) AS geom,
                lag(st_point(t.longitude, t.latitude))
                    OVER (PARTITION BY t.team_id ORDER BY t.ts) AS geom_prev,
                date_diff('second', lag(t.ts)
                    OVER (PARTITION BY t.team_id ORDER BY t.ts), t.ts) AS dt_s
            FROM track_point t
            LEFT JOIN conflicted c
                   ON c.team_id = t.team_id AND c.ts = t.ts
            WHERE c.team_id IS NULL
        ),
        implied AS (
            SELECT
                point_id,
                CASE WHEN geom_prev IS NOT NULL AND dt_s > 0
                     THEN st_distance_sphere(geom, geom_prev) / dt_s * 3.6
                END AS implied_speed_kmh,
                dt_s
            FROM clean_seq
        )
        SELECT
            t.point_id,
            t.team_id,
            t.ts,

            -- QA01  outside the stated campaign window            (excludes)
            NOT ({window})                                   AS qa01_out_of_window,

            -- QA02  outside duty hours 07:00-16:59               (excludes)
            (extract(hour FROM t.ts) <  {DUTY_START_HOUR}
             OR extract(hour FROM t.ts) >= {DUTY_END_HOUR})  AS qa02_out_of_duty_hours,

            -- QA03  logger-reported speed implausible            (excludes)
            (t.speed_kmh > {SPEED_LIMIT_KMH})                AS qa03_speed_reported,

            -- QA04  speed implied by consecutive fixes           (excludes when evaluable)
            (i.implied_speed_kmh > {SPEED_LIMIT_KMH})        AS qa04_speed_implied,
            (i.implied_speed_kmh IS NULL)                    AS qa04_not_evaluable,
            i.implied_speed_kmh,

            -- QA05  accuracy tier                                (flags only, never excludes)
            CASE WHEN t.accuracy_m > {ACCURACY_TIER_BOUNDARY_M}
                 THEN 'degraded' ELSE 'normal' END           AS qa05_accuracy_tier,
            t.accuracy_m,

            -- QA06  minute in dispute: same team, same minute, different position
            (c.team_id IS NOT NULL)                          AS qa06_timestamp_conflict,

            -- QA07  gap since the previous fix                   (flags)
            (i.dt_s > {GAP_INTERRUPTION_S})                  AS qa07_gap_interruption,
            (i.dt_s > {GAP_OUTAGE_S})                        AS qa07_gap_outage,
            i.dt_s                                           AS gap_seconds

        FROM track_point t
        LEFT JOIN implied    i ON i.point_id = t.point_id
        LEFT JOIN conflicted c ON c.team_id  = t.team_id AND c.ts = t.ts;
        """
    )

    # A point is usable for coverage attribution when no *excluding* rule fires.
    # Accuracy (QA05), conflicts (QA06) and gaps (QA07) deliberately do not
    # exclude - they are carried forward for the attribution stage to weigh.
    con.execute(
        """
        ALTER TABLE track_qa ADD COLUMN use_for_coverage BOOLEAN;
        UPDATE track_qa SET use_for_coverage =
            NOT qa01_out_of_window
        AND NOT qa02_out_of_duty_hours
        AND NOT qa03_speed_reported
        AND NOT coalesce(qa04_speed_implied, FALSE);
        """
    )


# The rule table, declared once. Adding a rule means adding a row here and a
# column in build_qa_table - not editing a query. Disposition is the honest
# distinction the question asks for: which rules removed points and which only
# marked them.
RULES = [
    ("QA01 outside campaign window",   "exclude",   "qa01_out_of_window"),
    ("QA02 outside duty hours",        "exclude",   "qa02_out_of_duty_hours"),
    ("QA03 reported speed > 15 km/h",  "exclude",   "qa03_speed_reported"),
    ("QA04 implied speed > 15 km/h",   "exclude",   "coalesce(qa04_speed_implied, FALSE)"),
    ("QA04 implied speed unevaluable", "note",      "qa04_not_evaluable"),
    ("QA05 degraded accuracy tier",    "flag only", "qa05_accuracy_tier = 'degraded'"),
    ("QA06 minute in dispute",         "flag only", "qa06_timestamp_conflict"),
    ("QA07 gap > 5 min",               "flag only", "coalesce(qa07_gap_interruption, FALSE)"),
    ("QA07 gap > 15 min",              "flag only", "coalesce(qa07_gap_outage, FALSE)"),
]


def rule_summary(con: duckdb.DuckDBPyConnection) -> list[tuple[str, str, int]]:
    """Points affected by each rule, with its disposition."""
    counts = ", ".join(
        f"sum(CAST({expr} AS INT)) AS r{i}" for i, (_, _, expr) in enumerate(RULES)
    )
    row = con.execute(f"SELECT {counts} FROM track_qa").fetchone()
    return [
        (name, disposition, int(count))
        for (name, disposition, _), count in zip(RULES, row)
    ]


def main() -> None:
    con = duckdb.connect(str(config.DB_PATH))
    con.execute("INSTALL spatial; LOAD spatial;")

    build_qa_table(con)

    total = con.execute("SELECT count(*) FROM track_qa").fetchone()[0]
    usable = con.execute(
        "SELECT count(*) FROM track_qa WHERE use_for_coverage"
    ).fetchone()[0]

    print("\nStage 02 - quality assurance")
    print("-" * 72)
    for name, disposition, points in rule_summary(con):
        print(f"  {name:34s} {disposition:10s} {points:>10,}")

    print("-" * 72)
    print(f"  {'points in store':34s} {'':10s} {total:>10,}")
    print(f"  {'usable for coverage':34s} {'':10s} {usable:>10,}"
          f"   ({100*usable/total:.1f}%)")

    # No point is dropped: every stored point has exactly one QA row.
    assert total == con.execute("SELECT count(*) FROM track_point").fetchone()[0], \
        "QA table does not cover every stored point"
    print("\n  every stored point has a QA row - nothing dropped")

    con.close()


if __name__ == "__main__":
    main()
