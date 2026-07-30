# Test plan — Form HH/2026/v1

**Partly generated.** Every numeric range in the form produces four cases
automatically — below minimum, at minimum, at maximum, above maximum — read
from the form's own constraints by `build_test_plan.py`. Add a range and its
boundary cases appear here; change a bound and the expected values follow.
The plan cannot drift from the form.

**54 cases** — 29 negative, 20 boundary, 5 positive/behavioural.

## Execution status

**These cases are specified. They have not been executed against a running
instance**, because no ODK Central project was available inside the
submission window. The check-digit logic behind S09 *is* executed —
exhaustively — in `tests/test_check_digit.py`. Everything else is a
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

### S01 — Specimen eligibility cut, lower side **[REQUIRED BY THE QUESTION]**

| | |
|---|---|
| **Type** | boundary |
| **Target** | `q5_01_specimen_eligible` |
| **Setup** | Roster child aged **11 completed months** |
| **Input** | advance to Section 5 |
| **Expected** | No specimen sought. 5.02-5.07 hidden; note shown that the child is under 12 months. The child module (Section 4) is still completed in full. |
| **Why it matters** | The paper form sends this child to Section 6, abandoning every remaining child in the household (defect B2). Here the skip ends only this child's iteration. |
| **Result** | _not yet executed_ |

### S02 — Specimen eligibility cut, upper side **[REQUIRED BY THE QUESTION]**

| | |
|---|---|
| **Type** | boundary |
| **Target** | `q5_01_specimen_eligible` |
| **Setup** | Roster child aged **12 completed months** |
| **Input** | advance to Section 5 |
| **Expected** | Specimen sought. 5.02 shown and required. |
| **Why it matters** | 12 months is the cut stated at 5.01. Paired with S01 it brackets it. |
| **Result** | _not yet executed_ |

### S03 — Measurement position change, below the cut **[REQUIRED BY THE QUESTION]**

| | |
|---|---|
| **Type** | boundary |
| **Target** | `q4_07_position` |
| **Setup** | Child aged **23 months**, height measured |
| **Input** | 4.07 = Standing height |
| **Expected** | WARNING shown, entry allowed |
| **Why it matters** | WHO convention is recumbent below 24 months. It warns rather than blocks: a child who cannot stand is legitimately measured recumbent at any age. |
| **Result** | _not yet executed_ |

### S04 — Measurement position change, at the cut **[REQUIRED BY THE QUESTION]**

| | |
|---|---|
| **Type** | boundary |
| **Target** | `q4_07_position` |
| **Setup** | Child aged **24 months**, height measured |
| **Input** | 4.07 = Standing height |
| **Expected** | No warning |
| **Why it matters** | 24 months and above is standing height. S03/S04 bracket the cut. |
| **Result** | _not yet executed_ |

### S05 — Date before the fieldwork window **[REQUIRED BY THE QUESTION]**

| | |
|---|---|
| **Type** | negative |
| **Target** | `q1_10_visit_date` |
| **Setup** | Device date set to 31 May 2026 |
| **Input** | 1.10 = 2026-05-31 |
| **Expected** | REJECT with the Hausa message |
| **Why it matters** | Most often a device with the wrong date, or a form completed later from paper notes. |
| **Result** | _not yet executed_ |

### S06 — Date after the fieldwork window **[REQUIRED BY THE QUESTION]**

| | |
|---|---|
| **Type** | negative |
| **Target** | `q1_10_visit_date` |
| **Input** | 1.10 = 2026-07-01 |
| **Expected** | REJECT |
| **Why it matters** | The window enforced is 1-30 June, the ethics-approved one, not the 14-day operational expectation. See the constraint register. |
| **Result** | _not yet executed_ |

### S07 — Roster disagrees with stated household size **[REQUIRED BY THE QUESTION]**

| | |
|---|---|
| **Type** | negative |
| **Target** | `roster_mismatch_note` |
| **Setup** | 3.01 = 6 usual residents |
| **Input** | Complete 4 roster lines and advance |
| **Expected** | WARNING shown naming both numbers. Entry continues. |
| **Why it matters** | Warns rather than blocks: the two legitimately differ when a usual resident is absent and cannot be described. A block would push enumerators to invent a line to clear the error. |
| **Result** | _not yet executed_ |

### S08 — Consent statement not read

| | |
|---|---|
| **Type** | negative |
| **Target** | `q2_01_statement_read` |
| **Input** | 2.01 = No |
| **Expected** | BLOCK. Cannot advance. |
| **Why it matters** | The only hard block in the form. The paper form records No and continues to 2.02 where consent may be given (defect B3). |
| **Result** | _not yet executed_ |

### S09 — Transposed pair of digits in the specimen serial

| | |
|---|---|
| **Type** | negative |
| **Target** | `q5_03_check_digit` |
| **Setup** | Valid label BSN480123-? with correct check character |
| **Input** | Enter serial 480132 (last two digits swapped) with the original check character |
| **Expected** | REJECT |
| **Why it matters** | Proven exhaustively in tests/test_check_digit.py: 292,960 transpositions tested, none escaped. |
| **Result** | _not yet executed_ |

### S10 — Label from another team's book

