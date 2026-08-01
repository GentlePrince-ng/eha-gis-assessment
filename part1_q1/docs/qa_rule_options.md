# QA rule set - candidate thresholds and the argument for each

Working document. Each rule below gives the measured evidence, two or three defensible
threshold choices with what each costs, and a recommendation. **Nothing here is settled
until Solomon picks**, at which point it moves to `DECISIONS.md` with its reasoning and
into `qa_rules.md` as the implemented rule.

All counts are against the **296,526 in-campaign points** (9-13 March 2026) unless stated.

---

## Two corrections to earlier findings

Both came out of verification, and both change a rule.

### C-1. The degraded accuracy is **not** urban multipath. It is an equipment tier.

I earlier read the ~36 m accuracy cohort as the seeded urban-multipath effect in Idi-Oro,
the one Urban LGA. That was inference from accuracy alone and it is **wrong**.

Spatially joining every point to its LGA and splitting each team's accuracy by urban versus
non-urban:

| Team | Median acc. in Urban LGA | Median acc. elsewhere |
|---|---|---|
| T01 | 36.2 | 35.9 |
| T03 | 36.4 | 36.3 |
| T06 | 36.0 | 36.1 |
| T07 | 36.3 | 36.3 |
| T08 | 35.7 | 36.1 |
| T02 | 8.1 | 8.0 |
| T05 | 8.0 | 8.0 |
| T29 | 7.0 | 8.0 |

Accuracy follows the **team**, not the ground. Eight loggers - GL-7210, GL-4592, GL-1005,
GL-1647, GL-1429, GL-1388, GL-9693, GL-3464, on teams T03, T07, T01, T06, T08, T14, T20,
T15 - report ~36 m everywhere, including in rural Gwarin. The other 24 report ~8 m
everywhere, including in urban Idi-Oro.

The apparent LGA effect (Idi-Oro median 33.3 m against Gwarin 8.2 m) is **composition**:
the degraded loggers happen to spend most of their fixes in Idi-Oro. T15 has 16,964 urban
fixes against 29 elsewhere; T20 9,939 against 30.

**The reported accuracy is honest.** On a conflict-free series, comparing consecutive fixes
sixty seconds apart while near-stationary:

| Tier | Teams | Reported accuracy | Actual median step | 95th pct step |
|---|---|---|---|---|
| Degraded | 8 | 39.2 m | 30.7 m | 100.9 m |
| Normal | 31 | 8.0 m | 7.2 m | 27.5 m |

So the field can be trusted, and the two tiers are physically real.

**Why this changes the answer.** The question asks how I would treat dense urban areas where
multipath degrades accuracy. The defensible answer is that **this dataset does not show
multipath** - it shows a two-tier logger fleet - and reporting a multipath finding the data
contradicts would be the exact failure the question is testing for.

That is not a reason to skip the treatment, so it is set out here in full, together with
what it would cost.

### How I would treat genuine multipath

Multipath is *spatial and systematic*: signals bounce off buildings, so error rises in
built-up areas regardless of which device is carried. Four things follow.

1. **Widen the tolerance in the affected area only** - not globally, which would blur
   rural attribution for no reason.
2. **Lean on dwell rather than single fixes.** Multipath scatters individual positions but
   a team genuinely present still accumulates minutes near the settlement. Raising the
   dwell requirement while widening the radius trades a noisier position for a stronger
   time signal.
3. **Trust the accuracy field if it responds.** Most receivers inflate their reported error
   under multipath. Here it does not vary by location, which is itself the evidence that
   this is not multipath.
4. **Report urban and rural coverage separately**, because a single state-wide figure
   would average a well-measured area with a poorly-measured one and hide the difference.

### How the choice changes the result - measured

Widening the tolerance in the urban LGA only, holding everything else fixed:

| Urban tolerance | Settlements visited | Change | Ambiguous points | Agree with e-tally |
|---|---|---|---|---|
| **× 1 - 66-122 m (as submitted)** | **797** | - | **253** | 765 |
| × 1.5 - 66-183 m | 870 | +73 | 434 | 819 |
| × 2 - 66-244 m | 952 | +155 | 763 | 879 |
| × 3 - 66-366 m | 1,038 | +241 | 1,930 | 939 |

**The result is materially sensitive to this choice**, and that is worth saying plainly:
doubling the urban tolerance finds 155 more settlements - a 19% increase in measured
coverage - and would move the reconciliation gap by the same amount.

It also costs three times the ambiguity (763 points inside more than one settlement's
radius against 253), because the urban LGA holds 1,046 of the 2,562 settlements. Beyond
about ×2 the ambiguity grows faster than the coverage, which is where the trade stops being
worth making.

**I did not apply the widening**, because the accuracy evidence shows the degradation is
per-device rather than per-place, so there is nothing here for it to correct. Had the
pattern been spatial, ×1.5 to ×2 is the range I would have defended - and the sensitivity
above is what I would have published alongside it, rather than a single number.

