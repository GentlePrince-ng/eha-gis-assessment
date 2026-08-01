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

## D-003 — Projected coordinate reference system: EPSG:32632, WGS 84 / UTM zone 32N

**Decided** by Solomon, 30 July. Full measurement table in
`part1_q1/docs/crs_and_tolerance_options.md`.

**Source:** measured against true geodesic distance on the WGS84 ellipsoid (`pyproj.Geod`)
over 4,000 settlement pairs, and geodesic polygon area over 40 wards. UTM 32N: 7.8 m median
distance error, 0.13 m at short range, −0.031% on ward area.

**Rejected — Web Mercator (EPSG:3857):** 1,382.6 m median distance error and **17.5 m even
at short range**, which is a third of a 50 m tolerance, plus 4.44% on ward area.

**Rejected — Africa Albers (ESRI:102022):** the best area projection measured (0.000%
median) and the worst for distance (1,737.1 m). Right tool, wrong job — this analysis is
dominated by buffers and distances. Remains the correct choice if an area-normalised
statistic is ever needed; at this extent UTM's 0.03% area error makes that unnecessary.

**Rejected — Minna / Nigeria Mid Belt (EPSG:26332):** nominally 0.3 m better than UTM across
4,000 pairs, which is far below GPS noise and therefore not a reason to prefer it. The
deciding factor is **datum**: the tracks are GPS, hence WGS84, and UTM 32N is WGS84-based,
so reprojection is a pure map projection with no datum change. EPSG:26332 sits on the Minna
datum (Clarke 1880) and would introduce a datum transformation carrying its own
metre-order uncertainty, for no measurable gain.

**Also checked:** the study area spans 6.954–8.429°E, entirely inside zone 32 (6°–12°E), so
UTM's real weakness — straddling a zone boundary — does not arise here.

---

## D-005 — Attribution tolerance: accuracy-scaled, `50 m + 2 × reported accuracy`

**Decided** by Solomon, 30 July. Normal-tier points get ≈ 66 m, degraded-tier ≈ 122 m.

**The measurement that decided it.** Compared at equivalent reach:

| Method | Settlements visited | Ambiguous points |
|---|---|---|
| Fixed 100 m | 1,069 | 501 |
| Scaled, base 50 m | 1,071 | 253 |

Same coverage, half the ambiguity. The scaled rule **dominates** the fixed rule on both
axes rather than trading between them — which independently vindicates D-004d, since the
accuracy information a fixed cut discards is demonstrably doing work.

**Why base 50 m:** at 50 m only 1.6% of settlements have overlapping buffers (42 of 2,562),
so ambiguity is structurally small before accuracy widens it. Settlement spacing bounds the
choice: median nearest neighbour 734 m, 5th percentile 194 m, 1st percentile 79 m.

**Why k = 2:** approximately a 95% radius if reported accuracy is a 1-sigma horizontal
error, the usual convention for a GPS accuracy field. **This is an assumption about the
logger firmware, not a documented property of these devices**, and the methods note says so.

**Not claimed:** a tighter urban tolerance. Idi-Oro's median nearest-neighbour distance is
669 m against 734–834 m in the rural LGAs, so the usual "settlements are packed closer in
town" argument is not supported by this data.

---

## D-004 — Track quality assurance thresholds

Rules **flag**, they do not delete. The pack states twice that records must not be silently
dropped. Each rule records threshold, source, rows affected, and whether it excludes a point
from coverage attribution or merely marks it. Full evidence and the rejected options are in
`part1_q1/docs/qa_rule_options.md`.

### D-004a — Campaign window: 9–13 March 2026

**Source:** stated in the pack README. Not a judgement call.
**Effect:** excludes. 633,207 of 929,733 stored records (68%) fall outside it — several
loggers ran continuously to 29 March.

### D-004b — Duty hours: 07:00–16:59

**Decided** by Solomon, 30 July.

**Source:** measured from this campaign. Earliest first-fix across team-days clusters at
07:09–07:38; collision-collapsed team-minutes per hour plateau at 08:00–14:59 (~9,100–9,440)
against an overnight baseline of ~4,000–5,100 left by loggers never switched off.

**Rejected:** 06:00–18:59 — retains roughly two idle hours each side; reported as a
sensitivity instead. Per-team-day first-to-last-fix — circular for the eight runaway
loggers, whose "day" is 24 hours, which is precisely the cohort needing constraint.

