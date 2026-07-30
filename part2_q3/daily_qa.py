"""Daily fieldwork quality check (F11) - run every evening, not after close.

The operating conditions describe the failure this exists to catch:

    "In the last round one enumerator submitted 94 interviews with a mean
    duration of 4 minutes and almost no vaccination cards sighted. This was
    discovered only after fieldwork had closed."

Discovered after close is the whole problem. Ninety-four households were burned
and the round could not be repaired. So this runs against whatever has been
submitted **so far**, every evening, and produces a ranked list a supervisor can
act on the next morning.

Design decisions
----------------
**Robust statistics, not fixed thresholds.** "Flag under 10 minutes" is wrong on
day one of a different survey. Each indicator is compared against the *cohort's*
own median using median absolute deviation, so the rule adapts to how this round
is actually running and needs no recalibration.

**Two signals together, not one.** Short interviews alone are weak evidence - a
household of two with no eligible children is legitimately quick. Low card
sighting alone is weak - some settlements genuinely have few cards. The
described pattern is *both at once, from one enumerator, at high volume*, and
requiring conjunction is what keeps the flag list short enough to be worked.

**A minimum volume gate.** An enumerator with four submissions has no stable
median. Below the gate they are reported as "insufficient data", never as clean.

**It flags for review; it does not accuse.** Every output names the evidence and
the action, and the action is always a supervisor visit or an accompanied
re-interview. Fabrication is a finding a person makes, not a script.

Run:  python part2_q3/daily_qa.py --demo
      python part2_q3/daily_qa.py --submissions path/to/export.csv --day 3
"""

from __future__ import annotations

import argparse
import csv
import random
import statistics
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent

# Indicators are computed per enumerator per cumulative day of fieldwork.
MIN_SUBMISSIONS_FOR_STATS = 8      # below this, no stable median
MAD_THRESHOLD = 3.0                # robust equivalent of ~3 standard deviations
FLAG_SCORE_FOR_ESCALATION = 2      # how many indicators must fire together


def robust_z(value: float, values: list[float]) -> float:
    """Modified z-score using median absolute deviation.

    MAD rather than standard deviation because a fabricator with extreme values
    inflates the SD and hides themselves inside their own outlier. The median
    and MAD are unmoved by up to half the sample being contaminated.
    """
    if len(values) < 3:
        return 0.0
    median = statistics.median(values)
    deviations = [abs(v - median) for v in values]
    mad = statistics.median(deviations)
    if mad == 0:
        spread = statistics.pstdev(values)
        if spread == 0:
            return 0.0
        return (value - median) / spread
    return 0.6745 * (value - median) / mad


