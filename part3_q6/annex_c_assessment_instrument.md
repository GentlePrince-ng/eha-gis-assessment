# Annex C - Pre and post assessment instrument

Excluded from the Q6 page limit.

## What this measures, and what it refuses to

**Demonstrated capability only.** No confidence items, no satisfaction items, no
self-rating as an outcome. §1.2 of the main response disqualifies all three: at a
self-rating/tested correlation of **0.11**, a rise in self-assessment after
training measures comfort, not competence, and would let the programme report
success while nothing had changed.

The instrument is **a practical task**, scored against the level definitions in
Annex A. Participants do the work; the work is marked.

| | |
|---|---|
| Format | Practical, at a machine, individual |
| Duration | **3 hours** including a 15-minute break |
| Items | 8 tasks, scored 0-4 | **32 points** |
| Administered | Days −7 (pre) and 61-90 (post) |
| Datasets | `D_PRE_facilities_raw.csv` / `D_POST_facilities_raw.csv` |
| Marking | Blind - no names, no administration order |

---

## The eight tasks

Tasks 1-7 are performed by the participant. **Task 8 is performed on them.**

| # | Task | Domain | What a 4 looks like |
|---|---|---|---|
| **1** | **Profile the file.** Report what it contains and what is wrong with it. Change nothing. | D1 | Row count, column types, what one row represents, and a defect inventory **with counts** - not impressions |
| **2** | **Canonicalise names.** Reduce `lga_name` and `facility_type` to their true values. | D2 | Correct mapping, stated as a table, with rows affected. Trimming done **before** grouping, and the reason given |
| **3** | **Handle the coordinates.** Find and treat every coordinate defect. | D2, D4 | All three classes found - decimal comma, transposition, missing - each fixed or retained deliberately, with counts |
| **4** | **Identify the judgement calls.** Which defects have no single correct treatment? | D2, D6 | Names all three (duplicates, missing coordinates, `999`), states a decision for each **and the defensible alternative** |
| **5** | **Write the record.** So that a colleague could reproduce your cleaned file. | **D3** | Source, ordered steps with counts, decisions with alternatives, rows in and rows out with the difference explained |
| **6** | **Join to wards and report failures.** | D4 | Join performed, unmatched rows **counted and reported** rather than silently dropped |
| **7** | **Produce a map, and state one thing it does not show.** | D5, D6 | Complete furniture, projection stated, and an unprompted limitation that is actually true of this data |
| **8** | **Independent reproduction.** *Performed by an assessor, not the participant.* | **D3** | An assessor with the raw file and the participant's record, forbidden to contact them, produces a matching file |

### Why Task 8 carries the design

It is the only item that tests **level 3 directly**, and the only one that cannot
be inflated by a confident participant, coached by a supervisor, or improved by
knowing the marker. A participant can produce excellent work on tasks 1-7 and
still score zero on 8 - and that combination is precisely the department's
current condition, so the instrument has to be able to detect it.

It is also the item most likely to be dropped for being inconvenient. It costs an
assessor roughly 30 minutes per participant. **That cost is the measurement.**

---

## Scoring

Each task scored against Annex A's levels:

| Score | Meaning |
|---|---|
| **0** | Not attempted, or attempted with no correct element |
| **1** | Assisted standard - correct only where the task itself supplied the procedure |
| **2** | Independent standard - correct output, not reproducible |
| **3** | Reproducible standard - correct, counted, and documented |
| **4** | Improving standard - as 3, plus identifies a problem the task did not ask about |

**Total 32.** Reported as a total *and* as a per-domain profile, because a
department that moves from 12 to 18 by improving map production while
documentation stays at 1 has not achieved what this programme is for.

### Interpretation bands

| Total | Reading |
|---|---|
| 0-8 | Level 0-1. Cannot yet work unsupervised |
| 9-16 | Level 1-2. Produces correct work that cannot be handed over. **Expected baseline** |
| 17-24 | Level 2-3. Reproducible on familiar tasks |
| 25-32 | Level 3-4. Can review others' work |

**Expected pre-assessment total: 11-14.** Consistent with a composite of 36 and
a documentation score of 1.5. If the cohort scores materially above this, the
composite was mismeasured and the course design should be revisited before
delivery rather than after.

---

## Comparability across the two administrations

Five controls, because a pre/post comparison is worthless if the two are not the
same test:

1. **Identical tasks and identical rubric.** Nothing is added or reworded.
2. **Parallel datasets, not the same dataset.** `D_PRE` and `D_POST` are
   generated to the *same defect specification* with different values.
3. **The parallel-form claim is verified, not asserted.** `make_dataset.py`
   compares the defect profile of all three datasets and **fails if they differ**:

   | | D1 | D_PRE | D_POST |
   |---|---|---|---|
   | rows | 203 | 203 | 203 |
   | distinct `facility_id` | 200 | 200 | 200 |
   | duplicate id rows | 3 | 3 | 3 |
   | missing coordinates | 5 | 5 | 5 |
   | `staff_total = 999` | 3 | 3 | 3 |
   | whitespace in name | 24 | 24 | 24 |
   | `lga_name` variants | 16 | 16 | 16 |
   | `facility_type` variants | 9 | 9 | 9 |
   | comma in longitude | 6 | 6 | 6 |

   Same difficulty, different values - so the post-test cannot be passed from
   memory of the pre-test, and cannot be *harder* either, which is the failure
   that makes a genuine improvement invisible.

4. **Blind marking.** Submissions are stripped of names and administration order
   before marking, so a marker expecting improvement cannot unconsciously supply
   it.
5. **The same assessor does not mark the same participant twice.** Cheap to
   arrange with two assessors and it removes the strongest source of drift.

**D1 is deliberately not used for assessment.** It is the teaching dataset, seen
for two full days, and testing on it would measure recall of a specific file.

---

## The calibration measure - reported, never as an outcome

One self-rating item is retained at both administrations: *"Rate your ability to
document a cleaning workflow so a colleague could repeat it, 1 to 5."*

It is **not** scored and does not enter the total. It exists to recompute the
correlation between self-rating and tested score.

| | |
|---|---|
| Baseline | **r = 0.11** |
| Target | r > 0.4 |

A department that can judge its own competence asks for help before producing a
wrong number, and stops asking for training it does not need. That is a real
result, worth measuring - and it is reported in its own line, never as evidence
of capability, because that is exactly the conflation §1.2 rules out.

---

## What this instrument does not measure

Stated so nobody claims it does.

- **Whether the work is faster.** Speed is not assessed, and a participant who
  slows down because they have started documenting has improved.
- **Whether it holds under real conditions.** A three-hour assessment is not a
  deadline with a supervisor waiting. The 90-day applied work is what tests that.
- **Retention beyond 90 days.** A third administration at six months would, and
  is not in scope of the contracted programme. Worth proposing separately.
- **Anything about the 21 as individuals for HR purposes.** Scores are for
  programme design and for the participant. If they become a performance
  instrument the room will optimise for the score, the pre-assessment will be
  gamed downward, and the measurement is destroyed.
