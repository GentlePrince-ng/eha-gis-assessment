"""Stage 04 - settlement and ward coverage, reconciled against the reported e-tally.

The two sources disagree by roughly a thousand settlements. This stage quantifies
that, and then does the part that actually matters: **classifies why**, claim by
claim, using evidence already in the store rather than assertion.

The classification exists because "the tracks and the e-tally disagree" is not a
finding an Incident Manager can act on. "Eighty-one of these claims come from a
team whose logger had failed, and nine hundred come from days when the team was
demonstrably working elsewhere" are different problems with different responses.

Cause classes, in the order they are tested (first match wins)
-------------------------------------------------------------
``not_in_masterlist``   the e-tally names a settlement the masterlist does not
                        contain, so no coordinate exists and no track can ever
                        confirm it. Unverifiable by construction, not a failure.
``security_excluded``   the settlement was classified inaccessible before the
                        round, yet doses were reported against it.
``logger_failed``       the claiming team had almost no usable fixes that day.
                        Absence of track evidence is explained by the equipment,
                        so the e-tally is the better source for this claim.
``brief_presence``      tracks put the team at the settlement, but for less than
                        the dwell threshold. Presence is real; "visited" is the
                        judgement in dispute.
``near_miss``           usable fixes fall just outside the attribution tolerance
                        (within 250 m). Plausibly a position or tolerance effect
                        rather than an absence.
``team_elsewhere``      the team had ample usable tracking that day and none of
                        it is near this settlement. The strongest class, and the
                        one that needs the most careful language.
``no_track_evidence``   none of the above - no usable tracking, but no
                        demonstrable logger failure either.
"""

from __future__ import annotations

import sys
from pathlib import Path

import duckdb

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config  # noqa: E402


DWELL_MINUTES = 5            # D-009, must match stage 03
NEAR_MISS_M = 250            # a fix this close is plausibly a tolerance effect
LOGGER_FAILED_MAX_FIXES = 60 # under one hour of usable logging on a working day


def build_claim_nearest_fix(con: duckdb.DuckDBPyConnection) -> None:
    """Stage 04a - true distance from each claimed settlement to the claiming team's
    nearest usable fix that day.

    This is deliberately computed against *every* usable fix the team recorded,
    not against the attribution table. The attribution table only contains points
    that matched a settlement, so using it would guarantee that no claim could
    ever be classified as a near miss - and every near miss would be misfiled as
    "team elsewhere", which is the one class that implies the team was not where
    it said it was. Getting this wrong would overstate the accusatory class.
    """
    import numpy as np
    import pandas as pd
    from pyproj import Transformer
    from scipy.spatial import cKDTree

    fixes = con.execute(
        """
        SELECT team_id, CAST(ts AS DATE) AS campaign_date,
               longitude_use AS longitude, latitude_use AS latitude
        FROM track_qa WHERE use_for_coverage
        """
    ).df()
    claims = con.execute(
        """
        SELECT DISTINCT e.team_id, e.settlement_id,
               CAST(e.campaign_date AS DATE) AS campaign_date,
               s.longitude, s.latitude
        FROM etally e JOIN settlement s USING (settlement_id)
        """
    ).df()

    transformer = Transformer.from_crs("EPSG:4326", "EPSG:32632", always_xy=True)

    def to_xy(frame: pd.DataFrame) -> np.ndarray:
        x, y = transformer.transform(frame.longitude.values, frame.latitude.values)
        return np.column_stack([x, y])

    fixes["key"] = fixes.team_id + "|" + fixes.campaign_date.astype(str)
    claims["key"] = claims.team_id + "|" + claims.campaign_date.astype(str)

    trees = {
        key: cKDTree(to_xy(group)) for key, group in fixes.groupby("key")
    }

    rows = []
    for key, group in claims.groupby("key"):
        tree = trees.get(key)
        if tree is None:
            # The team recorded no usable fix at all that day. Distance is
            # undefined rather than infinite, and is left NULL.
            distances = [None] * len(group)
        else:
            distances, _ = tree.query(to_xy(group), k=1)
        for (_, claim), distance in zip(group.iterrows(), distances):
            rows.append(
                {
                    "team_id": claim.team_id,
                    "settlement_id": claim.settlement_id,
                    "campaign_date": claim.campaign_date,
                    "nearest_m": None if distance is None else float(distance),
                }
            )

    con.register("claim_nearest_df", pd.DataFrame(rows))
    con.execute(
        "CREATE OR REPLACE TABLE claim_nearest_fix AS SELECT * FROM claim_nearest_df"
    )