### C-2. T14's logger failure is real but differently shaped.

I earlier reported "11 points on two days" from the row count of `T14_2026-03-11.csv`. That
was a *file* count, and the files overlap, so it understated the day. On the collision-
collapsed series:

**T14, 12 March: 210 distinct minutes, first fix 00:00, last fix 07:38.** The logger ran
overnight, then stopped at 07:38 - losing the entire working day. Against a median of 1,006
distinct minutes per team-day and a 5th percentile of 454, that is the worst team-day in
the campaign.

Same shape, real finding, but "the logger died at the start of the duty day" is a different
statement from "the logger recorded eleven points", and only one of them is true.

---

## R1 - Campaign window

**Evidence.** 633,207 of 929,733 stored records (68%) fall outside 9-13 March 2026. Several
loggers ran continuously for weeks: T01's fixes continue to 29 March, around the clock at
60-second intervals.

**Not a judgement call.** The campaign dates are stated in the pack README. The only
decision is *where* the filter lives, and that is settled in `DECISIONS.md` D-002a: applied
at QA as a counted rule, not silently at ingest.

**Action:** exclude from coverage attribution, retain in store, report the count.

---

## R2 - Duty hours ← **needs your decision**

**Evidence.** Collision-collapsed team-minutes by hour show a real but soft working signal
on top of a runaway-logger baseline:

```
00-06   ~4,000-5,100 per hour   (baseline: loggers left switched on)
07       7,269                  (ramp)
08-14   ~9,100-9,440            (plateau)
15-17    8,806 -> 8,235         (decline)
18-23    7,816 -> 6,327         (long taper)
```

Earliest first-fix across team-days clusters at **07:09-07:38**. Clean team-days end between
11:44 and 16:26.

| Option | Window | Flags | Argument |
|---|---|---|---|
| **A** | 07:00-16:59 | 144,411 (48.7%) | Matches the observed data: teams start 07:09-07:38 and the plateau runs 08:00-14:59. Derived from this campaign rather than imported. |
| **B** | 06:00-18:59 | 123,096 (41.5%) | Conservative. Keeps the ramp and taper, so a team genuinely working late is not erased. Costs precision - retains ~2 hours of probable idle logging each side. |
| **C** | Per-team-day, first to last fix on that day | - | No global window; each team-day defines its own. Adapts to genuine variation, but it is circular for the runaway loggers, whose "day" is 24 hours. |

**Recommendation: A, with B reported as a sensitivity.** A is evidence-led and I can defend
every boundary from the hourly profile. C is attractive but self-defeating on precisely the
eight teams that most need constraining.

**The honest caveat either way:** the taper to 23:00 never reaches zero, so no time window
cleanly separates work from idle logging. The window is a proxy, and the reconciliation
against the e-tally is what actually tests it.

---

## R3 - Implausible speed

**Evidence - this one is a gift.** Reported speed is cleanly bimodal with nothing in
between:

| Threshold | Points flagged |
|---|---|
| > 6 km/h | 1,437 |
| > 15 km/h | 1,437 |
| > 50 km/h | 1,437 |
| > 120 km/h | 1,437 |
| > 150 km/h | 1,394 |

Median reported speed is 4.0 km/h and the 99th percentile is 5.58 - walking pace, as
expected for house-to-house teams. **Every point above 6 km/h is also above 120 km/h.**

Independently, implied speed computed from consecutive conflict-free fixes 60 seconds
apart: median 3.95 km/h, 95th percentile 6.14, maximum **93,734 km/h**. 1,300 implied
steps exceed 15 km/h.

**Recommendation: flag reported speed > 15 km/h, and separately flag implied speed
> 15 km/h between consecutive fixes.**

**Why 15.** It sits far above sustained walking (~5 km/h) and far below the implausible
cluster, and - the actual argument - **the result is identical for any threshold from 6 to
120 km/h.** The strongest defence of a threshold is that the finding does not depend on it.
The two rules differ: reported speed is the logger's own claim, implied speed is derived
from position, and a point can fail one without the other. Flagging both catches teleports
that the logger reported as stationary.

---

## R4 - Positional accuracy ← **needs your decision, and it is the dangerous one**

**Evidence.** Distribution across in-campaign points: median 11.1 m, 75th 32.9, 90th 48.0,
99th 57.0, max 58.0.

Any threshold you pick touches **exactly the same eight teams** - no normal-tier point
exceeds 15 m:

| Cut | Points flagged | Teams touched |
|---|---|---|
| > 15 m | 124,103 (41.9%) | 8 |
| > 30 m | 80,868 (27.3%) | 8 |
| > 50 m | 23,158 (7.8%) | 8 |

And a >30 m cut would remove **62% of every degraded team's points**:

