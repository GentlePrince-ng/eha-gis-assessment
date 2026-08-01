---
title: "eHealth Africa - Technical Assessment"
subtitle: "Senior Coordinator, Data and GIS Analytics · Data Informatics Department"
author: "Solomon Oladimeji"
date: "1 August 2026"
lang: en-GB
---

# Submission summary

| Part | Question attempted |
|---|---|
| **Part 1** | **Q1** - Campaign team tracking and coverage reconciliation |
| **Part 2** | **Q3** - Converting a paper questionnaire into a digital form |
| **Part 3** | **Q5** - Coordinating delivery through the round |
| **Part 3** | **Q6** - Building capability in the counterpart agency |

Part 1 Q2 and Part 2 Q4 are not attempted. The instructions state that depth is
valued over breadth, and Part 2 states that the unattempted option will be
probed at the walkthrough regardless; I have prepared for that rather than
submitting thin work on both.

**Question 7 is referenced three times in the question paper but was not issued
with it.** Its marking box appears after Q6 with no question attached. The
connection it asks for - between coordination fragility and the capability gap -
is made in §6 of Q5 and §7 of Q6.

## Repository

**github.com/GentlePrince-ng/eha-gis-assessment** - public, with the full commit
history. Everything in this document is reproducible from the supplied data pack
by `python run_all.py`; `verify_claims.py` re-checks every headline figure quoted
here against the rebuilt outputs.

**AI assistance is declared in `AI_USE.md`**, including how the work was
structured and which errors independent verification caught and corrected.

## Page limits

Q5 is within three pages. Q6 is within six pages excluding annexes, as the
question permits. Annexes A-E carry artefacts to be used rather than argument to
be read.

\newpage



```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# PART 1 - Question 1

## Campaign team tracking and coverage reconciliation


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



```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```



# Projection and attribution tolerance - measured options

Two thresholds the assessment explicitly warns about (*"thresholds, buffers, or tolerances
asserted without justification"* is an automatic mark loss). Both measured rather than
asserted. Decision goes to `DECISIONS.md` D-003 and D-005 once chosen.

---

## D-003 - Projected coordinate reference system

Everything arrives EPSG:4326. Distortion measured against **true geodesic distance on the
WGS84 ellipsoid** (`pyproj.Geod.inv`), over 4,000 random settlement pairs, and against
true geodesic polygon area for the 40 wards.

Study area: longitude 6.954-8.429, latitude 10.366-11.573.

### Distance error

| CRS | Median abs. error | 95th pct | Max | Max relative |
|---|---|---|---|---|
| **EPSG:32632 - WGS 84 / UTM zone 32N** | **7.8 m** | 21.9 m | 33.6 m | 0.035% |
| EPSG:26332 - Minna / Nigeria Mid Belt | 7.5 m | 21.6 m | 33.2 m | 0.034% |
| EPSG:3857 - Web Mercator | 1,382.6 m | 2,554.6 m | 3,350.1 m | 2.665% |
| ESRI:102022 - Africa Albers Equal Area | 1,737.1 m | 4,658.6 m | 6,758.5 m | 4.995% |

### Error at short range - the scale a settlement tolerance actually operates at

| CRS | Median error | Max abs. error |
|---|---|---|
| UTM 32N | −0.12 m | 0.13 m |
| Minna Mid Belt | −0.12 m | 0.13 m |
| Web Mercator | +17.49 m | 18.79 m |
| Africa Albers | +8.42 m | 13.46 m |

### Area error, ward polygons

| CRS | Median relative | Max abs. relative |
|---|---|---|
| UTM 32N | −0.031% | 0.068% |
| Minna Mid Belt | −0.030% | 0.068% |
| Web Mercator | +4.437% | 4.801% |
| Africa Albers | **0.000%** | 0.028% |

### Recommendation: **EPSG:32632, WGS 84 / UTM zone 32N**

- **Web Mercator is disqualified**, and it matters that this is measured rather than
  recited: a 17.5 m error at the scale of a 50 m tolerance is a third of the tolerance, and
  4.4% on ward area would corrupt any density or rate.
- **Africa Albers is the right tool for the wrong job here.** It is the best area
  projection measured (0.000% median), and the worst distance one. This analysis is
  dominated by buffers and distances, so it is not the working CRS - though it remains the
  correct choice if an area-normalised statistic is ever wanted. At this extent UTM's area
  error of 0.03% makes that unnecessary.
- **UTM 32N over Minna Mid Belt**, despite Minna being nominally 0.3 m better across 4,000
  pairs - a difference far below GPS noise and therefore not a reason. The real reason is
  **datum**: the track data is GPS, i.e. WGS84. UTM 32N is WGS84-based, so reprojection is a
  pure map projection with no datum change. EPSG:26332 sits on the Minna datum
  (Clarke 1880), so using it introduces a datum transformation whose own uncertainty is of
  the order of metres - buying nothing measurable and adding an error term.
- **The study area sits entirely inside zone 32** (6°E-12°E), so UTM's real weakness,
  straddling a zone boundary, does not arise. Worth stating, because it is the first thing
  a reviewer should check.

---

## D-005 - Attribution tolerance ← **needs your decision**

### What bounds the tolerance: how far apart settlements are

Distance to nearest other settlement, projected to UTM 32N:

| LGA | Type | n | Min | 5th pct | Median | 75th pct |
|---|---|---|---|---|---|---|
| Idi-Oro | Urban | 1,046 | 8 m | 190 m | 669 m | 1,124 m |
| Katsuma | Rural | 504 | 56 m | 212 m | 734 m | 1,218 m |
| Gwarin | Rural | 432 | 22 m | 176 m | 796 m | 1,299 m |
| Ilela | Mixed | 580 | 40 m | 195 m | 834 m | 1,381 m |

Overall median 734 m, 5th percentile 194 m, 1st percentile 79 m, minimum 8 m.

**Note the urban LGA is not much denser than the rural ones** - median 669 m against
734-834 m. The usual justification for a tighter urban tolerance ("settlements are packed
closer together in town") is not supported here, and I would be wrong to assert it.

### What a wider tolerance costs: settlement buffers begin to overlap

A point inside two settlements' buffers cannot be attributed unambiguously.

| Tolerance | Settlements with an overlapping buffer | % of masterlist |
|---|---|---|
| 25 m | 8 | 0.3% |
| 50 m | 42 | 1.6% |
| 100 m | 136 | 5.3% |
| 200 m | 543 | 21.2% |
| 300 m | 985 | 38.4% |
| 500 m | 1,674 | 65.3% |

### Coverage against tolerance, on the 150,948 usable points

| Tolerance | Ambiguous points | Settlements visited | % of masterlist | Agree with e-tally | Tracks only | **e-tally only** |
|---|---|---|---|---|---|---|
| 25 m | 28 | 813 | 31.7% | 770 | 43 | 1,253 |
| 50 m | 65 | 901 | 35.2% | 832 | 69 | 1,191 |
| 100 m | 501 | 1,069 | 41.7% | 950 | 119 | 1,073 |
| 200 m | 1,766 | 1,262 | 49.3% | 1,095 | 167 | 928 |
| 300 m | 4,765 | 1,415 | 55.2% | 1,196 | 219 | 827 |
| 500 m | 14,601 | 1,652 | 64.5% | 1,360 | 292 | 663 |

### Accuracy-scaled tolerance - `tolerance = base + 2 × reported accuracy`

This is the mechanism D-004d promised: a point's search radius widens with its own
reported error rather than the whole tier being excluded.

| Base | Normal tier gets | Degraded tier gets | Ambiguous points | Settlements visited | Agree with e-tally | e-tally only |
|---|---|---|---|---|---|---|
| 25 m | 41 m | 97 m | 117 | 987 | 901 | 1,122 |
| **50 m** | **66 m** | **122 m** | **253** | **1,071** | **954** | **1,069** |
| 100 m | 116 m | 172 m | 938 | 1,193 | 1,045 | 978 |

### The result that decides it

Compare like for like:

| Method | Settlements visited | Ambiguous points |
|---|---|---|
| Fixed 100 m | 1,069 | **501** |
| Scaled, base 50 m | 1,071 | **253** |

**Same coverage, half the ambiguity.** The accuracy-scaled tolerance is not a compromise -
it dominates the fixed tolerance on both axes at equivalent reach. That is an independent
vindication of D-004d: information in the accuracy field that a fixed cut throws away is
doing real work.

**Recommendation: accuracy-scaled, base 50 m, k = 2** (normal ≈ 66 m, degraded ≈ 122 m).

Why base 50: at 50 m only 1.6% of settlements have overlapping buffers, so the ambiguity is
structurally small before accuracy widens it; and k = 2 is approximately a 95% confidence
radius if reported accuracy is read as a 1-sigma horizontal error, which is the usual
convention for a GPS accuracy field. That convention is an assumption about the logger
firmware, not a documented fact about these devices, and the write-up will say so.

---

## The finding that outranks the threshold choice

**Track-derived coverage is far below the reported e-tally at every tolerance.**

At the recommended setting, 1,071 settlements have track evidence against **2,023 reported
in the e-tally** - 1,069 settlements report doses administered with no supporting track.
Even at an absurd 500 m tolerance, 663 remain unexplained.

This is not a tolerance artefact. It is the reconciliation finding the question asks for,
and no defensible tolerance closes the gap.

### Testing whether our own QA rules caused it

If the duty-hours rule were cutting real work, teams would report doses on days their
loggers show nothing usable. Measured across all 155 e-tally team-days:

**Exactly one team-day has fewer than 60 usable fixes** - T14 on 12 March, with **11 usable
fixes against 16 settlements and 2,207 doses reported**. That is the day its logger died at
07:38.

So the duty window is not manufacturing the discrepancy: 154 of 155 reporting team-days
have ample usable tracking. And T14 is the clean example of the distinction the question
asks for - a settlement with no tracks may have been missed *or* the logger may have
failed, and here it is provably the logger, because the failure is visible in the fix
sequence rather than inferred from absence.

---

## What I need from you

1. **D-003 - CRS.** UTM 32N as recommended?
2. **D-005 - tolerance.** Accuracy-scaled base 50 m, k = 2? Or fixed, if you would rather
   defend a simpler rule at the walkthrough.

---

## One caveat on a diagnostic, recorded so it does not mislead later

A per-team summary I ran used `any_value(qa05_accuracy_tier)` to label each team's tier.
`any_value` picks an arbitrary row, and it mislabelled T15 as *normal* when it is
*degraded*. The underlying data is fine; the diagnostic was wrong. Tier must be derived per
team as a median or a majority, never by `any_value`. Not used in any result above.



```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```



# Two coordinate defects the QA rule set did not catch

Found at stage 03, not stage 02 - the attribution stage asked "why did 83.7% of usable
points match no settlement?" and the answer surfaced them. Recording that honestly: the
rule set as designed missed both, and a rule set that only looks at time, speed, accuracy
and sequence has no way of noticing that a coordinate is *geographically* impossible.

## What was found

Across the whole store of 929,733 points:

| Defect | Points | Signature |
|---|---|---|
| Null island | **71** | `longitude = 0, latitude = 0` exactly |
| Latitude/longitude transposed | **199** | longitude 10.3-11.6, latitude 6.9-8.5 - the state's own bounding box with the axes exchanged |

Restricted to the 150,948 points that passed QA and were used for coverage: **27** fall
outside the state polygon - 8 null island and 19 transposed. The two subsets account for
all 27 exactly.

The state bounding box is longitude 7.000-8.441, latitude 10.343-11.598. A point at
longitude 11.1003, latitude 7.0660 is not in a neighbouring state; it is the same location
with the axes swapped.

## The transposition is proven, not inferred

For each of the 199 transposed points, the swapped coordinate was compared against the same
team's other fixes within ±10 minutes:

| Measure | Result |
|---|---|
| Median distance to the team's nearest neighbouring fix, **as supplied** | **510.7 km** |
| Median distance to the same fix, **with axes swapped** | **60.4 m** |
| Points landing within 500 m of a neighbouring fix when swapped | **198 of 199** |

Sixty metres is within ordinary GPS noise for these loggers. A point that is 510 km from
where its own team was sixty seconds earlier, and 60 m from it once the axes are exchanged,
has one explanation.

## Why this matters more than 199 points

The count is trivial - 0.02% of the store. The finding is not, for three reasons.

1. **It is the clearest available example of the distinction the question asks for.** A
   settlement with no tracks may have been missed, or the logger may have failed, or the
   coordinate may be corrupt. Here the corruption is diagnosable *and* provable from the
   data, without going back to the field.
2. **It would have passed every rule in the set.** Null island has an accuracy value, a
   plausible walking speed, an in-window timestamp and a 60-second fix interval. Nothing in
   a time/speed/accuracy/sequence rule set flags a well-formed record in the Gulf of Guinea.
3. **The transposed points are recoverable, and null island is not.** They are different
   defects that a single "bad coordinate" rule would wrongly merge.

## Proposed rule QA08 - geographic validity

Two sub-rules, because the dispositions differ:

| Sub-rule | Test | Points | Disposition |
|---|---|---|---|
| QA08a null island | `longitude = 0 AND latitude = 0` | 71 | exclude - position is unrecoverable |
| QA08b transposed | outside the state polygon, but inside it when axes are swapped | 199 | **decision required** |

For QA08b the options are:

- **Exclude.** Safe, costs 199 points (0.02%), and never edits field data. But it discards
  a position we can demonstrate we know.
- **Correct, flagged and auditable.** Swap the axes, mark the row `corrected_transposed`,
  retain the original values alongside. The evidence meets any reasonable standard - 198 of
  199 land within 500 m of a contemporaneous fix. Defensible precisely because it is
  recorded rather than silent, and reversible.
- **Correct only where corroborated.** Apply the swap solely to points whose swapped
  position falls within 500 m of a fix within ±10 minutes; exclude the remaining 1. Most
  conservative of the three, and the rule states its own evidence standard.

There is a real argument against correcting anything: the pack says *"do not edit source
files by hand"*, and while a scripted, audited correction is not a hand edit, an analyst
silently repairing field data is how provenance is lost. The counter is that excluding a
point whose true position is provably known is also a distortion, just a less visible one.

## What should change in the rule set

Stage 02 should gain QA08 and run it **before** attribution, so that geographic validity is
a stated rule with a count rather than something attribution happens to notice. That the
defect was found downstream is itself worth reporting - a rule set is only as good as the
failure modes its author thought of, and this one was found by asking why a number looked
wrong.



```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```



# Reconciliation: track-derived coverage against the reported e-tally

## The discrepancy

| Measure | Settlements | % of 2,562 planned |
|---|---|---|
| Planned in the masterlist | 2,562 | 100% |
| **Confirmed visited by tracks** (dwell ≥ 5 min) | **797** | 31.1% |
| **Claimed in the e-tally** | **2,023** | 79.0% |
| Classified inaccessible before the round | 75 | 2.9% |

Doses: **170,104 reported against a planned under-5 target of 255,931 - 66.5%.** Eight
settlements carry no denominator at all and are excluded from that ratio rather than
counted as zero.

## Why each claim is or is not corroborated

Every e-tally claim (team × settlement × day) is classified by evidence already in the
store. First match wins.

| Cause class | Claims | % | Doses |
|---|---|---|---|
| `confirmed` - tracks put the claiming team there ≥ 5 min | 556 | 27.5% | 34,286 |
| **`team_elsewhere`** - team had ample tracking that day, none near this settlement | **1,336** | **66.0%** | 123,653 |
| `near_miss` - a usable fix within 250 m, just outside tolerance | 66 | 3.3% | 6,930 |
| `brief_presence` - team was there, below the dwell threshold | 37 | 1.8% | 2,955 |
| `logger_failed` - claiming team had < 60 usable fixes that day | 16 | 0.8% | 2,207 |
| `not_in_masterlist` - settlement has no coordinate; unverifiable by construction | 7 | 0.3% | 300 |
| `security_excluded` - classified inaccessible, yet doses reported | 5 | 0.2% | 73 |

## Three alternative explanations, tested and rejected

The 66% is a serious number, so the innocent explanations were tested before it was
allowed to stand.

**1. Are the team identifiers mismatched between the two sources?** If `T04` in the e-tally
were `T11` in the tracks, real work would be misfiled as absence. Rejected: of the 1,336
`team_elsewhere` claims, **exactly one** was visited by *any other* team on the same day
(0.1%), while 100% of `confirmed` claims match. A scrambled identifier would not produce
that pattern.

**2. Did somebody else cover those settlements on another day?** Rejected as a general
explanation: only **192 of 1,336** (14.4%) were visited by any team on any day of the
round. Coverage is genuinely absent, not merely misdated.

**3. Are the masterlist coordinates systematically offset?** A datum or digitisation shift
would push every track just outside tolerance. Rejected: where tracks *do* match, the
median distance to the settlement centroid is **11.3 m**. A systematic offset would show as
a distance cluster at the offset value, not at 11 m.

**How far away were they?** For the `team_elsewhere` claims, the claiming team's nearest
usable fix that day sits a median of **3.47 km** from the settlement (p25 1.44 km, p75
9.68 km, max 101.8 km). This is not a tolerance argument.

## What this does and does not license

**Supported:** two-thirds of reported claims have no supporting track evidence; the
claiming team was kilometres away; no other team covered those settlements; and the gap is
not explained by identifier error, date shift, coordinate offset, or the analyst's
thresholds - it persists at every dwell value from 1 to 15 minutes.

**Not supported:** that the doses were not administered. The analysis observes where
*loggers* were, not where *people* were. At least three benign mechanisms would produce the
same pattern and cannot be separated with the data supplied:

- the logger stayed with a vehicle or a team leader while members worked on foot;
- the logger was switched off during work and on during transit - plausible given eight
  loggers ran continuously for three weeks, showing switching discipline was not uniform;
- one logger per team was issued, but teams split to cover more ground.

**Nothing here licenses a statement about any individual team, and nothing licenses a
statement about any individual child.** A team with a low confirmation rate is a team whose
logger did not corroborate its report, which is not the same as a team that did not work.

## Which source goes to the Incident Manager

**Neither alone. The e-tally as the operational figure, with the track data as a
verification overlay - and the disagreement reported, not resolved.**

The reasoning:

- **The e-tally is the only source that measures the outcome.** Tracks record presence;
  only the e-tally records doses. An Incident Manager deciding on mop-up needs children
  vaccinated, and no GPS pipeline can supply that.
- **The tracks cannot be the headline** because they under-detect by construction. Only
  16.2% of the supplied points survived QA, and 83.7% of survivors sit more than a
  tolerance away from any planned settlement. A figure derived from them is a lower bound
  on presence, not a measure of coverage.
- **But the e-tally cannot go up unqualified.** It reports doses exceeding the target
  population in 201 records, names 7 settlements that do not exist in the masterlist, and
  reports doses against 5 settlements the programme itself had classified inaccessible.
- **The overlay is where the value is.** The 1,336 uncorroborated claims are not a coverage
  estimate; they are a **verification worklist**, ranked by doses at stake. That is
  actionable in a way neither source is alone.

**What I would put in front of the Incident Manager:** reported coverage of 66.5% of the
under-5 target, flagged as unverified; 797 settlements with independent presence evidence;
and 1,336 claims requiring supervisory confirmation before the round is signed off - with
the honest statement that the tracking data can neither confirm nor refute them, and that
the fastest route to an answer is a supervisor spot-check of a sample, not more analysis.



```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```



# Spatial clustering of missed settlements

## Definition of "missed"

A settlement is counted missed when **no doses were reported against it in the e-tally and
no track confirms a visit**. It requires both sources to agree on absence, which is the
least contestable definition available given that the two disagree about a thousand
settlements.

The 75 settlements classified inaccessible on security grounds before the round are
**excluded from the analysis**, not counted as missed. They were never expected to be
reached, and including them would manufacture hot spots in exactly the wards the programme
had already written off.

**2,487 settlements analysed. 444 missed - 17.9%.**

## Method, stated once in full

| | |
|---|---|
| **Statistic** | **Getis-Ord Gi\*** (Ord & Getis 1995), the local form, computed with `esda.getisord.G_Local(star=True)` |
| **Why this statistic** | The operational question is one-directional - *where do missed settlements concentrate* - and Gi\* answers exactly that, separating hot spots from cold. Local Moran's I detects spatial association of any kind, including outliers, which is a different question |
| **Weights** | **Queen contiguity**, row-standardised, zero islands (final analysis). Row standardisation matters: it makes the local weighted *sum* a local weighted *mean*, so Gi\* compares a neighbourhood's missed **rate** against the study-area rate rather than rewarding neighbourhoods that simply contain more settlements |
| **Significance** | **Conditional permutation, 9,999 draws.** No normality assumption is made - the analytical p-value assumes a distribution this data does not satisfy |
| **Multiple-testing correction** | **Benjamini-Hochberg false discovery rate**, α = 0.05, implemented directly rather than imported. Testing 40 wards at 5% yields two false positives by construction; testing 2,487 settlements yields ~124 |
| **Global check** | **Global Moran's I**, same permutation scheme, run first - to confirm spatial structure exists at all before mapping local clusters |

Abbreviations used below: **Gi\*** for Getis-Ord Gi\*, **BH FDR** for the
Benjamini-Hochberg false discovery rate correction.

## The analysis was run twice, because the first version was not trustworthy

### Attempt 1 - Gi\* on the binary indicator at settlement level. Rejected.

| | |
|---|---|
| Weights | k-nearest neighbours, k = 8, row-standardised |
| Inference | conditional permutation, 9,999 draws |
| Global Moran's I | **0.0032, p = 0.34 - not significant** |
| Hot spots, raw p ≤ 0.05 | 77 |
| Hot spots after BH FDR | 8 |
| "Cold spots" after BH FDR | 516 |

The 516 cold spots are an **artefact and are not reported as a finding.** The diagnostic:

- Every one has a pseudo p of exactly **0.00010**, the floor of 9,999 permutations.
- Their z-scores span only **−0.47 to −0.18** - nowhere near unusual.
- The binary indicator over 8 neighbours produces just **20 distinct local values** across
  2,487 locations.

For a settlement whose neighbourhood contains no missed settlement, the observed statistic
is already the minimum attainable, so *no* permutation can return a smaller one and the
pseudo p pins to the floor regardless of how ordinary the location is. That is a degenerate
permutation distribution, not a cluster. The surviving 8 hot spots carry a maximum z of
1.28, which is not strong evidence either.

**Reporting the 516 as cold spots would have been the single biggest error available in
this question.** They are a property of the arithmetic, not of the campaign.

### Attempt 2 - Gi\* on the ward-level missed *rate*. Reported.

| | |
|---|---|
| Unit | 40 wards |
| Variable | proportion of settlements missed (min 0.039, median 0.174, max 0.340) |
| Weights | **Queen contiguity**, row-standardised, 0 islands |
| Inference | conditional permutation, 9,999 draws |
| Distinct pseudo p-values | **40** - continuous variable, no degeneracy |
| Global Moran's I | **0.3560, p = 0.0004 - significant** |
| Hot spots, raw p ≤ 0.05 | 15 |
| **Hot spots after BH FDR** | **3** |
| Cold spots after BH FDR | 0 |

Three reasons this is the right unit: the variable is continuous, so the inference means
what it claims; the ward is the unit mop-up is actually deployed by; and 40 tests are
tractable where 2,487 are not. Queen contiguity replaces KNN because wards are polygons
that tile the study area - shared boundaries are the natural neighbour definition and no
distance threshold has to be invented.

## Result

**Three wards form a statistically significant cluster of high missed rates.**

| Ward | LGA | Settlements | Missed | Rate | Under-5 | Gi\* z | p |
|---|---|---|---|---|---|---|---|
| W027 Daberi | Katsuma | 40 | 10 | 0.250 | 2,215 | 1.27 | 0.0023 |
| W026 Kungomi | Katsuma | 48 | 10 | 0.208 | 2,598 | 1.23 | 0.0018 |
| W015 Baluru | Idi-Oro | 139 | 31 | 0.223 | 27,137 | 0.92 | 0.0037 |

**227 settlements, 51 of them missed, 31,950 under-5 children in the cluster.**

Baluru dominates the population at stake - 27,137 of the 31,950 - because it is a large
urban ward. Rate and burden are different quantities and the brief must not conflate them.

### Highest rate is not the same as hot spot

| Ward | Missed rate | Gi\* z | p | Hot spot? |
|---|---|---|---|---|
| W023 Suwade | **0.340** - the highest in the study area | 0.82 | 0.0103 | **No** |
| W025 Okriba | 0.324 | 0.04 | 0.2322 | No |
| W031 Satide | 0.308 | 0.99 | 0.0190 | No |

Suwade has the worst missed rate of any ward and is **not** a hot spot, because its
neighbours do not share the pattern - it is an isolated poor performer, not a cluster. That
distinction is the entire point of using a local spatial statistic rather than a ranking,
and it changes the response: Suwade needs a ward-level intervention, the Katsuma cluster
needs an area-level one.

## What the result does not license

**It does not license any statement about an individual settlement.** Gi\* is a statement
about a *neighbourhood*. A settlement inside a hot-spot ward may have been perfectly
covered; a settlement outside every hot spot may have been missed entirely. The unit of
inference is the ward, and the map must be read at that unit.

**It does not license any statement about an individual child.** Nothing here measures
vaccination status. "Missed" means no dose was reported and no track confirms a visit - an
absence of *evidence about a settlement*, not an observation of any child's status.

**It does not license a causal claim.** The analysis says where missed settlements
concentrate, not why. Terrain, distance, team assignment, insecurity spillover and logger
discipline are all untested candidates.

**It does not license treating the point-level result as corroboration.** The two levels
disagree - settlement-level Moran's I is not significant, ward-level is strongly so - and
that is not a contradiction to be smoothed over. Individual missed settlements are
interspersed with covered ones, so there is no clustering *among settlements*; but wards
differ systematically in their missed rate, and the high-rate wards adjoin one another.
This is a modifiable areal unit effect, and it means **the finding is genuinely a ward-level
finding** and would not survive being restated at settlement level.

**Sensitivity.** The hot-spot set was computed on the both-sources definition of missed. A
track-only definition would classify far more settlements as missed (1,765 rather than 444)
and is not used, because 83.7% of usable fixes fall more than a tolerance from any planned
settlement - a track-only definition measures logger discipline as much as coverage.



```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```



# Telling a data artefact from a programmatic failure

The question asks how a settlement with no tracks is distinguished from a settlement that
was genuinely missed - and what is done when the two cannot be separated. This is the
consolidated answer. Every row is measured; the underlying working is in the linked
documents.

## The test applied throughout

For every anomaly, three questions in order:

1. **Does the pattern follow the equipment or the ground?** If a defect travels with a
   logger or a team across different places, it is the equipment. If it appears in one
   place regardless of who is there, it is the ground.
2. **Is the true value recoverable from the data itself?** If the correct answer can be
   demonstrated without going back to the field, the record is repairable. If not, it is
   only excludable.
3. **If neither question resolves it, what would?** An undecidable case is escalated to the
   method that *can* decide it - usually a field check - rather than assigned to whichever
   class looks more likely.

## What was found, and how it was classified

| # | Observation | Verdict | Evidence that decided it | Disposition |
|---|---|---|---|---|
| 1 | Eight loggers report ~36 m accuracy, twenty-four report ~8 m | **Artefact** - equipment tier, **not** urban multipath | The eight report ~36 m in rural Gwarin as well as urban Idi-Oro; the clean twenty-four report ~8 m *inside* Idi-Oro. Stationary scatter confirms the field is honest: 30.7 m actual against 39.2 m reported, versus 7.2 m against 8.0 m | **Not excluded.** Accuracy scales the attribution tolerance instead. A 30 m cut would have removed 62% of those eight teams' tracks and made them appear to have visited nothing |
| 2 | T14 has 210 distinct minutes on 12 March, ending 07:38 | **Artefact** - logger failure, not absence of work | The failure is *visible in the fix sequence*, not inferred from missing data. The team reported 2,207 doses across 16 settlements that day | Claims from that team-day classed `logger_failed`. The e-tally is the better source for them |
| 3 | 199 points outside the state | **Artefact - recoverable** | Median 510.7 km from the same team's fixes within ±10 min as supplied; **60.4 m** once the axes are swapped; 198 of 199 within 500 m | **Corrected**, flagged, originals retained. The 1 that failed corroboration was **excluded, not corrected** |
| 4 | 71 points at exactly (0, 0) | **Artefact - unrecoverable** | Null island. No information survives to reconstruct the true position | **Excluded.** Deliberately *not* merged with row 3 - same symptom, opposite disposition |
| 5 | 501 further points outside the state | **Neither** - real movement | Median 10.7 km outside the boundary, max 70 km, overwhelmingly post-campaign dates, 428 of 501 from the eight never-switched-off loggers | Excluded from coverage as outside the operational area. Relabelled from "unexplained" once measured |
| 6 | 516 Gi\* "cold spots" at settlement level | **Statistical artefact** | All at pseudo p = 0.00010, the permutation floor, with z of only −0.47 to −0.18. The binary indicator over 8 neighbours yields 20 distinct values across 2,487 sites, so no permutation can beat the minimum | **Not reported as a finding.** Analysis moved to ward level, where the variable is continuous and the inference means what it claims |
| 7 | 633,207 points outside the campaign window; 585,951 minutes in dispute | **Artefact** - procedural, loggers never switched off | T01 records continuously to 29 March, around the clock at 60-second intervals | Excluded as a *counted* QA rule, never silently at ingest - a two-thirds cut must be visible |
| 8 | 201 e-tally records with doses exceeding target population | **Programmatic** - reporting or denominator error | Arithmetic, internal to the e-tally | Reported. Not corrected - the denominator may be wrong rather than the numerator, and we cannot tell which |
| 9 | 5 security-classified settlements reporting doses | **Undecided - programmatic either way** | Could be an out-of-date classification, a keying error, or a team working where it was told not to | **Escalated.** Named in the decision brief as a same-day phone call, not resolved analytically |
| 10 | 1,336 claims with no corroborating track | **Undecidable from this data** | See below | **Escalated** to a supervisor spot-check |

## Row 10 - the case that cannot be decided, and what was done about it

Two thirds of reported claims have no supporting track, with the claiming team a median
**3.47 km** away. Three artefact explanations were tested and **rejected**:

| Hypothesis | Test | Result |
|---|---|---|
| Team identifiers differ between the two sources | Were those settlements visited by *another* team the same day? | **1 of 1,336.** Rejected - 100% of confirmed claims match |
| Work happened on a different day | Visited by any team on any day? | **192 of 1,336 (14.4%).** Rejected as a general explanation |
| Masterlist coordinates are systematically offset | Distance where tracks *do* match | **11.3 m median.** An offset would cluster distances at the offset value |

**What remains cannot be separated with the data supplied.** At least three operational
mechanisms produce an identical signature:

- the logger travelled with a vehicle or team leader while members worked on foot;
- the logger was switched off during work and on during transit - plausible, since eight
  loggers ran for three weeks straight, so switching discipline was demonstrably uneven;
- one device per team, but the team split to cover more ground.

None is distinguishable from over-reporting using GPS alone.

**So the analysis stops there and says so.** The 1,336 are not presented as a coverage
estimate, nor as an allegation. They are presented as a **verification worklist ranked by
doses at stake**, with the recommendation that a supervisor spot-check 30 of them at random
during mop-up. That single field action resolves what no further analysis can, and it is
cheaper than the analysis already done.

## The principle, stated once

**Where the data can decide, it decides and the reasoning is recorded. Where it cannot, the
uncertainty is named and routed to something that can - never resolved by assumption.**

Concretely, this is why:

- a positional-accuracy cut was **refused** (it would have manufactured a coverage finding
  from an equipment property);
- transposed coordinates were **corrected but only where corroborated**, with the single
  uncorroborated point excluded rather than carried on the strength of the pattern;
- unevaluable implied speed is stored **NULL** - unknown, not passing;
- the settlement-level cluster result was **discarded rather than reported**, despite being
  the more eye-catching output;
- and `team_elsewhere` is described as *uncorroborated*, never as *false*.

## Where this is worked through in detail

| Topic | Document |
|---|---|
| QA thresholds, options and rejected alternatives | `qa_rule_options.md` |
| Coordinate defects and the corroboration standard | `coordinate_defects.md` |
| Projection and tolerance, measured | `crs_and_tolerance_options.md` |
| Reconciliation and cause classification | `reconciliation.md` |
| Cluster statistics and the rejected point-level run | `cluster_analysis.md` |
| Every judgement call with its rejected alternative | `../../DECISIONS.md` |



```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```



# DECISION BRIEF - where to send 24 hours of mop-up

**To:** Incident Manager, Bansara State SIA · **From:** Data and GIS Analytics · **14 March 2026**
**Round:** 9-13 March 2026 · **Decision needed:** where to deploy, today.

---

## Recommendation

**Daberi and Kungomi first as a single deployment - they share a boundary. Then Baluru.**

| | Ward | LGA | Settlements missed | Under-5 in ward | Why |
|---|---|---|---|---|---|
| **1** | Daberi + Kungomi | Katsuma | 20 | 4,813 | Adjacent, confirmed cluster - one team covers both in a day |
| **2** | Baluru | Idi-Oro | 31 | 27,137 | Largest child population of any hot spot; urban, so travel is quick |
| **3** | Suwade | Katsuma | 16 | 2,593 | Worst rate in the state (34%) but **isolated** - a ward problem, not an area problem |

Suwade is the trap in this data. Its neighbours performed normally, so an area-level
response there wastes capacity. Fix it as a single ward.

## What we found

Of **2,487 planned settlements** (excluding 75 classified inaccessible), **444 - 17.9% -
have no evidence of being reached**: no doses reported and no GPS track placing a team
there. Those gaps are not evenly spread. Three wards form a genuine cluster, and that
holds after allowing for the fact that testing 40 wards throws up false alarms by chance.

## Before you trust this

**Only 27.5% of reported activity can be corroborated.** Loggers confirm 556 of 2,023
reported visits. For **1,336**, the team's own logger places it a median of **3.5 km away**
at the time, and no other team went there either.

**This does not mean the vaccinations did not happen.** We measured where *loggers* were,
not where *people* were. A logger left in a vehicle, switched off during work, or carried
by one half of a team that split would each produce this exact pattern. We tested and ruled
out the data explanations - mismatched team numbers, wrong dates, faulty settlement
coordinates - but cannot rule out those operational ones from GPS alone.

**What it means for you: 444 is a floor, not a ceiling.** If a meaningful share of those
1,336 visits did not happen, the real gap is larger and may sit in different wards than
this map shows.

## Three things to do today

1. **Spot-check 30 of the 1,336 unverified claims at random** while mop-up runs. That
   settles more than any further analysis. If they check out, this map is your targeting
   tool; if not, the round needs a different conversation.
2. **Treat reported coverage - 170,104 doses against a 255,931 target, 66.5% - as
   unverified** until those checks return.
3. **Call about the five inaccessible settlements that reported doses.** Either the
   security classification is stale or the reporting is wrong.

## Confidence, and limits

| Finding | Confidence |
|---|---|
| 444 settlements show no coverage in **either** source | **High** - both sources agree |
| They cluster in Daberi, Kungomi and Baluru | **High** - survives correction for multiple testing |
| Reported coverage of 66.5% | **Low** - two-thirds uncorroborated |
| The true missed total is 444 | **Low** - a floor; the ceiling is unknown |

This brief says **nothing about any individual child** (no vaccination status was
measured), **nothing reliable about any individual settlement** (the finding holds at ward
level - a settlement inside a hot-spot ward may have been covered perfectly), **nothing
about why** the gaps concentrate, and **nothing about any team's honesty** - poor
corroboration describes a logger, not the people carrying it.

*From 956,702 GPS fixes across 160 logger files, of which 150,940 (16.2%) were usable after
quality control. Method and limitations in the accompanying technical note.*



```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# PART 2 - Question 3

