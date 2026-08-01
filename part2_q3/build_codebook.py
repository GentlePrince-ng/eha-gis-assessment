"""Generate the codebook from the form (F13).

Like the constraint register and the test plan, this is read out of
`build_form.py` rather than maintained beside it. A codebook that drifts from
the instrument is worse than none, because the analysis team trusts it.

What it produces:
  * the three analysable tables the repeats flatten into, and their keys
  * every field, its type, its analysis variable, and the relevance rule that
    determines when it is null
  * value labels for every coded field
  * the paper-to-digital crosswalk for the re-based codes (F3)

Run:  python part2_q3/build_codebook.py
"""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from build_form import FORM_ID, FORM_VERSION, choices_rows, survey_rows  # noqa: E402

OUT = HERE / "docs" / "codebook.md"

# Paper code -> digital value, for the lists re-based to avoid sentinel
# collisions. Without this, a paper round and a digital round cannot be
# concatenated, and someone will try.
CROSSWALK = {
    "6.01 water source": [
        ("1", "w01", "Piped into dwelling"), ("2", "w02", "Piped into compound"),
        ("3", "w03", "Public tap or standpipe"), ("4", "w04", "Tube well or borehole"),
        ("5", "w05", "Protected dug well"), ("6", "w06", "Unprotected dug well"),
        ("7", "w07", "Protected spring"),
        ("8", "w08", "Unprotected spring  <- paper 8 also meant 'does not know'"),
        ("9", "w09", "Rainwater  <- paper 9 also meant 'no answer'"),
        ("10", "w10", "Tanker or cart"), ("11", "w11", "Surface water"),
    ],
    "6.02 toilet facility": [
        ("1", "t01", "Flush to sewer"), ("2", "t02", "Flush to septic tank"),
        ("3", "t03", "Flush to pit latrine"), ("4", "t04", "Ventilated improved pit"),
        ("5", "t05", "Pit latrine with slab"), ("6", "t06", "Pit latrine without slab"),
        ("7", "t07", "Composting toilet"),
        ("8", "t08", "Bucket  <- paper 8 also meant 'does not know'"),
        ("9", "t09", "No facility or bush  <- paper 9 also meant 'no answer'"),
    ],
}


def partition_tables() -> dict[str, list[dict]]:
    """Walk the survey and assign every field to the table it lands in."""
    tables: dict[str, list[dict]] = {"household": [], "roster": [], "child": []}
    current = "household"
    depth_stack: list[str] = []

    for row in survey_rows():
        rtype = row.get("type", "")
        name = row.get("name", "")

        if rtype == "begin_repeat":
            depth_stack.append(current)
            current = "roster" if name == "roster" else "child"
            continue
        if rtype == "end_repeat":
            current = depth_stack.pop() if depth_stack else "household"
            continue
        if rtype in ("begin_group", "end_group", "note"):
            continue

        tables[current].append({
            "name": name,
            "type": rtype,
            "label": row.get("label::English (en)", "").strip(),
            "relevant": row.get("relevant", ""),
            "calculation": row.get("calculation", ""),
        })
    return tables


def value_labels() -> dict[str, list[tuple[str, str]]]:
    lists: dict[str, list[tuple[str, str]]] = {}
    for c in choices_rows():
        lists.setdefault(c["list_name"], []).append(
            (c["name"], c["label::English (en)"]))
    return lists


