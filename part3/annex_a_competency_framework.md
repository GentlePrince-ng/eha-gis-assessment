# Annex A — Competency framework

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

Level 3 is scored without judgement — hand the artefact to a colleague with the
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
| 4 | Distinguishes a defect from a finding — recognises when unusual data is real and must be preserved rather than corrected |

## D3 · Documenting a reproducible workflow — **weakest measured competency, 1.5 / 5**

| L | Observable behaviour |
|---|---|
| 0 | Cleans by editing cells directly. No record of what changed |
| 1 | Keeps the raw file untouched and works on a copy, when reminded |
| 2 | Keeps raw and working copies separate and can describe the changes from memory, on the same day |
| 3 | Leaves a written record naming every change, its reason, and the rows affected — **and a colleague reproduces the cleaned file from the raw file using only that record** |
| 4 | Reviews a colleague's record, identifies the step that cannot be repeated, and rewrites it so the next person does not hit the same gap |

## D4 · Spatial data handling

| L | Observable behaviour |
|---|---|
| 0 | Treats coordinates as ordinary numbers; unaware that a projection exists |
| 1 | Loads a point layer following a procedure, and it appears in roughly the right place |
| 2 | Loads and joins layers unaided; notices when points land in the sea or the wrong hemisphere |
| 3 | States the CRS in use and why, converts deliberately rather than by accident, and **reports join failures with a count** instead of quietly losing the unmatched rows |
| 4 | Chooses a projection appropriate to the measurement being made, and can say what the choice costs |

## D5 · Map production and cartography — **strongest stated demand**

| L | Observable behaviour |
|---|---|
| 0 | Produces a screenshot of the map canvas |
| 1 | Produces a map with a title and a legend, following a checklist |
| 2 | Produces a complete map unaided: title, legend, scale, north arrow, source, date |
| 3 | The map states its **projection and its data source**, and a colleague can rebuild it from the record — and it says what it does **not** show |
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
| D4 Spatial handling | ~1 | 2 | 2–3 |
| D5 Map production | ~2 (strongest) | 3 | 3 |
| D6 Interpretation | ~1 | 2 | 2–3 |

**Only D3 is targeted at level 3 within the week, and only on one workflow.**
Claiming level 3 across six domains in five days would be the same design failure
as promising spatial statistics and remote sensing — it would read well and
would not survive contact with the post-assessment.

Baselines other than D3 are inferred from the composite score of 36 and are
marked approximate, because only D3 was measured directly. **The pre-assessment
in Annex C establishes the others properly**, which is a second reason to run it
before day one rather than relying on the composite.
