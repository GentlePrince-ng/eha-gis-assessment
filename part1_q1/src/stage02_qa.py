"""Stage 02 - apply the documented quality assurance rule set to the track data.

Every rule **flags**. No rule deletes. The pack states twice that records must
not be silently dropped, and the question asks how many points each rule removed
or flagged - which is only answerable if nothing has already vanished.

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
tracks - a quality rule manufacturing a coverage finding. Accuracy is recorded
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
STATIONARY_RUN_MIN = 5            # D-004g: sustained stationary period, in minutes
CORROBORATION_RADIUS_M = 500      # D-008
CORROBORATION_WINDOW_MIN = 10     # D-008


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


def apply_geographic_validity(con: duckdb.DuckDBPyConnection) -> None:
    """Rule QA08 - coordinates that are geographically impossible (DECISIONS.md D-008).

    Two defects that every other rule passes, because a null-island record has a
    plausible accuracy, a walking speed, an in-window timestamp and a clean
    60-second interval. Only geography catches them.

    Membership is derived from the state polygon rather than a hardcoded bounding
    box: a point is *transposed* if it lies outside the state as supplied and
    inside it once the axes are exchanged. The rule therefore states its own
    logic instead of embedding magic numbers.

    Transposed points are corrected only where corroborated - the swapped
    position must fall within CORROBORATION_RADIUS_M of another fix by the same
    team within CORROBORATION_WINDOW_MIN. Correction is scripted, applied here
    rather than to the source file, keeps the original coordinates alongside,
    and is reversible.
    """
    con.execute(
        f"""
        CREATE OR REPLACE TEMP TABLE geo_status AS
        SELECT
            t.point_id, t.team_id, t.ts, t.longitude, t.latitude,
            CASE
                WHEN t.longitude = 0 AND t.latitude = 0 THEN 'null_island'
                WHEN NOT st_within(st_point(t.longitude, t.latitude), s.geom)
                     AND st_within(st_point(t.latitude, t.longitude), s.geom) THEN 'transposed'
                WHEN NOT st_within(st_point(t.longitude, t.latitude), s.geom) THEN 'outside_area'
                ELSE 'ok'
            END AS status
        FROM track_point t CROSS JOIN state s;

        -- Corroboration: does the swapped position sit near a contemporaneous
        -- fix by the same team? Only geometrically sound points may corroborate.
        CREATE OR REPLACE TEMP TABLE corroborated AS
        SELECT b.point_id
        FROM geo_status b
        JOIN geo_status g
          ON  g.team_id = b.team_id
         AND  g.status  = 'ok'
         AND  g.ts BETWEEN b.ts - INTERVAL {CORROBORATION_WINDOW_MIN} MINUTE
                       AND b.ts + INTERVAL {CORROBORATION_WINDOW_MIN} MINUTE
        WHERE b.status = 'transposed'
        GROUP BY b.point_id
        HAVING min(st_distance_sphere(
                   st_point(b.latitude, b.longitude),
                   st_point(g.longitude, g.latitude))) <= {CORROBORATION_RADIUS_M};
        """
    )

    con.execute(
        """
        ALTER TABLE track_qa ADD COLUMN qa08_status  VARCHAR;
        ALTER TABLE track_qa ADD COLUMN longitude_use DOUBLE;
        ALTER TABLE track_qa ADD COLUMN latitude_use  DOUBLE;

        UPDATE track_qa q SET
            qa08_status = CASE
                WHEN g.status = 'transposed' AND c.point_id IS NOT NULL
                     THEN 'transposed_corrected'
                WHEN g.status = 'transposed' THEN 'transposed_uncorroborated'
                ELSE g.status
            END,
            -- Corrected coordinates for downstream use. The originals stay
            -- untouched in track_point; nothing is overwritten.
            longitude_use = CASE WHEN g.status='transposed' AND c.point_id IS NOT NULL
                                 THEN g.latitude  ELSE g.longitude END,
            latitude_use  = CASE WHEN g.status='transposed' AND c.point_id IS NOT NULL
                                 THEN g.longitude ELSE g.latitude  END
        FROM geo_status g
        LEFT JOIN corroborated c ON c.point_id = g.point_id
        WHERE q.point_id = g.point_id;
        """
    )


def apply_stationary_clusters(con: duckdb.DuckDBPyConnection) -> None:
    """Rule QA09 - sustained stationary periods (DECISIONS.md D-004g).

    Named explicitly in the question's minimum rule set. It is the one rule here
    that is **not** primarily a defect detector, because for house-to-house
    vaccination a stationary period is also the *visit* signal - a team stopped
    for several minutes is what "visited" looks like in GPS. Treating stationary
    points as noise would discard the evidence coverage depends on.

    "Stationary" is defined against the reading's **own reported accuracy**: a
    step smaller than the device's stated error is movement indistinguishable
    from measurement jitter. That avoids a fixed metre threshold, which would
    call the 36 m loggers stationary far too readily and the 8 m loggers rarely.

    Runs are flagged, never excluded. Whether a given run means "worked here" or
    "logger sat in a vehicle" depends on settlement context, which does not
    exist until attribution - so the rule marks and counts, and stage 03 decides.
    """
    con.execute(
        f"""
        CREATE OR REPLACE TEMP TABLE stationary AS
        WITH stepped AS (
            SELECT point_id, team_id, ts,
                   CASE WHEN st_distance_sphere(
                            st_point(longitude_use, latitude_use),
                            lag(st_point(longitude_use, latitude_use))
                              OVER (PARTITION BY team_id ORDER BY ts)
                        ) < accuracy_m THEN 1 ELSE 0 END AS still
            FROM track_qa
            WHERE use_for_coverage IS NULL OR use_for_coverage
        ),
        grouped AS (
            SELECT point_id, team_id, still,
                   row_number() OVER (PARTITION BY team_id ORDER BY ts)
                 - row_number() OVER (PARTITION BY team_id, still ORDER BY ts) AS run_id
            FROM stepped
        )
        SELECT point_id,
               count(*) OVER (PARTITION BY team_id, run_id) AS run_minutes
        FROM grouped WHERE still = 1;
        """
    )
    con.execute(
        f"""
        ALTER TABLE track_qa ADD COLUMN stationary_run_minutes INTEGER;
        UPDATE track_qa q SET stationary_run_minutes = s.run_minutes
        FROM stationary s WHERE s.point_id = q.point_id;
        ALTER TABLE track_qa ADD COLUMN qa09_stationary_cluster BOOLEAN;
        UPDATE track_qa SET qa09_stationary_cluster =
            coalesce(stationary_run_minutes, 0) >= {STATIONARY_RUN_MIN};
        """
    )


def set_usability(con: duckdb.DuckDBPyConnection) -> None:
    """A point is usable when no *excluding* rule fires.

    Accuracy (QA05), conflicts (QA06) and gaps (QA07) deliberately do not
    exclude - they are carried forward for the attribution stage to weigh.
    QA08 excludes only what cannot be repaired: null island, points outside the
    area with no transposition explanation, and the transposed points whose
    correction could not be corroborated.
    """
    con.execute(
        """
        ALTER TABLE track_qa ADD COLUMN use_for_coverage BOOLEAN;
        UPDATE track_qa SET use_for_coverage =
            NOT qa01_out_of_window
        AND NOT qa02_out_of_duty_hours
        AND NOT qa03_speed_reported
        AND NOT coalesce(qa04_speed_implied, FALSE)
        AND qa08_status IN ('ok', 'transposed_corrected');
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
    ("QA08a null island (0,0)",        "exclude",   "qa08_status = 'null_island'"),
    ("QA08b transposed, corrected",    "correct",   "qa08_status = 'transposed_corrected'"),
    ("QA08b transposed, uncorrob.",    "exclude",   "qa08_status = 'transposed_uncorroborated'"),
    # QA08c is a finding, not a corruption: median 10.7 km outside the state
    # boundary, up to 70 km, overwhelmingly on post-campaign dates and
    # concentrated in the eight teams whose loggers were never switched off.
    # Real movement outside the operational area, not a bad coordinate.
    ("QA08c outside operational area", "exclude",   "qa08_status = 'outside_area'"),
    # QA09 flags only. It marks the visit signal as much as a defect - see the
    # function docstring and DECISIONS.md D-004g.
    ("QA09 stationary cluster >= 5 min", "flag only", "qa09_stationary_cluster"),
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
    apply_geographic_validity(con)
    set_usability(con)
    apply_stationary_clusters(con)

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