## Converting a paper questionnaire into a digital form


# Defects in Form HH/2026/v1, and what was done about each

The questionnaire is ethics-approved (BSHREC/2026/041) and will not be redesigned. That
constrains the response: **a defect that changes what is asked, or what a response means,
is escalated, not silently repaired.** A defect that only concerns how an answer is
captured is fixed in the digital form, because that is what the digital form is for.

Each entry states the disposition and why. Numbering follows the paper form.

---

## A. Internal contradictions

### A1 - Column (7) is "office use, leave blank", yet 3.02 asks the enumerator to read it
**Severity: high. This one stops the form working.**

The roster instruction says *"Column (7) is completed by the office and must be left blank
in the field."* Then 3.02 asks: *"**From column (7)**, how many children in this household
are aged 9 to 59 completed months?"*

The enumerator is instructed to read a total from a column they were forbidden to fill.
On paper a clerk resolves this silently. A digital form cannot.

**Disposition: resolved in the form, and it resolves itself.** Eligibility is derived from
the roster ages rather than transcribed - the count of residents with age 9-59 completed
months is calculated. 3.02 becomes a read-only calculated field, and column (7) disappears
as a field-entered concept. **Escalated as a note** because the paper instrument's
intent is ambiguous: it is not certain whether the office was meant to determine
eligibility on a different rule.

### A2 - 4.08 asks for a three-way distinction and offers a two-way code
**Severity: medium.**

*"Record whether a card, a card copy, or an electronic record was seen by you."* Coding
categories: `Card seen 1 / No card seen 2`.

The question asks the enumerator to distinguish three document types; the coding cannot
record which. Any analysis of documentation quality is impossible, and the enumerator is
left guessing whether a photographed card counts.

**Disposition: escalated, with a minimal in-form mitigation.** Changing the response
options changes what is asked, which requires ethics re-approval. The form keeps the
two-way code and adds an optional follow-up capturing document type **only when
`card_seen = 1`**, flagged in the codebook as an addition not present on paper. Recommend
the paper form be corrected at the next revision.

### A3 - Section 5 says "every eligible child", 5.01 restricts to 12 months and over
**Severity: medium.**

Section 5's instruction reads *"A stool specimen is sought from every eligible child."*
Eligible children are 9-59 months (per Section 4). But 5.01 asks *"Is the child aged 12
completed months or older?"* with `No → Section 6`.

Children aged 9-11 months are eligible for Section 4 and ineligible for a specimen. The
instruction and the filter contradict each other.

**Disposition: resolved in the form.** 5.01 is calculated from `age_months`, not asked, so
the filter governs and the contradiction cannot produce inconsistent data. The instruction
text is corrected to "every eligible child aged 12 months or older". **Escalated** so the
paper wording is fixed.

### A4 - Roster holds 12 lines; household size accepts two digits
**Severity: medium.**

3.01 records household size in a two-digit field (up to 99). The roster table has **12
rows**. A household of 15 cannot be listed, so the roster and the stated size will
disagree by construction, and the paper form gives the enumerator nowhere to put residents
13 onward.

**Disposition: resolved in the form.** The digital roster is an unbounded repeat, so the
constraint vanishes. The consistency check between 3.01 and the roster count (see F4) then
becomes meaningful rather than an artefact of table height.

### A5 - Section 4 page number is one digit; eligible-children count is two
**Severity: low.**

*"Section 4 page number ⌷ of ⌷"* allows 9 children; 3.02 accepts up to 99. Same class of
error as A4, and it disappears with a repeat group.

**Disposition: resolved in the form.** Page numbering is replaced by the repeat index.

---

## B. Missing or ambiguous skip instructions

### B1 - 5.02 has no skip instruction at all
**Severity: high. This is the missing skip the assessment refers to.**

5.02 asks *"Was a stool specimen obtained from this child?"* `Yes 1 / No 2` - and the SKIP
column is **empty**.

The following questions are 5.03 label, 5.04 time into cold box, 5.05 cold-box
temperature, then 5.06 *reason no specimen was obtained*. So:

- if a specimen **was** obtained, 5.06 should not be asked, and it has no filter;
- if a specimen was **not** obtained, 5.03-5.05 are unanswerable, and there is no skip.

On paper, a clerk diagonal-lines the inapplicable boxes. In a digital form this must be
explicit or the data is uninterpretable.

**Disposition: resolved in the form.** `5.02 = 1` → 5.03-5.05 required, 5.06-5.07 hidden.
`5.02 = 2` → 5.03-5.05 hidden, 5.06 required. This does not change what is asked of any
respondent; it enforces the logic the paper form leaves to a clerk.

### B2 - 5.01 skips to Section 6, abandoning the remaining children
**Severity: high.**

5.01 `No → Section 6`. Section 5 is completed **per child**; Section 6 is household-level
and terminal. So a household whose first eligible child is under 12 months sends the
enumerator to the household section, and every remaining child's module is never reached.

The skip target is wrong: it should be *next child*, not *Section 6*.

**Disposition: resolved in the form.** Sections 4 and 5 sit inside one per-child repeat, so
"skip" means "end this child's iteration". The paper defect cannot occur. **Escalated**,
because on paper this will already have cost data in previous rounds.

### B3 - 2.01 records that consent was not read, and proceeds anyway
**Severity: high - ethical, not just structural.**

2.01 *"Consent statement read aloud to the respondent in full?"* `Yes 1 / No 2`, no skip.
A `No` is recorded and the interview continues to 2.02, where consent may then be "given".

Consent recorded after an unread consent statement is not informed consent.

**Disposition: escalated, and blocked in the form.** The form prevents progression while
`2.01 = 2`, with a message instructing the enumerator to read the statement and then
record `Yes`. This is the one place a hard block is used rather than a warning, because
the alternative is collecting biological specimens from children under defective consent.
Flagged to the ethics committee as a paper-form correction.

---

## C. Data the paper design permits that cannot be analysed

### C1 - 4.13 discards multiple antibiotics in an antimicrobial resistance survey
**Severity: high, analytically.**

*"Which antibiotic was taken? ... Where more than one was taken, record the most recent."*

This is an AMR survey. Concurrent or sequential multiple-antibiotic exposure is among the
most important things such a survey could measure, and the instrument deliberately
discards it, keeping one drug with no record that others existed.

**Disposition: escalated, not changed.** Converting to select-multiple changes what is
asked and what the variable means, so it cannot be done unilaterally on an approved
instrument. The form adds **one** yes/no - *was more than one antibiotic taken?* - which
does not alter 4.13 but lets the analysis know when the single code is incomplete.
Recommended as a priority correction before the next round.

### C2 - 6.07 allows "None of these" together with owned assets
**Severity: medium.**

*"Which of the following does this household own? Record all that apply."* Options A-G are
assets; **H is "None of these"**. Nothing prevents H being marked alongside D.

**Disposition: resolved in the form.** H is made exclusive by constraint. This corrects a
logical impossibility rather than changing the question.

### C3 - 5.05 cannot record a cold-chain failure
**Severity: medium, and easy to miss.**

Cold-box temperature is captured as `⌷ . ⌷ °C` - one digit and one decimal, so 0.0 to 9.9.

The acceptable range is roughly 2-8 °C, so the field holds valid readings comfortably. It
**cannot record a failure**: a box at 15.0 °C, or one that has frozen below zero, has no
representable value. The field can only record success, which makes it useless as a
quality control.

**Disposition: escalated, and widened in the form** to accept −20.0 to 40.0 with a warning
outside 2-8. Widening a measurement range does not change what is asked.

### C4 - 1.05 collects an alternative settlement name as free text
**Severity: low.**

Useful operationally, unanalysable as supplied, and it will produce spelling variants.
**Disposition: kept as free text, flagged in the codebook** as an operational field not
intended for analysis.

---

## D. Sentinel codes colliding with real values

The completion notes define: **8 / 98** = does not know; **9 / 99** = asked, no answer
obtained; **96** = Other. Three collisions follow from that rule.

### D1 - 6.02 codes 8 AND 9 both collide
**Severity: high.**

**Corrected after a systematic scan.** This entry originally named code 9 only.
`scan_sentinels.py` checks every coding category against the declared sentinels
and found **six collisions across four questions**, not three - code `8` also
collides in both 6.01 and 6.02 (`Bucket` and `Unprotected spring` respectively).
Written from reading, the first pass missed them. See `docs/coding_scheme.md`
for the full table; the scan is now the authority.

6.02 has nine categories and its ninth is `No facility or bush . . . 9`. In a single-digit
field, 9 is the standard no-answer sentinel. **Open defecation - the single most important
category in a sanitation question - is indistinguishable from a missing answer.**

**Disposition: resolved in storage, not in the question.** The category set and the numbers
read to the respondent are unchanged. The digital form stores the response and the
non-response reason in **separate fields**, so `9` always means "no facility or bush" and
missingness is carried elsewhere. Escalated for paper renumbering.

### D2 - 6.01 code 9 is "Rainwater", with an 11-category list
**Severity: medium.**

Same mechanism. The list runs to 11, so the field is arguably two-digit and the sentinel
would be 99 - but the form does not say so, and `9` is genuinely ambiguous between
"rainwater" and "no answer" for anyone applying the completion note literally.

**Disposition: as D1.** Sentinels never share a field with substantive values.

### D3 - 99 is both "Not measured" and a plausible child height
**Severity: high. This is the sentinel-inside-a-measurement case the brief warns about.**

4.06 records length or height as `⌷⌷⌷ . ⌷ cm` with `Not measured . . . 99`.

**99 cm is an entirely ordinary height for a three-year-old.** A child measured at 99.0 cm
and a child not measured at all are recorded identically. 4.05 weight carries the same
`99` convention; 99 kg is implausible for a child so the collision is latent there, but
present.

**Disposition: resolved in storage.** Measurement and measurement-status are separate
fields: `not measured` is a boolean, and the measurement is null when it is true. No
sentinel is ever stored inside a numeric measurement. This is the single most important
storage decision in the form.

---

## E. Problems with the external files, not the questionnaire

### E1 - The medicine list does not exist
**Severity: high. Blocking.**

4.13 says *"Record from the medicine list."* The data pack README states the reference
files support *"a settlement list, **a medicine list**, a staff roster and pre-printed
specimen labels."*

`reference_media/` contains seven files: `lgas.csv`, `wards.csv`, `settlements.csv`,
`settlements.geojson`, `previous_round_households.csv`, `staff_roster.csv`,
`specimen_label_allocation.csv`. **There is no medicine list.**

**Disposition: escalated, with a documented stand-in.** 4.13 cannot be implemented as a
coded lookup without the codelist. The form implements it as a coded select against a
**placeholder list built from the WHO AWaRe classification**, clearly marked as a
substitute, so the mechanism is demonstrable and the real list can be dropped in by
replacing one CSV. Every occurrence is flagged in the codebook. **The real list must be
obtained before deployment** - a substituted codelist would silently recode the AMR
variable.

### E2 - Code-box widths do not match the identifiers they hold
**Severity: low, but it affects validation.**

1.02 LGA `Code ⌷⌷⌷` against actual `LGA02` (five characters); 1.03 Ward `⌷⌷⌷` against
`W018` (four); 1.04 Settlement `⌷⌷⌷⌷⌷⌷` against `S01324` (six, fits).

The boxes plausibly hold the numeric part with the prefix implied, but the form does not
say so. **Disposition: resolved.** All three become cascading selects from the reference
files, so codes are chosen rather than typed and the width question disappears.

### E3 - The check digit can be `X`, and the paper form provides a digit box
**Severity: medium.**

`specimen_label_allocation.csv` gives the scheme as *"Modulus 11, weights 2 to 7 applied
right to left, remainder 10 recorded as X"*. Label format at 5.03 is `BSN ⌷⌷⌷⌷⌷⌷ - ⌷`.

Roughly one label in eleven carries a check character of `X`, which a digit box cannot
hold. **Disposition: resolved in the form** - the check character field accepts `0-9` and
`X`. Escalated for the paper form.

### E4 - Supervisor codes legitimately use the `ENU` prefix
**Not a defect. Recorded so it is not "fixed".**

7.04 labels the supervisor field `ENU ⌷⌷⌷`, which looks like a copy-paste error from 1.08.
It is not: `staff_roster.csv` shows team supervisors carry `ENU###` identifiers
(e.g. `ENU005`, role *Team supervisor*). The form validates 7.04 against roster members
whose role is supervisor, and leaves the prefix alone.

---

## F. Tension between the questionnaire and the stated operating conditions

### F1 - The form says fieldwork runs 1-30 June; the operating conditions say 14 days
The header reads *"Fieldwork period 1 to 30 June 2026."* The brief states fieldwork runs
14 days.

**Disposition:** the date constraint uses **1-30 June**, the ethics-approved window, since
narrowing it could reject a legitimate submission if the 14 days shift. The 14-day
expectation is enforced as a **soft warning**, not a block. Recorded in the constraint
register as a deliberate choice with the reasoning.

### F2 - Names are collected where line numbers would serve
Roster column (2) and 4.02 both collect *"name or initials"*, alongside GPS to six decimal
places at the dwelling entrance, structure number, and the previous round's household
identifier.

Together these identify a specific dwelling and the children in it. **Disposition: raised
under data protection** (see the data protection note) rather than as a form defect. The
recommendation is that 4.02 be dropped entirely - it duplicates the roster line reference
at 4.01, which is sufficient to link child to roster.

---

## Summary of dispositions

| Resolved in the form | Escalated | Both |
|---|---|---|
| A1, A4, A5, B1, B2, C2, D1, D2, D3, E2, E3 | C1, F2 | A2, A3, B3, C3, E1 |

**Escalated items are listed for the survey manager and the ethics committee in a single
memo** rather than left inside a technical document, because escalation that nobody reads
is the same as a silent fix.



```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```



# Sentinel codes and how they are stored (F3)

## The scheme the paper form declares

From the notes on completion:

> Where a respondent does not know the answer, code **8** in a single-digit field
> or **98** in a two-digit field. Where the question was asked but no answer was
> obtained, code **9** or **99**. Where a coding category list ends in **96**,
> that category is "Other".

The scheme is coherent. The problem is that it is declared globally and then
contradicted locally.

## Every collision in the questionnaire

Found by systematic scan of all coding categories against the declared sentinels
(`scan_sentinels.py`), not by reading. The scan returned 13 hits; 7 are the
sentinel used **correctly** as its own category (`8 = Do not know` at 1.12, 4.10,
4.11, 4.12, 4.15, 6.04, 6.06) and are not defects.

**Six are genuine collisions, across four questions.**

| Question | Code | Substantive meaning | Also means | Severity |
|---|---|---|---|---|
| **6.01** Drinking water | `8` | Unprotected spring | Do not know | High |
| **6.01** Drinking water | `9` | Rainwater | No answer obtained | High |
| **6.02** Toilet facility | `8` | Bucket | Do not know | High |
| **6.02** Toilet facility | `9` | **No facility or bush** | No answer obtained | **Highest** |
| **4.05** Weight | `99` | - (sentinel inside a measurement) | Not measured | High |
| **4.06** Height | `99` | **99.0 cm is an ordinary height** | Not measured | **Highest** |

