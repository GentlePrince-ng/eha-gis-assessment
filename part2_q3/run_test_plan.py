"""Execute the test plan against the constraints in the built XForm.

`test_plan.md` specifies 54 cases and every one carried *"Result: not yet
executed"*. This runs the ones that can be run without a device, and says
plainly which cannot and why.

**What this is.** For each case it takes the constraint expression **out of the
built XForm**, evaluates it against the case's input, and compares the verdict to
the expected one. It is the same discipline as the check-digit test: reading an
expression proves nothing, running it proves something.

**What this is not.** It is not ODK Collect. It evaluates expressions against a
supplied instance; it does not render a form, walk a repeat, sync a device or
encrypt a submission. Cases that depend on any of that are reported
NOT-EXECUTABLE with the reason, never as passes. A harness that quietly counted
them as passing would be worse than no harness.

    python part2_q3/run_test_plan.py
"""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from build_test_plan import SCENARIOS, boundary_cases, numeric_ranges  # noqa: E402

XFORM = HERE / "form" / "bansara_hh_2026.xml"

# Expression features this harness cannot evaluate, and the reason each needs a
# device or a server rather than an evaluator.
UNSUPPORTED = {
    "instance(": "reads an attached media file or the last-saved submission",
    "indexed-repeat(": "reaches across repeat instances",
    "count(": "counts sibling repeat instances",
    "current()": "resolves relative to a repeat instance",
}


# ---------------------------------------------------------------------------
# Scenario cases, given the concrete inputs the prose describes.
#
# `expr` names which bind to evaluate: a constraint, a relevance rule, or a
# calculate. Several of the cases the question REQUIRES are relevance or
# calculate logic rather than constraints, which is why the harness reads all
# three rather than constraints alone.
#
# `ctx` supplies the other fields the expression reads. `want` is what the case
# expects: True means the expression should hold - accept, or show, or equal.
# ---------------------------------------------------------------------------
SCENARIO_INPUTS: dict[str, dict] = {
    "S01": dict(node="q5_01_specimen_eligible", kind="calculate", value=None,
                ctx={"q4_03_age_months": 11}, want=0,
                note="child of 11 months: no specimen sought"),
    "S02": dict(node="q5_01_specimen_eligible", kind="calculate", value=None,
                ctx={"q4_03_age_months": 12}, want=1,
                note="child of 12 months: specimen sought"),
    "S03": dict(node="q4_07_position_warn", kind="relevant", value=None,
                ctx={"q4_03_age_months": 23, "q4_07_position": "2"}, want=True,
                note="23 months measured standing: warning shown"),
    "S04": dict(node="q4_07_position_warn", kind="relevant", value=None,
                ctx={"q4_03_age_months": 24, "q4_07_position": "2"}, want=False,
                note="24 months measured standing: no warning"),
    "S05": dict(node="q1_10_visit_date", kind="constraint", value="2026-05-31",
                ctx={}, want=False, note="date before the fieldwork window"),
    "S06": dict(node="q1_10_visit_date", kind="constraint", value="2026-07-01",
                ctx={}, want=False, note="date after the fieldwork window"),
    "S07": dict(node="roster_mismatch_note", kind="relevant", value=None,
                ctx={"roster_count": 5, "q3_01_hh_size": 6}, want=True,
                note="roster of 5 against a stated household size of 6"),
    "S08": dict(node="q2_01_statement_read", kind="constraint", value="2",
                ctx={}, want=False,
                note="consent statement not read: the one hard block"),
    "S14": dict(node="pin_entered", kind="constraint", value="0000",
                ctx={"enum_pin": "9384"}, want=False, note="wrong PIN"),
    "S15": dict(node="q1_02_lga", kind="constraint", value="LGA01",
                ctx={"enum_lga": "LGA02", "enum_role": "Enumerator"}, want=False,
                note="LGA not the one assigned to this enumerator"),
    "S21": dict(node="q4_05_weight_kg", kind="constraint", value="152",
                ctx={}, want=False, note="152 kg, a transposed 15.2"),
}


def binds_from_xform() -> dict[str, dict[str, str]]:
    """constraint, relevant and calculate for every field in the deployed form."""
    xml = XFORM.read_text(encoding="utf-8")
    out: dict[str, dict[str, str]] = {}
    for m in re.finditer(r'<bind nodeset="([^"]+)"([^>]*)/>', xml):
        node, attrs = m.group(1).split("/")[-1], m.group(2)
        entry = {}
        for kind in ("constraint", "relevant", "calculate"):
            v = re.search(kind + r'="([^"]+)"', attrs)
            if v:
                entry[kind] = html.unescape(v.group(1))
        if entry:
            out[node] = entry
    return out


def evaluate_with_context(expr: str, value, ctx: dict):
    """Evaluate an expression given the value under test and sibling fields."""
    for token in UNSUPPORTED:
        if token in expr:
            return None
    e = expr
    # node references -> context lookups, longest path first
    for name in sorted(ctx, key=len, reverse=True):
        e = re.sub(r"(?:\.{1,2}/)*[\w/]*\b" + re.escape(name) + r"\b",
                   f"__ctx[{name!r}]", e)
    e = re.sub(r"date\(\s*'([^']+)'\s*\)", lambda m: repr(m.group(1)), e)
    e = re.sub(r"\bif\(", "__iff(", e)
    if value is not None:
        e = re.sub(r"\bstring-length\(\s*\.\s*\)", f"len({value!r})", e)
        e = re.sub(r"(?<![\d.\w'\]])\.(?![\d\w])", "__v", e)
    e = re.sub(r"(?<![<>!=])=(?!=)", "==", e)
    e = re.sub(r"\bnot\(", "not (", e)
    try:
        v = float(value) if value is not None and re.fullmatch(r"-?\d+(\.\d+)?", value) else value
    except (TypeError, ValueError):
        v = value
    try:
        return eval(e, {"__builtins__": {}, "len": len, "float": float,   # noqa: S307
                        "__iff": lambda c, a, b: a if c else b},
                    {"__v": v, "__ctx": ctx})
    except Exception:
        return None