def build_claim_reconciliation(con: duckdb.DuckDBPyConnection) -> None:
    """One row per e-tally claim (team, settlement, day) with its cause class."""
    con.execute(
        f"""
        CREATE OR REPLACE TABLE claim_reconciliation AS
        WITH
        claim AS (
            SELECT team_id, settlement_id, CAST(campaign_date AS DATE) AS campaign_date,
                   sum(doses_administered) AS doses
            FROM etally
            GROUP BY 1, 2, 3
        ),
        -- Usable tracking the claiming team had on the claimed day.
        team_day AS (
            SELECT team_id, CAST(ts AS DATE) AS d,
                   count(*) AS usable_fixes
            FROM track_qa WHERE use_for_coverage
            GROUP BY 1, 2
        ),
        -- Dwell the tracks record for this exact team/settlement/day.
        visit AS (
            SELECT team_id, settlement_id, campaign_date, sum(dwell_minutes) AS dwell
            FROM settlement_visit GROUP BY 1, 2, 3
        ),
        -- Nearest usable fix by that team on that day, computed in stage 04a
        -- against ALL the team's fixes, not only those that matched something.
        -- Deriving it from settlement_visit would have been circular: that table
        -- exists only where a match occurred, so "near miss" could never fire and
        -- every near miss would have been swept into team_elsewhere.
        nearest AS (
            SELECT team_id, settlement_id, campaign_date, nearest_m
            FROM claim_nearest_fix
        )
        SELECT
            c.team_id, c.settlement_id, c.campaign_date, c.doses,
            coalesce(v.dwell, 0)          AS dwell_minutes,
            n.nearest_m,
            coalesce(td.usable_fixes, 0)  AS team_usable_fixes_that_day,
            (m.settlement_id IS NULL)     AS not_in_masterlist,
            (i.settlement_id IS NOT NULL) AS security_excluded,
            CASE
                WHEN m.settlement_id IS NULL                       THEN 'not_in_masterlist'
                WHEN i.settlement_id IS NOT NULL                   THEN 'security_excluded'
                WHEN coalesce(v.dwell,0) >= {DWELL_MINUTES}        THEN 'confirmed'
                WHEN coalesce(td.usable_fixes,0) < {LOGGER_FAILED_MAX_FIXES}
                                                                   THEN 'logger_failed'
                WHEN coalesce(v.dwell,0) > 0                       THEN 'brief_presence'
                WHEN n.nearest_m <= {NEAR_MISS_M}                  THEN 'near_miss'
                WHEN coalesce(td.usable_fixes,0) >= {LOGGER_FAILED_MAX_FIXES}
                                                                   THEN 'team_elsewhere'
                ELSE 'no_track_evidence'
            END AS cause_class
        FROM claim c
        LEFT JOIN visit      v  USING (team_id, settlement_id, campaign_date)
        LEFT JOIN nearest    n  USING (team_id, settlement_id, campaign_date)
        LEFT JOIN team_day   td ON td.team_id = c.team_id AND td.d = c.campaign_date
        LEFT JOIN settlement m  ON m.settlement_id = c.settlement_id
        LEFT JOIN inaccessible i ON i.settlement_id = c.settlement_id;
        """
    )