| | |
|---|---|
| **Type** | negative |
| **Target** | `q5_03_label_serial` |
| **Setup** | Signed in as a TM01 enumerator (range 480000-480899) |
| **Input** | 5.03 serial = 480900 |
| **Expected** | REJECT (out of allocated range) |
| **Why it matters** | This label passes the check digit - it is internally valid. Only the range constraint catches it. |
| **Result** | _not yet executed_ |

### S11 — Same label used twice in one household

| | |
|---|---|
| **Type** | negative |
| **Target** | `q5_03_label_serial` |
| **Setup** | Two eligible children, specimen taken from both |
| **Input** | Enter the same serial for the second child |
| **Expected** | REJECT |
| **Why it matters** | The most common genuine duplicate: two entries minutes apart from the same book. |
| **Result** | _not yet executed_ |

### S12 — Label reused from the previous submission

| | |
|---|---|
| **Type** | negative |
| **Target** | `q5_03_label_serial` |
| **Setup** | Complete and save a submission using serial X, start the next |
| **Input** | Enter serial X again |
| **Expected** | REJECT |
| **Why it matters** | last-saved covers one submission of history only. Submission n-2 and earlier are NOT caught - see docs/label_reuse.md. |
| **Result** | _not yet executed_ |

### S13 — 'None of these' selected with an owned asset

| | |
|---|---|
| **Type** | negative |
| **Target** | `q6_07_assets` |
| **Input** | 6.07 = Radio + None of these |
| **Expected** | REJECT |
| **Why it matters** | A logical impossibility the paper form permits (defect C2). |
| **Result** | _not yet executed_ |

### S14 — Wrong PIN for the selected enumerator code

| | |
|---|---|
| **Type** | negative |
| **Target** | `pin_entered` |
| **Input** | Select ENU001, enter PIN 0000 |
| **Expected** | REJECT |
| **Why it matters** | Prevents one enumerator submitting under another's code - the precondition for the fabrication pattern in the operating conditions. |
| **Result** | _not yet executed_ |

### S15 — LGA not assigned to this enumerator

| | |
|---|---|
| **Type** | negative |
| **Target** | `q1_02_lga` |
| **Setup** | Signed in as an enumerator assigned to Gwarin |
| **Input** | 1.02 = Idi-Oro |
| **Expected** | REJECT (relaxed for supervisors) |
| **Why it matters** | staff_roster.csv assigned_lga. |
| **Result** | _not yet executed_ |

### S16 — Skip logic when no specimen is obtained

| | |
|---|---|
| **Type** | positive |
| **Target** | `q5_02_specimen_obtained` |
| **Input** | 5.02 = No |
| **Expected** | 5.03-5.05 hidden; 5.06 reason shown and required |
| **Why it matters** | 5.02 has NO skip instruction on the paper form at all (defect B1). This is the case that defect produces. |
| **Result** | _not yet executed_ |

### S17 — Skip logic when a specimen IS obtained

| | |
|---|---|
| **Type** | positive |
| **Target** | `q5_02_specimen_obtained` |
| **Input** | 5.02 = Yes |
| **Expected** | 5.03-5.05 shown and required; 5.06-5.07 hidden |
| **Why it matters** | The mirror of S16. On paper, 5.06 applies to everyone. |
| **Result** | _not yet executed_ |

### S18 — Child module pointed at an adult

| | |
|---|---|
| **Type** | negative |
| **Target** | `q4_01_line` |
| **Setup** | Roster line 1 is a 34-year-old head of household |
| **Input** | 4.01 = 1 |
| **Expected** | REJECT |
| **Why it matters** | Validated with indexed-repeat() against the roster. The paper form cannot check this. |
| **Result** | _not yet executed_ |

### S19 — Result of visit is not 'Completed'

| | |
|---|---|
| **Type** | positive |
| **Target** | `q1_14_result` |
| **Input** | 1.14 = Dwelling vacant or demolished |
| **Expected** | Sections 2-6 hidden. Note instructs the enumerator to sign at 7.03 and hand the form to the supervisor. |
| **Why it matters** | Mirrors the paper instruction after 1.14. |
| **Result** | _not yet executed_ |

### S20 — Eligible-children count is derived, not typed

| | |
|---|---|
| **Type** | positive |
| **Target** | `q3_02_eligible` |
| **Setup** | Roster with children aged 8, 9, 59 and 60 completed months |
| **Input** | Advance past the roster |
| **Expected** | Eligible count = 2 (the 9- and 59-month children). Two child modules generated. |
| **Why it matters** | Brackets BOTH ends of the 9-59 eligibility window in one case, and demonstrates defect A1's fix: the count is derived from roster ages, never transcribed from an office-use column. This is also the second cross-question consistency check - stated eligible children and modules completed cannot disagree because they are the same quantity. |
| **Result** | _not yet executed_ |

### S21 — Clinically implausible but typeable weight

| | |
|---|---|
| **Type** | positive |
| **Target** | `q4_05_weight_kg` |
| **Setup** | Child aged 24 months |
| **Input** | 4.05 weight = 4.0 kg |
| **Expected** | WARNING shown, entry ALLOWED |
| **Why it matters** | The hard bounds are a typo guard; clinical implausibility warns. Blocking here would delete the severely wasted children the survey exists to count. |
| **Result** | _not yet executed_ |

### S22 — Placeholder medicine list is visible at the point of capture

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
  construction — see `docs/label_reuse.md`.
- **Encryption round-trip.** The public key in settings is a placeholder;
  decryption cannot be tested until the real keypair is issued.
