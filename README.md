# eHealth Africa - Technical Assessment

**Senior Coordinator, Data and GIS Analytics** · Data Informatics Department
Submitted by Solomon Oladimeji

| Part | Question attempted |
|---|---|
| **Part 1** | **Q1** - Campaign team tracking and coverage reconciliation |
| **Part 2** | **Q3** - Converting a paper questionnaire into a digital form |
| **Part 3** | **Q5** - Coordinating delivery through the round |
| **Part 3** | **Q6** - Building capability in the counterpart agency |

Part 1 Q2 and Part 2 Q4 are not attempted. The instructions value depth over
breadth, and Part 2 states the unattempted option will be probed at the
walkthrough regardless.

AI assistance is declared in **[`AI_USE.md`](AI_USE.md)**. Every judgement call
- thresholds, tolerances, projections, weights, conclusions - is logged with its
rejected alternative in **[`DECISIONS.md`](DECISIONS.md)**.

---

## Reproducing everything

### 1. Environment

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Developed on **Python 3.12.10**. **Java 8+ must be on PATH** - pyxform uses ODK
Validate to check the XForm's XPath, and without it the form converts but is not
deeply validated. `run_all.py` warns rather than passing quietly if Java is
absent.

### 2. Data

The supplied pack is **not committed**. Place it unmodified at the repository
root, or beside it - both are found automatically:

```
eha-gis-assessment/
  eHA_Assessment_Data_Pack_v4_CANDIDATE/
```

Override with `EHA_DATA_PACK` if it lives elsewhere. **No file in the pack is
edited at any point**; two reference files that ODK cannot consume as issued are
transformed in code by `part2_q3/prepare_media.py`, leaving the sources
untouched.

### 3. Run

```bash
python run_all.py
```

Rebuilds every output from the raw pack in about 40 seconds, across 18 stages.
It wipes prior artefacts first and **stops at the first failure** rather than
producing a partial result that looks complete.

---

## Layout

```
run_all.py            rebuild everything from raw
verify_claims.py      check figures quoted in the write-ups against the outputs
DECISIONS.md          every judgement call, with its rejected alternative
AI_USE.md             declaration of AI assistance and how the work was structured

part1_q1/
  src/                stage01_ingest → 02_qa → 03_attribute → 04_reconcile
                      → 05_cluster → 06_map
  docs/               QA rule options, CRS and tolerance, coordinate defects,
                      reconciliation, cluster analysis, artefact-vs-failure,
                      decision brief
  outputs/            DuckDB store, A3 PDF map, preview PNG   (rebuilt, not committed)

part2_q3/
  build_form.py       the XLSForm, defined in Python and converted by pyxform
  constraint_sources.py   justification for every rule; the register build FAILS
                          if a constraint has no entry here
  build_register.py · build_test_plan.py · build_codebook.py
  prepare_media.py    external media, built from the pack without editing it
  validate_media.py   every external reference resolves to a real file and column
  check_digit.py      one definition of the specimen check digit, used by both
                      the form and the tests
  scan_sentinels.py · daily_qa.py
  tests/              executable check-digit suite
  form/               XLSForm, XForm, conversion log, media   (rebuilt)
  docs/               13 documents - defect report, constraint register,
                      test plan, codebook, data protection, and the rest

part3_q5/             Q5 written response
part3_q6/             Q6 written response and Annexes A-E
  annex_b_session_in_full/   the 90-minute session: facilitator guide,
                             participant briefs, model answer, dataset generator

writeup/
  assemble.py         combines 31 sources into the submission document
  responses.docx      the single combined response document
```

---

## Part 1 Q1 - pipeline stages

| Stage | Does | Output |
|---|---|---|
| `stage01_ingest` | 160 track files, 956,702 fixes → DuckDB. **Idempotent by content hash**, not by `(team, timestamp)` - 585,951 records share a team and minute while carrying different coordinates | spatial store |
| `stage02_qa` | Eight rule groups. Flags, never deletes | QA flags with counts per rule |
| `stage03_attribute` | Accuracy-scaled attribution to settlements, EPSG:32632 | settlement visits |
| `stage04_reconcile` | Settlement and ward coverage against the e-tally, with a per-claim cause classification | reconciliation tables |
| `stage05_cluster` | Getis-Ord Gi\* on the ward missed rate, with FDR correction | cluster results |
| `stage06_map` | A3 PDF map and the Incident Manager decision brief | PDF, PNG |

