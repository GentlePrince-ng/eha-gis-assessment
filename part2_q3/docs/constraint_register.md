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