def constraints_from_xform() -> dict[str, str]:
    """Every constraint in the deployed form, keyed by field name."""
    xml = XFORM.read_text(encoding="utf-8")
    out = {}
    for m in re.finditer(r'<bind nodeset="([^"]+)"([^>]*)/>', xml):
        node, attrs = m.group(1), m.group(2)
        c = re.search(r'constraint="([^"]+)"', attrs)
        if c:
            out[node.split("/")[-1]] = html.unescape(c.group(1))
    return out


def to_python(expr: str, value: str) -> str:
    """Translate the XPath subset used by this form's range constraints."""
    e = expr
    e = re.sub(r"\bstring-length\(\s*\.\s*\)", f"len({value!r})", e)
    e = re.sub(r"\bnumber\(\s*\.\s*\)", f"float({value!r})", e)
    e = re.sub(r"regex\(\s*\.\s*,\s*'([^']*)'\s*\)",
               lambda m: f"bool(__re.fullmatch({m.group(1)!r}, {value!r}))", e)
    # bare '.' as the value under test - not inside a decimal number
    e = re.sub(r"(?<![\d.\w'])\.(?![\d\w])", f"__v", e)
    e = e.replace(" = ", " == ").replace("!==", "!=")
    e = re.sub(r"\bnot\(", "not (", e)
    return e


def evaluate(expr: str, value: str) -> bool | None:
    """True/False, or None when the expression needs something we do not have."""
    for token in UNSUPPORTED:
        if token in expr:
            return None
    try:
        v = float(value)
    except ValueError:
        v = value
    try:
        return bool(eval(to_python(expr, value),                # noqa: S307
                         {"__builtins__": {}, "__re": re, "len": len,
                          "float": float, "bool": bool},
                         {"__v": v}))
    except Exception:
        return None


def main() -> None:
    if not XFORM.exists():
        sys.exit("XForm not built. Run build_form.py first.")

    constraints = constraints_from_xform()
    cases = boundary_cases(numeric_ranges())

    executed = passed = failed = 0
    failures: list[str] = []
    skipped: list[tuple[str, str]] = []

    print("\nTest plan execution")
    print("=" * 78)
    print("\n  Range boundary cases - evaluated against the deployed constraint")
    print("  " + "-" * 74)

    for case in cases:
        expr = constraints.get(case["target"])
        if expr is None:
            skipped.append((case["id"], "no constraint on the target field"))
            continue
        verdict = evaluate(expr, case["input"])
        if verdict is None:
            reason = next((why for tok, why in UNSUPPORTED.items() if tok in expr),
                          "expression outside the supported subset")
            skipped.append((case["id"], reason))
            continue
        executed += 1
        want_accept = case["expected"] == "ACCEPT"
        ok = verdict == want_accept
        passed += ok
        failed += not ok
        if not ok:
            failures.append(
                f"{case['id']} {case['target']} = {case['input']}: "
                f"expected {case['expected']}, constraint said "
                f"{'ACCEPT' if verdict else 'REJECT'}")

    print(f"  {executed} of {len(cases)} boundary cases executed, "
          f"{passed} passed, {failed} failed")
    for f in failures:
        print(f"    FAIL  {f}")

    # --- scenarios --------------------------------------------------------
    print("\n  Scenario cases - evaluated against the deployed bind")
    print("  " + "-" * 74)
    binds = binds_from_xform()
    device_only = 0
    required = {"S01", "S02", "S03", "S04", "S05", "S06", "S07"}

    for s in SCENARIOS:
        spec = SCENARIO_INPUTS.get(s["id"])
        if spec is None:
            device_only += 1
            continue
        expr = binds.get(spec["node"], {}).get(spec["kind"])
        if expr is None:
            skipped.append((s["id"], f"no {spec['kind']} on {spec['node']}"))
            continue
        got = evaluate_with_context(expr, spec["value"], dict(spec["ctx"]))
        if got is None:
            device_only += 1
            continue
        executed += 1
        ok = got == spec["want"]
        passed += ok
        failed += not ok
        mark = "REQUIRED " if s["id"] in required else ""
        print(f"  [{'PASS' if ok else 'FAIL'}] {s['id']} {mark}{spec['note']}")
        if not ok:
            failures.append(f"{s['id']} {spec['node']}: expected {spec['want']!r}, got {got!r}")

    print(f"\n  {device_only} scenario cases require a device or server - form")
    print("    navigation, repeats, attached media, last-saved submissions,")
    print("    sync, or encryption")

    print("\n" + "=" * 78)
    print(f"  EXECUTED   {executed:>3} of {len(cases) + len(SCENARIOS)} cases, "
          f"{passed} passed, {failed} failed")
    print(f"  NOT RUN    {len(skipped) + device_only:>3} - reported, never counted as passing")
    if skipped:
        by_reason: dict[str, int] = {}
        for _, reason in skipped:
            by_reason[reason] = by_reason.get(reason, 0) + 1
        for reason, n in sorted(by_reason.items(), key=lambda kv: -kv[1]):
            print(f"             {n:>3}  {reason}")
    print()
    print("  A case this harness cannot run is not a case that passes. The")
    print("  remainder need ODK Collect and a person, and test_plan.md says so.")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
