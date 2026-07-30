"""Generate the constraint register from the form itself.

The register is not written by hand. It is produced by reading `build_form.py`'s
own definition and joining it to the justifications in `constraint_sources.py`.

**The build fails if any rule in the form has no documented source.** That is the
mechanism, not a nicety: a register maintained separately from a form is wrong
within a day, and the assessment lists thresholds asserted without justification
as an automatic loss of marks. Here a constraint cannot be added without saying
where its value came from, because the register will not build.

Run:  python part2_q3/build_register.py
"""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from build_form import survey_rows  # noqa: E402
from constraint_sources import SOURCES  # noqa: E402

OUT = HERE / "docs" / "constraint_register.md"

SOURCE_LABEL = {
    "paper form": "Paper form",
    "reference data": "Reference data",
    "published standard": "Published standard",
    "judgement": "**My judgement**",
}


def collect_rules() -> tuple[list[dict], list[dict]]:
    """Split the form's rules into blocking constraints and warnings."""
    blocking, warnings = [], []
    for row in survey_rows():
        name = row.get("name", "")
        if row.get("constraint"):
            blocking.append({
                "name": name,
                "question": row.get("label::English (en)", "").strip(),
                "type": row.get("type", ""),
                "rule": row["constraint"],
                "message": row.get("constraint_message::English (en)", "").strip(),
            })
        # A `note` carrying a relevance condition is a warning: it appears only
        # when the condition is met and does not stop the enumerator.
        elif row.get("type") == "note" and row.get("relevant") and (
            "warn" in name or "mismatch" in name or name in SOURCES
        ):
            warnings.append({
                "name": name,
                "question": row.get("label::English (en)", "").strip(),
                "type": "warning",
                "rule": row["relevant"],
                "message": row.get("label::English (en)", "").strip(),
            })
    return blocking, warnings


def check_coverage(rules: list[dict]) -> list[str]:
    return [r["name"] for r in rules if r["name"] not in SOURCES]


def render(blocking: list[dict], warnings: list[dict]) -> str:
    lines: list[str] = []
    add = lines.append

    add("# Constraint register — Form HH/2026/v1")
    add("")
    add("**Generated** by `build_register.py` from `build_form.py` (the form) and")
    add("`constraint_sources.py` (the justifications). It is not maintained by hand,")
    add("and **the build fails if any rule in the form has no documented source** —")
    add("so a constraint cannot be added without stating where its value came from.")
    add("")
    add(f"{len(blocking)} blocking constraints · {len(warnings)} warnings · "
        f"{len(blocking) + len(warnings)} rules documented")
    add("")
    add("## How to read the source column")
    add("")
    add("| Source | Meaning |")
    add("|---|---|")
    add("| Paper form | The value is stated or directly implied by Form HH/2026/v1 |")
    add("| Reference data | The value comes from a supplied lookup file |")
    add("| Published standard | Named, external and checkable |")
    add("| **My judgement** | Mine, with reasoning. Never left unlabelled. |")
    add("")
    add("## Blocking versus warning — and why the split matters")
    add("")
    add("A rule **blocks** only when continuing would produce data that is")
    add("meaningless or unsafe. Everything else **warns**, because a block that an")
    add("enumerator cannot satisfy honestly is a block they will satisfy")
    add("dishonestly — inventing a roster line to clear an error is worse than the")
    add("error. There is exactly one hard block on a judgement call in this form:")
    add("the consent statement at 2.01.")
    add("")
    add("Two rules are deliberately **wider** than clinical plausibility — child")
    add("weight and height. Their hard bounds are typo guards; implausibility is")
    add("raised as a warning. A clinical range enforced as a block would delete the")
    add("severely malnourished children the survey exists to count.")
    add("")

    for title, rules, kind in (
        ("Blocking constraints", blocking, "blocks"),
        ("Warnings", warnings, "warns"),
    ):
        add(f"## {title}")
        add("")
        for r in rules:
            meta = SOURCES[r["name"]]
            add(f"### `{r['name']}` — {r['question'] or '(no visible label)'}")
            add("")
            add(f"| | |")
            add(f"|---|---|")
            add(f"| **Action** | {kind} |")
            add(f"| **Rule** | `{r['rule']}` |")
            if kind == "blocks":
                add(f"| **Message shown** | {r['message']} |")
            add(f"| **What it prevents** | {meta['prevents']} |")
            add(f"| **Source** | {SOURCE_LABEL[meta['source']]} |")
            add(f"| **Detail** | {meta['detail']} |")
            add("")

    add("## Language")
    add("")
    add("Every constraint message exists in **Hausa and English**, Hausa default.")
    add("Interviews are conducted in Hausa and 38% of enumerators are not confident")
    add("readers of English, so an English-only message is a message that does not")
    add("exist. **The Hausa strings are indicative and require native-speaker review")
    add("before deployment** — they are my own and have not been checked.")
    add("")
    add("## What is not constrained, and why")
    add("")
    add("- **`q1_05_alt_name`, `q4_14_medicine_other`, `q5_07_reason_other`, "
        "`q7_02_observation`** — free text by design. Constraining an "
        "other-specify field defeats its purpose.")
    add("- **`q1_11_gps`** — no geofence. A settlement centroid is not a household "
        "location, and a boundary constraint would block legitimate dwellings on "
        "the edge of a settlement. Out-of-area points are better found in back-"
        "office QA against the settlement list than blocked at the doorstep.")
    add("- **`q4_13_medicine`** — no validity constraint beyond selection from the "
        "list, because the real codelist does not exist. See defect E1.")
    return "\n".join(lines) + "\n"


def main() -> None:
    blocking, warnings = collect_rules()
    missing = check_coverage(blocking + warnings)

    if missing:
        print("REGISTER BUILD FAILED - rules with no documented source:\n")
        for name in missing:
            print(f"    * {name}")
        print("\nAdd an entry to constraint_sources.py for each, stating what the")
        print("rule prevents and where its value came from.")
        sys.exit(1)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(blocking, warnings), encoding="utf-8")

    print("\nConstraint register")
    print("-" * 52)
    print(f"  blocking constraints   {len(blocking):>3}")
    print(f"  warnings               {len(warnings):>3}")
    print(f"  total documented       {len(blocking) + len(warnings):>3}")
    by_source: dict[str, int] = {}
    for r in blocking + warnings:
        s = SOURCES[r["name"]]["source"]
        by_source[s] = by_source.get(s, 0) + 1
    print()
    for source, count in sorted(by_source.items(), key=lambda kv: -kv[1]):
        print(f"  {source:22s} {count:>3}")
    print(f"\n  written to {OUT.relative_to(HERE.parent)}")


if __name__ == "__main__":
    main()
