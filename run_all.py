"""Rebuild every output in this submission from the supplied data pack.

    python run_all.py

The assessment requires that code run end to end from the raw data to the final
outputs without manual intervention. This is that entry point. It rebuilds
everything, re-runs every check, and **stops at the first failure** rather than
carrying on and producing a partial result that looks complete.

Nothing here is incremental. Every stage runs from scratch each time, so a
failed run can never leave a half-written state that the next run treats as
input.

Prerequisites
-------------
* Python 3.12 with `pip install -r requirements.txt`
* The data pack, unmodified, at the repository root or beside it
* **Java 8+ on PATH** for ODK Validate. Without it the XLSForm still converts
  but is not deeply validated, and the run says so rather than passing quietly.

Runtime is roughly four minutes, dominated by the 956,702-point ingest.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# (label, script, argv) - order matters; later stages read earlier outputs.
PIPELINE: list[tuple[str, str, list[str]]] = [
    ("Part 1 Q1  ingest 956,702 GPS fixes",     "part1_q1/src/stage01_ingest.py", []),
    ("Part 1 Q1  quality assurance rules",      "part1_q1/src/stage02_qa.py", []),
    ("Part 1 Q1  settlement attribution",       "part1_q1/src/stage03_attribute.py", []),
    ("Part 1 Q1  coverage reconciliation",      "part1_q1/src/stage04_reconcile.py", []),
    ("Part 1 Q1  Gi* cluster analysis",         "part1_q1/src/stage05_cluster.py", []),
    ("Part 1 Q1  A3 map and decision brief",    "part1_q1/src/stage06_map.py", []),

    ("Part 2 Q3  build external form media",    "part2_q3/prepare_media.py", []),
    ("Part 2 Q3  build and convert XLSForm",    "part2_q3/build_form.py", []),
    ("Part 2 Q3  external references resolve",  "part2_q3/validate_media.py", []),
    ("Part 2 Q3  questionnaire coverage",       "part2_q3/check_coverage.py", []),
    ("Part 2 Q3  constraint register",          "part2_q3/build_register.py", []),
    ("Part 2 Q3  test plan",                    "part2_q3/build_test_plan.py", []),
    ("Part 2 Q3  codebook",                     "part2_q3/build_codebook.py", []),
    ("Part 2 Q3  check-digit test suite",       "part2_q3/tests/test_check_digit.py", []),
    ("Part 2 Q3  sentinel collision scan",      "part2_q3/scan_sentinels.py", []),
    ("Part 2 Q3  daily fabrication check",      "part2_q3/daily_qa.py", ["--demo"]),

    ("Part 3 Q6  training and assessment data",
     "part3_q6/annex_b_session_in_full/make_dataset.py", []),

    ("Verify     write-ups match the outputs",  "verify_claims.py", []),
    ("Assemble   responses.docx",               "writeup/assemble.py", []),
]

# Rebuilt every run. Removed first so nothing stale can be mistaken for output.
ARTEFACTS = [
    "part1_q1/outputs/campaign.duckdb",
    "part1_q1/outputs/campaign.duckdb.wal",
    "part2_q3/form/bansara_hh_2026.xlsx",
    "part2_q3/form/bansara_hh_2026.xml",
    "part2_q3/form/media",
]


def check_java() -> bool:
    if shutil.which("java") is None:
        return False
    return subprocess.run(["java", "-version"], capture_output=True).returncode == 0


def main() -> None:
    started = time.time()
    print("\n" + "=" * 68)
    print("  eHA technical assessment - full rebuild from the supplied data pack")
    print("=" * 68)

    if not check_java():
        print("\n  WARNING: Java not found on PATH.")
        print("  pyxform will still convert the XLSForm, but ODK Validate cannot run,")
        print("  so XPath expressions are NOT deeply checked. Install Java 8+ and")
        print("  re-run before trusting the form. Continuing.\n")

    for path in ARTEFACTS:
        target = ROOT / path
        if target.is_dir():
            shutil.rmtree(target)
        elif target.exists():
            target.unlink()

    width = max(len(label) for label, _, _ in PIPELINE)
    for index, (label, script, argv) in enumerate(PIPELINE, start=1):
        print(f"  [{index:2d}/{len(PIPELINE)}] {label:<{width}} ", end="", flush=True)
        began = time.time()
        result = subprocess.run(
            [sys.executable, str(ROOT / script), *argv],
            capture_output=True, text=True, cwd=ROOT)
        elapsed = time.time() - began

        if result.returncode != 0:
            print(f"FAILED  ({elapsed:.1f}s)\n")
            print("-" * 68)
            print(result.stdout[-2500:])
            print(result.stderr[-2500:])
            print("-" * 68)
            print(f"\n  Stopped at stage {index}: {script}")
            print("  Nothing after this point was rebuilt.")
            sys.exit(1)
        print(f"ok  ({elapsed:4.1f}s)")

    print("\n" + "=" * 68)
    print(f"  All {len(PIPELINE)} stages completed in {time.time() - started:.0f}s")
    print("=" * 68)
    print("""
  Outputs
    part1_q1/outputs/     spatial store, A3 PDF map, preview PNG
    part1_q1/docs/        QA rules, reconciliation, clusters, decision brief
    part2_q3/form/        XLSForm, XForm, conversion log, external media
    part2_q3/docs/        constraint register, test plan, codebook, and the rest
    part3_q6/annex_b_session_in_full/   training and assessment datasets
    writeup/responses.docx              the combined submission document
""")


if __name__ == "__main__":
    main()