**Honest caveat:** the evening taper never reaches zero, so no time window cleanly separates
work from idle logging. The window is a proxy; the e-tally reconciliation is what tests it.

### D-004c — Implausible speed: 15 km/h, on reported *and* implied speed

**Source:** measured. Reported speed is bimodal with nothing between 6 and 120 km/h — **any
threshold in that range flags the same 1,437 points.** Median reported speed is 4.0 km/h,
99th percentile 5.58, consistent with house-to-house walking.

**Why 15:** far above sustained walking, far below the implausible cluster — and the real
argument is that *the result does not depend on the threshold*.

**Two rules, not one:** reported speed is the logger's own claim; implied speed is derived
from consecutive positions. A point can fail one without the other, and flagging both
catches teleports the logger reported as stationary. Implied speed is only evaluable on
conflict-free consecutive minutes; where it cannot be evaluated it is recorded as null, not
as passing.

### D-004d — Positional accuracy: **no exclusion**

**Decided** by Solomon, 30 July.

**Source:** measured. Every candidate cut touches exactly the same eight teams — no
normal-tier point exceeds 15 m — and a 30 m cut removes ~62% of each of their tracks.

**Rejected:** any fixed cut. It confounds the rule with the finding: those eight teams would
appear to have visited almost nothing, and since most of their work is in Idi-Oro the urban
LGA absorbs a coverage loss that the analyst created. A data-quality rule must not
manufacture a programmatic finding.

**Instead:** accuracy is carried into attribution, where a point's search tolerance scales
with its own reported error. Accuracy becomes a property of the measurement rather than a
gate on it.

**Defence if challenged.** The counter is real: retaining low-quality fixes lets them
attribute to settlements and inflate coverage. The answer is not to argue it away but to
report coverage both ways and quantify the movement — see D-004f.

### D-004e — Fix-sequence gaps: 5 minutes interruption, 15 minutes outage

**Source:** the 60-second nominal rate is stated in the pack README. 108,686 of 108,742
conflict-free intervals are exactly 60 s, and every other gap is a whole-minute multiple —
dropped fixes, not clock drift. Counts barely move across a 3× threshold change (155 above
5 min, 111 above 15 min), so the finding is again insensitive to the cut.

### D-004g — Stationary clusters: flagged at 5 minutes, never excluded

**Named explicitly in the question's minimum rule set**, and the one rule that is not
primarily a defect detector — for house-to-house vaccination a stationary period is also
the *visit* signal.

**"Stationary" is defined against the reading's own reported accuracy:** a step smaller
than the device's stated error is movement indistinguishable from jitter. A fixed metre
threshold would call the 36 m loggers stationary constantly and the 8 m loggers almost
never, so the definition scales with the measurement — the same principle as D-005.

**Measured:** median step between consecutive fixes is **73.9 m per minute** (≈4.4 km/h,
consistent with walking); 6,794 of 88,556 steps fall below the reading's own accuracy.
Stationary runs are short — median 1 minute, 95th percentile 6, longest 22 — with **262
runs of 5 minutes or more** and none over 30. Flagging at 5 minutes marks 2,063 points.

**The analytical finding this produces:** in this campaign a stationary cluster is *not*
the visit signal. Teams move almost continuously at walking pace, including while inside a
settlement, because house-to-house work means walking between houses. Presence is therefore
measured by **dwell within a settlement's tolerance** (D-009), not by standing still — and
confirmed visits average 24 minutes of dwell while rarely being stationary for more than
six. Had the rule been built on stationarity, it would have found almost nothing.

**Flags, never excludes.** Whether a run means "worked here" or "logger left in a vehicle"
depends on settlement context, which does not exist until attribution.

---

### D-004f — Sensitivity reporting is mandatory, not optional

Because D-004b and D-004d are judgement calls that move the headline, coverage is reported
under both duty windows and both accuracy treatments. If coverage is stable the thresholds
stop being a vulnerability; if it is not, that instability is itself a finding for the
decision brief, because it tells the Incident Manager how far to trust the number.

---

## D-009 — Dwell threshold for "visited": 5 distinct minutes

**Decided** by Solomon, 30 July. Calibrated, not chosen by preference.

