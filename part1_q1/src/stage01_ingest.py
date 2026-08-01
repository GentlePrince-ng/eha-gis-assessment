"""Stage 01 - ingest the raw campaign pack into a spatially enabled DuckDB store.

The requirement is that ingestion be *idempotent*: running it twice must not
duplicate records. There is a trap in this dataset that makes the obvious
implementation of that requirement lossy, so the choice is spelled out here and
in DECISIONS.md (D-002).

The trap
--------
The track files overlap. A file named for one campaign day contains fixes for
later days too, so the same team and the same minute appear in more than one
file. Measured on team T01: 72,669 duplicated ``(team_id, timestamp)`` pairs and
**zero** duplicated full rows. The repeated minutes carry *different
coordinates*.

So ``(team_id, timestamp)`` is not a safe identity. Deduplicating on it would
silently discard one of two contradictory position fixes and nothing downstream
would ever know a conflict existed.

The choice
----------
The primary key is a hash of the record exactly as supplied. That gives real
idempotency - re-reading the same file inserts nothing - while keeping both
sides of every contradiction in the store, where the QA stage counts and reports
them.

Ingestion does not make analytical decisions. It records what arrived, and how
much of it disagreed.
"""

from __future__ import annotations

import sys
from pathlib import Path

import duckdb

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config  # noqa: E402


# The seven columns as supplied in every track file, in file order.
TRACK_COLUMNS = [
    "team_id",
    "logger_id",
    "timestamp",
    "longitude",
    "latitude",
    "accuracy_m",
    "speed_kmh",
]


def connect(db_path: Path | None = None) -> duckdb.DuckDBPyConnection:
    """Open the store and load the spatial extension."""
    config.ensure_dirs()
    con = duckdb.connect(str(db_path or config.DB_PATH))
    con.execute("INSTALL spatial; LOAD spatial;")
    return con


def create_schema(con: duckdb.DuckDBPyConnection) -> None:
    """Create tables if absent.

    ``CREATE TABLE IF NOT EXISTS`` rather than ``CREATE OR REPLACE``: dropping
    and rebuilding would make the script trivially idempotent while proving
    nothing about the insert logic. The point is that a second run inserts zero
    rows into an existing table.
    """
    con.execute(
        """
        CREATE TABLE IF NOT EXISTS track_point (
            point_id      VARCHAR PRIMARY KEY,  -- hash of the record as supplied
            team_id       VARCHAR   NOT NULL,
            logger_id     VARCHAR   NOT NULL,
            ts            TIMESTAMP NOT NULL,
            longitude     DOUBLE    NOT NULL,
            latitude      DOUBLE    NOT NULL,
            accuracy_m    DOUBLE,
            speed_kmh     DOUBLE,
            source_file   VARCHAR   NOT NULL,   -- first file this record was seen in
            n_occurrences INTEGER   NOT NULL    -- how many files carried it identically
        );

        CREATE TABLE IF NOT EXISTS ingest_run (
            run_id        INTEGER,
            stage         VARCHAR,
            metric        VARCHAR,
            value         BIGINT
        );
        """
    )


def stage_track_files(con: duckdb.DuckDBPyConnection) -> None:
    """Read every track CSV into a staging table, keyed by content hash.

    Columns are read as text (``all_varchar``) so that the hash is taken over
    the bytes exactly as supplied, before any type coercion could normalise
    them. Casting happens afterwards.
    """
    pattern = str(config.TRACKS_DIR / "*.csv").replace("\\", "/")

    con.execute(
        f"""
        CREATE OR REPLACE TEMP TABLE staging_raw AS
        SELECT *, regexp_extract(filename, '[^/\\\\]+$') AS source_file
        FROM read_csv(
            '{pattern}',
            all_varchar = true,
            filename    = true,
            header      = true
        );
        """
    )

    # One row per distinct record. n_occurrences records how many times the
    # identical record appeared across the pack, so that collapsing duplicates
    # is visible rather than silent.
    hash_expr = "md5(concat_ws('|', " + ", ".join(TRACK_COLUMNS) + "))"

    con.execute(
        f"""
        CREATE OR REPLACE TEMP TABLE staging AS
        SELECT
            {hash_expr}                    AS point_id,
            any_value(team_id)             AS team_id,
            any_value(logger_id)           AS logger_id,
            CAST(any_value(timestamp) AS TIMESTAMP)  AS ts,
            CAST(any_value(longitude)  AS DOUBLE)    AS longitude,
            CAST(any_value(latitude)   AS DOUBLE)    AS latitude,
            CAST(any_value(accuracy_m) AS DOUBLE)    AS accuracy_m,
            CAST(any_value(speed_kmh)  AS DOUBLE)    AS speed_kmh,
            min(source_file)               AS source_file,
            CAST(count(*) AS INTEGER)      AS n_occurrences
        FROM staging_raw
        GROUP BY {hash_expr};
        """
    )


