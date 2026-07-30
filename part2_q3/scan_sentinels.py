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

DUMP = Path(__file__).resolve().parents[2] / "questionnaire_dump.txt"

SENTINELS = {"8": "does not know", "9": "no answer obtained",
             "98": "does not know", "99": "no answer obtained"}

# Where the sentinel IS the intended category, this is correct use, not a clash.
CORRECT_USE = {"do not know", "don't know"}


def main() -> None:
    if not DUMP.exists():
        sys.exit(f"Questionnaire text dump not found at {DUMP}")
    lines = [l for l in DUMP.read_text(encoding="utf-8").splitlines()
             if re.match(r"^\d\.\d\d \|", l)]

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