Two of these are worse than the rest:

**6.02 code 9 is open defecation.** It is the single most policy-relevant
category in a sanitation question, and under the declared scheme it is
indistinguishable from a question nobody answered. Any analysis that treats 9 as
missing silently deletes exactly the households that matter most; any analysis
that treats it as substantive silently invents open defecation for every
non-response.

**4.06 code 99 is a real child's height.** A three-year-old at 99.0 cm is
entirely typical. A measured child and an unmeasured child are recorded
identically, and no amount of downstream cleaning can separate them.

**My earlier defect report understated this.** It named 6.01 code 9, 6.02 code 9
and the 99 measurements, and missed code `8` in both 6.01 and 6.02 - because it
was written from reading rather than scanning. The scan is now in the repository
and is the authority.

## Three further collisions the scan cannot see

These are not category lists, so a category scan misses them. They come from
field width alone.

| Field | Collision | Notes |
|---|---|---|
| Roster age in years | `98`, `99` are plausible ages **and** the two-digit sentinels | A 98-year-old resident is unusual, not impossible. The paper form cannot record one |
| 3.01 household size | `98`, `99` likewise | Implausible in practice; the ambiguity is still formally present |
| 1.06 structure, 1.07 serial | **Three-digit fields, and the scheme defines no three-digit sentinel** | 8/98 and 9/99 are defined; nothing says what a three-digit non-response looks like. A clerk must improvise, and different clerks will improvise differently |

The last one is the most interesting: it is not a collision but a **gap**. The
declared scheme simply does not cover the field widths the form actually uses.

## How the digital form stores these

One principle, applied without exception:

> **A field carries a value or it carries a status. Never both.**

### 1. Measurements: value and status are separate fields

```
q4_05_weight_status   select_one measured | not_measured
q4_05_weight_kg       decimal, relevant only when status = 'measured'
```

`q4_05_weight_kg` is **null** when the child was not weighed. Not 99, not −1, not
a blank string that a CSV reader might coerce. The reason the child was not
measured lives in `q4_05_weight_status`, where it cannot be arithmetic.

The analysis team cannot mistake a sentinel for a value here, because no sentinel
is ever stored in a numeric field. `mean(q4_06_height_cm)` is correct by
construction rather than by remembering to filter.

### 2. Categorical answers: values re-based off the sentinel range

The choice lists for 6.01 and 6.02 are stored with prefixed values -
`w01`-`w11`, `t01`-`t09` - rather than `1`-`11` and `1`-`9`.

The categories, their order, and the numbers **read aloud to the respondent** are
unchanged, so paper and digital rounds remain comparable. What changes is the
stored value: `t09` cannot collide with any sentinel because it is not a number.

Rejected alternative: renumbering categories to avoid 8 and 9. That would have
broken comparability with every previous paper round, for no gain over
prefixing.

### 3. "Do not know" stays a first-class answer

Where the paper form offers `8 = Do not know`, the digital form keeps it as an
explicit choice - because *the respondent not knowing* is a substantive finding,
particularly for 4.15 (was the antibiotic obtained without prescription) and
6.04 (were antibiotics given to livestock). It is stored as `8`, matching paper.

The distinction the form maintains is between **"the respondent said they do not
know"** (recorded, code 8) and **"this question was never reached"** (null,
because the relevance condition was false). The paper form conflates these
routinely; a clerk draws a diagonal line through the boxes and the two become
identical at data entry.

### 4. Non-response is structural, not coded

A question that was skipped is **absent from the submission**, not filled with 9.
Relevance conditions are recorded in the XForm, so the analysis team can
reconstruct exactly why any field is empty: it was not asked, and the form states
the condition under which it would have been.

That is the deepest change from paper. On paper, "empty" is ambiguous between
skipped, refused, overlooked and lost. In the submission, skipped fields are
absent and their absence is explained by a rule the codebook publishes.

## What this costs

Paper rounds and digital rounds will not concatenate without a mapping. A round
where open defecation is `9` and a round where it is `t09` need a crosswalk, and
if nobody writes one, someone will union the two files and produce nonsense.

**The crosswalk is in the codebook**, and it is the reason the codebook exists as
a deliverable rather than as documentation.



```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```



# Cross-question consistency (F4)

The paper form relies on a clerk to notice contradictions, weeks after the
household could be revisited. These are the checks the digital form makes at the
doorstep instead.

## The two the question requires

### 1. Stated household size against the roster - **warns**

```
3.01 = "How many people usually live in this household?"
roster_count = count(${roster})
```

When they disagree, a warning names both numbers:

> ⚠ You recorded 6 usual residents but listed 4. Check the roster before
> continuing.

**Why it warns rather than blocks.** The two legitimately differ. A usual
resident may be absent and the respondent unable to give their age or
relationship; a household may include someone the respondent counts and the
enumerator cannot describe. Blocking would leave the enumerator with one way
out - **invent a line to clear the error** - and a fabricated roster row is
worse than a recorded discrepancy.

So the discrepancy is surfaced, recorded, and left in the data where the
analysis team can see it. `roster_count` and `q3_01_hh_size` are both stored.

**What paper does instead:** the roster table has twelve rows and 3.01 accepts
two digits, so a household of fifteen produces a discrepancy the paper form
cannot even represent (defect A4). Here the repeat is unbounded, so the check
measures a real disagreement rather than an artefact of table height.

### 2. Stated eligible children against child modules completed - **cannot disagree**

The paper form asks the enumerator to read a count from an office-use column
(3.02, defect A1), then to complete that many Section 4 pages, and relies on the
clerk to check the two match.

The digital form removes the possibility rather than checking for it:

```
r_eligible       = 1 when age is 9-59 completed months, per roster member
q3_02_eligible   = sum(${r_eligible})
child repeat     repeat_count = ${q3_02_eligible}
```

The number of child modules **is** the derived eligible count. They are the same
quantity, so a check would compare a number to itself.

**This is the stronger form of the requirement.** A consistency check that can
fail is a check someone must monitor; a design where the inconsistency is
unrepresentable needs no monitoring. Where that was achievable it was preferred,
and where it was not - as in check 1 - the check warns and records.

## Further checks, not required but cheap once the structure exists

| Check | Rule | Action | Why |
|---|---|---|---|
| Child module points at an eligible child | `indexed-repeat(${r_eligible}, ${roster}, ${q4_01_line}) = 1` | **blocks** | The paper form cannot verify 4.01 at all - a module can point at an adult |
| Specimen eligibility follows recorded age | `q5_01` calculated from `q4_03_age_months` | derived | Removes the 5.01 contradiction (defect A3) |
| Measurement position against age | recumbent < 24 months | **warns** | WHO convention; warns because a child who cannot stand is legitimately measured recumbent |
| Weight and height against age | WHO growth standards | **warns** | Clinical implausibility must never block - see the constraint register |
| Label serial within the team's allocation | `range_start`-`range_end` for the signed-in team | **blocks** | Catches another team's book, which the check digit cannot |
| Label unique within the submission | `count(...) = 1` | **blocks** | Same label for two children in one household |
| Enumerator LGA against assignment | `staff_roster.csv` | **blocks** | Relaxed for supervisors |
| Visit date within the fieldwork window | 1-30 June 2026 | **blocks** | Catches a wrong device date |
| Cold-box temperature against 2-8 °C | | **warns** + instructs | Blocking would leave the failure unrecorded, which is the defect being fixed |

## The pattern

**Blocks** are used where continuing produces data that is meaningless (a child
module attached to a 34-year-old) or unsafe (consent recorded after an unread
statement). **Warnings** are used wherever the discrepancy might be true.

That split is not a preference, it is a fabrication-control decision. Every
block an enumerator cannot satisfy honestly is a block they will satisfy
dishonestly, and the dishonest satisfaction is invisible in the data while the
recorded discrepancy is not.

## Where the checks are enforced, and where they are not

All of the above run **on the device**, at the point of capture. None depends on
connectivity, which matters given nine days offline.

Three things are deliberately left to back-office QA rather than enforced in the
form:

- **Duplicate labels beyond one submission of history** - impossible on device
  (`docs/label_reuse.md`).
- **Fabrication patterns** - only visible across submissions and across
  enumerators, so they belong in the daily check (`docs/fabrication_detection.md`).
- **GPS plausibility against the selected settlement** - not enforced, because a
  settlement centroid is not a household location and a geofence would block
  legitimate dwellings at the edge of a settlement. Better handled as a
  back-office flag than a doorstep block.



```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```



# Constraint register - Form HH/2026/v1

**Generated** by `build_register.py` from `build_form.py` (the form) and
`constraint_sources.py` (the justifications). It is not maintained by hand,
and **the build fails if any rule in the form has no documented source** -
so a constraint cannot be added without stating where its value came from.

16 blocking constraints · 6 warnings · 22 rules documented

## How to read the source column

| Source | Meaning |
|---|---|
| Paper form | The value is stated or directly implied by Form HH/2026/v1 |
| Reference data | The value comes from a supplied lookup file |
| Published standard | Named, external and checkable |
| **My judgement** | Mine, with reasoning. Never left unlabelled. |

## Blocking versus warning - and why the split matters

A rule **blocks** only when continuing would produce data that is
meaningless or unsafe. Everything else **warns**, because a block that an
enumerator cannot satisfy honestly is a block they will satisfy
dishonestly - inventing a roster line to clear an error is worse than the
error. There is exactly one hard block on a judgement call in this form:
the consent statement at 2.01.

Two rules are deliberately **wider** than clinical plausibility - child
weight and height. Their hard bounds are typo guards; implausibility is
raised as a warning. A clinical range enforced as a block would delete the
severely malnourished children the survey exists to count.

## Blocking constraints

### `pin_entered` - Enter your 4-digit PIN

| | |
|---|---|
| **Action** | blocks |
| **Rule** | `string-length(.) = 4 and . = ${enum_pin}` |
| **Message shown** | PIN does not match this enumerator code. |
| **What it prevents** | One enumerator submitting under another's code, which is the precondition for the fabrication pattern described in the operating conditions (94 interviews, 4-minute mean). |
| **Source** | Reference data |
| **Detail** | 4-digit PIN held per enumerator in staff_roster.csv. The paper form has no equivalent: 1.08 is a code anyone can write. |

### `q1_02_lga` - 1.02 Local Government Area

| | |
|---|---|
| **Action** | blocks |
| **Rule** | `. = ${enum_lga} or ${enum_role} != 'Enumerator'` |
| **Message shown** | This LGA is not the one assigned to you. Check with your supervisor. |
| **What it prevents** | Work recorded in an LGA the enumerator was not assigned to, which corrupts both the sampling frame and workload tracking. |
| **Source** | Reference data |
| **Detail** | staff_roster.csv assigned_lga. Relaxed for supervisors, who legitimately move between LGAs. |

### `q1_06_structure` - 1.06 Structure number painted on the dwelling

| | |
|---|---|
| **Action** | blocks |
| **Rule** | `. >= 1 and . <= 999` |
| **Message shown** | Enter a number between 1 and 999. |
| **What it prevents** | A mistyped structure number that cannot be traced back to a dwelling on revisit. |
| **Source** | Paper form |
| **Detail** | 1.06 provides three coding boxes, so 1-999. |

### `q1_07_hh_serial` - 1.07 Household serial number within the settlement

| | |
|---|---|
| **Action** | blocks |
| **Rule** | `. >= 1 and . <= 999` |
| **Message shown** | Enter a number between 1 and 999. |
| **What it prevents** | A household serial outside the range the paper form can hold, breaking comparability with paper rounds. |
| **Source** | Paper form |
| **Detail** | 1.07 provides three coding boxes, so 1-999. |

### `q1_10_visit_date` - 1.10 Date of visit

| | |
|---|---|
| **Action** | blocks |
| **Rule** | `. >= date('2026-06-01') and . <= date('2026-06-30')` |
| **Message shown** | Date must fall within the fieldwork window, 1-30 June 2026. |
| **What it prevents** | A visit dated outside the approved fieldwork window - most often a device with the wrong date, or a form completed later from notes. |
| **Source** | Paper form |
| **Detail** | Header states 'Fieldwork period 1 to 30 June 2026'. The operating conditions say fieldwork runs 14 days, which is narrower. The ETHICS-APPROVED window is enforced as the hard constraint and the 14-day expectation is a soft warning, because a hard 14-day rule would reject legitimate submissions if the schedule shifts. |

### `q2_01_statement_read` - 2.01 Consent statement read aloud to the respondent in full?

| | |
|---|---|
| **Action** | blocks |
| **Rule** | `. = '1'` |
| **Message shown** | The consent statement must be read in full before continuing. Read it now, then record Yes. |
| **What it prevents** | An interview proceeding, and biological specimens being taken from children, after the consent statement was not read. |
| **Source** | **My judgement** |
| **Detail** | The paper form records 'No' and continues to 2.02, where consent may then be given. Consent recorded after an unread statement is not informed consent. This is the ONLY hard block in the form; every other rule warns. Escalated to the ethics committee as a paper-form correction. See defect B3. |

### `q3_01_hh_size` - 3.01 How many people usually live in this household?

| | |
|---|---|
| **Action** | blocks |
| **Rule** | `. >= 1 and . <= 40` |
| **Message shown** | Enter between 1 and 40. If larger, notify your supervisor. |
| **What it prevents** | A household size that is a typo rather than a count, and the runaway repeat it would generate. |
| **Source** | **My judgement** |
| **Detail** | Upper bound 40. The paper field accepts two digits (to 99) and the paper roster holds 12 lines, so the instrument itself is inconsistent (defect A4). 40 is set well above any plausible single household while still catching a slipped digit. It is my judgement, not a published figure. A household above 40 is referred to the supervisor rather than silently truncated. |

### `r_age_years` - (5) Age in completed years

| | |
|---|---|
| **Action** | blocks |
| **Rule** | `. >= 5 and . <= 120` |
| **Message shown** | 5 to 120 years. For children under 5, record months instead. |
| **What it prevents** | An under-five recorded in years, which would make the child invisible to the eligibility calculation and lose them from the survey entirely. |
| **Source** | Paper form |
| **Detail** | Roster instruction: ages in YEARS for residents five and over, MONTHS for under-fives. Lower bound 5 enforces that split. Upper bound 120 is my judgement as an implausibility guard. |

### `r_age_months` - (6) Age in completed months

| | |
|---|---|
| **Action** | blocks |
| **Rule** | `. >= 0 and . <= 59` |
| **Message shown** | 0 to 59 months. At 60 months and above, record age in years. |
| **What it prevents** | A child of 60 months or more recorded in the months column, which would wrongly make them eligible. |
| **Source** | Paper form |
| **Detail** | Roster instruction, column (6): 'under 5 only', so 0-59 completed months. |

### `q4_01_line` - 4.01 Line number of this child in the Section 3 roster

| | |
|---|---|
| **Action** | blocks |
| **Rule** | `. >= 1 and . <= ${roster_count} and indexed-repeat(${r_eligible}, ${roster}, .) = 1` |
| **Message shown** | That line is not a child aged 9-59 completed months. Check the roster. |
| **What it prevents** | A child module pointing at an adult, at a line that does not exist, or at a resident outside 9-59 months. |
| **Source** | Paper form |
| **Detail** | 4.01 asks for the roster line number. The paper form cannot check it; indexed-repeat() validates against the roster itself. |

### `q4_05_weight_kg` - 4.05 Weight in kg

| | |
|---|---|
| **Action** | blocks |
| **Rule** | `. >= 2.0 and . <= 30.0` |
| **Message shown** | Weight must be between 2.0 and 30.0 kg for a child aged 9-59 months. |
| **What it prevents** | A transposed or slipped digit at data entry - 152 kg for 15.2. |
| **Source** | **My judgement** |
| **Detail** | Hard bounds 2.0-30.0 kg are a TYPO guard, deliberately wider than clinical plausibility, so that a genuinely severely wasted child is never blocked from being recorded. Clinical implausibility is handled by a separate soft warning against WHO Child Growth Standards, which flags rather than blocks. Blocking on clinical range would delete the very cases the survey exists to find. |

### `q4_06_height_cm` - 4.06 Length or height in cm

| | |
|---|---|
| **Action** | blocks |
| **Rule** | `. >= 45.0 and . <= 130.0` |
| **Message shown** | Height must be between 45.0 and 130.0 cm for a child aged 9-59 months. |
| **What it prevents** | A transposed or slipped digit - 811 cm for 81.1. |
| **Source** | **My judgement** |
| **Detail** | Hard bounds 45.0-130.0 cm on the same principle as weight: a typo guard, not a clinical filter, with WHO-based implausibility raised as a warning. |

### `q5_03_label_serial` - 5.03 Specimen label serial (6 digits, after BSN)

| | |
|---|---|
| **Action** | blocks |
| **Rule** | `regex(., '^[0-9]{6}$') and number(.) >= number(instance('specimen_label_allocation')/root/item[team_code=${enum_team}]/range_start) and number(.) <= number(instance('specimen_label_allocation')/root/item[team_code=${enum_team}]/range_end) and count(/data/child/s5_specimen[q5_03_label_serial = current()/.]) = 1 and count(${last-saved#q5_03_label_serial}[. = current()/.]) = 0` |
| **Message shown** | Label rejected: it is either outside your team's allocated range, already used for another child in this household, or the label used in your previous submission. Check the label book. |
| **What it prevents** | A specimen recorded against a label from outside the team's allocation, which the laboratory cannot reconcile - and an unreconcilable specimen is discarded and the child revisited. |
| **Source** | Reference data |
| **Detail** | range_start and range_end per team in specimen_label_allocation.csv. Six digits enforced by regex. |

### `q5_03_check_digit` - 5.03 Check character (after the hyphen)

| | |
|---|---|
| **Action** | blocks |
| **Rule** | `translate(., 'x', 'X') = ${check_digit_expected}` |
| **Message shown** | Check character does not match the serial. Re-read the label - two digits may have been swapped. |
| **What it prevents** | A mis-keyed or transposed specimen serial reaching the laboratory. Modulus 11 detects every single-digit error and every transposition of two adjacent digits. |
| **Source** | Reference data |
| **Detail** | Scheme stated in specimen_label_allocation.csv: 'Modulus 11, weights 2 to 7 applied right to left, remainder 10 recorded as X'. The check character field accepts X as well as 0-9, which the paper form's digit box cannot (defect E3). |

### `q5_05_coldbox_temp` - 5.05 Temperature shown on the cold box thermometer

| | |
|---|---|
| **Action** | blocks |
| **Rule** | `. >= -20.0 and . <= 40.0` |
| **Message shown** | Temperature must be between -20.0 and 40.0 °C. |
| **What it prevents** | A cold-chain failure being unrecordable. The paper field is one digit and one decimal, so 0.0-9.9: a box at 15 degrees or a frozen box has no representable value, and the field can only record success. |
| **Source** | **My judgement** |
| **Detail** | Widened to -20.0 to 40.0 as a device-range guard. The acceptable 2-8 degree range is enforced as a WARNING that tells the enumerator to notify their supervisor, not as a block - blocking would leave the failure unrecorded, which is the defect being fixed. See defect C3. |

### `q6_07_assets` - 6.07 Which of the following does this household own?

| | |
|---|---|
| **Action** | blocks |
| **Rule** | `not(selected(., 'H') and count-selected(.) > 1)` |
| **Message shown** | 'None of these' cannot be selected together with any other item. |
| **What it prevents** | 'None of these' being selected alongside owned assets, a logical impossibility the paper form permits. |
| **Source** | **My judgement** |
| **Detail** | Standard exclusivity rule for a none-of-the-above option. See defect C2. |

## Warnings

### `roster_mismatch_note` - ⚠ You recorded ${q3_01_hh_size} usual residents but listed ${roster_count}. Check the roster before continuing.

| | |
|---|---|
| **Action** | warns |
| **Rule** | `${roster_count} != ${q3_01_hh_size}` |
| **What it prevents** | A roster that disagrees with the stated household size passing unnoticed until data entry, weeks after the household could be revisited. |
| **Source** | **My judgement** |
| **Detail** | Required by the question: reconcile stated household size against the roster. Implemented as a WARNING, not a block: the two legitimately differ when a usual resident is absent and the enumerator cannot obtain their details. Blocking would push enumerators to invent a line to clear the error. |

### `weight_implausible_warn` - ⚠ This weight is outside the usual range for a child aged ${q4_03_age_months} months. Re-weigh to confirm, then record what you measure.

| | |
|---|---|
| **Action** | warns |
| **Rule** | `${q4_05_weight_status} = 'measured' and (${q4_05_weight_kg} < 5.0 or ${q4_05_weight_kg} > 28.0)` |
| **What it prevents** | A weight that is possible to type but not to observe, passing unnoticed into analysis. |
| **Source** | Published standard |
| **Detail** | WHO Child Growth Standards, approximately -4 SD to +4 SD across 9-59 months. Warns; never blocks. |

### `height_implausible_warn` - ⚠ This height is outside the usual range for a child aged ${q4_03_age_months} months. Re-measure to confirm, then record what you measure.

| | |
|---|---|
| **Action** | warns |
| **Rule** | `${q4_06_height_status} = 'measured' and (${q4_06_height_cm} < 60.0 or ${q4_06_height_cm} > 125.0)` |
| **What it prevents** | A height outside any observed value for the age band. |
| **Source** | Published standard |
| **Detail** | WHO Child Growth Standards, approximately -4 SD to +4 SD across 9-59 months. Warns; never blocks. |

### `q4_07_position_warn` - ⚠ Convention is recumbent below 24 months and standing at 24 months and above. Confirm this was intended.

| | |
|---|---|
| **Action** | warns |
| **Rule** | `(${q4_03_age_months} < 24 and ${q4_07_position} = '2') or (${q4_03_age_months} >= 24 and ${q4_07_position} = '1')` |
| **What it prevents** | Length and height being recorded against the wrong convention, which biases every derived z-score by roughly 0.7 cm. |
| **Source** | Published standard |
| **Detail** | WHO Child Growth Standards: recumbent length below 24 months, standing height at 24 months and above. Warns rather than blocks, because a child who cannot stand is legitimately measured recumbent at any age. |

### `q4_13_placeholder_warning` - ⚠ PLACEHOLDER MEDICINE LIST - NOT FOR DEPLOYMENT. The codelist referenced by the paper form was not supplied. See defect E1.

| | |
|---|---|
| **Action** | warns |
| **Rule** | `${q4_12_antibiotic} = '1'` |
| **What it prevents** | Placeholder medicine codes being collected without the enumerator, the supervisor or the analyst realising the codelist is not the real one. |
| **Source** | **My judgement** |
| **Detail** | The medicine list referenced by 4.13 is absent from the data pack (defect E1). The substitute uses WHO ATC codes, which cannot be confused with the two-digit local codes the paper form expects, so placeholder data is self-identifying. This banner is the second guard: the substitution is visible at the point of capture, not only in documentation nobody reads in the field. |

### `q5_05_temp_warn` - ⚠ Temperature is outside 2-8 °C. Report to your supervisor now - the cold chain may have failed.

| | |
|---|---|
| **Action** | warns |
| **Rule** | `${q5_02_specimen_obtained} = '1' and (${q5_05_coldbox_temp} < 2 or ${q5_05_coldbox_temp} > 8)` |
| **What it prevents** | A cold-chain excursion being recorded and then ignored. |
| **Source** | Published standard |
| **Detail** | 2-8 degrees C is the standard specimen cold-chain range. Warns and instructs the enumerator to notify the supervisor immediately. |

## Language

Every constraint message exists in **Hausa and English**, Hausa default.
Interviews are conducted in Hausa and 38% of enumerators are not confident
readers of English, so an English-only message is a message that does not
exist. **The Hausa strings are indicative and require native-speaker review
before deployment** - they are my own and have not been checked.

## What is not constrained, and why

- **`q1_05_alt_name`, `q4_14_medicine_other`, `q5_07_reason_other`, `q7_02_observation`** - free text by design. Constraining an other-specify field defeats its purpose.
- **`q1_11_gps`** - no geofence. A settlement centroid is not a household location, and a boundary constraint would block legitimate dwellings on the edge of a settlement. Out-of-area points are better found in back-office QA against the settlement list than blocked at the doorstep.
- **`q4_13_medicine`** - no validity constraint beyond selection from the list, because the real codelist does not exist. See defect E1.



```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```



# How this form was validated, and how to validate it yourself

## Read this before opening the form in XLSForm Online

**XLSForm Online will report "Can't find settlements.csv" and five more like it.
That is expected, and the form is not broken.**

The tool does two separate things: it converts the workbook, then previews the
result in Enketo. Conversion is what the assessment requires and it succeeds.
The **preview** fails, because the form uses `select_one_from_file` against seven
external CSVs and XLSForm Online has no mechanism to attach media. Enketo is
being asked to render a form whose lookup tables are absent.

The distinction matters: **conversion succeeded, form loading failed.** Any form
that serves a 2,524-row settlement list from external media will behave this way
in that preview. The alternative - putting 2,524 settlements on the `choices`
worksheet so the preview works - is the design this question explicitly rules
out.

## What was validated, and with what

| Stage | Tool | Result |
|---|---|---|
| Workbook → XForm conversion | **pyxform 4.5.0** | SUCCESS, output in `form/conversion_log.txt` |
| XForm structure and XPath | **ODK Validate** (bundled with pyxform, **OpenJDK 21**) | SUCCESS |
| External references resolve | `validate_media.py` (written for this submission) | PASSED |

