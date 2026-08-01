"""Shared paths and campaign constants for the Part 1 Q1 pipeline.

Everything the rest of the pipeline needs to know about *where* things are and
*what the campaign was* lives here, so that no path or magic date is buried in
an analysis module.
"""

import os
from pathlib import Path

# --- Paths ----------------------------------------------------------------
# Repository root is two levels above this file (part1_q1/src/config.py).
REPO_ROOT = Path(__file__).resolve().parents[2]

PACK_DIR_NAME = "eHA_Assessment_Data_Pack_v4_CANDIDATE"


def _locate_pack() -> Path:
    """Find the supplied data pack.

    The pack is never committed, so its location depends on who is running
    this. Searched in order:

    1. ``$EHA_DATA_PACK``, if set - an explicit override always wins.
    2. Inside the repository root, which is where the README asks a marker
       to put it.
    3. Beside the repository root, which is where it sits on my machine.

    Resolving both layouts rather than hardcoding one means the pipeline runs
    unmodified for the marker and for me. Failing loudly with the paths tried
    is better than a bare "no files matched" from three stages down.
    """
    override = os.environ.get("EHA_DATA_PACK")
    candidates = [Path(override)] if override else []
    candidates += [REPO_ROOT / PACK_DIR_NAME, REPO_ROOT.parent / PACK_DIR_NAME]

    for candidate in candidates:
        if candidate.is_dir():
            return candidate

    tried = "\n  ".join(str(c) for c in candidates)
    raise FileNotFoundError(
        f"Could not find the data pack '{PACK_DIR_NAME}'. Tried:\n  {tried}\n"
        "Place it at the repository root, or set EHA_DATA_PACK to its path."
    )


PACK_ROOT = _locate_pack()
PACK = PACK_ROOT / "Part1_Q1_Campaign_Tracking"

TRACKS_DIR = PACK / "tracks"
SETTLEMENTS_CSV = PACK / "settlement_masterlist.csv"
ETALLY_CSV = PACK / "etally_daily.csv"
INACCESSIBLE_CSV = PACK / "inaccessible_settlements.csv"
BOUNDARIES_GPKG = PACK / "boundaries.gpkg"

OUTPUTS = REPO_ROOT / "part1_q1" / "outputs"
DOCS = REPO_ROOT / "part1_q1" / "docs"
# Overridable so the store can be built somewhere disposable. `tests/test_store.py`
# uses it to run the ingest twice into a scratch database and prove the second run
# inserts nothing, without touching the real one.
DB_PATH = Path(os.environ.get("EHA_DB_PATH", OUTPUTS / "campaign.duckdb"))

# --- Campaign definition --------------------------------------------------
# Stated in the data pack README: Bansara State ran a five day house-to-house
# SIA from 9 to 13 March 2026 across four LGAs.
CAMPAIGN_START = "2026-03-09"
CAMPAIGN_END = "2026-03-13"

# Loggers were specified to record a fix approximately every 60 seconds.
# Used by the QA stage to detect gaps in the fix sequence; it is the stated
# design interval, not a threshold I chose.
NOMINAL_FIX_INTERVAL_S = 60


def ensure_dirs() -> None:
    """Create output directories if they do not exist. Safe to call repeatedly."""
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)
