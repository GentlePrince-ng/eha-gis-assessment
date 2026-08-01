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
| External references resolve, values join, cross-references exist | `validate_media.py` (written for this submission) | PASSED, 5 checks |
| Every printed question implemented or declared | `check_coverage.py` (written for this submission) | PASSED, 58 accounted for |
| Deployed and exercised on a real server | Kobo Toolbox, all seven media attached | **PARTIAL** - see below |

Versions are recorded by the build itself into `form/conversion_log.txt`, taken
from the running interpreter rather than transcribed here, and `verify_claims.py`
fails if the version stated in this document and the version that actually
converted the form disagree.

**All are run by `python run_all.py`, stages 8 to 10.**

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

## Two more classes, both found by deploying the form and using it

Neither is visible to a validator, and neither was caught by the three checks
above. Both are now checked on every build.

### 4. A reference that resolves and joins to nothing

`staff_roster.csv` records `assigned_lga` as the LGA **label** (`Gwarin`) while
`lgas.csv` keys on the **code** (`LGA02`). Question 1.02 constrains the selected
LGA to the enumerator's assignment, so the comparison was a code against a
label: never equal. **All 96 enumerators were stopped at the first question**,
while the 24 supervisors passed, because the constraint exempts them by role.

Every tool reported success. The column existed, the path resolved, the file was
present. **A column existing is not the same as its values meaning what they are
compared against.** `validate_media.py` now checks five cross-file value domains
and fails if a child column holds a value absent from its parent.

Recorded as defect E5, and escalated: the mismatch is in the supplied reference
data and will recur every round until the roster ships with a code column.

### 5. An instruction pointing at a question that does not exist

The 1.14 stop note read *"Sign at 7.03 and hand the form to your supervisor."*
**There is no 7.03 in this form.** It is the paper enumerator-signature field,
deliberately replaced by authenticated submission along with 7.01 and 7.06 - and
the instruction survived the field's removal.

This is **defect A1's failure mode, reproduced in my own form**: the paper
questionnaire told the enumerator to read a column it had told them to leave
blank; the digital form told them to sign at a question it had removed. Finding
that class in someone else's instrument and shipping it in your own is the
reason the check is now automatic rather than a matter of proofreading.

`validate_media.py` extracts every question number appearing in visible text,
compares it against the numbers implemented as fields, and fails on any that are
referenced but absent. Paper numbers implemented under a different node name -
1.08 asked at sign-in, 7.01 captured automatically - are listed explicitly so a
legitimate back-reference is not reported as a defect.

## Validating it properly

### Attach `part2_q3/form/media/`, NOT the pack's `reference_media/`

**This is the one thing that will make the form look broken when it is not.**
The two folders hold files with the same names and different contents. The
supplied `reference_media/` cannot drive this form, and could not before any
choice I made:

| File | As supplied in the pack | Why it cannot be attached directly |
|---|---|---|
| `previous_round_households.csv` | keyed on `household_id` | **no `name` or `label` column**, which `select_one_from_file` requires |
| `specimen_label_allocation.csv` | keyed on `team_code` | **no `name` or `label` column** |
| `medicines.csv` | **does not exist** | never issued with the pack. See defect E1 |
| `staff_roster.csv` | `assigned_lga` holds `Gwarin` | the label where every other file keys on `LGA02`. See defect E5 |

The first three are why `prepare_media.py` exists at all. Attaching the raw
folder produces a form that converts, uploads, and then fails at 1.02 with *"This
LGA is not the one assigned to you"* - because the roster's LGA column is a label
being compared against a code.

`python part2_q3/prepare_media.py` writes the seven correct files. They are also
committed, so they can be attached straight from `part2_q3/form/media/` without
running anything.

### Then the two deployment routes

### ODK Central (recommended)
1. Create a project, **Draft** → upload `form/bansara_hh_2026.xlsx`.
2. On the draft, **Media Files** → upload all seven CSVs from `form/media/`.
3. **Preview** in Enketo, or publish and pull into ODK Collect.

### ODK Collect, no server
Copy `bansara_hh_2026.xml` into `Android/data/org.odk.collect.android/files/projects/<id>/forms/`
and the seven CSVs into a folder beside it named `bansara_hh_2026-media/`.
The folder name must match the form file exactly, or Collect will not find the
attachments and every external lookup will silently return nothing.

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

## What deployment testing found, and what it did not cover

The form was deployed to **Kobo Toolbox** with all seven media attachments and
worked through as an enumerator. That is not the same as executing the 54-case
plan, and the distinction is kept sharp below.

**It found two defects that every other check had passed.**

| Where | What happened | Fixed by |
|---|---|---|
| **1.02 LGA** | The constraint compared the selected LGA code against the roster's LGA *label*, so it rejected every selection. All 96 enumerators blocked at the first question; supervisors unaffected, because the rule exempts them by role | Defect E5. `assigned_lga_code` derived in `prepare_media.py`; five cross-file join checks added |
| **1.13 previous household** | A required autocomplete filtered to a settlement's previous-round households. The lookup covers 1,565 of 2,524 settlements, so in the other **959 (38%)** a household answering *yes* at 1.12 faced an empty required list: no way to answer, skip, or abandon | The list appears only when it has entries; a typed fallback with a format constraint always available; one calculate coalesces the two into a single analysis variable |

Neither is exotic. Both convert cleanly, validate cleanly, pass every static
check, and make the form unusable. **They were found by using it, which is the
only thing that finds them.**

**What is still not done.** The 54 cases in `test_plan.md` have **not** been
executed as a suite - no pass/fail record exists against them, and this document
does not claim one. What has been established is that the form loads on a real
server with real media, that the identification section can be completed, and
that the two defects above are gone. The check-digit logic behind case S09 is
separately executed in full by `tests/test_check_digit.py`.

**A test plan that has been written is not a test plan that has been run**, and
partially exercising a form is not the same as running its test plan. Both
statements are still true here, and the honest position is that deployment
testing found what static analysis could not and stopped short of the suite.