**All three are run by `python part2_q3/build_form.py && python part2_q3/validate_media.py`.**

## Why the third check had to be written

pyxform and ODK Validate both pass forms whose external lookups are broken. They
inspect the form in isolation; neither opens a media file. Three failures get
through:

1. A `jr://file-csv/x.csv` reference with no matching media file.
2. An `instance('x')` call inside a **constraint or calculation** where `x` was
   never declared. pyxform declares external instances only for
   `select_one_from_file` *types* - an `instance()` call in an expression is
   invisible to it.
3. A path naming a column the CSV does not contain.

All three convert clean, validate clean, and fail on the device.

**This form had defect 2**, and it was found by trying to load the form rather
than by any validator. The specimen serial-range constraint referenced
`instance('specimen_label_allocation')`, which no question declared. At runtime
that lookup returns an empty nodeset, `number()` of empty is `NaN`, and the
comparison is false - so **the constraint would have rejected every valid
specimen label in the field**, on a form that all tooling reported as correct.

The fix is not a dummy declaration. The enumerator now confirms the label book
issued to their team at sign-in; the filter leaves exactly one option, so it is
one tap, and it catches a team working from the wrong book - an error the check
digit cannot detect, because a label from another team's book is internally
valid. A defect found once by hand is now found automatically by
`validate_media.py`.

## Validating it properly

The form needs its seven attachments. Two routes:

### ODK Central (recommended)
1. Create a project, **Draft** → upload `form/bansara_hh_2026.xlsx`.
2. On the draft, **Media Files** → upload all seven CSVs from `form/media/`.
3. **Preview** in Enketo, or publish and pull into ODK Collect.

### ODK Collect, no server
Copy `bansara_hh_2026.xml` into `Android/data/org.odk.collect.android/files/projects/<id>/forms/`
and the seven CSVs into a folder beside it named `bansala_hh_2026-media/`.

## The seven required attachments

| File | Rows | Purpose |
|---|---|---|
| `lgas.csv` | 4 | 1.02 cascade root |
| `wards.csv` | 40 | 1.03, filtered by LGA |
| `settlements.csv` | 2,524 | 1.04, filtered by ward |
| `staff_roster.csv` | 120 | enumerator sign-in, PIN, supervisor at 7.04 |
| `previous_round_households.csv` | 3,982 | 1.13, filtered by settlement |
| `specimen_label_allocation.csv` | 24 | label-range constraint at 5.03 |
| `medicines.csv` | 23 | 4.13 - **placeholder, see defect E1** |

Built by `python part2_q3/prepare_media.py`, which reads the supplied reference
files and **never modifies them**.

## Known limitation of this validation

None of the above proves the form behaves correctly for a *respondent* - only
that it loads and that its references resolve. Behavioural correctness is
covered by the test plan in `test_plan.md`, which specifies expected results for
boundary and negative cases, including the specimen eligibility cut, the
measurement position change, the ends of every range, a date outside the
fieldwork window, and a roster that disagrees with the stated household size.

**Those test cases have been specified but not executed against a running
instance**, since no ODK Central project was available inside the submission
window. That is stated plainly here rather than left to be assumed: a test plan
that has been written is not a test plan that has been run.



```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```



# Serving 2,524 settlements to a 2 GB tablet (F6)

The question rules out the easy answer in advance: *"A choices worksheet is not
an acceptable answer, and saying so is not sufficient; describe the mechanism
you used instead."*

## The mechanism

The settlement list is delivered as an **external CSV attached to the form as
media**, and referenced with **`select_one_from_file settlements.csv`**. The
cascade from LGA to ward to settlement is expressed as a `choice_filter` on
those external files.

The difference from a choices worksheet is architectural, not cosmetic:

| | Choices worksheet | External CSV media |
|---|---|---|
| Where the options live | Compiled into the form definition itself | A separate file attached to the form |
| What happens on open | ODK Collect **parses the whole codelist into memory** | Nothing - the file was imported once |
| First use | - | Collect imports the CSV into its local **SQLite** database |
| Every use after | Walks an in-memory list | **Indexed query** against SQLite |
| Memory cost during the interview | The entire 2,524-row list, held for the whole session | A query result - the handful of rows that match the filter |
| Cascade filtering | Evaluated in the form engine | Evaluated by the database |

On a 2 GB device shared with the operating system, Collect, the camera and
whatever else the tablet is doing, the distinction is the difference between
carrying a codelist for the length of every interview and holding a few rows for
the length of one question.

## What that costs, and what it buys

Columns are trimmed to those the form actually references, because unused
columns cost import time and storage on every device, 120 times over:

| File | Rows | As supplied | Prepared |
|---|---|---|---|
| `settlements.csv` | 2,524 | 212.5 KB | **88.6 KB** |
| `previous_round_households.csv` | 3,982 | 328.8 KB | 289.3 KB |
| `wards.csv` | 40 | 1.1 KB | 1.1 KB |
| `staff_roster.csv` | 120 | 6.5 KB | 6.6 KB |
| `specimen_label_allocation.csv` | 24 | 2.5 KB | 1.3 KB |
| `medicines.csv` | 23 | - | 1.9 KB |
| `lgas.csv` | 4 | 0.1 KB | 0.1 KB |
| **Total shipped to each device** | | 551.4 KB | **388.9 KB** |

Built by `prepare_media.py`, which reads the supplied reference files and
**never modifies them**.

## What I rejected, and why

### 1. Putting the settlements on the `choices` worksheet

**Rejected on memory.** This is the option the question names, and the reason is
above: 2,524 rows compiled into the form definition and parsed into RAM at open,
for the whole interview, on a 2 GB device.

There is a second reason worth stating. A choices worksheet is **part of the
form**, so correcting a settlement name means publishing a new form version -
and with devices offline for up to nine days, a form version change mid-round is
the most disruptive thing you can do (see `deployment_plan.md`). An external CSV
is a **media file**: it can be replaced without touching the form's logic.

### 2. The `search()` appearance

The older ODK idiom for pulling options from a CSV. **Rejected because it is
deprecated** and was never fully supported in Enketo, so a form built on it
behaves differently on a tablet and in a browser preview. `select_one_from_file`
is the supported replacement and works in both.

### 3. Splitting the survey into four LGA-specific forms

Each form would carry only its own settlements - roughly 600 rows instead of
2,524.

**Rejected**, for three reasons that compound:

- It creates **four datasets, not one.** Every analysis then begins with a union,
  and the analysis team must remember that four form IDs are the same instrument.
- It **multiplies the mid-round change problem by four.** The operating
  conditions say a mid-round change is likely; four forms means four
  publications and four opportunities for a device to be running the wrong one.
- It solves a problem the external-file approach has already solved, at the cost
  of a structural complication that lasts for the whole round.

### 4. A live server lookup

Query the settlement list from a server as the enumerator types.

**Rejected outright by the operating conditions.** Nine consecutive days offline.
Anything requiring connectivity at the moment of data entry is not a candidate.
Recording this because it is the answer that a reviewer used to connected
deployments might expect.

### 5. Pre-filtering each device's list to its own team

Ship each team only the settlements in its assigned wards - about 100 rows per
device instead of 2,524.

**This one I did not reject on the merits**, and it is worth being precise about
why it is not implemented. On memory grounds it is strictly better. On data
protection grounds it is *considerably* better, and
`data_protection.md` recommends exactly this for
`previous_round_households.csv`, which currently ships 3,982 households with
initials and GPS to every tablet.

What stopped it is **operational, not technical**: one media set becomes
twenty-four. That changes provisioning, the update procedure, and what happens
when an enumerator is reassigned mid-round - a supervisor moving someone to
another ward would need to reprovision the device rather than just tell them.
That is the survey manager's decision, not mine, so it is recorded as a
recommendation in `deliberate_scope.md` rather than made unilaterally.

**At 389 KB total, memory is not the binding reason to do it. Data protection
is.**

## The check that keeps this honest

External media introduces a failure mode that a choices worksheet does not have:
**the form can reference a file that is not there, or a column that does not
exist, and still convert and validate cleanly.**

That happened twice in this build. `validate_media.py` now checks, on every
rebuild, that every `instance()` call resolves to a declared instance, every
declared media file exists, each has the `name` and `label` columns
`select_one_from_file` requires, and every column named in a path is present in
that CSV. See `validation.md`.



```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```



# Test plan - Form HH/2026/v1

**Partly generated.** Every numeric range in the form produces four cases
automatically - below minimum, at minimum, at maximum, above maximum - read
from the form's own constraints by `build_test_plan.py`. Add a range and its
boundary cases appear here; change a bound and the expected values follow.
The plan cannot drift from the form.

**54 cases** - 29 negative, 20 boundary, 5 positive/behavioural.

## Execution status

**These cases are specified. They have not been executed against a running
instance**, because no ODK Central project was available inside the
submission window. The check-digit logic behind S09 *is* executed -
exhaustively - in `tests/test_check_digit.py`. Everything else is a
specification awaiting a device.

Saying so matters: a test plan that has been written is not a test plan that
has been run, and reporting the two as equivalent would be the same
overclaim this form is designed to prevent elsewhere.

To execute: deploy per `docs/validation.md`, then work the table top to
bottom recording actual against expected.

## Coverage of the cases the question names

| Required by the question | Cases |
|---|---|
| Specimen eligibility cut | S01, S02 |
| Measurement position change | S03, S04 |
| Ends of every range set | all B-numbered cases, generated |
| Date outside the fieldwork window | S05, S06 |
| Roster disagrees with stated household size | S07 |
| Negative tests | 29 of 54 |

## Scenario cases

### S01 - Specimen eligibility cut, lower side **[REQUIRED BY THE QUESTION]**

| | |
|---|---|
| **Type** | boundary |
| **Target** | `q5_01_specimen_eligible` |
| **Setup** | Roster child aged **11 completed months** |
| **Input** | advance to Section 5 |
| **Expected** | No specimen sought. 5.02-5.07 hidden; note shown that the child is under 12 months. The child module (Section 4) is still completed in full. |
| **Why it matters** | The paper form sends this child to Section 6, abandoning every remaining child in the household (defect B2). Here the skip ends only this child's iteration. |
| **Result** | _not yet executed_ |

### S02 - Specimen eligibility cut, upper side **[REQUIRED BY THE QUESTION]**

| | |
|---|---|
| **Type** | boundary |
| **Target** | `q5_01_specimen_eligible` |
| **Setup** | Roster child aged **12 completed months** |
| **Input** | advance to Section 5 |
| **Expected** | Specimen sought. 5.02 shown and required. |
| **Why it matters** | 12 months is the cut stated at 5.01. Paired with S01 it brackets it. |
| **Result** | _not yet executed_ |

### S03 - Measurement position change, below the cut **[REQUIRED BY THE QUESTION]**

| | |
|---|---|
| **Type** | boundary |
| **Target** | `q4_07_position` |
| **Setup** | Child aged **23 months**, height measured |
| **Input** | 4.07 = Standing height |
| **Expected** | WARNING shown, entry allowed |
| **Why it matters** | WHO convention is recumbent below 24 months. It warns rather than blocks: a child who cannot stand is legitimately measured recumbent at any age. |
| **Result** | _not yet executed_ |

### S04 - Measurement position change, at the cut **[REQUIRED BY THE QUESTION]**

| | |
|---|---|
| **Type** | boundary |
| **Target** | `q4_07_position` |
| **Setup** | Child aged **24 months**, height measured |
| **Input** | 4.07 = Standing height |
| **Expected** | No warning |
| **Why it matters** | 24 months and above is standing height. S03/S04 bracket the cut. |
| **Result** | _not yet executed_ |

### S05 - Date before the fieldwork window **[REQUIRED BY THE QUESTION]**

| | |
|---|---|
| **Type** | negative |
| **Target** | `q1_10_visit_date` |
| **Setup** | Device date set to 31 May 2026 |
| **Input** | 1.10 = 2026-05-31 |
| **Expected** | REJECT with the Hausa message |
| **Why it matters** | Most often a device with the wrong date, or a form completed later from paper notes. |
| **Result** | _not yet executed_ |

### S06 - Date after the fieldwork window **[REQUIRED BY THE QUESTION]**

| | |
|---|---|
| **Type** | negative |
| **Target** | `q1_10_visit_date` |
| **Input** | 1.10 = 2026-07-01 |
| **Expected** | REJECT |
| **Why it matters** | The window enforced is 1-30 June, the ethics-approved one, not the 14-day operational expectation. See the constraint register. |
| **Result** | _not yet executed_ |

### S07 - Roster disagrees with stated household size **[REQUIRED BY THE QUESTION]**

| | |
|---|---|
| **Type** | negative |
| **Target** | `roster_mismatch_note` |
| **Setup** | 3.01 = 6 usual residents |
| **Input** | Complete 4 roster lines and advance |
| **Expected** | WARNING shown naming both numbers. Entry continues. |
| **Why it matters** | Warns rather than blocks: the two legitimately differ when a usual resident is absent and cannot be described. A block would push enumerators to invent a line to clear the error. |
| **Result** | _not yet executed_ |

### S08 - Consent statement not read

| | |
|---|---|
| **Type** | negative |
| **Target** | `q2_01_statement_read` |
| **Input** | 2.01 = No |
| **Expected** | BLOCK. Cannot advance. |
| **Why it matters** | The only hard block in the form. The paper form records No and continues to 2.02 where consent may be given (defect B3). |
| **Result** | _not yet executed_ |

### S09 - Transposed pair of digits in the specimen serial

| | |
|---|---|
| **Type** | negative |
| **Target** | `q5_03_check_digit` |
| **Setup** | Valid label BSN480123-? with correct check character |
| **Input** | Enter serial 480132 (last two digits swapped) with the original check character |
| **Expected** | REJECT |
| **Why it matters** | Proven exhaustively in tests/test_check_digit.py: 292,960 transpositions tested, none escaped. |
| **Result** | _not yet executed_ |

### S10 - Label from another team's book

| | |
|---|---|
| **Type** | negative |
| **Target** | `q5_03_label_serial` |
| **Setup** | Signed in as a TM01 enumerator (range 480000-480899) |
| **Input** | 5.03 serial = 480900 |
| **Expected** | REJECT (out of allocated range) |
| **Why it matters** | This label passes the check digit - it is internally valid. Only the range constraint catches it. |
| **Result** | _not yet executed_ |

### S11 - Same label used twice in one household

| | |
|---|---|
| **Type** | negative |
| **Target** | `q5_03_label_serial` |
| **Setup** | Two eligible children, specimen taken from both |
| **Input** | Enter the same serial for the second child |
| **Expected** | REJECT |
| **Why it matters** | The most common genuine duplicate: two entries minutes apart from the same book. |
| **Result** | _not yet executed_ |

### S12 - Label reused from the previous submission

| | |
|---|---|
| **Type** | negative |
| **Target** | `q5_03_label_serial` |
| **Setup** | Complete and save a submission using serial X, start the next |
| **Input** | Enter serial X again |
| **Expected** | REJECT |
| **Why it matters** | last-saved covers one submission of history only. Submission n-2 and earlier are NOT caught - see docs/label_reuse.md. |
| **Result** | _not yet executed_ |

### S13 - 'None of these' selected with an owned asset

| | |
|---|---|
| **Type** | negative |
| **Target** | `q6_07_assets` |
| **Input** | 6.07 = Radio + None of these |
| **Expected** | REJECT |
| **Why it matters** | A logical impossibility the paper form permits (defect C2). |
| **Result** | _not yet executed_ |

### S14 - Wrong PIN for the selected enumerator code

| | |
|---|---|
| **Type** | negative |
| **Target** | `pin_entered` |
| **Input** | Select ENU001, enter PIN 0000 |
| **Expected** | REJECT |
| **Why it matters** | Prevents one enumerator submitting under another's code - the precondition for the fabrication pattern in the operating conditions. |
| **Result** | _not yet executed_ |

### S15 - LGA not assigned to this enumerator

| | |
|---|---|
| **Type** | negative |
| **Target** | `q1_02_lga` |
| **Setup** | Signed in as an enumerator assigned to Gwarin |
| **Input** | 1.02 = Idi-Oro |
| **Expected** | REJECT (relaxed for supervisors) |
| **Why it matters** | staff_roster.csv assigned_lga. |
| **Result** | _not yet executed_ |

### S16 - Skip logic when no specimen is obtained

| | |
|---|---|
| **Type** | positive |
| **Target** | `q5_02_specimen_obtained` |
| **Input** | 5.02 = No |
| **Expected** | 5.03-5.05 hidden; 5.06 reason shown and required |
| **Why it matters** | 5.02 has NO skip instruction on the paper form at all (defect B1). This is the case that defect produces. |
| **Result** | _not yet executed_ |

### S17 - Skip logic when a specimen IS obtained

| | |
|---|---|
| **Type** | positive |
| **Target** | `q5_02_specimen_obtained` |
| **Input** | 5.02 = Yes |
| **Expected** | 5.03-5.05 shown and required; 5.06-5.07 hidden |
| **Why it matters** | The mirror of S16. On paper, 5.06 applies to everyone. |
| **Result** | _not yet executed_ |

### S18 - Child module pointed at an adult

| | |
|---|---|
| **Type** | negative |
| **Target** | `q4_01_line` |
| **Setup** | Roster line 1 is a 34-year-old head of household |
| **Input** | 4.01 = 1 |
| **Expected** | REJECT |
| **Why it matters** | Validated with indexed-repeat() against the roster. The paper form cannot check this. |
| **Result** | _not yet executed_ |

### S19 - Result of visit is not 'Completed'

| | |
|---|---|
| **Type** | positive |
| **Target** | `q1_14_result` |
| **Input** | 1.14 = Dwelling vacant or demolished |
| **Expected** | Sections 2-6 hidden. Note instructs the enumerator to sign at 7.03 and hand the form to the supervisor. |
| **Why it matters** | Mirrors the paper instruction after 1.14. |
| **Result** | _not yet executed_ |

### S20 - Eligible-children count is derived, not typed

| | |
|---|---|
| **Type** | positive |
| **Target** | `q3_02_eligible` |
| **Setup** | Roster with children aged 8, 9, 59 and 60 completed months |
| **Input** | Advance past the roster |
| **Expected** | Eligible count = 2 (the 9- and 59-month children). Two child modules generated. |
| **Why it matters** | Brackets BOTH ends of the 9-59 eligibility window in one case, and demonstrates defect A1's fix: the count is derived from roster ages, never transcribed from an office-use column. This is also the second cross-question consistency check - stated eligible children and modules completed cannot disagree because they are the same quantity. |
| **Result** | _not yet executed_ |

### S21 - Clinically implausible but typeable weight

| | |
|---|---|
| **Type** | positive |
| **Target** | `q4_05_weight_kg` |
| **Setup** | Child aged 24 months |
| **Input** | 4.05 weight = 4.0 kg |
| **Expected** | WARNING shown, entry ALLOWED |
| **Why it matters** | The hard bounds are a typo guard; clinical implausibility warns. Blocking here would delete the severely wasted children the survey exists to count. |
| **Result** | _not yet executed_ |

### S22 - Placeholder medicine list is visible at the point of capture

| | |
|---|---|
| **Type** | negative |
| **Target** | `q4_13_medicine` |
| **Setup** | 4.12 = Yes |
| **Input** | Advance to 4.13 |
| **Expected** | Banner shown: PLACEHOLDER LIST - NOT FOR DEPLOYMENT |
| **Why it matters** | Defect E1. The substitution must be visible in the field, not only in documentation nobody reads at a doorstep. |
| **Result** | _not yet executed_ |

## Generated boundary cases

Four per numeric range: the two values that must be accepted and the two
just outside that must be rejected.

| ID | Field | Question | Input | Expected | Boundary |
|---|---|---|---|---|---|
| B01 | `q1_06_structure` | 1.06 Structure number painted on the dwellin | `0` | **REJECT** | just below the minimum |
| B02 | `q1_06_structure` | 1.06 Structure number painted on the dwellin | `1` | **ACCEPT** | exactly at the minimum |
| B03 | `q1_06_structure` | 1.06 Structure number painted on the dwellin | `999` | **ACCEPT** | exactly at the maximum |
| B04 | `q1_06_structure` | 1.06 Structure number painted on the dwellin | `1000` | **REJECT** | just above the maximum |
| B05 | `q1_07_hh_serial` | 1.07 Household serial number within the sett | `0` | **REJECT** | just below the minimum |
| B06 | `q1_07_hh_serial` | 1.07 Household serial number within the sett | `1` | **ACCEPT** | exactly at the minimum |
| B07 | `q1_07_hh_serial` | 1.07 Household serial number within the sett | `999` | **ACCEPT** | exactly at the maximum |
| B08 | `q1_07_hh_serial` | 1.07 Household serial number within the sett | `1000` | **REJECT** | just above the maximum |
| B09 | `q3_01_hh_size` | 3.01 How many people usually live in this ho | `0` | **REJECT** | just below the minimum |
| B10 | `q3_01_hh_size` | 3.01 How many people usually live in this ho | `1` | **ACCEPT** | exactly at the minimum |
| B11 | `q3_01_hh_size` | 3.01 How many people usually live in this ho | `40` | **ACCEPT** | exactly at the maximum |
| B12 | `q3_01_hh_size` | 3.01 How many people usually live in this ho | `41` | **REJECT** | just above the maximum |
| B13 | `r_age_years` | (5) Age in completed years | `4` | **REJECT** | just below the minimum |
| B14 | `r_age_years` | (5) Age in completed years | `5` | **ACCEPT** | exactly at the minimum |
| B15 | `r_age_years` | (5) Age in completed years | `120` | **ACCEPT** | exactly at the maximum |
| B16 | `r_age_years` | (5) Age in completed years | `121` | **REJECT** | just above the maximum |
| B17 | `r_age_months` | (6) Age in completed months | `-1` | **REJECT** | just below the minimum |
| B18 | `r_age_months` | (6) Age in completed months | `0` | **ACCEPT** | exactly at the minimum |
| B19 | `r_age_months` | (6) Age in completed months | `59` | **ACCEPT** | exactly at the maximum |
| B20 | `r_age_months` | (6) Age in completed months | `60` | **REJECT** | just above the maximum |
| B21 | `q4_05_weight_kg` | 4.05 Weight in kg | `1.9` | **REJECT** | just below the minimum |
| B22 | `q4_05_weight_kg` | 4.05 Weight in kg | `2.0` | **ACCEPT** | exactly at the minimum |
| B23 | `q4_05_weight_kg` | 4.05 Weight in kg | `30.0` | **ACCEPT** | exactly at the maximum |
| B24 | `q4_05_weight_kg` | 4.05 Weight in kg | `30.1` | **REJECT** | just above the maximum |
| B25 | `q4_06_height_cm` | 4.06 Length or height in cm | `44.9` | **REJECT** | just below the minimum |
| B26 | `q4_06_height_cm` | 4.06 Length or height in cm | `45.0` | **ACCEPT** | exactly at the minimum |
| B27 | `q4_06_height_cm` | 4.06 Length or height in cm | `130.0` | **ACCEPT** | exactly at the maximum |
| B28 | `q4_06_height_cm` | 4.06 Length or height in cm | `130.1` | **REJECT** | just above the maximum |
| B29 | `q5_05_coldbox_temp` | 5.05 Temperature shown on the cold box therm | `-20.1` | **REJECT** | just below the minimum |
| B30 | `q5_05_coldbox_temp` | 5.05 Temperature shown on the cold box therm | `-20.0` | **ACCEPT** | exactly at the minimum |
| B31 | `q5_05_coldbox_temp` | 5.05 Temperature shown on the cold box therm | `40.0` | **ACCEPT** | exactly at the maximum |
| B32 | `q5_05_coldbox_temp` | 5.05 Temperature shown on the cold box therm | `40.1` | **REJECT** | just above the maximum |

## What this plan does not cover

- **Device behaviour under memory pressure.** A 40-person roster with 8
  eligible children on a 2 GB tablet needs a real device, not a plan.
- **Hausa comprehension.** Every string is bilingual, but whether an
  enumerator with six years of schooling *understands* a given message is
  a cognitive-interview question, not a test case. The strings need
  native-speaker review before deployment.
- **Duplicate labels beyond one submission of history.** Out of scope by
  construction - see `docs/label_reuse.md`.
- **Encryption round-trip.** The public key in settings is a placeholder;
  decryption cannot be tested until the real keypair is issued.



```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```



# Rejecting a specimen label already used in an earlier submission (F8)

## The plain answer

**No. A self-contained form cannot enforce this.**

Not because ODK lacks a feature, but because of what "self-contained" means. A
form instance is a document. It is filled, saved and submitted, and it has no
writable store that outlives it. Detecting reuse against *every* earlier
submission requires state that persists across instances and is consulted before
the current one is saved - which is, definitionally, not something the form
holds.

Anything claiming otherwise is either checking a narrower thing (the last
submission, this submission) or relying on a server the form cannot reach for
nine days.

## What was implemented anyway, and what each layer actually catches

Three layers are enforceable on the device. Their coverage is uneven and it is
worth being precise about which error each one stops.

| Layer | Rule | Catches | Misses |
|---|---|---|---|
| **1. Allocation range** | serial within the signed-in team's `range_start`-`range_end` | A label from another team's book - which the **check digit cannot detect**, because such a label is internally valid | Reuse within the team's own range |
| **2. Within this submission** | `count(/data/child/s5_specimen[q5_03_label_serial = current()/.]) = 1` | The same label entered for two children in the same household - the most common real duplicate, since both entries happen minutes apart from one book | Anything from an earlier household |
| **3. Previous submission** | `count(${last-saved#q5_03_label_serial}[. = current()/.]) = 0` | Re-entering the label from the household just completed, typically because the enumerator re-read the same sticker | Submission *n−2* and earlier |

