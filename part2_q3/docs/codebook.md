# Codebook - `bansara_hh_2026` version `20260630-24d842`

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

46 fields.

| Field | Type | Question / meaning | Null when |
|---|---|---|---|
| `start_time` | start | - | `never (always collected)` |
| `end_time` | end | - | `never (always collected)` |
| `today_date` | today | - | `never (always collected)` |
| `form_version` | calculate | derived: `'20260630-24d842'` | `never (always collected)` |
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
| `q1_13_prev_n` | calculate | derived: `count(instance('previous_round_households')/root/item[se` | `never (always collected)` |
| `q1_13_prev_id` | select_one_from_file | 1.13 Household identifier allocated in the October 2025 round | `${q1_12_prev_round} = '1' and ${q1_13_prev_n} > 0` |
| `q1_13_prev_id_other` | text | 1.13 Write the 2025 household identifier as printed on the household card, f | `${q1_12_prev_round} = '1' and (${q1_13_prev_n} = 0 or ${q1_13_pr` |
| `q1_13_prev_id_final` | calculate | derived: `if(${q1_13_prev_id} != '', ${q1_13_prev_id}, ${q1_13_pre` | `never (always collected)` |
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
