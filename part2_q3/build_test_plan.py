"""Generate the test plan (F9) - boundary cases derived from the form itself.

The question requires cases exercising "the ends of every range you set". Typing
those by hand guarantees one gets missed, and the missed one is the range added
last. So every numeric range is **read out of the form's own constraints** and
turned into four cases: below the minimum (reject), at the minimum (accept), at
the maximum (accept), above the maximum (reject).

Add a range to the form and its four boundary cases appear here automatically.
Change a bound and the expected values change with it. The plan cannot drift
from the form, for the same reason the constraint register cannot.

Scenario cases - skip logic, cross-question consistency, the named requirements -
are written by hand below, because they describe behaviour rather than bounds.

Run:  python part2_q3/build_test_plan.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from build_form import survey_rows  # noqa: E402

OUT = HERE / "docs" / "test_plan.md"

# ". >= 2.0 and . <= 30.0"  ->  (2.0, 30.0)
RANGE_RE = re.compile(r"\.\s*>=\s*(-?[\d.]+)\s*and\s*\.\s*<=\s*(-?[\d.]+)")


def numeric_ranges() -> list[dict]:
    """Every explicit numeric range in the form, with its bounds."""
    found = []
    for row in survey_rows():
        constraint = row.get("constraint", "")
        m = RANGE_RE.search(constraint) if constraint else None
        if not m:
            continue
        lo_s, hi_s = m.group(1), m.group(2)
        decimal = "." in lo_s or "." in hi_s
        step = 0.1 if decimal else 1
        cast = float if decimal else int
        found.append({
            "name": row["name"],
            "label": row.get("label::English (en)", "").strip(),
            "lo": cast(lo_s), "hi": cast(hi_s), "step": step, "decimal": decimal,
        })
    return found


def fmt(v: float, decimal: bool) -> str:
    return f"{v:.1f}" if decimal else str(int(v))


def boundary_cases(ranges: list[dict]) -> list[dict]:
    cases = []
    n = 0
    for r in ranges:
        lo, hi, step, dec = r["lo"], r["hi"], r["step"], r["decimal"]
        for value, expected, kind in (
            (round(lo - step, 1), "REJECT", "negative"),
            (lo, "ACCEPT", "boundary"),
            (hi, "ACCEPT", "boundary"),
            (round(hi + step, 1), "REJECT", "negative"),
        ):
            n += 1
            cases.append({
                "id": f"B{n:02d}",
                "kind": kind,
                "target": r["name"],
                "question": r["label"] or r["name"],
                "input": fmt(value, dec),
                "expected": expected,
                "why": ("just below the minimum" if expected == "REJECT" and value < lo
                        else "just above the maximum" if expected == "REJECT"
                        else "exactly at the minimum" if value == lo
                        else "exactly at the maximum"),
            })
    return cases


# ---------------------------------------------------------------------------
# Scenario cases. Behaviour, not bounds - written by hand.
# The five the question names explicitly are marked REQUIRED.
# ---------------------------------------------------------------------------
SCENARIOS: list[dict] = [
    dict(id="S01", kind="boundary", required=True,
         target="q5_01_specimen_eligible",
         question="Specimen eligibility cut, lower side",
         setup="Roster child aged **11 completed months**",
         input="advance to Section 5",
         expected="No specimen sought. 5.02-5.07 hidden; note shown that the "
                  "child is under 12 months. The child module (Section 4) is "
                  "still completed in full.",
         why="The paper form sends this child to Section 6, abandoning every "
             "remaining child in the household (defect B2). Here the skip ends "
             "only this child's iteration."),
    dict(id="S02", kind="boundary", required=True,
         target="q5_01_specimen_eligible",
         question="Specimen eligibility cut, upper side",
         setup="Roster child aged **12 completed months**",
         input="advance to Section 5",
         expected="Specimen sought. 5.02 shown and required.",
         why="12 months is the cut stated at 5.01. Paired with S01 it brackets it."),
    dict(id="S03", kind="boundary", required=True,
         target="q4_07_position",
         question="Measurement position change, below the cut",
         setup="Child aged **23 months**, height measured",
         input="4.07 = Standing height",
         expected="WARNING shown, entry allowed",
         why="WHO convention is recumbent below 24 months. It warns rather than "
             "blocks: a child who cannot stand is legitimately measured "
             "recumbent at any age."),
    dict(id="S04", kind="boundary", required=True,
         target="q4_07_position",
         question="Measurement position change, at the cut",
         setup="Child aged **24 months**, height measured",
         input="4.07 = Standing height",
         expected="No warning",
         why="24 months and above is standing height. S03/S04 bracket the cut."),
    dict(id="S05", kind="negative", required=True,
         target="q1_10_visit_date",
         question="Date before the fieldwork window",
         setup="Device date set to 31 May 2026",
         input="1.10 = 2026-05-31",
         expected="REJECT with the Hausa message",
         why="Most often a device with the wrong date, or a form completed later "
             "from paper notes."),
    dict(id="S06", kind="negative", required=True,
         target="q1_10_visit_date",
         question="Date after the fieldwork window",
         input="1.10 = 2026-07-01",
         expected="REJECT",
         why="The window enforced is 1-30 June, the ethics-approved one, not the "
             "14-day operational expectation. See the constraint register."),
    dict(id="S07", kind="negative", required=True,
         target="roster_mismatch_note",
         question="Roster disagrees with stated household size",
         setup="3.01 = 6 usual residents",
         input="Complete 4 roster lines and advance",
         expected="WARNING shown naming both numbers. Entry continues.",
         why="Warns rather than blocks: the two legitimately differ when a usual "
             "resident is absent and cannot be described. A block would push "
             "enumerators to invent a line to clear the error."),
    dict(id="S08", kind="negative",
         target="q2_01_statement_read",
         question="Consent statement not read",
         input="2.01 = No",
         expected="BLOCK. Cannot advance.",
         why="The only hard block in the form. The paper form records No and "
             "continues to 2.02 where consent may be given (defect B3)."),
    dict(id="S09", kind="negative",
         target="q5_03_check_digit",
         question="Transposed pair of digits in the specimen serial",
         setup="Valid label BSN480123-? with correct check character",
         input="Enter serial 480132 (last two digits swapped) with the original "
               "check character",
         expected="REJECT",
         why="Proven exhaustively in tests/test_check_digit.py: 292,960 "
             "transpositions tested, none escaped."),
    dict(id="S10", kind="negative",
         target="q5_03_label_serial",
         question="Label from another team's book",
         setup="Signed in as a TM01 enumerator (range 480000-480899)",
         input="5.03 serial = 480900",
         expected="REJECT (out of allocated range)",
         why="This label passes the check digit - it is internally valid. Only "
             "the range constraint catches it."),
    dict(id="S11", kind="negative",
         target="q5_03_label_serial",
         question="Same label used twice in one household",
         setup="Two eligible children, specimen taken from both",
         input="Enter the same serial for the second child",
         expected="REJECT",
         why="The most common genuine duplicate: two entries minutes apart from "
             "the same book."),
    dict(id="S12", kind="negative",
         target="q5_03_label_serial",
         question="Label reused from the previous submission",
         setup="Complete and save a submission using serial X, start the next",
         input="Enter serial X again",
         expected="REJECT",
         why="last-saved covers one submission of history only. Submission n-2 "
             "and earlier are NOT caught - see docs/label_reuse.md."),
    dict(id="S13", kind="negative",
         target="q6_07_assets",
         question="'None of these' selected with an owned asset",
         input="6.07 = Radio + None of these",
         expected="REJECT",
         why="A logical impossibility the paper form permits (defect C2)."),
    dict(id="S14", kind="negative",
         target="pin_entered",
         question="Wrong PIN for the selected enumerator code",
         input="Select ENU001, enter PIN 0000",
         expected="REJECT",
         why="Prevents one enumerator submitting under another's code - the "
             "precondition for the fabrication pattern in the operating "
             "conditions."),
    dict(id="S15", kind="negative",
         target="q1_02_lga",
         question="LGA not assigned to this enumerator",
         setup="Signed in as an enumerator assigned to Gwarin",
         input="1.02 = Idi-Oro",
         expected="REJECT (relaxed for supervisors)",
         why="staff_roster.csv assigned_lga."),
    dict(id="S16", kind="positive",
         target="q5_02_specimen_obtained",
         question="Skip logic when no specimen is obtained",
         input="5.02 = No",
         expected="5.03-5.05 hidden; 5.06 reason shown and required",
         why="5.02 has NO skip instruction on the paper form at all (defect B1). "
             "This is the case that defect produces."),
    dict(id="S17", kind="positive",
         target="q5_02_specimen_obtained",
         question="Skip logic when a specimen IS obtained",
         input="5.02 = Yes",
         expected="5.03-5.05 shown and required; 5.06-5.07 hidden",
         why="The mirror of S16. On paper, 5.06 applies to everyone."),
    dict(id="S18", kind="negative",
         target="q4_01_line",
         question="Child module pointed at an adult",
         setup="Roster line 1 is a 34-year-old head of household",
         input="4.01 = 1",
         expected="REJECT",
         why="Validated with indexed-repeat() against the roster. The paper form "
             "cannot check this."),
    dict(id="S19", kind="positive",
         target="q1_14_result",
         question="Result of visit is not 'Completed'",
         input="1.14 = Dwelling vacant or demolished",
         expected="Sections 2-6 hidden. Note instructs the enumerator to submit "
                  "and hand the device to the supervisor for review at 7.04. It "
                  "must NOT refer to 7.03, which is the paper signature field "
                  "and does not exist in this form.",
         why="Mirrors the paper instruction after 1.14."),
    dict(id="S20", kind="positive",
         target="q3_02_eligible",
         question="Eligible-children count is derived, not typed",
         setup="Roster with children aged 8, 9, 59 and 60 completed months",
         input="Advance past the roster",
         expected="Eligible count = 2 (the 9- and 59-month children). Two child "
                  "modules generated.",
         why="Brackets BOTH ends of the 9-59 eligibility window in one case, and "
             "demonstrates defect A1's fix: the count is derived from roster "
             "ages, never transcribed from an office-use column. This is also "
             "the second cross-question consistency check - stated eligible "
             "children and modules completed cannot disagree because they are "
             "the same quantity."),
    dict(id="S21", kind="positive",
         target="q4_05_weight_kg",
         question="Clinically implausible but typeable weight",
         setup="Child aged 24 months",
         input="4.05 weight = 4.0 kg",
         expected="WARNING shown, entry ALLOWED",
         why="The hard bounds are a typo guard; clinical implausibility warns. "
             "Blocking here would delete the severely wasted children the survey "
             "exists to count."),
    dict(id="S22", kind="negative",
         target="q4_13_medicine",
         question="Placeholder medicine list is visible at the point of capture",
         setup="4.12 = Yes",
         input="Advance to 4.13",
         expected="Banner shown: PLACEHOLDER LIST - NOT FOR DEPLOYMENT",
         why="Defect E1. The substitution must be visible in the field, not only "
             "in documentation nobody reads at a doorstep."),
]


def render(boundary: list[dict], scenarios: list[dict]) -> str:
    L: list[str] = []
    a = L.append
    total = len(boundary) + len(scenarios)
    negatives = sum(1 for c in boundary + scenarios if c["kind"] == "negative")
    bounds = sum(1 for c in boundary + scenarios if c["kind"] == "boundary")

    a("# Test plan - Form HH/2026/v1")
    a("")
    a("**Partly generated.** Every numeric range in the form produces four cases")
    a("automatically - below minimum, at minimum, at maximum, above maximum - read")
    a("from the form's own constraints by `build_test_plan.py`. Add a range and its")
    a("boundary cases appear here; change a bound and the expected values follow.")
    a("The plan cannot drift from the form.")
    a("")
    a(f"**{total} cases** - {negatives} negative, {bounds} boundary, "
      f"{total - negatives - bounds} positive/behavioural.")
    a("")
    a("## Execution status")
    a("")
    a("**These cases are specified. They have not been executed against a running")
    a("instance**, because no ODK Central project was available inside the")
    a("submission window. The check-digit logic behind S09 *is* executed -")
    a("exhaustively - in `tests/test_check_digit.py`. Everything else is a")
    a("specification awaiting a device.")
    a("")
    a("Saying so matters: a test plan that has been written is not a test plan that")
    a("has been run, and reporting the two as equivalent would be the same")
    a("overclaim this form is designed to prevent elsewhere.")
    a("")
    a("To execute: deploy per `docs/validation.md`, then work the table top to")
    a("bottom recording actual against expected.")
    a("")
    a("## Coverage of the cases the question names")
    a("")
    a("| Required by the question | Cases |")
    a("|---|---|")
    a("| Specimen eligibility cut | S01, S02 |")
    a("| Measurement position change | S03, S04 |")
    a("| Ends of every range set | all B-numbered cases, generated |")
    a("| Date outside the fieldwork window | S05, S06 |")
    a("| Roster disagrees with stated household size | S07 |")
    a("| Negative tests | " + str(negatives) + " of " + str(total) + " |")
    a("")
    a("## Scenario cases")
    a("")
    for c in scenarios:
        flag = " **[REQUIRED BY THE QUESTION]**" if c.get("required") else ""
        a(f"### {c['id']} - {c['question']}{flag}")
        a("")
        a("| | |")
        a("|---|---|")
        a(f"| **Type** | {c['kind']} |")
        a(f"| **Target** | `{c['target']}` |")
        if c.get("setup"):
            a(f"| **Setup** | {c['setup']} |")
        a(f"| **Input** | {c['input']} |")
        a(f"| **Expected** | {c['expected']} |")
        a(f"| **Why it matters** | {c['why']} |")
        a(f"| **Result** | _not yet executed_ |")
        a("")

    a("## Generated boundary cases")
    a("")
    a("Four per numeric range: the two values that must be accepted and the two")
    a("just outside that must be rejected.")
    a("")
    a("| ID | Field | Question | Input | Expected | Boundary |")
    a("|---|---|---|---|---|---|")
    for c in boundary:
        a(f"| {c['id']} | `{c['target']}` | {c['question'][:44]} | "
          f"`{c['input']}` | **{c['expected']}** | {c['why']} |")
    a("")
    a("## What this plan does not cover")
    a("")
    a("- **Device behaviour under memory pressure.** A 40-person roster with 8")
    a("  eligible children on a 2 GB tablet needs a real device, not a plan.")
    a("- **Hausa comprehension.** Every string is bilingual, but whether an")
    a("  enumerator with six years of schooling *understands* a given message is")
    a("  a cognitive-interview question, not a test case. The strings need")
    a("  native-speaker review before deployment.")
    a("- **Duplicate labels beyond one submission of history.** Out of scope by")
    a("  construction - see `docs/label_reuse.md`.")
    a("- **Encryption round-trip.** The public key in settings is a placeholder;")
    a("  decryption cannot be tested until the real keypair is issued.")
    return "\n".join(L) + "\n"


def main() -> None:
    ranges = numeric_ranges()
    boundary = boundary_cases(ranges)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(boundary, SCENARIOS), encoding="utf-8")

    print("\nTest plan")
    print("-" * 56)
    print(f"  numeric ranges found in the form   {len(ranges):>3}")
    print(f"  boundary cases generated           {len(boundary):>3}")
    print(f"  scenario cases hand-written        {len(SCENARIOS):>3}")
    print(f"  TOTAL                              {len(boundary) + len(SCENARIOS):>3}"
          f"   (question requires >= 15)")
    print()
    for r in ranges:
        print(f"    {r['name']:22s} {fmt(r['lo'], r['decimal']):>7} .. "
              f"{fmt(r['hi'], r['decimal']):>7}")
    print(f"\n  written to {OUT.relative_to(HERE.parent)}")


if __name__ == "__main__":
    main()