Layer 3 uses ODK's `last-saved` instance, which holds **only the immediately
preceding submission**. It is genuinely useful - consecutive re-entry is a common
slip - but it is one step of history, not a ledger. Describing it as duplicate
detection would be overclaiming.

**A note on how this was found.** The first implementation called
`instance('last-saved')` directly. pyxform exposes the previous submission only
through its own `${last-saved#field}` syntax and names the instance
`__last-saved`, so the raw call converted cleanly, passed ODK Validate, and
would have resolved to an empty nodeset in the field - making the constraint
pass unconditionally and silently disabling layer 3. `validate_media.py` caught
it. That is the second time the same class of defect has appeared in this form,
which is why the check is automated rather than remembered.

## What the requirement is really about

The labels are **pre-printed and physically affixed** - 5.03 says *"Affix the
specimen label in the box."* A physical sticker can be applied to exactly one
container. So a duplicated label number in the data is, in the overwhelming
majority of cases, **a transcription error rather than genuine reuse**: the
enumerator read the wrong line of the book, or typed the previous child's serial
from memory.

That matters, because transcription errors are precisely what layers 1-3 and the
check digit are good at. Genuine reuse - the same sticker on two containers -
is a physical impossibility unless labels were reprinted, which is a printing
control problem, not a form design problem.

The requirement should therefore be read as *"do not let a label be recorded
twice"*, and most of that is achievable on the device.

## The architecture that can enforce it fully

### Server-side uniqueness at submission - the authoritative layer

A `UNIQUE` constraint on the specimen identifier in the receiving store, applied
when a submission arrives. This is the only layer that is genuinely complete: it
sees every submission from every device, needs no device state, and cannot be
outrun by an enumerator who reinstalls the app.

**On ODK Central this is a validation step behind the submission endpoint**, not
a Central feature in itself - Central accepts submissions and does not reject on
content. In practice: submissions stream to a store, a job asserts uniqueness on
`specimen_label_full`, and a duplicate raises a flag on both submissions for
supervisor resolution. The laboratory then receives a reconciled list rather
than a raw one.

**It is detective, not preventive.** By the time it fires, the team has moved on.
It cannot stop the collection of a duplicate; it can stop a duplicate reaching
the laboratory, which is what the requirement asks for.

### ODK Entities - preventive, but defeated by the offline window

ODK Entities let a submission create or update a shared dataset that later form
downloads receive as an attachment. A `used_labels` entity list would make prior
labels visible to the form itself.

**It does not survive the operating conditions.** Entity updates propagate on
sync, and these devices are offline for **up to nine consecutive days**. A device
that has not synced has an entity list up to nine days stale, and two devices
that never sync during the round can never see each other's labels. It is the
right architecture for a connected deployment and the wrong one here.

Recording that explicitly, because "use Entities" is the fashionable answer and
it is wrong for this fieldwork.

### Procedural control - the layer that actually prevents

The one control that operates at the moment of the error: **the label book
itself.** Serials are issued to a team as a physical range; the enumerator
strikes through each label as it is used. A struck-through label cannot be
selected twice without the enumerator noticing.

This is cheap, needs no connectivity, and is the only layer that acts before the
data is recorded rather than after. It is also the layer most likely to be
skipped under time pressure, which is why the digital layers exist alongside it
rather than instead of it.

### Laboratory reconciliation - the backstop that already exists

The operating conditions state that the laboratory reconciles against the form
data and that an unmatched specimen is discarded and the child revisited. That
is a real, working duplicate detector - with a cost of one wasted specimen and
one revisit per occurrence. Every layer above exists to reduce how often that
cost is paid.

## Summary

| Layer | Preventive or detective | Works offline | Complete |
|---|---|---|---|
| Label book strike-through | **Preventive** | Yes | No - depends on discipline |
| Form: allocation range | Preventive | Yes | No - within-range reuse passes |
| Form: within submission | Preventive | Yes | No - this household only |
| Form: last-saved | Preventive | Yes | No - one submission of history |
| Server-side uniqueness | Detective | **No** | **Yes** |
| Laboratory reconciliation | Detective | Yes | Yes - at the cost of a revisit |

**No single layer satisfies the requirement.** The form contributes the three it
can, and the write-up says plainly which errors still get through - because a
supervisor who believes the form prevents duplicates will stop checking the
label book, and that trade is a net loss.



```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```



# Designing for fabrication detection (F11)

The operating conditions state the failure this has to prevent:

> In the last round one enumerator submitted 94 interviews with a mean duration
> of 4 minutes and almost no vaccination cards sighted. **This was discovered
> only after fieldwork had closed.**

The detection was not the problem - the pattern is obvious once you look. The
*timing* was. Ninety-four households were spent and the round could not be
repaired. So the requirement is not "can this be detected" but "is it detected
while there is still something to do about it".

**Implemented and demonstrated**: `daily_qa.py` flags the planted pattern at the
**end of day 2, on 22 submissions**, against a 14-day round. Run
`python part2_q3/daily_qa.py --demo`.

## Fields that exist solely to enable back-office QA

These answer no survey question. They are in the form because the paper form
cannot have them, and they are what makes daily detection possible at all.

| Field | Type | What it enables |
|---|---|---|
| `start_time` | `start` | Interview duration - the primary fabrication signal |
| `end_time` | `end` | as above |
| `interview_duration_min` | calculated | Duration in minutes, so no analyst has to derive it consistently |
| `device_id` | `deviceid` | Detects one device submitting under several enumerator codes |
| `audit` | `audit` with `track-changes`, `identify-user`, `track-changes-reasons` | Per-question timing and a change log. Reveals a form filled in one pass with no back-navigation, which real interviews do not look like |
| `today_date` | `today` | Device date, comparable against `q1_10_visit_date` - catches back-dating |
| `pin_entered` | text, masked | Binds a submission to a person, not just to a typed code |

**Dual-purpose fields** - operationally necessary, and also QA evidence:
`q1_11_gps` (household location; also reveals a stationary enumerator),
`q4_08_card` (a substantive coverage variable; also the second signal in the
described pattern), `q4_16_photo` (medicine packaging; also independently
verifiable evidence a visit occurred).

## The daily check

Run each evening against submissions received so far. Output is a ranked list a
supervisor acts on the next morning.

### Indicators

| Indicator | Compared against | Detects |
|---|---|---|
| Median interview duration | Cohort median | Interviews too short to have happened |
| Card sighting rate | Cohort median | Documentation not actually being asked for |
| Submissions per day | Cohort median | Volume no one could physically achieve |
| Distinct GPS locations | Absolute (≤2 across ≥8 submissions) | An enumerator not moving between households |
| Non-completion rate | Cohort median | Refusals being manufactured to skip work |

### Three design decisions

**Robust statistics, not fixed thresholds.** "Flag anything under 10 minutes" is
wrong on day one of a different survey, and wrong in an LGA with small
households. Each indicator is a modified z-score against the *cohort's own*
median using median absolute deviation. MAD rather than standard deviation
specifically because a fabricator's extreme values inflate the SD and help hide
them inside their own outlier; the median and MAD are unmoved by contamination
up to half the sample.

**Conjunction, not any-single-signal.** Short interviews alone are weak - a
household of two with no eligible children is legitimately quick. Low card
sighting alone is weak - some settlements genuinely have few cards. The
described pattern is *both, at high volume, from one person*. Requiring signals
to co-occur is what keeps the list short enough that supervisors actually work
it. A flag list nobody reads is worse than no flag list, because it looks like
control.

**A volume gate.** Below 8 submissions there is no stable median, so those
enumerators are reported as **"insufficient data"** and never as clean. The
distinction matters: silence about someone is not evidence about them.

### Demonstrated result

Nineteen enumerators behaving normally, one planted with the described pattern:

```
ENU020   3 indicator(s)   ESCALATE TODAY
   * interviews far shorter than the cohort
     median 4.1 min (cohort 22.3), z=-11.4
   * vaccination cards sighted far less often
     4% of children (cohort 64%), z=-5.7
   * submission volume far above the cohort
     11.0/day (cohort 6.8), z=3.8
```

**Flagged end of day 2 on 22 submissions.** Zero false positives among the
other nineteen. Against the round described in the operating conditions, that is
22 households at risk instead of 94, with twelve days left to act.

## What the report says, and deliberately does not say

Every escalation carries the same action:

> Supervisor accompanies this enumerator tomorrow and re-interviews three
> households already submitted. **Do not confront on the basis of this report
> alone - it is evidence for a visit, not a finding.**

That wording is deliberate. These indicators identify an enumerator whose data
*looks* different, which has innocent explanations: a dense urban ward with
small households, an area where cards genuinely are rare, a fast and experienced
worker. The check produces a **priority order for supervision**, and the finding
is made by a person who went and looked.

The same discipline applies as in the campaign-tracking analysis: where the data
can decide, it decides; where it cannot, the uncertainty is named and routed to
someone who can resolve it.

## What this does not catch

- **A careful fabricator.** Someone who idles the form for twenty minutes,
  varies durations, and occasionally records a card will not cross these
  thresholds. The check raises the effort required; it does not make fabrication
  impossible.
- **Whole-team collusion.** Every indicator is relative to the cohort. If a
  whole team fabricates together, they become the cohort. Cross-LGA comparison
  partly mitigates this and is not implemented - noted as a limitation rather
  than claimed.
- **Fabrication that produces plausible data.** Nothing here inspects whether
  the answers are true, only whether the process that produced them looks like
  interviewing.
- **Anything, if nobody runs it.** This is a script, not a control. The control
  is a named person opening it each evening. That belongs in the supervision
  plan, not in the code.



```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```



# Data protection (F12)

The question asks for a view, not compliance. Mine is that **this instrument
collects more identifying information than its analysis needs, and the digital
version I have built makes two of those exposures worse than the paper form
did** - which is worth stating before anything else, because both are mine.

## What the submission actually contains

A completed form holds, for one dwelling: GPS to six decimal places taken at the
entrance, the structure number painted on it, the settlement, the household
serial, the initials and ages of every resident, the name or initials of each
child under five, their weight, height, vaccination and antibiotic history, a
photograph of medicine packaging, a biological specimen identifier, and - where
the household was visited before - the identifier linking it to the October 2025
round.

That is not "survey data with some identifiers in it". **It is a re-identifiable
record of a specific dwelling and the children living in it**, linkable across
rounds. Six decimal places of latitude is roughly 0.1 m: it does not describe a
settlement, it describes a doorway.

## What is configured

| Control | Setting | Note |
|---|---|---|
| **Submission encryption** | `public_key` in `settings` | Encrypts at rest on the device and in transit. Automatic loss of marks if absent, and rightly so |
| PIN entry | `appearance: masked` | Shoulder-surfing at a doorstep is a real threat model |
| Photograph size | `max-pixels=1024` | Enough to read a medicine box; not enough to identify a room or a face in the background |
| Roster names | hint says **initials only**, in both languages | The paper column says "Name or initials"; the digital form pushes toward the minimising option |
| Audit log | `identify-user=true` | Accountability, and itself personal data about staff - retention applies to it too |
| Supervisor field | filtered to roster supervisors | Prevents an arbitrary code being typed |

**Encryption is live, not stubbed.** The `public_key` in `settings` is a **real
2048-bit RSA public key**, generated for this submission, so a form deployed from
this repository encrypts submissions as built. A placeholder would have left the
mechanism documented and disabled, which is the failure the automatic-loss rule
exists to catch.

**The matching private key is deliberately not in this repository.** It is held
outside the working tree and gitignored. That is the correct arrangement - a
private key in a public repository would make the encryption decorative - and it
carries the real consequence that submissions encrypted to this key can only be
decrypted by the holder of that file. A deployment substitutes the survey
manager's own keypair, generated by them and never transmitted.

## Two exposures this digital design creates that paper did not

Both come from external media, and neither is hypothetical.

### 1. `staff_roster.csv` puts all 120 PINs on all 120 devices

The PIN check I added at sign-in reads from `staff_roster.csv`, which is
attached to the form as media - so **every device carries every enumerator's
PIN in cleartext**, readable by anyone who opens the file.

That does not merely weaken the control, it **inverts** it. The PIN exists to
stop one enumerator submitting under another's code, and shipping the list makes
impersonation easier than it was on paper, where you would at least have to know
the person.

**Proposal.** Remove `pin` from the attached media entirely and authenticate
elsewhere:

- **Preferred:** ODK Central per-user accounts with device provisioning via QR.
  Identity is then a server-side credential, never a form attachment.
- **If an in-form check is required:** ship a per-team media file containing only
  that team's five enumerators, so exposure is bounded at five rather than 120;
  or store a salted hash rather than the PIN, accepting that XForms cannot hash,
  so this needs a pre-computed comparison the form only checks equality against.

Until then the PIN should be treated as a **usability aid, not a security
control**, and the constraint register describes it as such.

### 2. `previous_round_households.csv` ships a 3,982-household PII database to every tablet

To support 1.13 - recording the identifier from the October 2025 round - the
form attaches the previous round's household register: **3,982 households with
initials, structure numbers, settlement, and GPS coordinates**, on all 120
devices, for 14 days, including 9 consecutive days offline with no ability to
revoke.

A lost or stolen tablet exposes the previous round's entire sample, not the
handful of households that enumerator visited.

**Proposal.** Filter the attachment per team at deployment. An enumerator
assigned to Gwarin needs Gwarin's households, not Katsuma's. `prepare_media.py`
already builds these files from source, so partitioning is a change to that
script, not a change to the form. Estimated exposure reduction: from 3,982
households to roughly 300-400 per device.

**I have not implemented the partition**, because it changes the deployment
model - one media set becomes twenty-four - and that decision belongs to the
survey manager. It is listed in the deliberate-scope note rather than left
unsaid.

## What the questionnaire collects that it arguably need not

| Item | Why it is questionable | Proposal |
|---|---|---|
| **4.02 child name or initials** | Wholly redundant. 4.01 already records the roster line, which identifies the child within the household unambiguously. The name is copied from the roster and then never used analytically | **Remove.** The strongest single minimisation available, and it costs nothing |
| **Roster column (2) names** | Needed to conduct the interview - you must be able to ask about a specific person - but not needed *after* it | **Retain in the field, strip at ingest.** Names serve the interview; the analytical extract should carry line numbers only |
| **GPS at six decimal places** | ~0.1 m. Justified operationally for revisit and for the QA checks in F11. Not justified for analysis, which works at settlement level | **Retain raw during fieldwork, truncate to three decimals (~100 m) in the analytical release.** Preserves settlement-level analysis, removes doorway-level precision |
| **Structure number + GPS + previous-round ID together** | Individually defensible; together they make the record trivially re-identifiable, and the previous-round link makes it longitudinal | **Retain, but treat the joined dataset as restricted.** Access to the linkage key should be separable from access to the survey data |
| **`consent_to_follow_up` in the previous-round file** | Present in the attachment but never checked by the form. A household that declined follow-up can still be selected | **Wire it into 1.13's choice filter** so declining follow-up actually prevents it. Not implemented - flagged in the deliberate-scope note. That a consent flag exists and is ignored is a governance defect, not a technical one |

## What I would put to the ethics committee

Three things, in this order:

1. **Drop 4.02.** Redundant identifying data on an approved instrument, removable
   with no analytical loss.
2. **Fix the consent-to-follow-up gap.** A recorded refusal that nothing enforces
   is worse than no field at all, because it implies a control that is absent.
3. **Set a retention rule for the linkage key.** The instrument creates a
   longitudinal identifier across rounds and the questionnaire says nothing about
   how long that linkage is kept. The confidentiality box governs custody of
   paper forms; it is silent on a database that can be copied perfectly.

## What the confidentiality statement covers, and does not

The form's box (BSHREC/2026/041) commits to: purpose limitation, no disclosure
outside the survey team, and forms remaining in the supervisor's custody.

Written for paper, all three are physical controls. **Custody does not transfer
to a digital instrument**: a submission can be copied without leaving the
original's custody at all. Encryption, per-user accounts and server-side access
control are the digital equivalents, and none of them is mentioned because the
statement predates the medium.

That is not a criticism of the committee. It is the same observation that runs
through this whole question: **paper controls do not port, and assuming they do
is how a digitisation quietly loses the protections the paper process had.**



```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```



# Deployment and version control (F10)

**120 enumerators, 24 teams, 4 LGAs, 14 days, offline for up to 9 consecutive
days.** The operating conditions also state that a mid-round change to the
instrument is likely, because it has happened in every previous round.

So this plan assumes a mid-round change rather than hoping to avoid one.

## The versioning scheme

| Element | Value | Rule |
|---|---|---|
| `form_id` | `bansara_hh_2026` | **Never changes.** Changing it creates a *different form* on Central, and submissions against the old id become an orphaned dataset |
| `version` | `2026063001` - `yyyymmddnn` | Increments on every publish, including a one-character label fix |
| `form_version` | a calculate holding the same string | Stamped into the **data**, not only the metadata |

The last row matters more than it looks. Central records the version against each
submission, but metadata is the first thing lost when someone reshapes an export
in Excel - and a mixed-version round is precisely when that happens. A field in
the record itself survives the reshaping.

## What may and may not change mid-round

This is the part that determines whether a change is safe, and it is not
negotiable by urgency.

### Safe

- **Adding a field.** Records from earlier versions have it null, which the
  codebook explains as "not collected under version *n*". No existing value moves.
- **Loosening a constraint.** Data already collected remains valid.
- **Fixing a label, hint or translation.** No stored value changes.
- **Correcting a relevance rule** so a question appears where it should have.
- **Replacing a media file** - for example the real medicine list arriving. New
  attachment, new version, no form logic change.

### Unsafe - do not do mid-round

- **Renaming a field.** Central treats it as delete-plus-add. The old column
  stops and a new one starts, and the analysis team must union two columns that
  mean the same thing. If a name is wrong, live with it until the next round.
- **Changing a choice *value*.** Every record collected under the old value now
  means something different. This is the failure that recodes a variable
  silently. Change the *label* freely; never the value.
- **Tightening a constraint.** Records already saved under the looser rule cannot
  be revalidated, and drafts on devices may become unfinishable - the enumerator
  cannot advance and cannot save.
- **Removing a field**, or making an optional field required.

**The rule in one line:** *add and loosen freely; never rename, never re-value,
never tighten.*

## Pushing a change to devices that are offline

The nine-day window means a change does not arrive when it is published. It
arrives when each device next syncs, which is staggered and partly outside
anyone's control.

### Sequence

1. **Publish as a draft on Central and test it** against the test plan on two
   devices before it reaches anyone else. A mid-round change is the highest-risk
   moment in a round; it deserves the same testing as the original.
2. **Publish the new version.** Central serves it to any device that syncs.
3. **Tell people out of band.** Devices are offline; phones usually are not. A
   phone tree through the 24 team supervisors reaches 120 people faster than a
   sync does, and tells them *why* the update matters.
4. **Do not force an update.** ODK Collect finalises a form under the version it
   was **started** with. Forcing a refresh mid-interview is how a partially
   completed submission is lost.
5. **Accept a mixed-version round.** For a period - potentially the full nine
   days - some records are version *n* and some *n+1*. That is not a failure
   state to be prevented; it is the normal consequence of offline work, and the
   design has to make it analysable rather than avoid it.

### What protects data already collected

- **Finalised submissions are immutable on the device** and queue for upload.
  A form update does not touch them.
- **Drafts in progress stay on their original version.** This is the reason not
  to tighten constraints: a draft cannot be revalidated against a rule that did
  not exist when it was started.
- **Encryption is per-submission**, so a version change does not affect
  decryptability of anything already saved.
- **Media replacement is versioned with the form**, so a device that has not
  synced continues to use the media it has. It does not get the new medicine list
  and the old form logic, or vice versa.

## How the analysis team distinguishes versions

Three mechanisms, deliberately redundant, because the first two can be lost in
handling:

1. **`form_version` in every record.** Survives any export, reshape or merge.
2. **Central's submission metadata**, which records the version served.
3. **A published change log** - `docs/version_history.md`, one entry per publish:
   version, date, what changed, which fields affected, and what the analysis team
   must do about it.

The third is the one that actually matters. Knowing a record is version
`2026063002` is useless without knowing what changed in `002`.

### The change log entry format

```
## 2026063002 - 8 June 2026
Changed:  q4_13_medicine - placeholder list replaced with the ministry codelist
Affects:  child.q4_13_medicine
Analysis: records with form_version = 2026063001 carry WHO ATC codes;
          records from 2026063002 carry ministry two-digit codes.
          Crosswalk in codebook.md. DO NOT concatenate without mapping.
```

## Device provisioning

- **Central project QR code** configures server, project and credentials in one
  scan. No enumerator types a URL.
- **Per-user accounts, not a shared one.** A shared login makes `device_id` the
  only identity in the data, which defeats the fabrication checks.
- **Media pre-loaded before deployment.** 389 KB across seven files - trivial on
  arrival, painful over a rural connection on day one.
- **Storage headroom checked**: photographs at `max-pixels=1024` are roughly
  150 KB each; a 2 GB device with the OS and Collect installed has room for a
  full round, but not if the device is also used for anything else.

## What this plan does not solve

- **A device lost or broken before syncing** loses every unsynced submission.
  Nothing in the form prevents it. The mitigation is procedural: supervisors
  collect and sync at every opportunity, not only at the end of the offline
  window.
- **A change that genuinely requires a rename or re-value** cannot be done safely
  mid-round. The honest answer is to carry the defect to the end of the round and
  fix it in the next version, documenting the defect in the meantime.
- **Ethics re-approval** for anything altering what is asked. That is a
  timeline, not a technical step, and it is why the escalated defects in
  `defect_report.md` are escalated rather than fixed.



```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```



# Form version history

One entry per publish. The analysis team reads this alongside `form_version` in
the data; knowing a record is version `2026063002` is useless without knowing
what changed in `002`.

Format is fixed so it can be parsed later if it ever needs to be.

## 2026063001 - 30 June 2026 - initial release

    Changed:  initial publication of Form HH/2026/v1 as a digital instrument
    Affects:  all fields
    Analysis: baseline version. Value crosswalk to the paper instrument is in
              codebook.md - two choice lists (6.01, 6.02) are re-based to avoid
              collisions with non-response sentinels. Concatenating a paper
              round with this one without that mapping produces nonsense.
    Known:    q4_13_medicine uses a PLACEHOLDER codelist (WHO ATC codes). The
              ministry codelist was not supplied. Records under this version
              carry ATC values and must not be pooled with any later version
              using ministry codes without an explicit crosswalk.



```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```



# Codebook - `bansara_hh_2026` version `2026063001`

**Generated** from the form definition by `build_codebook.py`. Not
maintained by hand, so it cannot drift from the instrument.

## The three analysable tables

The form has two repeats, which flatten into three tables. ODK Central
exports them as separate CSVs; the join keys below are what makes them one
dataset.

```
household  ── one row per submission (one dwelling visited)
   │
   ├── roster  ── one row per usual resident
   │
   └── child   ── one row per eligible child (9-59 months)
                  Section 5 specimen fields live here too: the specimen
                  section sits INSIDE the child repeat, so there is no
                  separate specimen table.
```

### Primary and foreign keys

| Table | Primary key | Foreign key | Notes |
|---|---|---|---|
| `household` | `meta/instanceID` | - | ODK's submission UUID. Stable, globally unique, and the only key that survives a resubmission |
| `roster` | (`PARENT_KEY`, `line_no`) | `PARENT_KEY` → `instanceID` | `line_no` is `position(..)`, so it matches the paper roster line |
| `child` | (`PARENT_KEY`, `child_index`) | `PARENT_KEY` → `instanceID` | `q4_01_line` joins a child back to its `roster` row |

**A natural key also exists** and should be used for deduplication against
paper rounds, not for joins:
`(q1_04_settlement, q1_06_structure, q1_07_hh_serial, q1_10_visit_date)`.
It is not guaranteed unique - two teams could in principle number the same
dwelling - which is exactly why `instanceID` is the primary key.

**`specimen_label_full`** (`BSN######-C`) is the join key to the laboratory
system. It is unique per child where a specimen was obtained, and null
otherwise.

## Reading a null

A null in this dataset is never ambiguous, which is the main gain over the
paper round. Every field below lists the **relevance rule** that governs
when it is asked. If a field is null, either its relevance rule was false
- in which case the question was never put to the respondent - or a
measurement status field says explicitly why no value exists.

**No sentinel value is ever stored in a numeric field.** See
`coding_scheme.md`.

## Table: `household` - one row per submission

43 fields.

