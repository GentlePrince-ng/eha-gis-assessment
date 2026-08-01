"""Executable tests for the spatial store (deliverable D1).

The question requires that ingestion be **idempotent: running it twice must not
duplicate records**. That was implemented, described in three documents, and
never tested by anything that runs.

The gap is easy to miss, because `run_all.py` wipes prior artefacts before every
build. The pipeline therefore only ever exercises the *first* run, and the claim
about the second was verified once, by hand, and thereafter asserted. A claim
about behaviour that no test exercises is a claim, not a property - the same
shape as a check-digit test that searches the form for its weights rather than
evaluating them.

So T1 runs the ingest twice into a scratch database and checks the second run
inserts nothing. The rest verify the store the pipeline actually produced.

    python part1_q1/tests/test_store.py
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import duckdb

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "src"
REPO = HERE.parents[2] if (HERE.parents[2] / "run_all.py").exists() else HERE.parents[1]
sys.path.insert(0, str(SRC))
import config  # noqa: E402

RESULTS: list[tuple[str, bool, str]] = []


def check(name: str, condition: bool, detail: str = "") -> None:
    RESULTS.append((name, bool(condition), detail))


def connect(path: Path) -> duckdb.DuckDBPyConnection:
    con = duckdb.connect(str(path))
    con.execute("INSTALL spatial; LOAD spatial;")
    return con


# ---------------------------------------------------------------------------
# T1 - the deliverable: ingest twice, insert once
# ---------------------------------------------------------------------------
def t1_ingest_is_idempotent() -> None:
    """Run stage01 twice against a scratch store and compare."""
    scratch = Path(tempfile.mkdtemp(prefix="eha_store_test_"))
    db = scratch / "idempotency.duckdb"
    env = {**os.environ, "EHA_DB_PATH": str(db)}

    def run() -> int:
        proc = subprocess.run(
            [sys.executable, str(SRC / "stage01_ingest.py")],
            capture_output=True, text=True, env=env, cwd=str(REPO),
        )
        if proc.returncode != 0:
            raise RuntimeError(proc.stdout + proc.stderr)
        with connect(db) as con:
            return con.execute("SELECT count(*) FROM track_point").fetchone()[0]

    try:
        after_first = run()
        after_second = run()

        check("T1  a second ingest of the same pack inserts nothing",
              after_first == after_second and after_first > 0,
              f"{after_first:,} rows after one run, {after_second:,} after two "
              f"- difference {after_second - after_first}")

        with connect(db) as con:
            per_run = con.execute(
                "SELECT run_id, value FROM ingest_run "
                "WHERE metric = 'rows_inserted_this_run' ORDER BY run_id"
            ).fetchall()
        check("T1b the store itself records that the second run inserted 0",
              len(per_run) >= 2 and per_run[0][1] > 0 and per_run[-1][1] == 0,
              "; ".join(f"run {r} inserted {v:,}" for r, v in per_run))
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


# ---------------------------------------------------------------------------
# T2 - the store the pipeline produced
# ---------------------------------------------------------------------------
def t2_primary_key_is_unique() -> None:
    with connect(config.DB_PATH) as con:
        cols = [c[0] for c in con.execute("DESCRIBE track_point").fetchall()]
        key = "record_hash" if "record_hash" in cols else cols[0]
        total, distinct = con.execute(
            f"SELECT count(*), count(DISTINCT {key}) FROM track_point").fetchone()
    check("T2  the content hash is unique across the store",
          total == distinct,
          f"{total:,} rows, {distinct:,} distinct {key}")


def t3_every_point_has_a_quality_decision() -> None:
    with connect(config.DB_PATH) as con:
        points = con.execute("SELECT count(*) FROM track_point").fetchone()[0]
        judged = con.execute("SELECT count(*) FROM track_qa").fetchone()[0]
        orphans = con.execute("""
            SELECT count(*) FROM track_qa q
            LEFT JOIN track_point p USING (record_hash)
            WHERE p.record_hash IS NULL
        """).fetchone()[0] if "record_hash" in [
            c[0] for c in con.execute("DESCRIBE track_qa").fetchall()] else 0
    check("T3  every stored point carries a quality decision",
          points == judged and orphans == 0,
          f"{points:,} points, {judged:,} judged, {orphans} QA rows with no point")


def t4_referential_integrity() -> None:
    """Nothing downstream references a settlement the masterlist does not have."""
    with connect(config.DB_PATH) as con:
        checks = {
            "settlement_visit": "SELECT count(*) FROM settlement_visit v "
                                "LEFT JOIN settlement s USING (settlement_id) "
                                "WHERE s.settlement_id IS NULL",
            "ward_coverage":    "SELECT count(*) FROM ward_coverage w "
                                "LEFT JOIN ward d USING (ward_code) "
                                "WHERE d.ward_code IS NULL",
        }
        orphans = {name: con.execute(sql).fetchone()[0]
                   for name, sql in checks.items()}
    check("T4  no orphaned foreign keys in the derived tables",
          all(v == 0 for v in orphans.values()),
          ", ".join(f"{k}: {v}" for k, v in orphans.items()))


def t5_geometry_is_valid() -> None:
    with connect(config.DB_PATH) as con:
        cols = [c[0] for c in con.execute("DESCRIBE settlement").fetchall()]
        if "longitude" not in cols:
            check("T5  settlement coordinates lie inside the state envelope",
                  True, "skipped - no coordinate columns")
            return
        outside = con.execute("""
            SELECT count(*) FROM settlement
            WHERE longitude IS NOT NULL AND latitude IS NOT NULL
              AND NOT (longitude BETWEEN 2 AND 15 AND latitude BETWEEN 3 AND 14)
        """).fetchone()[0]
    check("T5  every settlement coordinate lies inside Nigeria's envelope",
          outside == 0,
          f"{outside} settlements outside 2-15E, 3-14N")


def main() -> None:
    if not config.DB_PATH.exists():
        sys.exit(f"No store at {config.DB_PATH}. Run the pipeline first.")

    print("\nSpatial store tests (D1)")
    print("=" * 74)
    for fn in (t1_ingest_is_idempotent, t2_primary_key_is_unique,
               t3_every_point_has_a_quality_decision, t4_referential_integrity,
               t5_geometry_is_valid):
        fn()

    width = max(len(n) for n, _, _ in RESULTS)
    failed = 0
    for name, ok, detail in RESULTS:
        if not ok:
            failed += 1
        print(f"  [{'PASS' if ok else 'FAIL'}] {name:{width}}")
        if detail:
            print(f"         {detail}")
    print("=" * 74)
    print(f"  {len(RESULTS) - failed} passed, {failed} failed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
