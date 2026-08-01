# Projection and attribution tolerance - measured options

Two thresholds the assessment explicitly warns about (*"thresholds, buffers, or tolerances
asserted without justification"* is an automatic mark loss). Both measured rather than
asserted. Decision goes to `DECISIONS.md` D-003 and D-005 once chosen.

---

## D-003 - Projected coordinate reference system

Everything arrives EPSG:4326. Distortion measured against **true geodesic distance on the
WGS84 ellipsoid** (`pyproj.Geod.inv`), over 4,000 random settlement pairs, and against
true geodesic polygon area for the 40 wards.

Study area: longitude 6.954-8.429, latitude 10.366-11.573.

### Distance error

| CRS | Median abs. error | 95th pct | Max | Max relative |
|---|---|---|---|---|
| **EPSG:32632 - WGS 84 / UTM zone 32N** | **7.8 m** | 21.9 m | 33.6 m | 0.035% |
| EPSG:26332 - Minna / Nigeria Mid Belt | 7.5 m | 21.6 m | 33.2 m | 0.034% |
| EPSG:3857 - Web Mercator | 1,382.6 m | 2,554.6 m | 3,350.1 m | 2.665% |
| ESRI:102022 - Africa Albers Equal Area | 1,737.1 m | 4,658.6 m | 6,758.5 m | 4.995% |

### Error at short range - the scale a settlement tolerance actually operates at

| CRS | Median error | Max abs. error |
|---|---|---|
| UTM 32N | −0.12 m | 0.13 m |
| Minna Mid Belt | −0.12 m | 0.13 m |
| Web Mercator | +17.49 m | 18.79 m |
| Africa Albers | +8.42 m | 13.46 m |

### Area error, ward polygons

| CRS | Median relative | Max abs. relative |
|---|---|---|
| UTM 32N | −0.031% | 0.068% |
| Minna Mid Belt | −0.030% | 0.068% |
| Web Mercator | +4.437% | 4.801% |
| Africa Albers | **0.000%** | 0.028% |

### Recommendation: **EPSG:32632, WGS 84 / UTM zone 32N**

- **Web Mercator is disqualified**, and it matters that this is measured rather than
  recited: a 17.5 m error at the scale of a 50 m tolerance is a third of the tolerance, and
  4.4% on ward area would corrupt any density or rate.
- **Africa Albers is the right tool for the wrong job here.** It is the best area
  projection measured (0.000% median), and the worst distance one. This analysis is
  dominated by buffers and distances, so it is not the working CRS - though it remains the
  correct choice if an area-normalised statistic is ever wanted. At this extent UTM's area
  error of 0.03% makes that unnecessary.
- **UTM 32N over Minna Mid Belt**, despite Minna being nominally 0.3 m better across 4,000
  pairs - a difference far below GPS noise and therefore not a reason. The real reason is
  **datum**: the track data is GPS, i.e. WGS84. UTM 32N is WGS84-based, so reprojection is a
  pure map projection with no datum change. EPSG:26332 sits on the Minna datum
  (Clarke 1880), so using it introduces a datum transformation whose own uncertainty is of
  the order of metres - buying nothing measurable and adding an error term.
- **The study area sits entirely inside zone 32** (6°E-12°E), so UTM's real weakness,
  straddling a zone boundary, does not arise. Worth stating, because it is the first thing
  a reviewer should check.

---

## D-005 - Attribution tolerance ← **needs your decision**

### What bounds the tolerance: how far apart settlements are

Distance to nearest other settlement, projected to UTM 32N:

| LGA | Type | n | Min | 5th pct | Median | 75th pct |
|---|---|---|---|---|---|---|
| Idi-Oro | Urban | 1,046 | 8 m | 190 m | 669 m | 1,124 m |
| Katsuma | Rural | 504 | 56 m | 212 m | 734 m | 1,218 m |
| Gwarin | Rural | 432 | 22 m | 176 m | 796 m | 1,299 m |
| Ilela | Mixed | 580 | 40 m | 195 m | 834 m | 1,381 m |

Overall median 734 m, 5th percentile 194 m, 1st percentile 79 m, minimum 8 m.

**Note the urban LGA is not much denser than the rural ones** - median 669 m against
734-834 m. The usual justification for a tighter urban tolerance ("settlements are packed
closer together in town") is not supported here, and I would be wrong to assert it.

### What a wider tolerance costs: settlement buffers begin to overlap

A point inside two settlements' buffers cannot be attributed unambiguously.

| Tolerance | Settlements with an overlapping buffer | % of masterlist |
|---|---|---|
| 25 m | 8 | 0.3% |
| 50 m | 42 | 1.6% |
| 100 m | 136 | 5.3% |
| 200 m | 543 | 21.2% |
| 300 m | 985 | 38.4% |
| 500 m | 1,674 | 65.3% |

### Coverage against tolerance, on the 150,948 usable points

| Tolerance | Ambiguous points | Settlements visited | % of masterlist | Agree with e-tally | Tracks only | **e-tally only** |
|---|---|---|---|---|---|---|
| 25 m | 28 | 813 | 31.7% | 770 | 43 | 1,253 |
| 50 m | 65 | 901 | 35.2% | 832 | 69 | 1,191 |
| 100 m | 501 | 1,069 | 41.7% | 950 | 119 | 1,073 |
| 200 m | 1,766 | 1,262 | 49.3% | 1,095 | 167 | 928 |
| 300 m | 4,765 | 1,415 | 55.2% | 1,196 | 219 | 827 |
| 500 m | 14,601 | 1,652 | 64.5% | 1,360 | 292 | 663 |

### Accuracy-scaled tolerance - `tolerance = base + 2 × reported accuracy`

This is the mechanism D-004d promised: a point's search radius widens with its own
reported error rather than the whole tier being excluded.

| Base | Normal tier gets | Degraded tier gets | Ambiguous points | Settlements visited | Agree with e-tally | e-tally only |
|---|---|---|---|---|---|---|
| 25 m | 41 m | 97 m | 117 | 987 | 901 | 1,122 |
| **50 m** | **66 m** | **122 m** | **253** | **1,071** | **954** | **1,069** |
| 100 m | 116 m | 172 m | 938 | 1,193 | 1,045 | 978 |

### The result that decides it

Compare like for like:

| Method | Settlements visited | Ambiguous points |
|---|---|---|
| Fixed 100 m | 1,069 | **501** |
| Scaled, base 50 m | 1,071 | **253** |

**Same coverage, half the ambiguity.** The accuracy-scaled tolerance is not a compromise -
it dominates the fixed tolerance on both axes at equivalent reach. That is an independent
vindication of D-004d: information in the accuracy field that a fixed cut throws away is
doing real work.

**Recommendation: accuracy-scaled, base 50 m, k = 2** (normal ≈ 66 m, degraded ≈ 122 m).

Why base 50: at 50 m only 1.6% of settlements have overlapping buffers, so the ambiguity is
structurally small before accuracy widens it; and k = 2 is approximately a 95% confidence
radius if reported accuracy is read as a 1-sigma horizontal error, which is the usual
convention for a GPS accuracy field. That convention is an assumption about the logger
firmware, not a documented fact about these devices, and the write-up will say so.

---

## The finding that outranks the threshold choice

**Track-derived coverage is far below the reported e-tally at every tolerance.**

At the recommended setting, 1,071 settlements have track evidence against **2,023 reported
in the e-tally** - 1,069 settlements report doses administered with no supporting track.
Even at an absurd 500 m tolerance, 663 remain unexplained.

This is not a tolerance artefact. It is the reconciliation finding the question asks for,
and no defensible tolerance closes the gap.

### Testing whether our own QA rules caused it

If the duty-hours rule were cutting real work, teams would report doses on days their
loggers show nothing usable. Measured across all 155 e-tally team-days:

**Exactly one team-day has fewer than 60 usable fixes** - T14 on 12 March, with **11 usable
fixes against 16 settlements and 2,207 doses reported**. That is the day its logger died at
07:38.

So the duty window is not manufacturing the discrepancy: 154 of 155 reporting team-days
have ample usable tracking. And T14 is the clean example of the distinction the question
asks for - a settlement with no tracks may have been missed *or* the logger may have
failed, and here it is provably the logger, because the failure is visible in the fix
sequence rather than inferred from absence.

---

## What I need from you

1. **D-003 - CRS.** UTM 32N as recommended?
2. **D-005 - tolerance.** Accuracy-scaled base 50 m, k = 2? Or fixed, if you would rather
   defend a simpler rule at the walkthrough.

---

## One caveat on a diagnostic, recorded so it does not mislead later

A per-team summary I ran used `any_value(qa05_accuracy_tier)` to label each team's tier.
`any_value` picks an arbitrary row, and it mislabelled T15 as *normal* when it is
*degraded*. The underlying data is fine; the diagnostic was wrong. Tier must be derived per
team as a median or a majority, never by `any_value`. Not used in any result above.