| Field | Type | Question / meaning | Null when |
|---|---|---|---|
| `start_time` | start | - | `never (always collected)` |
| `end_time` | end | - | `never (always collected)` |
| `today_date` | today | - | `never (always collected)` |
| `form_version` | calculate | derived: `'2026063001'` | `never (always collected)` |
| `device_id` | deviceid | - | `never (always collected)` |
| `audit` | audit | - | `never (always collected)` |
| `enumerator_code` | select_one_from_file | Enumerator code (1.08) | `never (always collected)` |
| `enum_team` | calculate | derived: `instance('staff_roster')/root/item[name=${enumerator_cod` | `never (always collected)` |
| `enum_role` | calculate | derived: `instance('staff_roster')/root/item[name=${enumerator_cod` | `never (always collected)` |
| `enum_lga` | calculate | derived: `instance('staff_roster')/root/item[name=${enumerator_cod` | `never (always collected)` |
| `enum_pin` | calculate | derived: `instance('staff_roster')/root/item[name=${enumerator_cod` | `never (always collected)` |
| `pin_entered` | text | Enter your 4-digit PIN | `never (always collected)` |
| `q0_label_range` | select_one_from_file | Confirm the specimen label book issued to your team | `never (always collected)` |
| `q1_01_state` | calculate | derived: `'BAN'` | `never (always collected)` |
| `q1_02_lga` | select_one_from_file | 1.02 Local Government Area | `never (always collected)` |
| `q1_03_ward` | select_one_from_file | 1.03 Ward | `never (always collected)` |
| `q1_04_settlement` | select_one_from_file | 1.04 Settlement | `never (always collected)` |
| `q1_05_alt_name_yn` | select_one | 1.05 Is the settlement known locally by a different name? | `never (always collected)` |
| `q1_05_alt_name` | text | 1.05 Local name | `${q1_05_alt_name_yn} = '1'` |
| `q1_06_structure` | integer | 1.06 Structure number painted on the dwelling | `never (always collected)` |
| `q1_07_hh_serial` | integer | 1.07 Household serial number within the settlement | `never (always collected)` |
| `q1_10_visit_date` | date | 1.10 Date of visit | `never (always collected)` |
| `q1_11_gps` | geopoint | 1.11 GPS reading at the entrance to the dwelling | `never (always collected)` |
| `q1_12_prev_round` | select_one | 1.12 Was this household visited during the October 2025 round? | `never (always collected)` |
| `q1_13_prev_id` | select_one_from_file | 1.13 Household identifier allocated in the October 2025 round | `${q1_12_prev_round} = '1'` |
| `q1_14_result` | select_one | 1.14 Result of visit | `never (always collected)` |
| `q2_01_statement_read` | select_one | 2.01 Consent statement read aloud to the respondent in full? | `never (always collected)` |
| `q2_02_consent` | select_one | 2.02 Does the respondent consent to the household interview? | `never (always collected)` |
| `q2_03_relationship` | select_one | 2.03 Relationship of the respondent to the head of household | `${q2_02_consent} = '1'` |
| `q3_01_hh_size` | integer | 3.01 How many people usually live in this household? | `never (always collected)` |
| `roster_count` | calculate | derived: `count(${roster})` | `never (always collected)` |
| `q3_02_eligible` | calculate | derived: `sum(${r_eligible})` | `never (always collected)` |
| `q6_01_water` | select_one | 6.01 What is the main source of drinking water for this household? | `never (always collected)` |
| `q6_02_toilet` | select_one | 6.02 What kind of toilet facility do members of this household use? | `never (always collected)` |
| `q6_03_livestock` | select_one | 6.03 Does this household keep poultry or livestock inside the compound? | `never (always collected)` |
| `q6_04_animal_antibiotic` | select_one | 6.04 Have any antibiotic medicines been given to these animals in the past 1 | `${q6_03_livestock} = '1'` |
| `q6_05_handwashing` | select_one | 6.05 Observe: is there a handwashing station with both soap and water? | `never (always collected)` |
| `q6_06_hh_diarrhoea` | select_one | 6.06 Has any member of this household had diarrhoea in the past two weeks? | `never (always collected)` |
| `q6_07_assets` | select_multiple | 6.07 Which of the following does this household own? | `never (always collected)` |
| `interview_duration_min` | calculate | derived: `round((decimal-date-time(${end_time}) - decimal-date-tim` | `never (always collected)` |
| `q7_02_observation` | text | 7.02 Record any observation that may help the office interpret this form | `never (always collected)` |
| `q7_04_supervisor` | select_one_from_file | 7.04 Supervisor code | `never (always collected)` |
| `q7_05_supervisor_decision` | select_one | 7.05 Supervisor decision on this form | `${q7_04_supervisor} != ''` |

## Table: `roster` - one row per usual resident

8 fields.

| Field | Type | Question / meaning | Null when |
|---|---|---|---|
| `line_no` | calculate | derived: `position(..)` | `never (always collected)` |
| `r_initials` | text | (2) Initials | `never (always collected)` |
| `r_relationship` | select_one | (3) Relationship to head | `never (always collected)` |
| `r_sex` | select_one | (4) Sex | `never (always collected)` |
| `r_age_unit` | select_one | Age recorded in years or months? | `never (always collected)` |
| `r_age_years` | integer | (5) Age in completed years | `${r_age_unit} = 'years'` |
| `r_age_months` | integer | (6) Age in completed months | `${r_age_unit} = 'months'` |
| `r_eligible` | calculate | derived: `if(${r_age_unit} = 'months' and ${r_age_months} >= 9 and` | `never (always collected)` |

## Table: `child` - one row per eligible child, including specimen

32 fields.

| Field | Type | Question / meaning | Null when |
|---|---|---|---|
| `child_index` | calculate | derived: `position(..)` | `never (always collected)` |
| `q4_01_line` | integer | 4.01 Line number of this child in the Section 3 roster | `never (always collected)` |
| `q4_02_initials` | calculate | derived: `indexed-repeat(${r_initials}, ${roster}, ${q4_01_line})` | `never (always collected)` |
| `q4_03_age_months` | calculate | derived: `indexed-repeat(${r_age_months}, ${roster}, ${q4_01_line}` | `never (always collected)` |
| `q4_04_sex` | select_one | 4.04 Sex of the child | `never (always collected)` |
| `q4_05_weight_status` | select_one | 4.05 Was the child weighed? | `never (always collected)` |
| `q4_05_weight_kg` | decimal | 4.05 Weight in kg | `${q4_05_weight_status} = 'measured'` |
| `q4_06_height_status` | select_one | 4.06 Was the child measured? | `never (always collected)` |
| `q4_06_height_cm` | decimal | 4.06 Length or height in cm | `${q4_06_height_status} = 'measured'` |
| `q4_07_position` | select_one | 4.07 Position in which the child was measured | `${q4_06_height_status} = 'measured'` |
| `q4_08_card` | select_one | 4.08 May I see the child's vaccination card or health record? | `never (always collected)` |
| `q4_08a_doc_type` | select_one | 4.08a Which document was seen? (addition - not on the paper form) | `${q4_08_card} = '1'` |
| `q4_09_measles_card` | select_one | 4.09 Copy from the card: is a measles dose recorded? | `${q4_08_card} = '1'` |
| `q4_10_measles_recall` | select_one | 4.10 Has this child ever received a measles vaccination? | `${q4_08_card} = '2'` |
| `q4_11_diarrhoea` | select_one | 4.11 Has this child had diarrhoea in the past 14 days? | `never (always collected)` |
| `q4_12_antibiotic` | select_one | 4.12 Has this child taken any antibiotic medicine in the past 30 days? | `never (always collected)` |
| `q4_12a_more_than_one` | select_one | 4.12a Was more than one antibiotic taken? (addition - see defect C1) | `${q4_12_antibiotic} = '1'` |
| `q4_13_medicine` | select_one_from_file | 4.13 Which antibiotic was taken? | `${q4_12_antibiotic} = '1'` |
| `q4_14_medicine_other` | text | 4.14 Write the name of the medicine as reported | `${q4_13_medicine} = 'OTHER96'` |
| `q4_15_no_prescription` | select_one | 4.15 Was the medicine obtained without a prescription from a health worker? | `${q4_12_antibiotic} = '1'` |
| `q4_16_photo_status` | select_one | 4.16 Was a photograph of the medicine packaging taken? | `${q4_12_antibiotic} = '1'` |
| `q4_16_photo` | image | 4.16 Photograph of the medicine packaging | `${q4_16_photo_status} = '1'` |
| `q5_01_specimen_eligible` | calculate | derived: `if(${q4_03_age_months} >= 12, 1, 0)` | `never (always collected)` |
| `q5_02_specimen_obtained` | select_one | 5.02 Was a stool specimen obtained from this child? | `${q5_01_specimen_eligible} = 1` |
| `q5_03_label_serial` | text | 5.03 Specimen label serial (6 digits, after BSN) | `${q5_02_specimen_obtained} = '1'` |
| `check_digit_expected` | calculate | derived: `if((7 * number(substr(${q5_03_label_serial},0,1)) + 6 * ` | `never (always collected)` |
| `q5_03_check_digit` | text | 5.03 Check character (after the hyphen) | `${q5_02_specimen_obtained} = '1'` |
| `specimen_label_full` | calculate | derived: `concat('BSN', ${q5_03_label_serial}, '-', translate(${q5` | `never (always collected)` |
| `q5_04_coldbox_time` | time | 5.04 Time the specimen was placed in the cold box | `${q5_02_specimen_obtained} = '1'` |
| `q5_05_coldbox_temp` | decimal | 5.05 Temperature shown on the cold box thermometer | `${q5_02_specimen_obtained} = '1'` |
| `q5_06_reason` | select_one | 5.06 Reason no specimen was obtained | `${q5_02_specimen_obtained} = '2'` |
| `q5_07_reason_other` | text | 5.07 Specify | `${q5_06_reason} = '96'` |

## Value labels

**`age_unit`** - `years` Years · `months` Months (under 5 years)

**`assets`** - `A` Radio · `B` Television · `C` Mobile telephone · `D` Bicycle · `E` Motorcycle · `F` Car or truck · `G` Refrigerator · `H` None of these

**`card_seen`** - `1` Card seen · `2` No card seen

**`consent`** - `1` Consent given · `2` Consent refused

**`document_type`** - `card` Vaccination card · `copy` Card copy · `electronic` Electronic record

**`handwashing`** - `1` Observed, soap and water · `2` Reported only, not observed · `3` Not present

**`measure_position`** - `1` Recumbent length · `2` Standing height

**`measured`** - `measured` Measured · `not_measured` Not measured

**`no_specimen_reason`** - `1` Caregiver refused · `2` Child absent · `3` Unable to produce · `4` Container spoiled · `96` Other

**`photo_taken`** - `1` Yes · `2` No, not available · `3` Caregiver declined

**`relationship`** - `1` Head · `2` Spouse · `3` Son or daughter · `4` Parent · `5` Other relative · `6` Not related

**`result_of_visit`** - `1` Completed · `2` Refused · `3` No competent adult after three visits · `4` Dwelling vacant or demolished

**`sex`** - `1` Male · `2` Female

**`supervisor_decision`** - `1` Accept · `2` Return for correction · `3` Void

**`toilet`** - `t01` Flush to sewer · `t02` Flush to septic tank · `t03` Flush to pit latrine · `t04` Ventilated improved pit · `t05` Pit latrine with slab · `t06` Pit latrine without slab · `t07` Composting toilet · `t08` Bucket · `t09` No facility or bush

**`water_source`** - `w01` Piped into dwelling · `w02` Piped into compound · `w03` Public tap or standpipe · `w04` Tube well or borehole · `w05` Protected dug well · `w06` Unprotected dug well · `w07` Protected spring · `w08` Unprotected spring · `w09` Rainwater · `w10` Tanker or cart · `w11` Surface water

**`yes_no`** - `1` Yes · `2` No

**`yes_no_dk`** - `1` Yes · `2` No · `8` Do not know

## Paper-to-digital crosswalk

Two lists were re-based so that no stored value can collide with a
non-response sentinel (see `coding_scheme.md`). **The categories and the
numbers read aloud to the respondent are unchanged** - only the stored
value differs. Concatenating a paper round with a digital round without
this mapping will produce nonsense.

### 6.01 water source

| Paper code | Digital value | Category |
|---|---|---|
| `1` | `w01` | Piped into dwelling |
| `2` | `w02` | Piped into compound |
| `3` | `w03` | Public tap or standpipe |
| `4` | `w04` | Tube well or borehole |
| `5` | `w05` | Protected dug well |
| `6` | `w06` | Unprotected dug well |
| `7` | `w07` | Protected spring |
| `8` | `w08` | Unprotected spring  <- paper 8 also meant 'does not know' |
| `9` | `w09` | Rainwater  <- paper 9 also meant 'no answer' |
| `10` | `w10` | Tanker or cart |
| `11` | `w11` | Surface water |

### 6.02 toilet facility

| Paper code | Digital value | Category |
|---|---|---|
| `1` | `t01` | Flush to sewer |
| `2` | `t02` | Flush to septic tank |
| `3` | `t03` | Flush to pit latrine |
| `4` | `t04` | Ventilated improved pit |
| `5` | `t05` | Pit latrine with slab |
| `6` | `t06` | Pit latrine without slab |
| `7` | `t07` | Composting toilet |
| `8` | `t08` | Bucket  <- paper 8 also meant 'does not know' |
| `9` | `t09` | No facility or bush  <- paper 9 also meant 'no answer' |

## Fields added that are not on the paper form

| Field | Why it exists |
|---|---|
| `start_time`, `end_time`, `interview_duration_min` | Fabrication detection - see `fabrication_detection.md` |
| `device_id`, `audit` | as above |
| `enumerator_code`, `pin_entered` | Binds a submission to a person. 1.08 on paper is a code anyone can write |
| `q0_label_range` | Confirms the team's specimen label book |
| `q4_08a_doc_type` | 4.08 asks for a three-way distinction its coding cannot hold (defect A2) |
| `q4_12a_more_than_one` | Lets analysis know when 4.13's single code is incomplete (defect C1) |
| `form_version` | Stamped into the data so mixed-version rounds are separable - see `deployment_plan.md` |

## Paper questions satisfied by a differently-named field

Every question on the paper form is accounted for. These four are captured
under a different name, because the digital form can derive or capture them
more reliably than an enumerator can type them.

| Paper | Digital field | How |
|---|---|---|
| **1.08** Enumerator code | `enumerator_code` | Selected from the staff roster at sign-in and confirmed by PIN, rather than written. On paper, 1.08 is a code anyone can enter |
| **1.09** Team code | `enum_team` | **Derived** from the roster once the enumerator signs in. Cannot be mistyped, and cannot disagree with 1.08 |
| **7.01** Time the interview ended | `end_time`, and `interview_duration_min` | Captured automatically by the device. More reliable than a written time, and it is what makes the daily fabrication check possible (see `fabrication_detection.md`) |
| **4.02** Child name or initials | `q4_02_initials` | **Copied from the roster by calculation**, exactly as the paper form instructs, rather than re-typed. Recommended for removal on data-protection grounds |

## Fields on the paper form that are NOT collected

| Paper field | Why |
|---|---|
| 1.01 State | Single-valued. Stored as a constant, not asked |
| Roster column (7) *Eligible for Section 4* | Office-use column the enumerator was told to leave blank, then asked to read (defect A1). Eligibility is derived from roster ages |
| Roster column (8) *Section 4 page number* | Replaced by the repeat index |
| 5.01 specimen eligibility | Calculated from age, not asked (defect A3) |
| 7.03, 7.06 signatures | Replaced by authenticated submission and the supervisor review fields |
| 8.01-8.03 office use | Data entry and second-entry verification do not exist in a digital pipeline. This is the largest single saving: an entire double-entry step removed |



```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```



# What I deliberately did not implement, and why (F14)

The question says *"a defensible scope scores better than an exhaustive one."*
This is that scope. Each item was reachable and was left out for a stated
reason, and every one is cross-referenced to where it is discussed.

## Left out because the input does not exist

### The real medicine codelist
4.13 says *"record from the medicine list"* and the pack README claims one is
supplied. It is not - verified by searching every file in the pack, and inside
the `.docx` for embedded objects. A clearly-marked WHO ATC placeholder is
implemented instead, so the mechanism is demonstrable and the real list drops in
by replacing one CSV.

**Why not invent two-digit codes:** the paper form expects them, so invented
codes would be indistinguishable from real ones and would silently recode the
AMR variable. ATC codes cannot be mistaken for a two-digit local code, which
makes any placeholder data self-identifying. → `defect_report.md` E1

### A real encryption keypair
`public_key` in settings is a labelled placeholder. Submissions encrypted to it
cannot be decrypted, so the real key is a deployment gate rather than a form
change. The round-trip is untestable until the keypair is issued.
→ `data_protection.md`

## Left out because the decision is not mine

### Per-team partitioning of the media files
`previous_round_households.csv` ships **3,982 households with initials, structure
numbers and GPS to all 120 devices**, and `staff_roster.csv` ships **all 120
PINs to all 120 devices**. Both should be partitioned per team - exposure drops
from 3,982 households to roughly 300-400, and from 120 PINs to five.

`prepare_media.py` already builds these files, so partitioning is a change to
that script rather than to the form. **Not implemented because it turns one
media set into twenty-four**, which changes the deployment model, the
provisioning QR codes and the update procedure. That is the survey manager's
call, not a technical detail I should decide unilaterally. → `data_protection.md`

### Removing 4.02, the child's name
Recommended for removal: 4.01 already identifies the child by roster line, and
the name is never used analytically. **Not removed**, because dropping a field
from an ethics-approved instrument changes what is collected and requires
committee approval. Escalated with a recommendation rather than done.

### Wiring `consent_to_follow_up` into 1.13
The previous-round file carries a follow-up consent flag that nothing checks, so
a household that declined can still be selected. Implementing the filter is two
lines. **Not implemented** because a household refusing follow-up and then being
visited anyway is a governance question - someone must decide whether the flag is
authoritative - and silently enforcing it could suppress legitimate revisits
that were consented verbally. Escalated as the second of three items for the
ethics committee.

## Left out because it is impossible in the medium

### Cross-submission duplicate label detection
A self-contained form cannot check a label against every earlier submission,
because it has no writable store outliving the instance. Three layers are
implemented - allocation range, within-submission uniqueness, and the
`last-saved` instance - and the write-up states plainly which errors still get
through. ODK Entities would solve it for a connected deployment and is **wrong
here**, because entity updates propagate on sync and these devices are offline up
to nine days. → `label_reuse.md`

### Hashing the PIN
XForms has no hash function, so an in-form PIN check must compare against a
value shipped in the media. The fix is architectural - Central per-user accounts
- not a form change. → `data_protection.md`

## Left out because it needs a device or a person

### Executing the test plan
54 cases specified, **none executed against a running instance**, because no ODK
Central project was available in the window. The check-digit logic behind case
S09 *is* executed exhaustively in `tests/test_check_digit.py`. Everything else
is a specification. → `test_plan.md`

### Native-speaker review of the Hausa
Every label and constraint message is bilingual with Hausa as the default,
because an English-only message is a message that does not exist for the 38% of
enumerators who are not confident readers of English. **The strings are mine and
are indicative.** Whether an enumerator with six years of schooling understands
a given message is a cognitive-interview question, not a translation one, and
both need doing before deployment.

### Device testing under memory pressure
A 40-person roster with eight eligible children on a 2 GB tablet needs a real
device. The external-media design exists precisely to keep memory pressure low -
2,524 settlements queried from SQLite rather than parsed into RAM - but the claim
is reasoned, not measured. → `prepare_media.py`

## Left out on judgement

### A GPS geofence on 1.11
No constraint that the household falls inside the selected settlement. A
settlement centroid is not a household location, and a boundary rule would block
legitimate dwellings at the edge of a settlement - which are disproportionately
the poorest. Out-of-area points are better surfaced as a back-office flag than
blocked at a doorstep. → `consistency_checks.md`

### Blocking on clinically implausible measurements
Weight and height carry hard bounds that are typo guards, deliberately wider
than clinical plausibility, with WHO-based implausibility raised as a warning. A
clinical range enforced as a block would delete the severely malnourished
children the survey exists to count. → `constraint_register.md`

### Converting 4.13 to select-multiple
The single most valuable analytical fix available - an AMR survey that records
only the most recent antibiotic is discarding its central measurement. **Not
done**, because it changes what the variable means and requires re-approval. One
added yes/no lets analysis know when the code is incomplete, without altering
4.13 itself. → `defect_report.md` C1

## What I would do first with another day

1. Partition the media files per team. Largest risk reduction per hour of work.
2. Execute the test plan on a real device, since Central access resolves it.
3. Get the Hausa reviewed.

Everything else on this list is either blocked on someone else's decision or
correctly out of scope.



```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# PART 3 - Question 5


# Q5 - Coordinating delivery through the round

Day 3 of 7. Four things have arrived at once and only one is genuinely urgent.

## 1. The first twenty-four hours

Ordering principle: **contain, protect today's deliverable, then diagnose.**
Diagnosing first lets the corruption grow while I investigate it.

**0-15 min · Freeze writes to the settlement layer**, reads unaffected. Cheap and
reversible; every hour of open editing adds records I must later adjudicate.

**15-45 min · Tell the EOC before they ask** that the figure is under
verification, with a time for the answer. It is already being discussed
nationally, and arriving second to my own problem costs more than the error does.

**45 min-3 h · Test whether the duplicates and the discrepancy are one incident.**
Duplicated settlements change the denominator. If that is the cause I have one
problem and one fix, not two workstreams.

**3-8 h · Reconstruct the figure** from the last known-good state (§2), then
**issue today's product caveated, or hold it with a stated reason.** The EOC
deploys against this daily; silence is a decision to give them nothing.

**8-16 h ·** Root cause on the concurrency failure (§3), then handover triage -
credentials and access only (§5).

**Within 24 h · Confirm the counterpart's training dates.** Two minutes.
Deferring damages a contractual relationship to save nothing.

**What I deliberately do not do first.** Not **delete the duplicates**: they are
the evidence and probably the cause, and removing them before establishing which
edit was correct destroys the audit trail and leaves a corrected figure with no
explanation for why it moved. Not **publish a corrected figure**: a second wrong
number is far worse than the first, because the first is an error and the second
is a pattern. Not **argue the discrepancy on the merits** before checking my own
figure - that turns a technical disagreement into an institutional one. And not
the **handover documentation or the partner report**: both feel productive, both
have over a week of runway against four days of live round.

## 2. One authoritative coverage figure

**One named owner, one source, one computation, one publication time.** The
absence of that is why two figures exist.

Restore the layer to a point-in-time state from before the concurrent edits,
recompute my figure, then recompute *the state's* from the same base using their
method. **Same answer** means the difference is *method*, and the fix is a
written definition rather than a data repair. **Different answer** means it is
*data*, and the duplicates are the first suspect.

Root cause, cheapest first: **definitional** - same quantity? planned
settlements or those with a target, inaccessible in or out, cumulative or daily,
sync time or end of day (most field discrepancies are definitional, and this
costs one phone call); then **duplicates** - do they change the denominator by
the size of the gap; then **latency** - does the state hold submissions I have
not received; then **genuine divergence**, only if the first three are excluded.

**To national level, before I know** - *would claim:* the figures differ by X,
both are being recomputed from a common base, the likely causes are definitional
or a contained integrity issue, and I will have an answer by 14:00 tomorrow.
*Would not claim:* which figure is correct, that the state is wrong, a cause, or
a corrected number.

**Committing to a time is what buys the time.** "We are looking into it" invites
hourly escalation; a named hour converts an incident into a scheduled item.

## 3. Concurrent editing on the shared database

**PostgreSQL/PostGIS.** Five mechanisms; the first matters most because it
*prevents* the conflict rather than resolving it.

**1 · Edit scope enforced by the database.** Each analyst holds write rights to a
defined set of wards via **row-level security** on ward ownership, so two
analysts cannot edit overlapping areas at all. This is what actually failed here:
the incident is an *assignment* failure, which a concurrency mechanism would only
have detected, not avoided.

**2 · Identifiers.** **Client-generated UUID** primary keys, so two analysts
creating a settlement offline cannot collide, with identity separately protected
by a **`UNIQUE` constraint on the natural key** (settlement code within ward).
The UUID prevents accidental collision; the constraint prevents genuine
duplication. The current incident is the second kind - two rows, two ids, one
settlement.

**3 · Conflict detection by optimistic concurrency, not locking.** Every feature
carries a `version`; an update supplies the version it read and applies only if
it still matches. A stale write is **rejected and returned to its author**, never
silently applied. Locking is rejected because analysts are intermittently
connected, and a lock held from a disconnected session blocks a whole ward.

**4 · Staged merge.** Analysts write to a personal staging schema; a merge
applies only if the §4 validation passes, so nothing enters the authoritative
layer unvalidated - the property that would have stopped this incident reaching
the daily product.

**5 · Append-only audit by trigger.** Who, when, before, after, which merge
accepted it. **Records are superseded, never deleted** - which is what makes
*"which of these two edits was correct"* answerable, and why my first action was
a freeze rather than a cleanup.

## 4. Automated data quality rules

**Blocked** - rejected, because accepting produces data nobody can later
untangle: invalid geometry; a settlement outside its declared ward; a duplicate
natural key; referential integrity failure; coordinates outside the state
boundary; a version conflict.

**Flagged** - applied, recorded and queued, because the change may be correct: a
settlement moved more than 200 m; target population changed by more than 20%; a
first settlement created in a ward; an implausible route length for one team-day;
any edit outside working hours.

**The reasoning.** Block only where the data would be wrong irrecoverably.
Everything else flags, because **a block an analyst cannot satisfy honestly is a
block they will satisfy dishonestly** - refuse a settlement that genuinely moved
and it reappears under a new code, and the duplicate problem returns wearing a
different hat. **The bar is higher mid-round than between rounds:** a rule that
halts a state analyst on day 4 of 7 is an operational failure even when
technically correct.

## 5. Handover in ten days, round live

**Do not ask them to write documentation.** Written from memory under notice, it
records what they believe they do. Instead the **successor performs the task
while the departing analyst watches and corrects** - faster, and it produces a
procedure known to work because it has just been used. The handover is complete
when the successor completes the daily product **without asking a question** -
deliberately the same test as level 3 in the counterpart competency framework
(Q6).

**Days 1-2: credentials and access** - miss this and nothing else matters.
**Days 3-5: the daily EOC product**, successor running it shadowed while the
analyst corrects but does not touch the keyboard. **Days 6-8: reverse-shadow**,
successor unaided, every question asked marking a gap in the procedure that gets
written down. **Days 9-10:** the known-issues list - which settlements are
known-bad, which contacts answer, which manual steps exist and why.

**What I accept losing:** their counterpart relationships, their tacit sense of
which numbers in their state look wrong, and the rationale behind past decisions.
Ten days cannot transfer these, and pretending otherwise produces four thin
handovers instead of two solid ones. Better to lose the context knowingly than
the pipeline by accident.

## 6. Delegating without becoming the single point of failure

**Four problems, four named owners, four deadlines** - not "the team will look at
it". Coverage figure to a named central analyst; the integrity fix to the data
engineer who found it; handover to the two state supervisors; partner report to a
central analyst from day 5. **I keep two things only:** the sequencing decision
and communication to national level, neither delegable mid-incident.

**Supervision without reviewing every output.** Per-record checking is what §4's
rules are for, and a coordinator repeating them by eye is the bottleneck rather
than the control. So I review **exceptions, not passes**; peer review is paired
and rotating, so capacity scales with the team rather than with me; a 15-minute
daily stand-up covers only what is blocked, flagged or late; and a **named deputy
publishes the coverage figure** when I am unavailable.

**The test I hold myself to:** if I am uncontactable for 48 hours, does the daily
product still ship and the partner report still progress? If not, I have
distributed tasks while keeping the dependencies.

**And the connection to the other half of this scenario:** two resignations
threaten delivery only because knowledge lived in two people rather than in a
process - the same finding as the counterpart department's 1.5 out of 5 for
documenting a reproducible workflow. The handover method above and the standard
that department drafts on day 3 of its training are the same artefact, and
building it once, in the open, serves both.



```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# PART 3 - Question 6


