"""Scan the paper questionnaire for coding categories that collide with sentinels.

The defect report's first pass was written from reading the form and missed
code 8 in both 6.01 and 6.02. This scan is the authority instead - it checks
every coding category in every question against the declared sentinel set,
rather than relying on someone noticing.

Declared scheme (notes on completion):
    8 / 98  = respondent does not know
    9 / 99  = question asked, no answer obtained
    96      = other, specify

Run:  python part2_q3/scan_sentinels.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# Read the questionnaire out of the supplied pack, not out of a text dump.
#
# This previously read `questionnaire_dump.txt` from two directories above the
# repository - a file produced by hand, never committed, and present only on the
# machine that made it. A clean clone plus the pack, which is what the README
# promises is sufficient, would have failed at this stage. The dump was moved
# and the stage broke, which is how it was found; the fix is not to restore the
# path but to stop depending on a file nobody else has.
#
# The tables are parsed from the .docx with the standard library, so this adds
# no dependency. Same source as check_coverage.py.
PACK_NAME = "eHA_Assessment_Data_Pack_v4_CANDIDATE"
REPO_ROOT = Path(__file__).resolve().parents[1]
for _candidate in (REPO_ROOT / PACK_NAME, REPO_ROOT.parent / PACK_NAME):
    if _candidate.is_dir():
        QUESTIONNAIRE = (_candidate / "Part2_Q3_ODK_Form_Design"
                         / "Household_Questionnaire_HH2026v1.docx")
        break
else:
    raise FileNotFoundError(f"Could not locate {PACK_NAME}")

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def questionnaire_rows() -> list[str]:
    """Numbered question rows, as `qid | question | coding | skip`."""
    import xml.etree.ElementTree as ET
    import zipfile

    root = ET.fromstring(zipfile.ZipFile(QUESTIONNAIRE).read("word/document.xml"))

    def text_of(cell) -> str:
        paragraphs = []
        for p in cell.iter(f"{W}p"):
            joined = "".join(t.text or "" for t in p.iter(f"{W}t")).strip()
            if joined:
                paragraphs.append(joined)
        return " / ".join(paragraphs)

    rows = []
    for tr in root.iter(f"{W}tr"):
        cells = [text_of(tc) for tc in tr.findall(f"{W}tc")]
        if cells and re.match(r"^\d\.\d\d$", cells[0].strip()):
            rows.append(" | ".join(cells))
    return rows

SENTINELS = {"8": "does not know", "9": "no answer obtained",
             "98": "does not know", "99": "no answer obtained"}

# Where the sentinel IS the intended category, this is correct use, not a clash.
CORRECT_USE = {"do not know", "don't know"}


def main() -> None:
    if not QUESTIONNAIRE.exists():
        sys.exit(f"Questionnaire not found at {QUESTIONNAIRE}")
    lines = questionnaire_rows()

    collisions, correct = [], []
    for line in lines:
        parts = line.split(" | ")
        qid, coding = parts[0].strip(), (parts[2] if len(parts) > 2 else "")
        for m in re.finditer(r"([A-Za-z][A-Za-z ,'/\-]+?)\s*[. ]{2,}\s*(\d{1,2})\b", coding):
            label, code = m.group(1).strip(), m.group(2)
            if code not in SENTINELS:
                continue
            (correct if label.lower() in CORRECT_USE else collisions).append(
                (qid, code, label, SENTINELS[code]))

    print("\nSentinel collision scan - Form HH/2026/v1")
    print("=" * 74)
    print(f"\n  Correct use ({len(correct)}): the sentinel IS the category")
    for qid, code, label, meaning in correct:
        print(f"    {qid}  {code} = {label}")

    print(f"\n  COLLISIONS ({len(collisions)}): a substantive category carries a "
          f"sentinel value")
    print(f"    {'Q':6} {'code':5} {'substantive meaning':28} also means")
    print("    " + "-" * 66)
    for qid, code, label, meaning in collisions:
        print(f"    {qid:6} {code:5} {label:28} {meaning}")

    print("\n  Not visible to this scan - collisions from field width alone:")
    print("    roster age in years   98 and 99 are plausible ages")
    print("    3.01 household size   98 and 99 likewise")
    print("    1.06, 1.07            THREE-digit fields; the scheme defines no")
    print("                          three-digit sentinel at all - a gap, not a clash")
    print("=" * 74)
    print(f"  {len(collisions)} collisions requiring separate storage of value and status")


if __name__ == "__main__":
    main()
