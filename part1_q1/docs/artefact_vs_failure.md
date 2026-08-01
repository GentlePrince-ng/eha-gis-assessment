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