# Q6 - Building capability in the counterpart agency

**Main response: 6 pages; Annexes A-E excluded**, per the question. The annexes
carry artefacts to be used - the session, the grid, the instrument, the datasets,
the session-by-session plan. The response carries the argument.

---

## 1. What the evidence says, before designing anything

Four findings, and three of them contradict the obvious course.

### 1.1 They know more than they can do

| | |
|---|---|
| Composite capability score | **36 / 100** |
| Objective knowledge test | **57%** across 12 items |

These do not agree, and the gap is the design brief. Recalling 57% while scoring
36 on applied capability is not a knowledge problem - **it is an application
problem.** That rules out the default response: more instruction closes a
knowledge gap, and this cohort has already met the material and cannot convert it
into work. The lever is supervised practice, which is why the course runs at
**70% hands-on** and every block ends in a product rather than a summary.

### 1.2 They cannot judge their own competence - so nothing self-reported can steer the design

A correlation of **0.11** between self-rating and tested knowledge is not weak.
It is *nothing*: knowing someone's self-assessment tells you essentially nothing
about their ability. Three consequences follow, and each removes a tool I would
normally use.

- **No streaming by self-assessment** - groups formed by confidence would be
  uncorrelated with ability. Streaming comes from the demonstrated
  pre-assessment (Annex C).
- **Stated demand is not a needs analysis.** Demand is *"near universal"*, from a
  cohort that cannot locate its own gaps: it says what is attractive, not what is
  missing, and treating it as a needs assessment produces a syllabus optimised
  for appeal.
- **Self-rated improvement is worthless as an outcome.** If self-rating is
  uninformative at baseline, a rise after training measures comfort. §5 therefore
  rests on demonstrated tasks and independent reproduction.

**It also dictates day one.** Twenty-one people will arrive believing they are
more capable than they are, and being told otherwise produces defensiveness by
mid-morning and disengagement by the afternoon. The gap must be **discovered, not
announced**: day 1 opens with a task at their stated level that they cannot
finish, followed immediately by the technique that makes it tractable. The
realisation is theirs and the recovery is immediate. Facilitator rule throughout:
**never name an individual's score, never compare two participants aloud.**

### 1.3 The binding constraint is software access - and the finding is stranger than it looks

**Zero of 21 have access to QGIS or ArcGIS.**

The important thing is that **QGIS is free**, and runs on any machine of the last
decade. This is not a budget finding. Zero access to a free tool means no
administrative rights to install; or machines too old or too few; or an IT policy
blocking installations; or no machines allocated to this work at all.

**These have entirely different remedies and nobody has established which
applies** - a single unanswered question that decides whether the constraint
lifts in two weeks or two quarters. Establishing it is action one of the 90-day
plan (§6), scheduled *before* the course.

It also settles the platform. I will not teach on software the department cannot
open on Monday; that produces a pleasant week and zero transfer. The course runs
on **QGIS Portable from USB - installs nothing, needs no administrative rights**
- and each participant keeps the stick. If the cause is rights or policy, the
constraint lifts on day one. If it is hardware, portable QGIS proves it
immediately and the escalation becomes a costed case with evidence behind it.

### 1.4 The weakest competency is also the highest-leverage one

**Documenting a reproducible cleaning workflow: 1.5 / 5** - the lowest measured
score.

Fortunate, because it is also the skill that determines whether anything else
survives: a department that cannot document a cleaning workflow cannot hand work
over, audit a number, or absorb a resignation - the same fragility as the
coordination scenario, in a different building (§7). So documentation is not a
module here. **It is the spine**, and every other block is assessed by whether
its output can be re-run by someone else.

### 1.5 The one thing they want, used rather than refused

Strongest stated demand is **map production and cartography** - not what they
most need, but refusing it would be a mistake: it is the visible end of this work
and where the department already feels ownership. **So it becomes the vehicle,
not the syllabus.** Every exercise ends in a map, and every map is accepted only
if a colleague can repeat the steps. They get what they asked for; the price of
receiving it is the thing they need.


---

## 2. Competency framework

Five levels, defined by **what a person is observed to do**, not by how much they
know. Full 6-domain grid in **Annex A**.

### 2.1 The levels

| Level | Name | The observable test |
|---|---|---|
| **0** | Not yet demonstrated | Cannot begin the task without someone performing it for them |
| **1** | Assisted | Completes the task while following a written procedure step by step. Stops when the procedure does not match what is on screen |
| **2** | Independent | Completes the task correctly from a stated objective, without a procedure. **Cannot yet be re-run by anyone else** |
| **3** | Reproducible | Output is correct **and** a colleague of the same level reproduces it from what was left behind, without asking the author a question |
| **4** | Improving | Diagnoses why someone else's workflow failed, repairs the process rather than the output, and the repair holds for the next person |

The line that matters is **between 2 and 3**, and most frameworks do not draw it.
"Can do it alone" is where training normally stops and where this department's
problem actually starts: twenty-one people at level 2 still produce a department
that cannot survive one of them leaving.

**Level 3 is testable without judgement.** Hand the artefact to a colleague, give
them the raw data, forbid them to ask the author anything, and see whether the
output matches. It either does or it does not.

### 2.2 The target, and its limit

Baseline for documentation is **1.5** - between "keeps a copy when reminded" and
"can describe it from memory today". The course targets **level 3 for the whole
cohort on one workflow**: not level 3 across all six domains, which is not
achievable in five days, and claiming it would read well and not survive the
post-assessment.

Full grid - six domains × five levels, each cell an observable behaviour - in
**Annex A**.

---

## 3. The five-day course

**Ratio: 70% hands-on, 30% instruction.** Instruction blocks are capped at 20
minutes and each is followed immediately by the task that uses it. This follows
directly from §1.1 - the cohort's deficit is application, and lecture is the
wrong instrument for an application deficit.

Learning outcomes are written at the cognitive level the evidence supports.
Nothing is set at *evaluate* or *create* on day one for a cohort scoring 36.

### Day allocation and outcomes

Full session-by-session detail - every exercise, dataset and duration - in
**Annex E**. Learning outcomes are written at the cognitive level the evidence
supports; nothing is set at *evaluate* or *create* on day one for a cohort
scoring 36.

| Day | Focus | Outcome | Hands-on |
|---|---|---|---|
| **1** | What is actually in the data | **Apply** - given an unfamiliar dataset, produce a written inventory of its defects, in counts rather than impressions, without cleaning anything | 260 / 20 min |
| **2** | Cleaning that can be checked | **Apply** - clean a dataset so every change is counted and no record is silently dropped | 240 / 20 min |
| **3** | **Reproducibility - the spine** | **Apply → analyse** - produce a record from which a colleague reproduces your cleaned dataset without speaking to you | 240 / 0 min |
| **4** | Spatial data, and the map they came for | **Apply** - produce a correctly projected, properly furnished map, and state what it does not show | 255 / 20 min |
| **5** | Their own work, and what happens next | **Apply → evaluate** - complete a real departmental product to level 3, and review a colleague's to level 4 | 270 / 0 min |

Three sessions carry the design. **Day 1 opens with a task they cannot finish**
(§1.2) and still ends in a product, so the morning's discomfort resolves the same
day. **Day 3 session 1 - "Make your work someone else's" - is the session
developed in full as Annex B**, and session 3 has the cohort draft *their own*
documentation standard, because a standard issued to this department will not be
followed and one they wrote and tested might be. **Day 5 uses the department's
real work**, since training data produces training-shaped competence and transfer
is the problem this programme exists to solve; its closing peer-reproduction
doubles as the post-assessment.

## 4. What I have chosen not to teach, and why

A five-day course promising spatial statistics, remote sensing, web mapping and
automation to a cohort scoring 36 is a design failure. Each of these was
considered and cut.

| Not taught | Why |
|---|---|
| **Spatial statistics** | Requires trust in the underlying data. This cohort cannot yet establish that a dataset is clean, so a significance test would be a confident answer resting on unexamined input - actively worse than no answer |
| **Remote sensing** | An entire discipline. Five days would produce vocabulary and no capability, and there is no departmental workflow currently demanding it |
| **Web mapping / dashboards** | Publishing is the last problem this department has. It would put unverified data in front of more people, faster |
| **Python / R automation** | The one I most wanted to include, and cutting it was the hardest call. It adds a *second* novel discipline - programming - on top of the first, reproducibility, before the first is secure. Reproducibility is achievable with the tools they have; automation is a later programme for those who reach level 4 |
| **Geodatabase administration** | No database to administer until access is resolved |
| **Advanced cartographic design** | Their strongest demand, and deliberately capped at competent-and-honest rather than beautiful. Beauty is not the department's constraint |

**The principle:** at capability 36 with the weakest score in documentation,
breadth produces people who can *name* techniques and *deliver* none. Depth on
one chain - profile, clean, document, map, hand over - produces people who can
complete a real task and prove it. Nothing here is permanently excluded; each is
a candidate for the programme after the 90 days, conditional on measured
progress.

---

## 5. Pre and post assessment

**Demonstrated capability only.** No confidence items, no satisfaction items, no
self-rating as an outcome - §1.2 disqualifies all three. Full instrument, rubric
and datasets in **Annex C**.

A **practical task**: 8 items scored 0-4 against the level definitions, 32
points, 3 hours, blind marked. Identical tasks and rubric at both administrations
on **parallel datasets** - same defect specification, same frequencies, different
values, so the difficulty matches and the post-test cannot be passed from memory.
The parallel-form claim is *verified rather than asserted*: the dataset generator
compares defect profiles across the files and fails if they differ.

**Task 8 carries the design, and the participant does not perform it.** Their
submitted work goes to an assessor who has not seen it, with the raw data and no
access to the author; the score is whether the output reproduces. It is the only
item that tests level 3 directly, and the only one that cannot be faked, coached
or inflated by a confident participant. Someone can score well on tasks 1-7 and
**zero on 8** - which is precisely this department's present condition, so the
instrument has to be able to detect it.

**One secondary measure, never an outcome.** The self-rating item is retained
only to recompute the 0.11 correlation as a measure of *calibration*. If it
rises, participants have learned to judge their own competence - and a department
that knows what it cannot do asks for help before producing a wrong number.
Reported on its own line, never as evidence of capability.

---

## 6. The ninety days after the course

Training that ends when the course ends is the failure mode this section exists
to prevent.

### Days −14 to 0 - before the course: resolve the binding constraint

**This runs before day one, not after.** Nothing transfers if participants cannot
open the software on the Monday afterwards.

1. **Establish why access is zero.** One conversation with the agency's IT
   function and one attempt to install QGIS on a departmental machine
   distinguishes admin rights from hardware from policy. Until this is known,
   every remedy is a guess.
2. **Deploy QGIS Portable on USB** to all 21. No administrative rights, no
   installation - it removes the constraint immediately if the cause is rights or
   policy, and demonstrates it hard if the cause is hardware.
3. **Escalate with evidence, not a request.** If hardware is the cause, the ask
   to the counterpart's management is specific and costed, and carries the
   finding: a department contractually committed to geospatial output with zero
   capacity to run geospatial software.

### Days 1-30 - applied work under review

Each participant leaves day 5 with **one named real product, a delivery date and
a named reviewer.** Fortnightly 60-minute remote clinics - not teaching;
participants bring work that is stuck. Every product passes **peer reproduction**
before acceptance, so the level-3 test becomes routine practice rather than an
assessment event.

### Days 31-60 - the standard becomes binding

The documentation standard drafted on day 3 is **formally adopted** by the
department head, having been tested on 30 days of real work rather than issued
from outside. Two or three participants reaching level 4 take over **reviewing**
others' work - capability transfers when the review stops being mine. **Access is
resolved or formally escalated**; if neither, the programme reports it as a
failure of the commitment rather than of the training, and that distinction
belongs on the record.

### Days 61-90 - measure, and decide what is next

- **Post-assessment**, including the independent reproduction task.
- **Capability transfer measured**, not satisfaction:

| Indicator | Measures |
|---|---|
| % of participants with working GIS software on their own machine | Whether the binding constraint was actually lifted |
| Number of real departmental products delivered to level 3 | Whether skills reached real work |
| Independent reproduction success rate | Whether the core skill transferred |
| Number of reviews conducted **by the department**, not by me | Whether capability is now self-sustaining |
| Change in tested score, pre to post | Capability |
| Change in self-rating/tested correlation | Calibration, reported separately |

**Not measured, deliberately:** satisfaction, self-rated confidence, attendance,
or number trained. Every one of them can be excellent while nothing changed.

- **The next programme is conditional.** Automation and spatial statistics become
  available to participants who reach level 4 - earned by demonstration, not by
  attendance. A cohort that has not reached level 3 gets a repeat of this
  programme, and saying so at the outset is what makes level 3 mean something.

---

## 7. Why this is the same problem as the coordination scenario

The scenario presents two obligations competing for my time. They are one
problem.

Two of six state analysts resign and delivery is threatened - true only because
their knowledge was never written down. The counterpart department scores **1.5
out of 5 on documenting a reproducible workflow.** The same finding in two
organisations: capability living in individuals rather than in the process, so
competence is exactly as durable as staffing.

That is why documentation is the spine of this course, and why level 3 - *a
colleague reproduces it without asking you* - is the threshold the programme is
built around. It is the operational definition of knowledge that has left
someone's head.

It is also why the two obligations do not compete as the scenario implies. The
handover protocol for my own departing analysts and the standard this department
drafts on day 3 are **the same artefact**, and building it once, in the open,
with the counterpart participating, serves both.

**The honest caveat:** this is a genuine connection, not a universal one. If the
counterpart's real constraint proves to be hardware rather than knowledge, no
documentation standard fixes it and the two problems come apart completely. The
90-day plan's first action exists because the answer decides whether this
argument holds.


### Annexes (excluded from the page limit)

**A** competency framework · **B** the 90-minute session in full - facilitator
guide, participant briefs, model answer and dataset generator · **C** pre/post
assessment instrument · **D** dataset specifications · **E** session-by-session
course plan



```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# ANNEXES

Excluded from the Q6 page limit, as the question permits.


# Annex A - Competency framework

Six domains × five levels. Excluded from the Q6 page limit.

**The framework describes what a person is observed to do, not what they know.**
Every cell is a behaviour an assessor can witness in one sitting and score
without discussion. Where a cell needs a judgement about intent or understanding,
it is written wrong and has been rewritten.

## The five levels

| Level | Name | The test |
|---|---|---|
| **0** | Not yet demonstrated | Cannot begin without someone performing the task for them |
| **1** | Assisted | Completes it while following a written procedure step by step. Stops when the procedure stops matching the screen |
| **2** | Independent | Completes it correctly from a stated objective, with no procedure. **Cannot yet be re-run by anyone else** |
| **3** | Reproducible | Correct output **and** a colleague at the same level reproduces it from what was left behind, asking the author nothing |
| **4** | Improving | Diagnoses why someone else's workflow failed, repairs the *process* rather than the output, and the repair holds for the next person |

**The 2→3 boundary is the one that matters** and is why a generic
beginner/intermediate/advanced scale would not do. "Can do it alone" is where
most training stops and where this department's problem begins: twenty-one people
at level 2 still produce a department that cannot survive one resignation.

Level 3 is scored without judgement - hand the artefact to a colleague with the
raw data, forbid questions, and see whether the output matches. It does or it
does not.

---

## D1 · Data acquisition and structure

| L | Observable behaviour |
|---|---|
| 0 | Opens a file and begins editing without establishing what it contains |
| 1 | States row and column counts when prompted to |
| 2 | Establishes structure unprompted: rows, columns, types, what one row represents |
| 3 | Records the source, its date, its row count and its provenance, so a colleague can confirm they are holding the same file |
| 4 | Identifies that two files claiming to be the same register are not, and establishes which is authoritative |

## D2 · Data cleaning and validation

| L | Observable behaviour |
|---|---|
| 0 | Corrects values by typing over them in the source file |
| 1 | Fixes defects that are pointed out, one at a time, in the order given |
| 2 | Finds defects unaided, fixes them, and the output is correct |
| 3 | Expresses each fix as a **rule with a count of rows affected**, and reconciles input rows against output rows so that no record is silently lost |
| 4 | Distinguishes a defect from a finding - recognises when unusual data is real and must be preserved rather than corrected |

## D3 · Documenting a reproducible workflow - **weakest measured competency, 1.5 / 5**

| L | Observable behaviour |
|---|---|
| 0 | Cleans by editing cells directly. No record of what changed |
| 1 | Keeps the raw file untouched and works on a copy, when reminded |
| 2 | Keeps raw and working copies separate and can describe the changes from memory, on the same day |
| 3 | Leaves a written record naming every change, its reason, and the rows affected - **and a colleague reproduces the cleaned file from the raw file using only that record** |
| 4 | Reviews a colleague's record, identifies the step that cannot be repeated, and rewrites it so the next person does not hit the same gap |

## D4 · Spatial data handling

| L | Observable behaviour |
|---|---|
| 0 | Treats coordinates as ordinary numbers; unaware that a projection exists |
| 1 | Loads a point layer following a procedure, and it appears in roughly the right place |
| 2 | Loads and joins layers unaided; notices when points land in the sea or the wrong hemisphere |
| 3 | States the CRS in use and why, converts deliberately rather than by accident, and **reports join failures with a count** instead of quietly losing the unmatched rows |
| 4 | Chooses a projection appropriate to the measurement being made, and can say what the choice costs |

## D5 · Map production and cartography - **strongest stated demand**

| L | Observable behaviour |
|---|---|
| 0 | Produces a screenshot of the map canvas |
| 1 | Produces a map with a title and a legend, following a checklist |
| 2 | Produces a complete map unaided: title, legend, scale, north arrow, source, date |
| 3 | The map states its **projection and its data source**, and a colleague can rebuild it from the record - and it says what it does **not** show |
| 4 | Chooses the symbology to fit the question, and can explain why a different choice would mislead |

## D6 · Interpretation and communication

| L | Observable behaviour |
|---|---|
| 0 | Reports the output as fact without reference to how it was produced |
| 1 | Repeats a stated caveat when reminded of it |
| 2 | Describes what the analysis found, accurately, in plain language |
| 3 | States the limitation **unprompted**, including what the data cannot support, and separates what was measured from what was inferred |
| 4 | Anticipates how a decision-maker will misread the output, and structures the product to prevent it |

---

## Baseline, and what five days can actually move

| Domain | Baseline | After 5 days | After 90 days |
|---|---|---|---|
| D1 Acquisition and structure | ~1 | 2 | 3 |
| D2 Cleaning and validation | ~1 | 2 | 3 |
| **D3 Documentation** | **1.5 (measured)** | **3 on one workflow** | **3 across routine work** |
| D4 Spatial handling | ~1 | 2 | 2-3 |
| D5 Map production | ~2 (strongest) | 3 | 3 |
| D6 Interpretation | ~1 | 2 | 2-3 |

**Only D3 is targeted at level 3 within the week, and only on one workflow.**
Claiming level 3 across six domains in five days would be the same design failure
as promising spatial statistics and remote sensing - it would read well and
would not survive contact with the post-assessment.

Baselines other than D3 are inferred from the composite score of 36 and are
marked approximate, because only D3 was measured directly. **The pre-assessment
in Annex C establishes the others properly**, which is a second reason to run it
before day one rather than relying on the composite.



```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```



# Annex B - The 90-minute session, in full

**"Make your work someone else's"** · Day 3, session 1 · 21 participants in pairs.

The question asks for one session developed as *an artefact a colleague could
deliver in my absence*. That is the standard this annex is written to, so it is
four separate documents rather than one description - a facilitator running it
needs the guide in hand, the briefs printed, and the model answer withheld.

| File | What it is | Who sees it |
|---|---|---|
| `facilitator_guide.md` | Minute-by-minute timings, verbatim wording where it matters, expected errors and interventions | Facilitator |
| `participant_brief.md` | Briefs A and B. **B is held back until minute 25** - issuing both at once lets participants write the record with the reproduction task already in mind, which is what the session tests them not to do | Participants |
| `model_answer.md` | The level-3 exemplar, the reconciliation numbers, and what to look for when judging | **Facilitator only - do not distribute** |
| `make_dataset.py` | Generates the dataset. Fixed seed, so a colleague produces exactly the file the model answer expects | - |
| `D1_facilities_raw.csv` | The teaching dataset for Days 2 and 3 | Participants |
| `D_PRE_…`, `D_POST_…` | Parallel forms for the pre/post assessment (Annex C) | Assessor |

**Why the session exists.** Participants discover - by failing - that work they
can repeat themselves cannot be repeated by anyone else. That gap is the
difference between level 2 and level 3 in the competency framework, and it is
the single most important thing in the five days.

Full specification of every dataset in **Annex D**.



```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```



# Facilitator guide - "Make your work someone else's"

**Day 3, session 1 · 90 minutes · 21 participants in pairs (one three)**

This is written so a colleague can deliver it without me. Where the wording
matters, it is given verbatim in quotes. Where it does not, it says so.

---

## What this session is for

Participants discover - by failing - that work they can repeat *themselves*
cannot be repeated by *anyone else*. That gap is the difference between level 2
and level 3 in the competency framework, and it is the single most important
thing in the five days.

**Do not tell them this at the start.** The whole design depends on them finding
it. If you announce the lesson, they will write good documentation for the
exercise and poor documentation for the rest of their lives.

The baseline for this competency is **1.5 out of 5** across the department. Expect
the first attempt to fail almost universally. That is the intended result, and
managing how it feels is most of your job here.

---

## Before the session

| Check | Detail |
|---|---|
| Dataset loaded | `D1_facilities_raw.csv` on every machine, in `Day3/` |
| Yesterday's work | Each participant has their own cleaned file and whatever notes they made on Day 2. **Do not let them redo the cleaning** |
| Pairing list | Prepared in advance - see pairing rule below |
| Printed briefs | One per participant. Brief A at the start; **hold Brief B back** |
| Timer | Visible to the room |
| Flip chart | Headed "What stopped us" |

**Pairing rule.** Pair across the pre-assessment range - a higher scorer with a
lower scorer - but **never announce why pairs were formed**. Same-level pairs
produce either two failures with no diagnosis, or two people who assume the tool
is broken.

**One machine per pair for the reproduction phase.** They must work on the
partner's file together; watching someone struggle with your instructions is
where the learning is.

---

## Minute by minute

### 0-8 · Framing

Say, roughly - this wording is not load-bearing:

> "Yesterday you each cleaned the facility list. This morning we are going to
> check something simple: whether the work you did is *usable by the department*
> or only usable by you."

Then, verbatim, because this line prevents the session being read as a test:

> **"Nobody's cleaning is being marked this morning. What we are testing is the
> handover, not the person."**

Hand out **Brief A**. Do not hand out Brief B.

### 8-25 · Task A - write the record (17 min)

Participants work **alone**, writing the record of what they did yesterday. Brief
A gives them the format.

**Walk the room. Do not correct anything.** You will see records that say
"cleaned the LGA names" with no list of what changed. Leave them. Correcting now
destroys the session.

If asked *"how much detail?"*, reply:

> **"Enough that someone else could do exactly what you did."**

Then leave. Do not elaborate - the ambiguity is the point, and most will resolve
it too thinly.

At 25 minutes, stop them **whether or not they have finished.** Collect nothing.

### 25-50 · Task B - reproduce your partner's work (25 min)

Hand out **Brief B**. Announce the rule, verbatim:

> **"From now until I call time, you may not speak to your partner about their
> work. Not one question. If their record does not tell you something, write down
> what it did not tell you and carry on as best you can."**

Pairs move to one machine, open the **raw** file and the **partner's record**,
and attempt to produce the partner's cleaned file.

**Enforce the no-talking rule firmly.** It will be broken within four minutes,
usually by the record's author leaning in to explain. That instinct is exactly
what the session is about. Intervene with:

> "That is the fourth thing you have had to explain. Write each one down - that
> list is your real output this morning."

**Your job in this phase is to notice, not to help.** Track which failures recur;
you will need them at 50 minutes.

At 45 minutes, ask each pair to note **row counts** for the file they produced
and the partner's original.

### 50-65 · What stopped us (15 min)

Round the room. Each pair gives **one** thing the record failed to tell them.
Write them on the flip chart, grouped as they emerge. Do not attribute to
individuals - say "a pair found", never a name.

**Expected groupings** (see the errors table below): order not stated, "cleaned"
without saying how, decisions not recorded, source file ambiguous, counts absent.

Then ask the room, and wait for the answer rather than supplying it:

> **"How many of you produced a file with the same number of rows as your
> partner's?"**

Typically two or three pairs of ten. Let the silence sit. **This is the moment
the session exists for.** Do not rescue it, and do not lecture. Say only:

> "So the work was right, and it did not survive the handover."

### 65-83 · Repair and re-test (18 min)

Participants take back their own record and rewrite it using the flip chart.
**10 minutes.**

Then **re-pair with a different partner** and give **8 minutes** to attempt
reproduction again. Eight minutes is not enough to finish, and it does not need
to be - what is being tested is whether the second reader gets *further*, not
whether they finish.

Ask for a show of hands: **"Who got further this time?"** Near-universal, and it
is the first evidence they have that the fix is achievable.

### 83-90 · Consolidate

Ask the room for the minimum a record must contain. Take five or six items only.
You will get most of the model answer back; supply nothing they do not offer,
and do not correct omissions - Day 3 session 3 is where they draft the full
standard, and it must be theirs.

Close, verbatim:

> **"Your cleaning was not the problem. Every one of you could repeat your own
> work. The department cannot, and that is a different skill - it is the one we
> are building this week."**

---

## Common errors, and how to intervene

Ranked by how often they occur. **Interventions are all delayed to the 50-minute
discussion unless flagged otherwise** - correcting during Task B removes the
evidence.

| # | What you will see | Why it happens | Intervention |
|---|---|---|---|
| 1 | *"Removed duplicates"* - no key, no count, no rule for which was kept | Deduplication feels self-evident to the person who did it | At 50 min: "Which of the two rows survived? Did your partner keep the same one?" |
| 2 | Steps in the wrong order, or no order at all | They remember the *set* of actions, not the sequence | Ask a pair to state what happens if trimming spaces comes after grouping names. Let them work it out |
| 3 | *"Corrected the LGA names"* with no mapping | The variants were obvious on the day | "Your partner has seen `Idi Oro`, `IDI-ORO` and `Idi-oro`. Which is correct, and how would they know?" |
| 4 | No row counts anywhere | Counting feels bureaucratic until reproduction fails | This is why the row-count check at 45 min exists. Let the numbers make the argument |
| 5 | Source file ambiguous - several files named `facilities_final` | Nobody names a file for a reader | Ask which file the partner opened. Often the wrong one, and everything after was wasted |
| 6 | Judgement calls not recorded at all | The 5 facilities with no coordinates were dropped, or kept, and it seemed obvious | The most important error in the session. "You made a decision. Your partner made the opposite one. Neither of you is wrong - but the numbers now differ and nobody knows why" |
| 7 | The record describes *intent*, not *action* - "made the data consistent" | Writing about work is a different skill from doing it | "Read that sentence and tell me the first thing your partner should click" |
| 8 | Author explains verbally, then insists the record was fine | The gap is genuinely invisible from inside | **Intervene immediately.** "Stop - write down what you just said. That sentence is the missing line" |

### Two situations that need handling on the spot

**A pair reproduces the file exactly.** It happens once or twice, and it is a
genuine level-3 result. Do not make an example of them in a way that isolates the
room. Ask the *reproducer*, not the author: *"What did their record have that
made this possible?"* Their answer goes on the flip chart and carries more weight
than anything you say.

**A participant becomes defensive** - usually a senior one whose record failed
publicly. Redirect to the artefact, never the person: *"The record is the thing
we are fixing, not the cleaning. Your cleaning was correct."* If it persists,
move them into the repair phase early and let them succeed at the rewrite.

---

## If you are running short of time

Cut in this order:

1. **The second re-pair at 75 min** - shorten to 5 minutes. Getting further is
   the point; finishing is not.
2. **The consolidation at 83 min** - Day 3 session 3 covers it.
3. **Never cut the reproduction attempt or the row-count check.** Without them the
   session is a lecture about documentation, which is what the department has
   already had and has not acted on.

## What success looks like

Not a room that has written good documentation. **A room that has felt the gap.**

The measurable outcome is at 83 minutes: *"who got further this time?"* If most
hands go up, they have learned that the fix is small and achievable, which is
what makes them do it next week when nobody is watching.



```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```



# Participant briefs - "Make your work someone else's"

Two briefs. **Brief A is handed out at the start. Brief B is held back until
minute 25** - issuing both together lets participants write the record with the
reproduction task already in mind, which is precisely what the session is
testing them not to do.

Print single-sided, one set per participant.

---
---

# BRIEF A - Write the record

**Time: 17 minutes. Work alone.**

Yesterday you cleaned `D1_facilities_raw.csv`. You produced a cleaned file, and
you made a number of decisions along the way.

**Do not open the data again. Do not change your cleaned file.**

Write a record of what you did, so that the work can be repeated.

Use this format, on paper or on screen:

```
SOURCE FILE
    Which file did you start from? Give its exact name.

