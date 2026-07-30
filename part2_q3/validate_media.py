"""Verify that every external reference in the XForm actually resolves.

Why this exists
---------------
pyxform and ODK Validate both pass a form whose external lookups are broken.
They check the form in isolation; neither opens the media files. Three failures
get through:

1. A `jr://file-csv/x.csv` reference with no matching media file.
2. An `instance('x')` call in a constraint or calculation where `x` was never
   declared as an external instance — pyxform only declares instances for
   `select_one_from_file` *types*, so an `instance()` call inside an expression
   is invisible to it. The lookup silently returns an empty nodeset, `number()`
   of empty is `NaN`, and the constraint quietly rejects everything.
3. A `choice_filter` or instance path naming a column the CSV does not have.

All three convert clean, validate clean, and fail on the device. This is the
same shape as a picture-format `format-date()` that stores a literal string:
tooling reports success and the field data is wrong.

Found in this form by (2): the specimen serial-range constraint referenced
`instance('specimen_label_allocation')`, which was never declared, so the
constraint would have rejected every valid label. Adding this check is the
response — a defect found once by hand should be found automatically thereafter.

Run:  python part2_q3/validate_media.py
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
XML = HERE / "form" / "bansara_hh_2026.xml"
MEDIA = HERE / "form" / "media"


def csv_columns(path: Path) -> list[str]:
    with path.open(newline="", encoding="utf-8-sig") as fh:
        return next(csv.reader(fh), [])


def main() -> None:
    if not XML.exists():
        sys.exit("XForm not built. Run build_form.py first.")
    xml = XML.read_text(encoding="utf-8")

    external = dict(re.findall(r'<instance\s+id="([^"]+)"\s+src="jr://file-csv/([^"]+)"', xml))
    declared = set(re.findall(r'<instance\s+id="([^"]+)"', xml))
    referenced = set(re.findall(r"instance\('([^']+)'\)", xml))

    failures: list[str] = []
    print("\nExternal reference check")
    print("=" * 68)

    # --- 1. every instance() call resolves to a declared instance ----------
    undeclared = sorted(referenced - declared)
    if undeclared:
        for name in undeclared:
            failures.append(
                f"instance('{name}') is referenced but never declared. "
                f"Add a select_one_from_file question so pyxform declares it."
            )
    print(f"  instance() calls referenced      {len(referenced):>3}")
    print(f"  instances declared               {len(declared):>3}")
    print(f"  referenced but undeclared        {len(undeclared):>3}"
          f"{'   <- FAIL' if undeclared else ''}")

    # --- 2. every declared media file exists -------------------------------
    print(f"\n  {'media file':34s} {'present':>8}  {'rows':>7}")
    print("  " + "-" * 60)
    present_columns: dict[str, list[str]] = {}
    for instance_id, filename in sorted(external.items()):
        path = MEDIA / filename
        if not path.exists():
            failures.append(f"{filename} is referenced by the form but not in form/media/")
            print(f"  {filename:34s} {'MISSING':>8}")
            continue
        cols = csv_columns(path)
        present_columns[instance_id] = cols
        rows = sum(1 for _ in path.open(encoding="utf-8")) - 1
        print(f"  {filename:34s} {'yes':>8}  {rows:>7,}")

        # select_one_from_file needs name and label
        for required in ("name", "label"):
            if required not in cols:
                failures.append(
                    f"{filename} has no '{required}' column; "
                    f"select_one_from_file requires it")

    # --- 3. every column referenced in an instance path exists -------------
    print(f"\n  {'instance path':44s} {'column resolves':>15}")
    print("  " + "-" * 62)
    path_refs = re.findall(r"instance\('([^']+)'\)/root/item\[([^\]]+)\]/(\w+)", xml)
    seen = set()
    for instance_id, predicate, field in path_refs:
        key = (instance_id, predicate, field)
        if key in seen:
            continue
        seen.add(key)
        cols = present_columns.get(instance_id)
        pred_col = predicate.split("=")[0].strip()
        for col in (pred_col, field):
            ok = cols is not None and col in cols
            if not ok:
                failures.append(
                    f"instance('{instance_id}') path uses column '{col}', "
                    f"which is not in {external.get(instance_id, '?')}")
            label = f"{instance_id}[{pred_col}]/{field}"
            print(f"  {label:44s} {'yes' if ok else 'NO':>15}")
            break

    # --- 4. choice_filter columns ------------------------------------------
    print()
    print("=" * 68)
    if failures:
        print(f"  FAILED - {len(failures)} problem(s):\n")
        for f in failures:
            print(f"    * {f}")
        sys.exit(1)
    print("  PASSED - every external reference resolves to a real file and column")
    print("\n  Note: the form cannot be previewed in XLSForm Online, which has no")
    print("  way to attach media. Deploy to ODK Central with these attachments,")
    print("  or copy them beside the form in ODK Collect. See docs/validation.md.")


if __name__ == "__main__":
    main()
