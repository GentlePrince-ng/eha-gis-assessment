# Decision log

Every judgement call in this submission: what was decided, what was rejected, and why.

Two reasons this file exists. The assessment lists *"thresholds, buffers, or tolerances
asserted without justification"* as an automatic loss of marks — this is where the
justification lives, and the QA rule set and methods note cite it. And the walkthrough asks
for one decision explained in detail and one conclusion defended under challenge; this is
the revision sheet for that.

**Format.** One entry per decision. `Source` is either a published standard, a measured
property of the supplied data, or plainly *my judgement*. Never left blank.

---

## D-001 — Spatial store: DuckDB with the `spatial` extension

**Decided:** DuckDB + `spatial`, file-backed, rebuilt from raw by a single script.

**Rejected:** PostGIS — needs a server, an account and a credential held in two places for
a dataset this size, and the assessment must run end to end from the supplied files on the
marker's machine with no external service. SpatiaLite — viable, but weaker analytical SQL.
GeoPackage alone — a format, not a query engine.

**Source:** Measured. 956,702 track points across 160 files. DuckDB reads the CSV set
directly, and a from-scratch rebuild keeps a failed load from ever leaving half-written
state.

**Defence if challenged:** The trade-off is real — PostGIS has the richer spatial function
library and proper concurrent access, which is exactly why Part 3 Q5 proposes a
server-based store for the shared enterprise database. The requirements differ: this is a
single-analyst reproducible pipeline, that is nine analysts editing concurrently. Choosing
differently for the two is the point, not an inconsistency.

---

## D-002 — Ingestion idempotency key

**Decided:** `md5` hash of the record as supplied — all seven columns, hashed as raw text
before type coercion — as the primary key of `track_point`. Implemented in
`stage01_ingest.py`.

**The problem, measured.** The track files overlap: a file named for one campaign day
contains fixes for later days too, so the same team and minute appear in several files.
Across the whole pack:

| Measure | Count |
|---|---|
| Rows read, 160 files | 956,702 |
| Distinct records | 929,733 |
| Identical rows collapsed | 26,969 |
| **`(team_id, timestamp)` collisions remaining** | **585,951** |

585,951 of 929,733 records share a team and a minute with another record while carrying
**different coordinates**. That is 63% of the store. `(team_id, timestamp)` is therefore
not an identity — it is the thing most in dispute.

**Rejected:** deduplicating on `(team_id, timestamp)`. It satisfies the letter of
"idempotent" and is lossy in fact: it would discard one of two contradictory position
fixes for 585,951 records and nothing downstream would know a conflict had existed. Given
the question asks me to distinguish a data artefact from a programmatic failure, destroying
the evidence at load time is the wrong place to decide.

**Rejected:** `CREATE OR REPLACE` on every run. Trivially idempotent, but it proves nothing
about the insert logic — the table is simply rebuilt. The store is created if absent and
inserts are anti-joined on `point_id`, so idempotency is a property of the load rather than
of dropping the table.

**Verification.** Fresh store, same command twice: run 1 inserted 929,733 rows, run 2
inserted 0, store total unchanged. The row accounting asserts
`rows_read == distinct_records + identical_rows_collapsed` and fails the run if it does not.

**Source:** Measured against the supplied files.

**Defence if challenged.** The cost is a store 63% of whose rows are in dispute, pushed
downstream to QA. The alternative buys a cleaner table by making an analytical decision —
which fix to believe — inside a loader that has no basis for making it. Ingestion records
what arrived and how much of it disagreed; deciding comes later, with reasons and counts
attached.

---

## D-002a — Where the campaign window is applied

**Observed at ingest:** **633,207 of 929,733 records (68%) fall outside 9–13 March 2026**,
the stated campaign window. The loggers on several teams ran continuously for weeks
afterwards — T01's fixes run to 29 March, around the clock.

**Decided:** the window is *not* applied at ingest. Out-of-window points are loaded,
counted, and excluded at the QA stage as a named, counted rule.

**Why it matters:** two-thirds of this dataset is not campaign data. If that filter is
buried in a loader, every downstream figure silently rests on it. As a QA rule it appears
in the rule table with its count, which is what the question asks for.

---

## D-003 — Projected coordinate reference system

**Decided:** *(pending)*

Everything arrives EPSG:4326. Every distance, buffer and area operation needs a projected
CRS, and the choice must be stated on the map, in the README and in the methods note.

---

## D-004 — Track quality assurance thresholds

**Decided:** *(pending — one entry per rule)*

Rules **flag**, they do not delete. The pack states twice that records must not be silently
dropped. Each rule records: threshold, source, rows affected, and whether it excludes a
point from coverage attribution or merely marks it.

---

## D-005 — Settlement attribution method and tolerance

**Decided:** *(pending)*

Includes the separate treatment of the degraded-accuracy urban cohort — median
`accuracy_m` ≈ 36 m in Idi-Oro against ≈ 8 m elsewhere — and a sensitivity figure showing
how the coverage result moves with the tolerance.

---

## D-006 — Which coverage source is presented to the Incident Manager

**Decided:** *(pending)*

Neither source is clean and they fail in different directions. The e-tally reports doses
exceeding the target population in 201 records, references 7 settlements absent from the
masterlist, and covers 31 of 32 teams. The tracks cover all 32 teams but include a cohort
whose loggers ran continuously for weeks past the campaign and one team with an almost
total logger failure.

---

## D-007 — Spatial statistic, weights, and significance

**Decided:** *(pending)*

Must state the statistic, the weights definition, the significance approach including
correction for multiple testing, and — required explicitly by the question — what the
result does **not** license anyone to conclude about an individual settlement or an
individual child.

---

## D-008 — Part 2 Q3: scope deliberately not implemented

**Decided:** *(pending)*

Q3's final deliverable asks what was left out and why. *"A defensible scope scores better
than an exhaustive one."*