def insert_new_points(con: duckdb.DuckDBPyConnection) -> int:
    """Insert only records not already present. Returns rows inserted."""
    before = con.execute("SELECT count(*) FROM track_point").fetchone()[0]
    con.execute(
        """
        INSERT INTO track_point
        SELECT s.*
        FROM staging s
        WHERE NOT EXISTS (
            SELECT 1 FROM track_point t WHERE t.point_id = s.point_id
        );
        """
    )
    after = con.execute("SELECT count(*) FROM track_point").fetchone()[0]
    return after - before


def load_reference_tables(con: duckdb.DuckDBPyConnection) -> None:
    """Load the settlement masterlist, e-tally, inaccessible list and boundaries.

    These are small, authoritative-as-supplied reference files. They are
    replaced wholesale on each run rather than appended, so re-running cannot
    duplicate them. Nothing is filtered or corrected here - defects in these
    files are findings, and the QA stage reports them.
    """
    con.execute(
        f"""
        CREATE OR REPLACE TABLE settlement AS
          SELECT * FROM read_csv('{_p(config.SETTLEMENTS_CSV)}', header=true);

        CREATE OR REPLACE TABLE etally AS
          SELECT * FROM read_csv('{_p(config.ETALLY_CSV)}', header=true);

        CREATE OR REPLACE TABLE inaccessible AS
          SELECT * FROM read_csv('{_p(config.INACCESSIBLE_CSV)}', header=true);

        CREATE OR REPLACE TABLE ward AS
          SELECT * FROM st_read('{_p(config.BOUNDARIES_GPKG)}', layer='wards');

        CREATE OR REPLACE TABLE lga AS
          SELECT * FROM st_read('{_p(config.BOUNDARIES_GPKG)}', layer='lgas');

        CREATE OR REPLACE TABLE state AS
          SELECT * FROM st_read('{_p(config.BOUNDARIES_GPKG)}', layer='state');
        """
    )


def _p(path: Path) -> str:
    """Forward-slash a path for embedding in SQL (Windows-safe)."""
    return str(path).replace("\\", "/")


def ingest_report(con: duckdb.DuckDBPyConnection, inserted: int) -> dict[str, int]:
    """Counts that show what arrived and how much of it disagreed."""
    q = lambda sql: con.execute(sql).fetchone()[0]  # noqa: E731

    return {
        "track_files_read": q("SELECT count(DISTINCT source_file) FROM staging_raw"),
        "rows_read": q("SELECT count(*) FROM staging_raw"),
        "distinct_records": q("SELECT count(*) FROM staging"),
        "identical_rows_collapsed": q(
            "SELECT coalesce(sum(n_occurrences - 1), 0) FROM staging"
        ),
        "rows_inserted_this_run": inserted,
        "rows_in_store": q("SELECT count(*) FROM track_point"),
        "teams": q("SELECT count(DISTINCT team_id) FROM track_point"),
        # The headline integrity finding: same team, same minute, different position.
        "team_timestamp_collisions": q(
            """
            SELECT coalesce(sum(n - 1), 0) FROM (
                SELECT count(*) AS n
                FROM track_point
                GROUP BY team_id, ts
                HAVING count(*) > 1
            )
            """
        ),
        "points_outside_campaign_window": q(
            f"""
            SELECT count(*) FROM track_point
            WHERE CAST(ts AS DATE) < DATE '{config.CAMPAIGN_START}'
               OR CAST(ts AS DATE) > DATE '{config.CAMPAIGN_END}'
            """
        ),
        "settlements": q("SELECT count(*) FROM settlement"),
        "etally_rows": q("SELECT count(*) FROM etally"),
        "wards": q("SELECT count(*) FROM ward"),
    }


def main() -> None:
    con = connect()
    create_schema(con)

    stage_track_files(con)
    inserted = insert_new_points(con)
    load_reference_tables(con)

    report = ingest_report(con, inserted)

    # ASCII only in console output: the default Windows console codepage is
    # cp1252 and raises UnicodeEncodeError on characters outside it.
    print(f"\nStage 01 - ingest  ->  {config.DB_PATH}")
    print("-" * 58)
    for key, value in report.items():
        print(f"  {key:34s} {value:>12,}")

    # Nothing is dropped without being counted.
    assert report["rows_read"] == (
        report["distinct_records"] + report["identical_rows_collapsed"]
    ), "row accounting does not reconcile"
    print("\n  accounting reconciles: every row read is accounted for")

    con.close()


if __name__ == "__main__":
    main()