**The empirical anchor.** Visits the e-tally independently confirms — same team, settlement
and day in both sources — have a median dwell of **24 minutes** (p25 18, p75 31). Visits it
does not confirm have a median of **3 minutes**. Real working visits are long.

**The exchange rate that picks 5.**

| Threshold | Keeps confirmed | Keeps unconfirmed |
|---|---|---|
| ≥ 3 min | 95.6% | 55.7% |
| **≥ 5 min** | **93.6%** | **36.4%** |
| ≥ 10 min | 92.1% | 32.3% |
| ≥ 15 min | 89.7% | 31.5% |

Moving 3 → 5 sheds 19 points of unconfirmed for 2 points of confirmed, about ten to one.
Moving 5 → 10 sheds 4 more for 1.5, under three to one. Past 10 the trade goes negative.
**The unconfirmed curve flattens after 5** — beyond that the threshold has stopped
discriminating and is only deleting evidence.

**Three caveats, all going into the methods note rather than being left to be found.**

1. **The calibration is partly circular.** Tuning a track-derived threshold against the
   e-tally, then using the tracks to audit the e-tally, is self-referential if pushed. The
   defence is that 5 is taken from the *shape* of the dwell distribution — the elbow — not
   from the point of maximum agreement, which would have been 10. Weaker dependence on the
   e-tally being right, not zero dependence.
2. **"Unconfirmed" is not "false".** Some of the 635 unconfirmed visits are real work a team
   never reported, which is a finding rather than noise. The table measures agreement, not
   accuracy.
3. **Dwell does not predict volume of work.** Median doses by dwell band are 39, 48, 30, 31,
   36 — flat. Twenty-six confirmed visits had 1–2 minutes of dwell and a median of 39 doses,
   teams working while the logger was off or out of hours. The rule knowingly discards ~6.4%
   of provable visits and the write-up says so.

**What it does not change.** Coverage ranges from 735 to 1,066 settlements across every
threshold tested, against 2,023 claimed. The gap of roughly a thousand settlements survives
any choice, so the finding does not rest on this threshold — which belongs in the decision
brief, because it tells the Incident Manager the conclusion is not an artefact of an
analyst's cut point. The brief reports the band alongside the point estimate: wrongly
calling a settlement covered leaves children unvaccinated, while wrongly calling it missed
only dilutes finite mop-up capacity, and those costs are not symmetric.

---

## D-008 — Geographic validity (rule QA08): null island excluded, transposition corrected only where corroborated

**Decided** by Solomon, 30 July. Evidence in `part1_q1/docs/coordinate_defects.md`.

Found at stage 03, not stage 02 — attribution asked why 83.7% of usable points matched no
settlement. Recorded as a miss in the original rule set, because nothing in a
time/speed/accuracy/sequence rule set notices that a well-formed record sits in the Gulf of
Guinea.

| Sub-rule | Points | Disposition |
|---|---|---|
| QA08a null island (`longitude = 0 AND latitude = 0`) | 71 | exclude — position unrecoverable |
| QA08b transposed, corroborated | 198 | **corrected**, flagged, original retained |
| QA08b transposed, uncorroborated | 1 | exclude |

**Membership is derived from the state polygon, not a hardcoded bounding box:** a point is
transposed if it falls outside the state as supplied *and* inside it once the axes are
exchanged. That way the rule states its own logic rather than embedding magic numbers.

**Corroboration standard:** the swapped position must lie within **500 m** of another fix
from the same team within ±10 minutes. Measured before choosing it — against contemporaneous
fixes, transposed points sit a median of **510.7 km** away as supplied and **60.4 m** once
swapped, and 198 of 199 fall inside 500 m. The threshold sits in the empty space between
those two regimes, so like the speed rule the result does not depend on its exact value.

**Rejected — exclude all 199.** Never edits field data, but discards a position we can
demonstrate we know.

**Rejected — correct all 199 unconditionally.** Would have carried the single uncorroborated
point on the strength of a pattern rather than its own evidence.

**Why correction is legitimate here.** The pack forbids hand-editing source files. This is
not a hand edit: it is scripted, applied at the QA stage rather than to the source, records
the original coordinates alongside the corrected ones, flags every affected row, and is
reversible by changing one rule. The alternative — silently dropping points whose true
position is provable — is also a distortion, and a less visible one.

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
