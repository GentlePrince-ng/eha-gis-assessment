# Spatial clustering of missed settlements

## Definition of "missed"

A settlement is counted missed when **no doses were reported against it in the e-tally and
no track confirms a visit**. It requires both sources to agree on absence, which is the
least contestable definition available given that the two disagree about a thousand
settlements.

The 75 settlements classified inaccessible on security grounds before the round are
**excluded from the analysis**, not counted as missed. They were never expected to be
reached, and including them would manufacture hot spots in exactly the wards the programme
had already written off.

**2,487 settlements analysed. 444 missed — 17.9%.**

## The analysis was run twice, because the first version was not trustworthy

### Attempt 1 — Gi\* on the binary indicator at settlement level. Rejected.

| | |
|---|---|
| Weights | k-nearest neighbours, k = 8, row-standardised |
| Inference | conditional permutation, 9,999 draws |
| Global Moran's I | **0.0032, p = 0.34 — not significant** |
| Hot spots, raw p ≤ 0.05 | 77 |
| Hot spots after BH FDR | 8 |
| "Cold spots" after BH FDR | 516 |

The 516 cold spots are an **artefact and are not reported as a finding.** The diagnostic:

- Every one has a pseudo p of exactly **0.00010**, the floor of 9,999 permutations.
- Their z-scores span only **−0.47 to −0.18** — nowhere near unusual.
- The binary indicator over 8 neighbours produces just **20 distinct local values** across
  2,487 locations.

For a settlement whose neighbourhood contains no missed settlement, the observed statistic
is already the minimum attainable, so *no* permutation can return a smaller one and the
pseudo p pins to the floor regardless of how ordinary the location is. That is a degenerate
permutation distribution, not a cluster. The surviving 8 hot spots carry a maximum z of
1.28, which is not strong evidence either.

**Reporting the 516 as cold spots would have been the single biggest error available in
this question.** They are a property of the arithmetic, not of the campaign.

### Attempt 2 — Gi\* on the ward-level missed *rate*. Reported.

| | |
|---|---|
| Unit | 40 wards |
| Variable | proportion of settlements missed (min 0.039, median 0.174, max 0.340) |
| Weights | **Queen contiguity**, row-standardised, 0 islands |
| Inference | conditional permutation, 9,999 draws |
| Distinct pseudo p-values | **40** — continuous variable, no degeneracy |
| Global Moran's I | **0.3560, p = 0.0004 — significant** |
| Hot spots, raw p ≤ 0.05 | 15 |
| **Hot spots after BH FDR** | **3** |
| Cold spots after BH FDR | 0 |

Three reasons this is the right unit: the variable is continuous, so the inference means
what it claims; the ward is the unit mop-up is actually deployed by; and 40 tests are
tractable where 2,487 are not. Queen contiguity replaces KNN because wards are polygons
that tile the study area — shared boundaries are the natural neighbour definition and no
distance threshold has to be invented.

## Result

**Three wards form a statistically significant cluster of high missed rates.**

| Ward | LGA | Settlements | Missed | Rate | Under-5 | Gi\* z | p |
|---|---|---|---|---|---|---|---|
| W027 Daberi | Katsuma | 40 | 10 | 0.250 | 2,215 | 1.27 | 0.0023 |
| W026 Kungomi | Katsuma | 48 | 10 | 0.208 | 2,598 | 1.23 | 0.0018 |
| W015 Baluru | Idi-Oro | 139 | 31 | 0.223 | 27,137 | 0.92 | 0.0037 |

**227 settlements, 51 of them missed, 31,950 under-5 children in the cluster.**

Baluru dominates the population at stake — 27,137 of the 31,950 — because it is a large
urban ward. Rate and burden are different quantities and the brief must not conflate them.

### Highest rate is not the same as hot spot

| Ward | Missed rate | Gi\* z | p | Hot spot? |
|---|---|---|---|---|
| W023 Suwade | **0.340** — the highest in the study area | 0.82 | 0.0103 | **No** |
| W025 Okriba | 0.324 | 0.04 | 0.2322 | No |
| W031 Satide | 0.308 | 0.99 | 0.0190 | No |

Suwade has the worst missed rate of any ward and is **not** a hot spot, because its
neighbours do not share the pattern — it is an isolated poor performer, not a cluster. That
distinction is the entire point of using a local spatial statistic rather than a ranking,
and it changes the response: Suwade needs a ward-level intervention, the Katsuma cluster
needs an area-level one.

## What the result does not license

**It does not license any statement about an individual settlement.** Gi\* is a statement
about a *neighbourhood*. A settlement inside a hot-spot ward may have been perfectly
covered; a settlement outside every hot spot may have been missed entirely. The unit of
inference is the ward, and the map must be read at that unit.

**It does not license any statement about an individual child.** Nothing here measures
vaccination status. "Missed" means no dose was reported and no track confirms a visit — an
absence of *evidence about a settlement*, not an observation of any child's status.

**It does not license a causal claim.** The analysis says where missed settlements
concentrate, not why. Terrain, distance, team assignment, insecurity spillover and logger
discipline are all untested candidates.

**It does not license treating the point-level result as corroboration.** The two levels
disagree — settlement-level Moran's I is not significant, ward-level is strongly so — and
that is not a contradiction to be smoothed over. Individual missed settlements are
interspersed with covered ones, so there is no clustering *among settlements*; but wards
differ systematically in their missed rate, and the high-rate wards adjoin one another.
This is a modifiable areal unit effect, and it means **the finding is genuinely a ward-level
finding** and would not survive being restated at settlement level.

**Sensitivity.** The hot-spot set was computed on the both-sources definition of missed. A
track-only definition would classify far more settlements as missed (1,765 rather than 444)
and is not used, because 83.7% of usable fixes fall more than a tolerance from any planned
settlement — a track-only definition measures logger discipline as much as coverage.
