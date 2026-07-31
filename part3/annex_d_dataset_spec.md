# Annex D — Dataset specifications

Excluded from the Q6 page limit.

**Generated, not described.** `session_90min/make_dataset.py` produces all three
datasets from a fixed seed, so a colleague delivering the course in my absence
gets exactly the files the model answer and the rubric expect. A specification in
prose would drift from the file within one revision.

    python part3/session_90min/make_dataset.py

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
| 1 | `lga_name` variants — spacing, case, hyphenation | 16 variants → 4 real LGAs | No |
| 2 | Duplicate `facility_id`, **rows differ** | 3 pairs | **Yes** — which row survives? |
| 3 | Missing coordinates | 5 rows | **Yes** — drop, or keep unmapped? |
| 4 | Latitude/longitude transposed | 2 rows | No |
| 5 | Leading/trailing whitespace in names | 24 rows | No |
| 6 | `staff_total = 999` | 3 rows | **Yes** — sentinel, or real? |
| 7 | `facility_type` spelling variants | 9 variants → 3 real types | No |
| 8 | Decimal comma in `longitude` | 6 rows | No |

## Why three of them have no correct answer

Defects 2, 3 and 6 are the reason the design works.

A dataset containing only mechanical defects teaches participants that
documentation means listing steps. It does not — steps are usually recoverable by
inspecting the output. **Choices never are.**

With these three present, two participants can both clean the file competently
and arrive at 203, 200 or 195 rows. All three are defensible. **None is
reproducible unless the decision was written down** — which is the moment the
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