| Team | Points | Removed | % |
|---|---|---|---|
| T03 | 19,377 | 12,132 | 62.6 |
| T07 | 19,413 | 12,158 | 62.6 |
| T01 | 19,373 | 12,109 | 62.5 |
| T06 | 19,344 | 12,078 | 62.4 |
| T08 | 19,378 | 12,080 | 62.3 |
| T14 | 5,856 | 3,640 | 62.2 |
| T15 | 17,001 | 10,526 | 61.9 |
| T20 | 9,975 | 6,145 | 61.6 |

| Option | Rule | Consequence |
|---|---|---|
| **A** | Exclude points above a fixed cut (e.g. 30 m) | Removes ~62% of eight teams' tracks. Those teams then appear to have visited far fewer settlements - **a data-quality rule manufacturing a false coverage finding**, and the settlements they served look missed. |
| **B** | No accuracy exclusion. Carry accuracy into attribution instead: a point's search tolerance widens with its own reported error. | Keeps every team's work. Costs attribution precision for the eight teams, honestly and visibly, rather than deleting them. |
| **C** | Exclude only the extreme tail (>50 m, 7.8%), then apply B to the rest. | Removes the worst fixes without gutting a tier. Hybrid; hardest to justify cleanly because 50 m is arbitrary where 15 m and 30 m are not. |

**Recommendation: B.** With a fixed cut, the rule and the finding are confounded - you
cannot then say whether those eight teams underperformed or were filtered out, and Idi-Oro
is where most of their work is, so the urban LGA takes the hit. B makes accuracy a property
of the measurement rather than a gate on it, which is what the accuracy field is *for*.

This is also the rule most likely to be challenged at the walkthrough, and the strongest
counter is real: B lets low-quality fixes attribute to settlements, inflating coverage.
The answer is the sensitivity analysis in R9 - report coverage under both, and show how much
moves.

---

## R5 - Gaps in the fix sequence

**Evidence.** Of 108,742 consecutive intervals on the conflict-free series, **108,686 are
exactly 60 seconds** - matching the stated nominal rate. Every other gap is a whole-minute
multiple, i.e. dropped fixes rather than clock drift.

| Gap | Count |
|---|---|
| > 2 min | 156 |
| > 5 min | 155 |
| > 15 min | 111 |
| longest | 48,000 s (13.3 h) |

Note how few there are, and that >2 min and >5 min are almost the same set - gaps are
either one dropped fix or a long outage, with little between.

**Recommendation: flag > 5 minutes as a coverage interruption, > 15 minutes as an outage
requiring narrative.** Threshold defensible because the distribution is bimodal again: 155
versus 111 across a 3× change in threshold, so the choice barely moves the result. Source
for the 60-second baseline is the pack README, not my judgement.

---

## R6 - Stationary clusters

**Note:** for house-to-house vaccination, a stationary cluster is not only a QA signal, it
is the **visit signal**. A team stopped for several minutes at a settlement is what
"visited" looks like in GPS. Treating stationary points purely as noise would discard the
evidence the coverage analysis depends on.

Proposal: classify rather than flag - dwell clusters (stationary, inside a settlement's
tolerance, sustained beyond a minimum duration) as *visits*; stationary runs outside any
settlement as *idle*; stationary runs spanning a duty-day boundary as *logger left on*.
Needs the attribution tolerance from R7 before the durations can be set.

---

## R7 - `(team_id, timestamp)` conflicts, carried from ingest

**585,951 records** share a team and a minute with another record while carrying different
coordinates - 63% of the store. Options for resolution at the attribution stage (retain
the higher-accuracy fix; retain both and require agreement; treat the minute as unresolved)
are deferred until the attribution tolerance is set, since the right answer depends on
whether the disagreeing fixes fall inside the same settlement tolerance. If they do, the
conflict is immaterial and can be reported as such.

---

## R8 - Team-day completeness

**Evidence.** Distinct minutes per team-day across all 160 team-days: minimum 210, 5th
percentile 454, median 1,006, 95th percentile 1,440, maximum 1,440.

The 1,440 ceiling is a full 24 hours - the runaway loggers. The floor is T14 on 12 March
(see C-2).

**Recommendation:** flag team-days below the 5th percentile *of duty-hour minutes*, once R2
fixes the window - computing this on all-hours minutes rewards the runaway loggers and
penalises well-behaved ones, which is backwards.

---

## R9 - Required: sensitivity reporting

Given R2 and R4 are judgement calls that move the headline, the coverage result should be
reported under at least: duty window A vs B, and accuracy option A vs B. If coverage is
stable across them, the thresholds stop being a vulnerability and become a strength. If it
is not stable, that instability **is** a finding and belongs in the decision brief, because
it tells the Incident Manager how much to trust the number.

---

## What I need from you

1. **R2 - duty hours.** A (07:00-16:59, evidence-led) or B (06:00-18:59, conservative)?
2. **R4 - accuracy.** B (no exclusion, tolerance scales with accuracy) or A (fixed cut)?
   This is the one that can manufacture a false finding, so it is worth your time.
3. **R5 - gap threshold.** 5 minutes for interruption, 15 for outage - or different?

R1, R3, R6, R7, R8 I can proceed on as written unless you disagree.
