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
