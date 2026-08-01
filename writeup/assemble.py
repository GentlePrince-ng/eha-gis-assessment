"""Assemble the single submission document.

The question requires written responses in one document. This concatenates the
sources in a deliberate reading order - not alphabetical, which is what a glob
gives and which puts the decision brief before the method that produced it.

Page breaks are inserted before each part and each response so a marker opening
the file lands on a clean page rather than mid-table.

Run:  python writeup/assemble.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PANDOC = Path(r"C:/Users/SolomonOladimeji/AppData/Local/Pandoc/pandoc.exe")

# A native Word table-of-contents field, placed where we want it rather than
# where --toc puts it (immediately after the title block, which leaves the cover
# sharing page 1 with the contents). Word fills in the entries and page numbers;
# `dirty` asks it to do so when the document is opened.
TOC_FIELD = (
    "\n```{=openxml}\n"
    # TOCHeading, not Heading1: Word's TOC Heading style carries no outline
    # level, so the word "Contents" does not list itself as an entry.
    '<w:p><w:pPr><w:pStyle w:val="TOCHeading"/></w:pPr>'
    "<w:r><w:t>Contents</w:t></w:r></w:p>"
    '<w:p><w:r><w:fldChar w:fldCharType="begin" w:dirty="true"/></w:r>'
    '<w:r><w:instrText xml:space="preserve"> TOC \\o "1-2" \\h \\z \\u </w:instrText></w:r>'
    '<w:r><w:fldChar w:fldCharType="separate"/></w:r>'
    "<w:r><w:t>Select all and press F9 to build the table of contents.</w:t></w:r>"
    '<w:r><w:fldChar w:fldCharType="end"/></w:r></w:p>'
    "\n```\n\n"
)

PAGE_BREAK = '\n```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n\n'

# (heading, [files]) - order is the reading order, not the filesystem's.
SECTIONS: list[tuple[str, list[str]]] = [
    ("", ["writeup/00_cover.md"]),
    ("", ["writeup/01_summary.md"]),
    ("# PART 1 - Question 1\n\n## Campaign team tracking and coverage reconciliation\n",
     [
         "part1_q1/docs/qa_rules.md",
         "part1_q1/docs/qa_rule_options.md",
         "part1_q1/docs/crs_and_tolerance_options.md",
         "part1_q1/docs/coordinate_defects.md",
         "part1_q1/docs/reconciliation.md",
         "part1_q1/docs/cluster_analysis.md",
         "part1_q1/docs/artefact_vs_failure.md",
         "part1_q1/docs/decision_brief.md",
         "part1_q1/docs/deliverables.md",
     ]),
    ("# PART 2 - Question 3\n\n## Converting a paper questionnaire into a digital form\n",
     [
         "part2_q3/docs/deliverables.md",
         "part2_q3/docs/defect_report.md",
         "part2_q3/docs/coding_scheme.md",
         "part2_q3/docs/consistency_checks.md",
         "part2_q3/docs/constraint_register.md",
         "part2_q3/docs/validation.md",
         "part2_q3/docs/external_data.md",
         "part2_q3/docs/test_plan.md",
         "part2_q3/docs/label_reuse.md",
         "part2_q3/docs/fabrication_detection.md",
         "part2_q3/docs/data_protection.md",
         "part2_q3/docs/deployment_plan.md",
         "part2_q3/docs/version_history.md",
         "part2_q3/docs/codebook.md",
         "part2_q3/docs/deliberate_scope.md",
     ]),
    ("# PART 3 - Question 5\n", ["part3_q5/q5_coordination.md"]),
    ("# PART 3 - Question 6\n", ["part3_q6/q6_capability.md"]),
    ("# ANNEXES\n\nExcluded from the Q6 page limit, as the question permits.\n",
     [
         "part3_q6/annex_a_competency_framework.md",
         "part3_q6/annex_b_session_in_full/README.md",
         "part3_q6/annex_b_session_in_full/facilitator_guide.md",
         "part3_q6/annex_b_session_in_full/participant_brief.md",
         "part3_q6/annex_b_session_in_full/model_answer.md",
         "part3_q6/annex_c_assessment_instrument.md",
         "part3_q6/annex_d_dataset_spec.md",
         "part3_q6/annex_e_session_plan.md",
     ]),
]


def main() -> None:
    parts: list[str] = []
    n_files = 0
    for heading, files in SECTIONS:
        if heading:
            parts.append(PAGE_BREAK + heading)
        for i, rel in enumerate(files):
            path = ROOT / rel
            if not path.exists():
                sys.exit(f"missing source: {rel}")
            if heading and i > 0:
                parts.append(PAGE_BREAK)
            parts.append(path.read_text(encoding="utf-8"))
            n_files += 1
            # Cover page stands alone, then the contents, then the summary.
            # The cover carries no heading of its own, so it does not appear in
            # the table of contents it precedes.
            if rel.endswith("00_cover.md"):
                parts.append(PAGE_BREAK + TOC_FIELD + PAGE_BREAK)

    combined = HERE / "responses.md"
    combined.write_text("\n\n".join(parts), encoding="utf-8")

    out = HERE / "responses.docx"
    result = subprocess.run(
        [str(PANDOC), str(combined), "-o", str(out),
         "--from", "markdown+pipe_tables+raw_attribute",
         "--reference-doc", str(HERE / "reference.docx"),
         # images are written repo-root-relative, so pandoc can find them
         # from a combined document that lives in writeup/
         "--resource-path", str(ROOT),
         "-V", "lang=en-GB"],
        capture_output=True, text=True)
    if result.returncode != 0:
        sys.exit(result.stdout + result.stderr)

    words = len(combined.read_text(encoding="utf-8").split())
    print(f"\n  sources combined   {n_files:>6}")
    print(f"  words              {words:>6,}")
    print(f"  responses.docx     {out.stat().st_size / 1024:>6.0f} KB")
    if result.stderr.strip():
        print("\n  pandoc:", result.stderr.strip()[:400])


if __name__ == "__main__":
    main()