def build_ward_coverage(con: duckdb.DuckDBPyConnection) -> None:
    """Ward-level coverage from both sources, with the under-5 denominator.

    Settlements missing a target population are counted in the settlement
    columns but excluded from the population columns, and the count of those
    exclusions is carried so a reader can see the denominator is incomplete
    rather than assuming it is whole.
    """
    con.execute(
        f"""
        CREATE OR REPLACE TABLE ward_coverage AS
        WITH visited AS (
            SELECT settlement_id FROM settlement_visit
            GROUP BY settlement_id HAVING sum(dwell_minutes) >= {DWELL_MINUTES}
        ),
        claimed AS (SELECT DISTINCT settlement_id FROM etally),
        doses AS (
            SELECT settlement_id, sum(doses_administered) AS doses
            FROM etally GROUP BY 1
        )
        SELECT
            s.ward_code, any_value(s.ward_name) AS ward_name,
            any_value(s.lga_name) AS lga_name,
            count(*)                                              AS settlements_planned,
            sum(CASE WHEN v.settlement_id IS NOT NULL THEN 1 ELSE 0 END) AS visited_tracks,
            sum(CASE WHEN c.settlement_id IS NOT NULL THEN 1 ELSE 0 END) AS claimed_etally,
            sum(CASE WHEN i.settlement_id IS NOT NULL THEN 1 ELSE 0 END) AS inaccessible,
            sum(s.target_population_under5)                       AS target_under5,
            sum(CASE WHEN s.target_population_under5 IS NULL THEN 1 ELSE 0 END)
                                                                  AS settlements_no_denominator,
            sum(coalesce(d.doses, 0))                             AS doses_reported
        FROM settlement s
        LEFT JOIN visited      v USING (settlement_id)
        LEFT JOIN claimed      c USING (settlement_id)
        LEFT JOIN doses        d USING (settlement_id)
        LEFT JOIN inaccessible i USING (settlement_id)
        GROUP BY s.ward_code;
        """
    )


def main() -> None:
    con = duckdb.connect(str(config.DB_PATH))
    con.execute("INSTALL spatial; LOAD spatial;")

    build_claim_nearest_fix(con)
    build_claim_reconciliation(con)
    build_ward_coverage(con)

    print("\nStage 04 - reconciliation")
    print("=" * 74)

    print("\n  Coverage at settlement level")
    print("  " + "-" * 70)
    print(con.execute(f"""
      SELECT
        (SELECT count(*) FROM settlement)                                AS planned,
        (SELECT count(*) FROM (SELECT settlement_id FROM settlement_visit
           GROUP BY 1 HAVING sum(dwell_minutes) >= {DWELL_MINUTES}))     AS visited_tracks,
        (SELECT count(DISTINCT settlement_id) FROM etally)               AS claimed_etally,
        (SELECT count(*) FROM inaccessible)                              AS inaccessible
    """).df().to_string(index=False))

    print("\n  Why each e-tally claim is or is not confirmed by tracks")
    print("  " + "-" * 70)
    print(con.execute("""
      SELECT cause_class, count(*) AS claims,
             sum(doses)::BIGINT AS doses,
             round(100.0*count(*)/sum(count(*)) OVER (), 1) AS pct_claims
      FROM claim_reconciliation GROUP BY 1 ORDER BY claims DESC
    """).df().to_string(index=False))

    print("\n  Ward-level coverage, the ten widest gaps")
    print("  " + "-" * 70)
    print(con.execute("""
      SELECT ward_code, ward_name, lga_name, settlements_planned AS planned,
             visited_tracks AS tracks, claimed_etally AS etally,
             claimed_etally - visited_tracks AS gap, inaccessible AS inacc
      FROM ward_coverage ORDER BY gap DESC LIMIT 10
    """).df().to_string(index=False))

    print("\n  Dose reconciliation against the planned denominator")
    print("  " + "-" * 70)
    print(con.execute("""
      SELECT sum(doses_reported)::BIGINT AS doses_reported,
             sum(target_under5)::BIGINT  AS target_under5,
             round(100.0*sum(doses_reported)/sum(target_under5),1) AS pct_of_target,
             sum(settlements_no_denominator) AS settlements_without_denominator
      FROM ward_coverage
    """).df().to_string(index=False))

    con.close()


if __name__ == "__main__":
    main()