STEPS
    1.
    2.
    3.
    ...

DECISIONS
    Anything you had to choose, where another sensible person
    might have chosen differently.

RESULT
    Rows in.        Rows out.
```

That is all. You have 17 minutes.

> *If you are wondering how much detail to include: enough that someone else
> could do exactly what you did.*

---
---

# BRIEF B - Reproduce your partner's work

**Time: 25 minutes. Work at one machine, together.**

You now have your partner's record. Your task is to produce **their cleaned
file**, starting from the raw data.

## Rules

1. Start from `D1_facilities_raw.csv`. Not from their cleaned file.
2. Use **only** what is written in their record.
3. **You may not ask your partner anything.** Not one question. If they
   volunteer information, do not use it.
4. Where the record does not tell you something, **write down what it did not
   tell you**, make your best guess, and carry on.

## What to produce

- A cleaned file, produced by following their record.
- A list headed **"What the record did not tell me"**.

That list is the important output. It is not a criticism of your partner - the
same list is being written about your record, at the same time, by someone else.

## Before time is called

Record two numbers:

```
Rows in my reproduced file:      ______
Rows in my partner's file:       ______
```

You will be asked for these.



```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```



## Model answer - "Make your work someone else's"

For the facilitator. **Do not distribute.** Participants draft the standard
themselves in Day 3 session 3, and handing them the answer removes the reason
they would follow it.

---

## Part 1 - What a level-3 record looks like

This is the exemplar, not a template to issue. Compare participant records
against it to judge *what is missing*, not to mark them.

```
SOURCE FILE
    D1_facilities_raw.csv, 203 rows, as received 2 June 2026.
    Not modified. All work done on a copy.

STEPS, in this order
    1. Trimmed leading and trailing spaces from facility_name and lga_name.
       54 values changed - 24 in facility_name, 30 in lga_name.
       (Done FIRST - grouping before trimming leaves " Gwarin" as its own group.)

    2. Mapped lga_name to 4 canonical values using this table:
           Idi-Oro   <- "Idi Oro", "IDI-ORO", "Idi-oro", "idi-oro"
           Gwarin    <- "GWARIN", "gwarin"
           Katsuma   <- "KATSUMA"
           Ilela     <- "ILELA", "ilela"
       16 distinct values reduced to 4. 98 rows changed.

    3. Mapped facility_type to 3 canonical values:
           Primary Health Centre <- "Primary Health Center", "PHC",
                                    "Primary health centre"
           Health Post           <- "Health post", "HEALTH POST"
           Cottage Hospital      <- "Cottage hospital"
       9 distinct values reduced to 3. 120 rows changed.

    4. Replaced "," with "." in longitude. 6 values fixed.
       These were text like "7,914882" - a decimal comma, not a thousands
       separator. Checked: all 6 fall inside the state bounding box afterwards.

    5. Found 2 rows where longitude was between 10.37 and 11.57 and latitude
       between 6.95 and 8.43 - outside the state, but inside it when swapped.
       Swapped them. Flagged both in a column `coord_swapped`.

    6. Set staff_total to blank where it read 999 (3 rows). See DECISIONS.

    7. Removed 3 duplicate facility_id rows. See DECISIONS.

DECISIONS
    D1. staff_total = 999 in 3 rows.
        999 is not a plausible staff count for any facility in this register
        (max otherwise 24). Treated as a non-response sentinel, not a value.
        Set to blank rather than deleted, so the facility is retained.
        ALTERNATIVE: it could be a real data-entry error for 99 or 9. I could
        not distinguish these from the register alone. Flagged for the ministry.

    D2. 3 facility_ids appear twice, and the two rows DIFFER (staff_total).
        Kept the row with the HIGHER staff_total, on the assumption that the
        later entry is an update.
        ALTERNATIVE: keeping the first occurrence is equally defensible. This
        changes staff totals by 11 across the register.

    D3. 5 facilities have no coordinates.
        KEPT them in the cleaned file, with coordinates blank.
        They are real facilities; dropping them would silently reduce the
        facility count and understate coverage. They cannot be mapped, and any
        map made from this file must state that 5 of 200 are absent.
        ALTERNATIVE: dropping them makes the file directly mappable but
        changes the denominator without saying so.

RESULT
    Rows in:   203
    Rows out:  200
    Difference explained: 3 duplicate facility_id rows removed (D2).
    Facilities mappable: 195. Not mappable: 5 (D3).
```

## Part 2 - The numbers

Use these to check whether a pair actually reproduced the file.

| | |
|---|---|
| Rows in raw file | **203** |
| Distinct `facility_id` | **200** |
| Rows out, following the model | **200** |
| Mappable facilities | **195** |
| `lga_name` variants → canonical | 16 → **4** |
| `facility_type` variants → canonical | 9 → **3** |
| Whitespace values corrected | **24** |
| Decimal-comma longitudes | **6** |
| Transposed coordinate pairs | **2** |
| `staff_total = 999` | **3** |

**A pair has reproduced the work when the row count matches and the same
facilities are present.** Exact column-by-column equality is not the standard -
the standard is that the department would report the same numbers.

## Part 3 - Why participants get different answers, and why that is the lesson

Three defects have **no single correct treatment**: D1, D2 and D3 above.

Two participants can both clean this file competently and arrive at:

- **200 rows** (duplicates removed, missing coordinates kept), or
- **195 rows** (missing coordinates also dropped), or
- **203 rows** (duplicates kept as separate facilities)

**All three are defensible. None is reproducible unless the decision was
written down.**

This is the point of the whole session, and it is why the dataset was built with
judgement calls in it. A dataset with only mechanical defects would teach
participants that documentation means listing steps. It does not. **It means
recording the choices**, because the steps are usually recoverable by inspection
and the choices never are.

If the discussion at minute 50 reaches this on its own, the session has done
more than it needed to. If it does not, do not supply it - Day 3 session 3 is
where they will reach it while drafting their own standard, and it lands harder
there.

## Part 4 - What to look for when judging level 3

Not a mark scheme. A prompt for what to notice while walking the room.

| Signal | Level |
|---|---|
| Record describes intent - "made the data consistent" | 1 |
| Steps listed, no counts, no order stated | 2 |
| Steps in order, with counts, no decisions recorded | 2 (the most common outcome) |
| Steps, counts, order **and** decisions with their alternatives | **3** |
| The above, plus notes on what the *next* person should check | 4 |

**Expect the whole room at 2 or below on the first attempt.** The department's
measured baseline for this competency is 1.5 out of 5, and a single morning does
not move a department to level 3. What it moves is their understanding of what
level 3 requires - the remaining distance is closed over the 90 days, on real
work, under review.



```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```



# Annex C - Pre and post assessment instrument

Excluded from the Q6 page limit.

## What this measures, and what it refuses to

**Demonstrated capability only.** No confidence items, no satisfaction items, no
self-rating as an outcome. §1.2 of the main response disqualifies all three: at a
self-rating/tested correlation of **0.11**, a rise in self-assessment after
training measures comfort, not competence, and would let the programme report
success while nothing had changed.

The instrument is **a practical task**, scored against the level definitions in
Annex A. Participants do the work; the work is marked.

| | |
|---|---|
| Format | Practical, at a machine, individual |
| Duration | **3 hours** including a 15-minute break |
| Items | 8 tasks, scored 0-4 | **32 points** |
| Administered | Days −7 (pre) and 61-90 (post) |
| Datasets | `D_PRE_facilities_raw.csv` / `D_POST_facilities_raw.csv` |
| Marking | Blind - no names, no administration order |

---

## The eight tasks

Tasks 1-7 are performed by the participant. **Task 8 is performed on them.**

| # | Task | Domain | What a 4 looks like |
|---|---|---|---|
| **1** | **Profile the file.** Report what it contains and what is wrong with it. Change nothing. | D1 | Row count, column types, what one row represents, and a defect inventory **with counts** - not impressions |
| **2** | **Canonicalise names.** Reduce `lga_name` and `facility_type` to their true values. | D2 | Correct mapping, stated as a table, with rows affected. Trimming done **before** grouping, and the reason given |
| **3** | **Handle the coordinates.** Find and treat every coordinate defect. | D2, D4 | All three classes found - decimal comma, transposition, missing - each fixed or retained deliberately, with counts |
| **4** | **Identify the judgement calls.** Which defects have no single correct treatment? | D2, D6 | Names all three (duplicates, missing coordinates, `999`), states a decision for each **and the defensible alternative** |
| **5** | **Write the record.** So that a colleague could reproduce your cleaned file. | **D3** | Source, ordered steps with counts, decisions with alternatives, rows in and rows out with the difference explained |
| **6** | **Join to wards and report failures.** | D4 | Join performed, unmatched rows **counted and reported** rather than silently dropped |
| **7** | **Produce a map, and state one thing it does not show.** | D5, D6 | Complete furniture, projection stated, and an unprompted limitation that is actually true of this data |
| **8** | **Independent reproduction.** *Performed by an assessor, not the participant.* | **D3** | An assessor with the raw file and the participant's record, forbidden to contact them, produces a matching file |

### Why Task 8 carries the design

It is the only item that tests **level 3 directly**, and the only one that cannot
be inflated by a confident participant, coached by a supervisor, or improved by
knowing the marker. A participant can produce excellent work on tasks 1-7 and
still score zero on 8 - and that combination is precisely the department's
current condition, so the instrument has to be able to detect it.

It is also the item most likely to be dropped for being inconvenient. It costs an
assessor roughly 30 minutes per participant. **That cost is the measurement.**

---

## Scoring

Each task scored against Annex A's levels:

| Score | Meaning |
|---|---|
| **0** | Not attempted, or attempted with no correct element |
| **1** | Assisted standard - correct only where the task itself supplied the procedure |
| **2** | Independent standard - correct output, not reproducible |
| **3** | Reproducible standard - correct, counted, and documented |
| **4** | Improving standard - as 3, plus identifies a problem the task did not ask about |

**Total 32.** Reported as a total *and* as a per-domain profile, because a
department that moves from 12 to 18 by improving map production while
documentation stays at 1 has not achieved what this programme is for.

### Interpretation bands

| Total | Reading |
|---|---|
| 0-8 | Level 0-1. Cannot yet work unsupervised |
| 9-16 | Level 1-2. Produces correct work that cannot be handed over. **Expected baseline** |
| 17-24 | Level 2-3. Reproducible on familiar tasks |
| 25-32 | Level 3-4. Can review others' work |

**Expected pre-assessment total: 11-14.** Consistent with a composite of 36 and
a documentation score of 1.5. If the cohort scores materially above this, the
composite was mismeasured and the course design should be revisited before
delivery rather than after.

---

## Comparability across the two administrations

Five controls, because a pre/post comparison is worthless if the two are not the
same test:

1. **Identical tasks and identical rubric.** Nothing is added or reworded.
2. **Parallel datasets, not the same dataset.** `D_PRE` and `D_POST` are
   generated to the *same defect specification* with different values.
3. **The parallel-form claim is verified, not asserted.** `make_dataset.py`
   compares the defect profile of all three datasets and **fails if they differ**:

   | | D1 | D_PRE | D_POST |
   |---|---|---|---|
   | rows | 203 | 203 | 203 |
   | distinct `facility_id` | 200 | 200 | 200 |
   | duplicate id rows | 3 | 3 | 3 |
   | missing coordinates | 5 | 5 | 5 |
   | `staff_total = 999` | 3 | 3 | 3 |
   | whitespace in name | 24 | 24 | 24 |
   | `lga_name` variants | 16 | 16 | 16 |
   | `facility_type` variants | 9 | 9 | 9 |
   | comma in longitude | 6 | 6 | 6 |

   Same difficulty, different values - so the post-test cannot be passed from
   memory of the pre-test, and cannot be *harder* either, which is the failure
   that makes a genuine improvement invisible.

4. **Blind marking.** Submissions are stripped of names and administration order
   before marking, so a marker expecting improvement cannot unconsciously supply
   it.
5. **The same assessor does not mark the same participant twice.** Cheap to
   arrange with two assessors and it removes the strongest source of drift.

**D1 is deliberately not used for assessment.** It is the teaching dataset, seen
for two full days, and testing on it would measure recall of a specific file.

---

## The calibration measure - reported, never as an outcome

One self-rating item is retained at both administrations: *"Rate your ability to
document a cleaning workflow so a colleague could repeat it, 1 to 5."*

It is **not** scored and does not enter the total. It exists to recompute the
correlation between self-rating and tested score.

| | |
|---|---|
| Baseline | **r = 0.11** |
| Target | r > 0.4 |

A department that can judge its own competence asks for help before producing a
wrong number, and stops asking for training it does not need. That is a real
result, worth measuring - and it is reported in its own line, never as evidence
of capability, because that is exactly the conflation §1.2 rules out.

---

## What this instrument does not measure

Stated so nobody claims it does.

- **Whether the work is faster.** Speed is not assessed, and a participant who
  slows down because they have started documenting has improved.
- **Whether it holds under real conditions.** A three-hour assessment is not a
  deadline with a supervisor waiting. The 90-day applied work is what tests that.
- **Retention beyond 90 days.** A third administration at six months would, and
  is not in scope of the contracted programme. Worth proposing separately.
- **Anything about the 21 as individuals for HR purposes.** Scores are for
  programme design and for the participant. If they become a performance
  instrument the room will optimise for the score, the pre-assessment will be
  gamed downward, and the measurement is destroyed.



```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```



# Annex D - Dataset specifications

Excluded from the Q6 page limit.

**Generated, not described.** `annex_b_session_in_full/make_dataset.py` produces all three
datasets from a fixed seed, so a colleague delivering the course in my absence
gets exactly the files the model answer and the rubric expect. A specification in
prose would drift from the file within one revision.

    python part3_q6/annex_b_session_in_full/make_dataset.py

| Dataset | Used for | Seed |
|---|---|---|
| `D1_facilities_raw.csv` | Days 2 and 3 teaching; quoted exactly in the model answer | 20260731 |
| `D_PRE_facilities_raw.csv` | Pre-assessment (Annex C) | 20260832 |
| `D_POST_facilities_raw.csv` | Post-assessment (Annex C) | 20260933 |

## Structure

200 facilities, 8 columns: `facility_id`, `facility_name`, `facility_type`,
`lga_name`, `ward_name`, `longitude`, `latitude`, `staff_total`.

Sized to be cleanable in 120 minutes by people at capability 36. Large enough
that defects cannot be found by eye; small enough to finish.

## Seeded defects

| # | Defect | Count | Judgement call? |
|---|---|---|---|
| 1 | `lga_name` variants - spacing, case, hyphenation | 16 variants → 4 real LGAs, 98 rows | No |
| 2 | Duplicate `facility_id`, **rows differ** | 3 pairs | **Yes** - which row survives? |
| 3 | Missing coordinates | 5 rows | **Yes** - drop, or keep unmapped? |
| 4 | Latitude/longitude transposed | 2 rows | No |
| 5 | Leading/trailing whitespace in `facility_name` | 24 rows | No |
| 6 | `staff_total = 999` | 3 rows | **Yes** - sentinel, or real? |
| 7 | `facility_type` spelling variants | 9 variants → 3 real types, 120 rows | No |
| 8 | Decimal comma in `longitude` | 6 rows | No |

## Why three of them have no correct answer

Defects 2, 3 and 6 are the reason the design works.

A dataset containing only mechanical defects teaches participants that
documentation means listing steps. It does not - steps are usually recoverable by
inspecting the output. **Choices never are.**

With these three present, two participants can both clean the file competently
and arrive at 203, 200 or 195 rows. All three are defensible. **None is
reproducible unless the decision was written down** - which is the moment the
90-minute session is built around, and the thing tasks 4 and 5 of the assessment
are testing.

## Parallel-form verification

`make_dataset.py` compares the defect profile across all three files and **exits
non-zero if they differ**. The claim that D_PRE and D_POST are of equal
difficulty is therefore checked on every run rather than asserted once. Output
table in Annex C.

## Realism

Every defect class is one met in a real facility register: decimal commas from
locale-configured spreadsheets, transposed coordinates from manual entry,
duplicate identifiers from merged lists, `999` as an undeclared sentinel, and
name variants from free-text entry across offices.

Defects invented to be tidy teach people to spot invented defects.



```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```



# Annex E - Five-day course, session by session

Excluded from the Q6 page limit. The main response gives the day allocation,
the learning outcome for each day and the hands-on ratio; this is the
operational detail a facilitator needs - every session with its exercise,
dataset and duration.

Datasets D1, D2 and the assessment forms are specified
in **Annex D**; the Day 3 session marked in full is **Annex B**.

---

### Day 1 - What is actually in the data
**Outcome (apply):** Given an unfamiliar dataset, produce a written inventory of
its defects - counts, not impressions - without cleaning anything.

| Session | Min | Exercise | Dataset |
|---|---|---|---|
| The task you cannot yet do | 60 | Produce a facility map from raw data, unaided. Most will not finish | D1 (Annex D) |
| Why it failed | 20 | Facilitated, findings collected from the room, no individual named | - |
| Profiling before touching | 90 | Count rows, duplicates, blanks, out-of-range values, name variants | D1 |
| Writing a defect register | 90 | Produce a defect table: what, how many, how found | D1 |

Day 1 is the day the self-assessment gap gets closed by experience rather than by
being told. It ends with a product, so the discomfort of the morning resolves.

### Day 2 - Cleaning that can be checked
**Outcome (apply):** Clean a dataset so that every change is counted and no
record is silently dropped.

| Session | Min | Exercise | Dataset |
|---|---|---|---|
| Rules, not repairs | 20 | Instruction | - |
| Cleaning to a rule set | 120 | Fix each defect from Day 1 as a stated rule; record rows affected | D1 |
| Nothing disappears | 60 | Reconcile input rows against output rows; account for every difference | D1 |
| Ambiguous cases | 60 | Cases with no correct answer. Decide, and write down why | D1 |

### Day 3 - Reproducibility (the spine)
**Outcome (apply → analyse):** Produce a record from which a colleague
reproduces your cleaned dataset without speaking to you.

| Session | Min | Exercise | Dataset |
|---|---|---|---|
| **Make your work someone else's** | **90** | **Full artefact in Annex B** | D1 / D2 |
| Repairing the record | 60 | Rewrite the documentation that failed; re-test with a different partner | D1 |
| The department's own standard | 90 | The cohort drafts the minimum documentation standard *they* will use | - |

Drafting the standard themselves is deliberate. A standard issued to this
department will not be followed; one they wrote and immediately tested might be.

### Day 4 - Spatial data, and the map they came for
**Outcome (apply):** Produce a correctly projected, properly furnished map from a
cleaned dataset, and state what it does not show.

| Session | Min | Exercise | Dataset |
|---|---|---|---|
| Coordinates, joins, and why maps lie | 20 | Instruction | - |
| Joining and checking | 90 | Join facilities to wards; find and count the failures | D2 |
| Projection, in practice not theory | 45 | Measure the same distance in three CRS; see the answers differ | D2 |
| Map production | 120 | Full cartographic furniture; every map states its projection and source | D2 |

The projection block teaches by consequence, not by theory. Measuring one
distance three ways and getting three answers takes fifteen minutes and is
remembered; a lecture on datums is not.

### Day 5 - Their own work, and what happens next
**Outcome (apply → evaluate):** Complete a real departmental product to level 3,
and review a colleague's to level 4.

| Session | Min | Exercise | Dataset |
|---|---|---|---|
| Bring your own task | 150 | Each participant works a real, current departmental task | Their own |
| Peer reproduction | 60 | Exchange and attempt to reproduce. This is the post-assessment (§5) | Their own |
| The 90 days | 60 | Each participant leaves with a named product, a date, and a reviewer | - |

Day 5 uses the department's real work deliberately. Training data produces
training-shaped competence, and the transfer problem is the one this programme
exists to solve.

---