def load_submissions(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def summarise(rows: list[dict], up_to_day: int) -> dict[str, dict]:
    """Per-enumerator indicators from submissions received so far."""
    by_enum: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        if int(r["fieldwork_day"]) <= up_to_day:
            by_enum[r["enumerator_code"]].append(r)

    summary = {}
    for code, subs in by_enum.items():
        durations = [float(s["interview_duration_min"]) for s in subs]
        children = sum(int(s["children_enumerated"]) for s in subs)
        cards = sum(int(s["cards_seen"]) for s in subs)
        summary[code] = {
            "submissions": len(subs),
            "median_duration": statistics.median(durations),
            "card_rate": (cards / children) if children else None,
            "per_day": len(subs) / max(1, min(up_to_day, int(subs[-1]["fieldwork_day"]))),
            "consent_refusal_rate": sum(
                1 for s in subs if s["result"] != "completed") / len(subs),
            "distinct_gps": len({s["gps_rounded"] for s in subs}),
        }
    return summary


def evaluate(summary: dict[str, dict]) -> list[dict]:
    eligible = {c: s for c, s in summary.items()
                if s["submissions"] >= MIN_SUBMISSIONS_FOR_STATS}
    if len(eligible) < 3:
        return []

    durations = [s["median_duration"] for s in eligible.values()]
    per_days = [s["per_day"] for s in eligible.values()]
    card_rates = [s["card_rate"] for s in eligible.values() if s["card_rate"] is not None]

    findings = []
    for code, s in eligible.items():
        flags = []

        z_dur = robust_z(s["median_duration"], durations)
        if z_dur < -MAD_THRESHOLD:
            flags.append(("interviews far shorter than the cohort",
                          f"median {s['median_duration']:.1f} min "
                          f"(cohort {statistics.median(durations):.1f}), z={z_dur:.1f}"))

        if s["card_rate"] is not None and card_rates:
            z_card = robust_z(s["card_rate"], card_rates)
            if z_card < -MAD_THRESHOLD:
                flags.append(("vaccination cards sighted far less often",
                              f"{s['card_rate']:.0%} of children "
                              f"(cohort {statistics.median(card_rates):.0%}), "
                              f"z={z_card:.1f}"))

        z_vol = robust_z(s["per_day"], per_days)
        if z_vol > MAD_THRESHOLD:
            flags.append(("submission volume far above the cohort",
                          f"{s['per_day']:.1f}/day "
                          f"(cohort {statistics.median(per_days):.1f}), z={z_vol:.1f}"))

        if s["submissions"] >= MIN_SUBMISSIONS_FOR_STATS and s["distinct_gps"] <= 2:
            flags.append(("GPS barely moves between households",
                          f"{s['distinct_gps']} distinct locations across "
                          f"{s['submissions']} submissions"))

        if flags:
            findings.append({"enumerator": code, "flags": flags,
                             "score": len(flags), "summary": s})

    return sorted(findings, key=lambda f: -f["score"])


# ---------------------------------------------------------------------------
# Demonstration fixture. Synthetic, and generated here rather than shipped, so
# the check can be shown to catch the described pattern before any real data
# exists. One enumerator is planted with exactly that behaviour.
# ---------------------------------------------------------------------------
def make_demo(path: Path, seed: int = 20260730) -> Path:
    rng = random.Random(seed)
    rows = []
    normal = [f"ENU{n:03d}" for n in range(1, 20)]
    fabricator = "ENU020"

    for day in range(1, 15):
        for code in normal:
            for _ in range(rng.randint(4, 8)):
                children = rng.choice([0, 1, 1, 2, 2, 3])
                rows.append({
                    "enumerator_code": code, "fieldwork_day": day,
                    "interview_duration_min": round(rng.gauss(23, 5), 1),
                    "children_enumerated": children,
                    "cards_seen": sum(1 for _ in range(children) if rng.random() < 0.62),
                    "result": "completed" if rng.random() > 0.08 else "refused",
                    "gps_rounded": f"{rng.randint(0, 400)}",
                })
        # The planted pattern: high volume, ~4 minute interviews, almost no cards.
        for _ in range(rng.randint(10, 14)):
            children = rng.choice([1, 1, 2])
            rows.append({
                "enumerator_code": fabricator, "fieldwork_day": day,
                "interview_duration_min": round(rng.gauss(4.1, 0.8), 1),
                "children_enumerated": children,
                "cards_seen": sum(1 for _ in range(children) if rng.random() < 0.04),
                "result": "completed",
                "gps_rounded": f"{rng.randint(0, 2)}",
            })

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    return path


def report(day: int, summary: dict, findings: list[dict]) -> None:
    print(f"\nDaily fieldwork quality check - end of day {day}")
    print("=" * 72)
    total = sum(s["submissions"] for s in summary.values())
    thin = [c for c, s in summary.items() if s["submissions"] < MIN_SUBMISSIONS_FOR_STATS]
    print(f"  submissions so far      {total:>6,}")
    print(f"  enumerators reporting   {len(summary):>6}")
    print(f"  below the volume gate   {len(thin):>6}   (reported as insufficient "
          f"data, never as clean)")

    if not findings:
        print("\n  No enumerator flagged. This is not a clean bill of health - it "
              "means\n  nothing crossed the threshold today.")
        return

    print(f"\n  {len(findings)} enumerator(s) flagged for supervisor review, "
          f"ranked by signal count")
    for f in findings:
        escalate = f["score"] >= FLAG_SCORE_FOR_ESCALATION
        print("\n  " + "-" * 68)
        print(f"  {f['enumerator']}   {f['score']} indicator(s)   "
              f"{'ESCALATE TODAY' if escalate else 'monitor'}")
        for name, detail in f["flags"]:
            print(f"     * {name}")
            print(f"       {detail}")
        s = f["summary"]
        print(f"     submissions {s['submissions']}, median duration "
              f"{s['median_duration']:.1f} min, cards "
              f"{s['card_rate']:.0%}" if s["card_rate"] is not None else "")
        if escalate:
            print("     ACTION: supervisor accompanies this enumerator tomorrow "
                  "and re-interviews\n             three households already "
                  "submitted. Do not confront on the\n             basis of this "
                  "report alone - it is evidence for a visit, not a finding.")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--submissions", type=Path)
    ap.add_argument("--day", type=int, default=3)
    ap.add_argument("--demo", action="store_true")
    args = ap.parse_args()

    if args.demo:
        path = make_demo(HERE / "tests" / "fixtures" / "demo_submissions.csv")
        print(f"  demo fixture written to {path.relative_to(HERE)}")
        print("  19 enumerators behaving normally, 1 planted with the pattern "
              "described\n  in the operating conditions (high volume, ~4 minute "
              "interviews, no cards)")
        rows = load_submissions(path)
        for day in (2, 3):
            summary = summarise(rows, day)
            report(day, summary, evaluate(summary))
        return

    if not args.submissions:
        sys.exit("Provide --submissions <export.csv> or --demo")
    rows = load_submissions(args.submissions)
    summary = summarise(rows, args.day)
    report(args.day, summary, evaluate(summary))


if __name__ == "__main__":
    main()
