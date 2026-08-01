# Q1 deliverables - where each one is

The six deliverables, and the artefact that carries each. Everything below is
produced by `python run_all.py` from the supplied pack, in about 40 seconds.

| | Deliverable | Artefact |
|---|---|---|
| **D1** | Idempotent ingestion into a spatially enabled store | `part1_q1/outputs/campaign.duckdb` |
| **D2** | Documented QA rule set, with counts and thresholds | `qa_rules.md` (generated), `qa_rule_options.md` (the working out) |
| **D3** | Track to settlement attribution | `crs_and_tolerance_options.md`, `coordinate_defects.md` |
| **D4** | Settlement and ward coverage, reconciled against the e-tally | `reconciliation.md` |
| **D5** | Statistically significant clusters of missed settlements | `cluster_analysis.md` |
| **D6** | A3 map, and a one-page decision brief | `part1_q1/outputs/missed_settlement_clusters_A3.pdf`, `decision_brief.md` |

## The A3 map

**`part1_q1/outputs/missed_settlement_clusters_A3.pdf`** - committed to the
repository, so it can be opened without rebuilding anything. A PNG preview sits
beside it for anyone who wants a quick look.

420 x 297 mm, drawn for a technical audience, with the full furniture the
question asks for: title, two legends, scale bar in projected metres, north
arrow, the projection stated on the map face, data sources, and a methods block.

**What the map shows, and what it is evidence for.** The three hot-spot wards
identified in `cluster_analysis.md` - Daberi, Kungomi and Baluru - drawn on the
ward missed-rate surface, with Suwade annotated because it has the **worst
missed rate in the state (34%) and is not a hot spot**. That single annotation
is the argument for using a local spatial statistic rather than sorting a list,
and it is why the map exists rather than a table.

The map states its own limits on the face: the finding holds at **ward** level,
and a settlement inside a hot-spot ward may have been covered perfectly.

## The spatial store

**`part1_q1/outputs/campaign.duckdb`** - about 140 MB, so it is **not committed**
and is rebuilt from the pack rather than shipped. DuckDB with the `spatial`
extension, chosen in D-001.

| Table | Rows | |
|---|---|---|
| `track_point` | 929,733 | every fix read, keyed by content hash |
| `track_qa` | 929,733 | one quality decision per point, nothing unjudged |
| `point_attribution` | 24,677 | points matched to a settlement |
| `settlement_visit` | 1,230 | settlement-level dwell |
| `claim_reconciliation` | 2,023 | every e-tally claim, with its cause classification |
| `ward_coverage`, `ward_cluster` | 40 | ward coverage and the Gi\* result |
| `settlement_cluster` | 2,487 | settlement-level analysis, reported but not mapped |
| `ingest_run` | 12 | one row per metric per run, so a second run is auditable |

**Idempotency is tested, not asserted.** `part1_q1/tests/test_store.py` runs the
ingest twice into a scratch database and checks the second inserts nothing: run 1
inserted 929,733 rows, run 2 inserted 0. It also checks the content hash is
unique, that no point lacks a quality decision, and that no derived table holds
an orphaned key.

## Verifying the numbers in this document

`verify_claims.py` re-queries the store after a clean rebuild and compares 76
figures quoted across these write-ups against what the pipeline actually
produced. It runs as a stage of `run_all.py`, so a figure that drifts from its
source fails the build rather than reaching a reader.
