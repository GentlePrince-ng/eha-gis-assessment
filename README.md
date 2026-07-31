# eHealth Africa — Technical Assessment

**Senior Coordinator, Data and GIS Analytics** · Data Informatics Department
Submitted by Solomon Oladimeji

Questions attempted:

| Part | Question |
|---|---|
| 1 | **Q1** — Campaign team tracking and coverage reconciliation |
| 2 | **Q3** — Converting a paper questionnaire into a digital form |
| 3 | **Q5** — Coordinating delivery through the round |
| 3 | **Q6** — Building capability in the counterpart agency |

Part 1 Q2 and Part 2 Q4 are not attempted. The instructions state that depth is valued over
breadth and that the unattempted option in Part 2 will be probed at the walkthrough
regardless; I have prepared for that rather than submitting thin work on both.

AI assistance is declared in [`AI_USE.md`](AI_USE.md). Every judgement call — thresholds,
tolerances, projections, weights, and analytical conclusions — is logged with its reasoning
and its rejected alternative in [`DECISIONS.md`](DECISIONS.md).

---

## Reproducing this

### 1. Environment

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Developed and validated on Python 3.12.10.

### 2. Data

The supplied pack is **not** committed to this repository. Place it unmodified at the
repository root, keeping the folder structure exactly as issued:

```
eha-gis-assessment/
  eHA_Assessment_Data_Pack_v4_CANDIDATE/
    Part1_Q1_Campaign_Tracking/
    Part2_Q3_ODK_Form_Design/
    ...
```

No file in the pack is edited by hand at any point. Every transformation is in code.

### 3. Run

```bash
python run_all.py
```

Rebuilds everything from the raw pack to the final outputs with no manual intervention.
The script is idempotent: running it twice produces the same result and duplicates nothing.

*Any step that cannot be automated is listed under **Manual steps** below, with the reason.*

---

## Layout

```
part1_q1/
  src/            01_ingest → 02_qa → 03_attribute → 04_reconcile → 05_cluster → 06_map
  docs/           defect register, QA rule set, methods note
  outputs/        spatial store, coverage tables, A3 map, decision brief
part2_q3/
  form/           XLSForm and its conversion output
  docs/           constraint register, defect report, test plan, codebook
part3_q5/         Q5 written response
part3_q6/         Q6 written response and Annexes A-E
  annex_b_session_in_full/   the 90-minute session: guide, briefs,
                             model answer, dataset generator
writeup/          the single combined response document
```

---

## Part 1 Q1 — pipeline stages

| Stage | Does | Output |
|---|---|---|
| `01_ingest` | Loads 160 track files + reference data into DuckDB. Idempotent by content hash. | spatial store |
| `02_qa` | Applies the documented rule set. Flags, never deletes. | QA flags + counts per rule |
| `03_attribute` | Attributes cleaned tracks to planned settlements. | settlement visit table |
| `04_reconcile` | Track-derived coverage against the reported e-tally. | reconciliation + discrepancy classes |
| `05_cluster` | Significance testing for clusters of missed settlements. | cluster results |
| `06_map` | A3 PDF map and the Incident Manager decision brief. | PDF outputs |

Findings, thresholds and their justification: [`part1_q1/docs/`](part1_q1/docs/).

## Manual steps

*(none yet — any that arise are recorded here with the reason automation was not possible)*

## Known limitations

*(recorded as they are found, rather than discovered by the reader)*