def render(tables: dict[str, list[dict]], labels: dict) -> str:
    L: list[str] = []
    a = L.append

    a(f"# Codebook - `{FORM_ID}` version `{FORM_VERSION}`")
    a("")
    a("**Generated** from the form definition by `build_codebook.py`. Not")
    a("maintained by hand, so it cannot drift from the instrument.")
    a("")
    a("## The three analysable tables")
    a("")
    a("The form has two repeats, which flatten into three tables. ODK Central")
    a("exports them as separate CSVs; the join keys below are what makes them one")
    a("dataset.")
    a("")
    a("```")
    a("household  ── one row per submission (one dwelling visited)")
    a("   │")
    a("   ├── roster  ── one row per usual resident")
    a("   │")
    a("   └── child   ── one row per eligible child (9-59 months)")
    a("                  Section 5 specimen fields live here too: the specimen")
    a("                  section sits INSIDE the child repeat, so there is no")
    a("                  separate specimen table.")
    a("```")
    a("")
    a("### Primary and foreign keys")
    a("")
    a("| Table | Primary key | Foreign key | Notes |")
    a("|---|---|---|---|")
    a("| `household` | `meta/instanceID` | - | ODK's submission UUID. Stable, "
      "globally unique, and the only key that survives a resubmission |")
    a("| `roster` | (`PARENT_KEY`, `line_no`) | `PARENT_KEY` → `instanceID` | "
      "`line_no` is `position(..)`, so it matches the paper roster line |")
    a("| `child` | (`PARENT_KEY`, `child_index`) | `PARENT_KEY` → `instanceID` | "
      "`q4_01_line` joins a child back to its `roster` row |")
    a("")
    a("**A natural key also exists** and should be used for deduplication against")
    a("paper rounds, not for joins:")
    a("`(q1_04_settlement, q1_06_structure, q1_07_hh_serial, q1_10_visit_date)`.")
    a("It is not guaranteed unique - two teams could in principle number the same")
    a("dwelling - which is exactly why `instanceID` is the primary key.")
    a("")
    a("**`specimen_label_full`** (`BSN######-C`) is the join key to the laboratory")
    a("system. It is unique per child where a specimen was obtained, and null")
    a("otherwise.")
    a("")
    a("## Reading a null")
    a("")
    a("A null in this dataset is never ambiguous, which is the main gain over the")
    a("paper round. Every field below lists the **relevance rule** that governs")
    a("when it is asked. If a field is null, either its relevance rule was false")
    a("- in which case the question was never put to the respondent - or a")
    a("measurement status field says explicitly why no value exists.")
    a("")
    a("**No sentinel value is ever stored in a numeric field.** See")
    a("`coding_scheme.md`.")
    a("")

    titles = {
        "household": "Table: `household` - one row per submission",
        "roster": "Table: `roster` - one row per usual resident",
        "child": "Table: `child` - one row per eligible child, including specimen",
    }
    for table, fields in tables.items():
        a(f"## {titles[table]}")
        a("")
        a(f"{len(fields)} fields.")
        a("")
        a("| Field | Type | Question / meaning | Null when |")
        a("|---|---|---|---|")
        for f in fields:
            meaning = f["label"] or (
                f"derived: `{f['calculation'][:56]}`" if f["calculation"] else "-")
            null_when = f["relevant"] if f["relevant"] else "never (always collected)"
            a(f"| `{f['name']}` | {f['type'].split()[0]} | {meaning[:76]} | "
              f"`{null_when[:64]}` |")
        a("")

    a("## Value labels")
    a("")
    for list_name, options in sorted(labels.items()):
        a(f"**`{list_name}`** - " + " · ".join(f"`{v}` {lab}" for v, lab in options))
        a("")

    a("## Paper-to-digital crosswalk")
    a("")
    a("Two lists were re-based so that no stored value can collide with a")
    a("non-response sentinel (see `coding_scheme.md`). **The categories and the")
    a("numbers read aloud to the respondent are unchanged** - only the stored")
    a("value differs. Concatenating a paper round with a digital round without")
    a("this mapping will produce nonsense.")
    a("")
    for question, rows in CROSSWALK.items():
        a(f"### {question}")
        a("")
        a("| Paper code | Digital value | Category |")
        a("|---|---|---|")
        for paper, digital, label in rows:
            a(f"| `{paper}` | `{digital}` | {label} |")
        a("")

    a("## Fields added that are not on the paper form")
    a("")
    a("| Field | Why it exists |")
    a("|---|---|")
    a("| `start_time`, `end_time`, `interview_duration_min` | Fabrication "
      "detection - see `fabrication_detection.md` |")
    a("| `device_id`, `audit` | as above |")
    a("| `enumerator_code`, `pin_entered` | Binds a submission to a person. "
      "1.08 on paper is a code anyone can write |")
    a("| `q0_label_range` | Confirms the team's specimen label book |")
    a("| `q4_08a_doc_type` | 4.08 asks for a three-way distinction its coding "
      "cannot hold (defect A2) |")
    a("| `q4_12a_more_than_one` | Lets analysis know when 4.13's single code is "
      "incomplete (defect C1) |")
    a("| `form_version` | Stamped into the data so mixed-version rounds are "
      "separable - see `deployment_plan.md` |")
    a("")
    a("## Paper questions satisfied by a differently-named field")
    a("")
    a("Every question on the paper form is accounted for. These four are captured")
    a("under a different name, because the digital form can derive or capture them")
    a("more reliably than an enumerator can type them.")
    a("")
    a("| Paper | Digital field | How |")
    a("|---|---|---|")
    a("| **1.08** Enumerator code | `enumerator_code` | Selected from the staff "
      "roster at sign-in and confirmed by PIN, rather than written. On paper, 1.08 "
      "is a code anyone can enter |")
    a("| **1.09** Team code | `enum_team` | **Derived** from the roster once the "
      "enumerator signs in. Cannot be mistyped, and cannot disagree with 1.08 |")
    a("| **7.01** Time the interview ended | `end_time`, and "
      "`interview_duration_min` | Captured automatically by the device. More "
      "reliable than a written time, and it is what makes the daily fabrication "
      "check possible (see `fabrication_detection.md`) |")
    a("| **4.02** Child name or initials | `q4_02_initials` | **Copied from the "
      "roster by calculation**, exactly as the paper form instructs, rather than "
      "re-typed. Recommended for removal on data-protection grounds |")
    a("")
    a("## Fields on the paper form that are NOT collected")
    a("")
    a("| Paper field | Why |")
    a("|---|---|")
    a("| 1.01 State | Single-valued. Stored as a constant, not asked |")
    a("| Roster column (7) *Eligible for Section 4* | Office-use column the "
      "enumerator was told to leave blank, then asked to read (defect A1). "
      "Eligibility is derived from roster ages |")
    a("| Roster column (8) *Section 4 page number* | Replaced by the repeat index |")
    a("| 5.01 specimen eligibility | Calculated from age, not asked (defect A3) |")
    a("| 7.03, 7.06 signatures | Replaced by authenticated submission and the "
      "supervisor review fields |")
    a("| 8.01-8.03 office use | Data entry and second-entry verification do not "
      "exist in a digital pipeline. This is the largest single saving: an entire "
      "double-entry step removed |")
    return "\n".join(L) + "\n"


def main() -> None:
    tables = partition_tables()
    labels = value_labels()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(tables, labels), encoding="utf-8")

    print("\nCodebook")
    print("-" * 46)
    for table, fields in tables.items():
        print(f"  {table:12s} {len(fields):>3} fields")
    print(f"  {'choice lists':12s} {len(labels):>3}")
    print(f"\n  written to {OUT.relative_to(HERE.parent)}")


if __name__ == "__main__":
    main()
