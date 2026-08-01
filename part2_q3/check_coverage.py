"""Every question on the paper form is implemented, or declared as not carried.

The question's first requirement is to *implement the full questionnaire*. That
is easy to claim and easy to get wrong quietly: a question dropped during a
refactor leaves no trace, converts cleanly, validates cleanly, and is only
noticed when the analysis team asks where a variable went.

So it is checked rather than asserted. The paper question numbers are read from
the supplied questionnaire itself - not from a list transcribed into this repo,
which could drift from the instrument the same way any other prose does - and
every one must be either:

  * implemented as a field whose node name carries its number, or
  * implemented under a different node name, listed in RENAMED with the reason, or
  * declared not carried forward, listed in NOT_CARRIED with the reason.

Anything in none of the three fails the build. The two lists are the deliberate
scope, in code, next to the check that enforces them.

    python part2_q3/check_coverage.py
"""

from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent
PACK_NAME = "eHA_Assessment_Data_Pack_v4_CANDIDATE"
XML = HERE / "form" / "bansara_hh_2026.xml"

for candidate in (REPO_ROOT / PACK_NAME, REPO_ROOT.parent / PACK_NAME):
    if candidate.is_dir():
        QUESTIONNAIRE = (candidate / "Part2_Q3_ODK_Form_Design"
                         / "Household_Questionnaire_HH2026v1.docx")
        break
else:
    raise FileNotFoundError(f"Could not locate {PACK_NAME}")


# Implemented, but the node name does not carry the paper number.
RENAMED = {
    "1.08": "enumerator_code - asked once at sign-in rather than per household",
    "1.09": "enum_team - derived from the roster, so it cannot disagree with 1.08",
    "7.01": "end_time - captured automatically, not asked",
}

# Deliberately not carried into the digital form. Mirrored in the codebook's
# 'Fields on the paper form that are NOT collected' table and in
# deliberate_scope.md; stated here because this is where it is enforced.
NOT_CARRIED = {
    "7.03": "enumerator signature - replaced by authenticated submission",
    "7.06": "supervisor signature - replaced by the 7.04/7.05 review fields",
    "8.01": "office use - form received at office; no paper form is posted",
    "8.02": "office use - data entry clerk code; there is no data entry step",
    "8.03": "office use - second-entry verification; double entry removed entirely",
}


def paper_questions() -> set[str]:
    """Question numbers as printed in the supplied questionnaire."""
    document = zipfile.ZipFile(QUESTIONNAIRE).read("word/document.xml").decode("utf-8")
    return set(re.findall(r"\b[1-8]\.\d\d\b", re.sub(r"<[^>]+>", "\n", document)))


def implemented() -> set[str]:
    """Question numbers carried by a field node name, q<section>_<nn>_..."""
    xml = XML.read_text(encoding="utf-8")
    return {f"{s}.{n}" for s, n in re.findall(r"\bq(\d)_(\d\d)_", xml)}


def main() -> None:
    if not XML.exists():
        sys.exit("XForm not built. Run build_form.py first.")

    paper = paper_questions()
    built = implemented()
    accounted = built | set(RENAMED) | set(NOT_CARRIED)

    print("\nQuestionnaire coverage")
    print("=" * 68)
    print(f"  questions printed on the paper form        {len(paper):>10}")
    print(f"  implemented, node name carries the number  {len(built & paper):>10}")
    print(f"  implemented under another node name        {len(set(RENAMED) & paper):>10}")
    print(f"  declared not carried forward               {len(set(NOT_CARRIED) & paper):>10}")

    unaccounted = sorted(paper - accounted, key=lambda s: (int(s[0]), int(s[2:])))
    stale = sorted((set(RENAMED) | set(NOT_CARRIED)) - paper)

    print()
    for number, why in sorted(RENAMED.items()):
        print(f"  {number}  renamed      {why}")
    for number, why in sorted(NOT_CARRIED.items()):
        print(f"  {number}  not carried  {why}")

    print()
    print("=" * 68)
    if unaccounted:
        print(f"  FAILED - {len(unaccounted)} question(s) neither implemented nor declared:\n")
        for number in unaccounted:
            print(f"    * {number} is on the paper form and is not in the built "
                  f"XForm. Implement it, or add it to NOT_CARRIED with a reason.")
        sys.exit(1)
    if stale:
        print(f"  FAILED - {len(stale)} declared exception(s) not on the paper form:\n")
        for number in stale:
            print(f"    * {number} is declared here but does not appear in the "
                  f"questionnaire. The declaration is stale.")
        sys.exit(1)
    print(f"  PASSED - all {len(paper)} questions accounted for, "
          f"{len(built & paper)} implemented and "
          f"{len(NOT_CARRIED)} declared out of scope")


if __name__ == "__main__":
    main()