Reasoning in [`part1_q1/docs/`](part1_q1/docs/) - including
`artefact_vs_failure.md`, which consolidates how a data artefact was told apart
from a programmatic failure, and what was done where it could not be.

## Part 2 Q3 - the form and its supporting artefacts

Fourteen deliverables. Three things are worth knowing before reading:

**The form is defined in Python, not authored in Excel.** A binary `.xlsx`
shows in git as "changed" and nothing more; this way a reviewer sees exactly
which constraint moved between commits, and conversion is part of the pipeline
rather than a manual export step.

**The register, test plan and codebook are generated from the form**, so they
cannot drift from it. `build_register.py` **fails the build** if any constraint
has no documented source - it caught an undocumented rule on its first run.

**`validate_media.py` exists because tooling missed a real defect.** pyxform and
ODK Validate both pass a form whose `instance()` call in a constraint was never
declared - at runtime it returns an empty nodeset and the constraint silently
rejects everything. It happened twice; now it is checked automatically. See
[`part2_q3/docs/validation.md`](part2_q3/docs/validation.md).

**The form will not preview in XLSForm Online.** It uses seven external CSV media
files, which that tool cannot attach. Conversion succeeds; loading fails. Deploy
per `validation.md`.

**Attach the media from `part2_q3/form/media/`, not the pack's
`reference_media/`.** The folders share filenames and differ in content. Three
of the supplied files cannot drive the form as issued: two have no `name`/`label`
column, which `select_one_from_file` requires, and `medicines.csv` was never
issued at all. Attaching the raw folder gives a form that uploads cleanly and
then rejects every LGA at question 1.02. The seven correct files are committed;
`prepare_media.py` rebuilds them without touching the sources.

## Part 3 - Q5 and Q6

Written responses, within their stated page limits (Q5 three pages; Q6 six
excluding annexes), verified by paginating the rendered documents rather than
estimating.

Annex B is a working artefact rather than a description: a facilitator guide with
minute-by-minute timings, participant briefs, a model answer, and a **generator**
for the training dataset - so a colleague delivering the session produces exactly
the file the model answer expects.

---

## Checks that run on every rebuild

| Check | What it prevents |
|---|---|
| Row accounting in `stage01` | A record disappearing without being counted |
| QA coverage assertion in `stage02` | A stored point with no quality decision |
| `validate_media.py` | Five failures no validator sees: an external lookup that resolves to nothing, a lookup that **resolves and joins to nothing**, and an instruction pointing at a question the form does not contain |
| `check_coverage.py` | A question silently dropped from the questionnaire. Every one of the 58 printed questions must be implemented or declared out of scope with a reason, read from the supplied instrument rather than a transcribed list |
| `build_register.py` | A constraint whose threshold has no stated source |
| `tests/test_check_digit.py` | 292,960 transpositions, none escaping detection - and that the tested algorithm is the one in the built XForm |
| `verify_claims.py` | A figure quoted in the write-ups drifting from the output that produced it. 54 checks, including the pyxform version stated in prose against the one that actually ran; the Q6 annex figures are compared against the number parsed out of the annex, not against a literal, so document and dataset cannot disagree |

## Manual steps

**None.** `run_all.py` goes from the supplied pack to `responses.docx` without
intervention.

Two things sit deliberately outside it, and neither is a build step: the private
key for form encryption is held outside the repository and gitignored, and the
test plan in `part2_q3/docs/test_plan.md` is **specified but not executed against
a live ODK instance**, which is stated at the top of that document rather than
left to be assumed.

## Known limitations

Recorded where they belong rather than collected here: `deliberate_scope.md` for
Part 2, the *"what this does not license"* sections of the Part 1 documents, and
the caveats inside each Part 3 response.

The one worth repeating: Q1 observes **where loggers were, not where people
were**. Two-thirds of reported activity has no track corroboration, and at least
three benign mechanisms produce that pattern. It is presented as a verification
worklist, never as an accusation.
