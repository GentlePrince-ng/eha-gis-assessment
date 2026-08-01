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
