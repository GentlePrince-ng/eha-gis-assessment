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
| **4.05** Weight | `99` | — (sentinel inside a measurement) | Not measured | High |
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
and the 99 measurements, and missed code `8` in both 6.01 and 6.02 — because it
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

The choice lists for 6.01 and 6.02 are stored with prefixed values —
`w01`–`w11`, `t01`–`t09` — rather than `1`–`11` and `1`–`9`.

The categories, their order, and the numbers **read aloud to the respondent** are
unchanged, so paper and digital rounds remain comparable. What changes is the
stored value: `t09` cannot collide with any sentinel because it is not a number.

Rejected alternative: renumbering categories to avoid 8 and 9. That would have
broken comparability with every previous paper round, for no gain over
prefixing.

### 3. "Do not know" stays a first-class answer

Where the paper form offers `8 = Do not know`, the digital form keeps it as an
explicit choice — because *the respondent not knowing* is a substantive finding,
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
