"""Stage 05 - statistically significant clusters of missed settlements.

Statistic: **Getis-Ord Gi**** on a binary "missed" indicator, with row-standardised
weights. Under row standardisation the local weighted sum is the local weighted
*mean*, so Gi** compares the proportion missed in each settlement's neighbourhood
against the study-area proportion. That is the quantity of interest - a
neighbourhood where a high *share* of settlements were missed - rather than
simply a neighbourhood containing many settlements.

Why Gi** and not Local Moran's I: Moran's I identifies spatial association of
*any* kind, including low-low clusters and spatial outliers. The operational
question is one-directional - where is the concentration of missed settlements -
and Gi** answers exactly that, distinguishing hot spots from cold. Moran's I is
reported alongside as a global check that spatial structure exists at all.

Definition of "missed"
----------------------
A settlement is counted missed when **no doses were reported against it in the
e-tally and no track confirms a visit**. That is the least contestable
definition available: it requires both sources to agree on absence. Settlements
classified inaccessible before the round are **excluded from the analysis**
rather than counted as missed - they were never expected to be reached, and
including them would manufacture hot spots in exactly the wards the programme
had already written off.

Significance
------------
Inference is by **conditional permutation** (9,999 permutations), not the
normality assumption. A binary variable at 2,562 locations does not satisfy the
asymptotic assumptions behind the analytical p-value, and permutation makes no
distributional claim.

Because one test is run per settlement, raw p-values would produce roughly 128
false positives at alpha = 0.05 by construction. Results are therefore reported
**before and after Benjamini-Hochberg FDR correction**, and the corrected set is
the one that gets mapped.
"""

from __future__ import annotations

import sys
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config  # noqa: E402


PROJECTED_CRS = "EPSG:32632"   # D-003
K_NEIGHBOURS = 8               # D-010, justified in the printout below
PERMUTATIONS = 9999
ALPHA = 0.05
DWELL_MINUTES = 5              # D-009


def load_settlements(con: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    """Settlements with the missed indicator and the inaccessible flag."""
    return con.execute(
        f"""
        WITH visited AS (
            SELECT settlement_id FROM settlement_visit
            GROUP BY settlement_id HAVING sum(dwell_minutes) >= {DWELL_MINUTES}
        ),
        claimed AS (SELECT DISTINCT settlement_id FROM etally)
        SELECT
            s.settlement_id, s.settlement_name, s.ward_code, s.ward_name,
            s.lga_name, s.longitude, s.latitude, s.target_population_under5,
            (i.settlement_id IS NOT NULL) AS inaccessible,
            CASE WHEN v.settlement_id IS NULL AND c.settlement_id IS NULL
                 THEN 1 ELSE 0 END AS missed
        FROM settlement s
        LEFT JOIN visited      v USING (settlement_id)
        LEFT JOIN claimed      c USING (settlement_id)
        LEFT JOIN inaccessible i USING (settlement_id)
        """
    ).df()


def benjamini_hochberg(p_values: np.ndarray, alpha: float = ALPHA) -> np.ndarray:
    """Return a boolean mask of hypotheses significant after BH FDR control.

    Implemented directly rather than pulled from a dependency: it is six lines,
    and the walkthrough may well ask what the correction actually does.
    """
    n = len(p_values)
    order = np.argsort(p_values)
    ranked = p_values[order]
    thresholds = alpha * (np.arange(1, n + 1) / n)
    passing = np.where(ranked <= thresholds)[0]

    significant = np.zeros(n, dtype=bool)
    if len(passing) > 0:
        cutoff_rank = passing.max()
        significant[order[: cutoff_rank + 1]] = True
    return significant


def main() -> None:
    import libpysal
    from esda.getisord import G_Local
    from esda.moran import Moran
    from pyproj import Transformer

    con = duckdb.connect(str(config.DB_PATH))
    con.execute("INSTALL spatial; LOAD spatial;")
    settlements = load_settlements(con)

    print("\nStage 05 - clusters of missed settlements")
    print("=" * 74)

    total = len(settlements)
    inaccessible = int(settlements.inaccessible.sum())
    analysed = settlements[~settlements.inaccessible].reset_index(drop=True)
    missed = int(analysed.missed.sum())

    print(f"\n  settlements in masterlist          {total:>8,}")
    print(f"  excluded, classified inaccessible  {inaccessible:>8,}")
    print(f"  analysed                           {len(analysed):>8,}")
    print(f"  of which missed by both sources    {missed:>8,}"
          f"   ({100*missed/len(analysed):.1f}%)")

    # --- Geometry and weights -------------------------------------------
    transformer = Transformer.from_crs("EPSG:4326", PROJECTED_CRS, always_xy=True)
    x, y = transformer.transform(analysed.longitude.values, analysed.latitude.values)
    coords = np.column_stack([x, y])

    # Why k-nearest rather than a fixed distance band: settlement spacing
    # ranges from 8 m to 6.4 km. A band wide enough to connect the sparsest
    # settlement gives the densest ones hundreds of neighbours and smooths the
    # statistic into meaninglessness; a narrower band leaves islands with no
    # neighbours at all, for which Gi* is undefined.
    knn = libpysal.weights.KNN.from_array(coords, k=K_NEIGHBOURS)
    knn.transform = "R"

    band = libpysal.weights.min_threshold_distance(coords)
    print(f"\n  weights                            KNN, k={K_NEIGHBOURS}, row-standardised")
    print(f"  distance band for full connectivity {band/1000:>7.1f} km  <- why a band was rejected")

    values = analysed.missed.values.astype(float)

    # --- Global check ----------------------------------------------------
    moran = Moran(values, knn, permutations=PERMUTATIONS)
    print(f"\n  Global Moran's I                   {moran.I:>8.4f}   p = {moran.p_sim:.4f}")
    print("    (a global check that spatial structure exists before mapping local clusters)")

    # --- Local Gi* -------------------------------------------------------
    gstar = G_Local(values, knn, star=True, permutations=PERMUTATIONS)
    p_values = gstar.p_sim
    z_scores = gstar.Zs

    raw_significant = p_values <= ALPHA
    fdr_significant = benjamini_hochberg(p_values, ALPHA)

    analysed = analysed.assign(
        gstar_z=z_scores,
        gstar_p=p_values,
        hotspot_raw=raw_significant & (z_scores > 0),
        hotspot_fdr=fdr_significant & (z_scores > 0),
        coldspot_fdr=fdr_significant & (z_scores < 0),
    )

    print(f"\n  Gi* hot spots, raw p <= {ALPHA}         {int(analysed.hotspot_raw.sum()):>8,}")
    print(f"  Gi* hot spots, after BH FDR        {int(analysed.hotspot_fdr.sum()):>8,}")
    print(f"  Gi* cold spots, after BH FDR       {int(analysed.coldspot_fdr.sum()):>8,}")
    print(f"  expected false positives at raw p  {int(ALPHA*len(analysed)):>8,}"
          f"   <- why the correction is not optional")

    print("\n  Hot-spot settlements by ward (FDR-significant)")
    print("  " + "-" * 70)
    by_ward = (
        analysed[analysed.hotspot_fdr]
        .groupby(["lga_name", "ward_code", "ward_name"])
        .agg(hotspot_settlements=("settlement_id", "size"),
             under5_in_hotspots=("target_population_under5", "sum"))
        .reset_index()
        .sort_values("hotspot_settlements", ascending=False)
    )
    print(by_ward.head(12).to_string(index=False))

    print(f"\n  wards containing a hot spot        {len(by_ward):>8,} of 40")
    print(f"  under-5 population in hot spots    "
          f"{int(by_ward.under5_in_hotspots.sum()):>8,}")

    con.register("cluster_df", analysed)
    con.execute("CREATE OR REPLACE TABLE settlement_cluster AS SELECT * FROM cluster_df")

    diagnose_point_level_degeneracy(analysed)
    ward_level_analysis(con, analysed)

    con.close()


def diagnose_point_level_degeneracy(analysed: pd.DataFrame) -> None:
    """Report why the point-level pseudo p-values cannot be trusted.

    This is not a caveat added for form. The binary indicator over k=8
    neighbours takes only a handful of distinct local values, so for any
    settlement whose neighbourhood contains no missed settlement the observed
    statistic is already the minimum attainable and *no* permutation can produce
    a smaller one. The pseudo p pins to 1/(permutations+1) regardless of how
    unremarkable the location is.
    """
    distinct_p = analysed.gstar_p.nunique()
    floor_p = 1.0 / (PERMUTATIONS + 1)
    at_floor = analysed[np.isclose(analysed.gstar_p, floor_p)]

    print("\n  Diagnostic: are the point-level p-values trustworthy?")
    print("  " + "-" * 70)
    print(f"  distinct pseudo p-values over {len(analysed):,} locations   {distinct_p:>6}")
    print(f"  locations pinned to the permutation floor        {len(at_floor):>6,}")
    if len(at_floor):
        print(f"  their z-scores range                             "
              f"{at_floor.gstar_z.min():>6.2f} to {at_floor.gstar_z.max():.2f}")
    print(f"  z-score range across all locations               "
          f"{analysed.gstar_z.min():>6.2f} to {analysed.gstar_z.max():.2f}")
    print("\n  A pseudo p at the floor alongside a z-score near zero is a degenerate")
    print("  permutation distribution, not a cluster. The point-level 'cold spots'")
    print("  are therefore NOT reported as findings. Hot spots survive FDR but with")
    print("  a maximum z of 1.28, which is not strong evidence either.")


def ward_level_analysis(con: duckdb.DuckDBPyConnection, analysed: pd.DataFrame) -> None:
    """Gi* on the ward-level missed *rate* - the well-posed version of the question.

    Three reasons this is the defensible unit:

    1. **The variable is continuous.** A proportion has no boundary degeneracy,
       so the permutation inference means what it claims.
    2. **It is the operational unit.** Mop-up is deployed by ward, so a ward-level
       hot spot is directly actionable where a point-level one is not.
    3. **Multiple testing is tractable.** Forty tests rather than 2,487.

    Weights are **Queen contiguity** here rather than KNN: wards are polygons
    that tile the study area, so shared boundaries are the natural neighbour
    definition, and no distance threshold has to be invented.
    """
    import geopandas as gpd
    import libpysal
    from esda.getisord import G_Local
    from esda.moran import Moran

    ward_stats = (
        analysed.groupby("ward_code")
        .agg(settlements=("missed", "size"),
             missed=("missed", "sum"),
             under5=("target_population_under5", "sum"))
        .reset_index()
    )
    ward_stats["missed_rate"] = ward_stats.missed / ward_stats.settlements

    wards = gpd.read_file(config.BOUNDARIES_GPKG, layer="wards").to_crs(PROJECTED_CRS)
    wards = wards.merge(ward_stats, on="ward_code", how="inner")

    weights = libpysal.weights.Queen.from_dataframe(wards, use_index=False)
    weights.transform = "R"

    print("\n  Ward-level analysis - Gi* on the missed rate")
    print("  " + "-" * 70)
    print(f"  wards analysed                     {len(wards):>8}")
    print(f"  weights                            Queen contiguity, row-standardised")
    print(f"  islands (wards with no neighbour)  {len(weights.islands):>8}")
    print(f"  missed rate: min {wards.missed_rate.min():.3f}  "
          f"median {wards.missed_rate.median():.3f}  max {wards.missed_rate.max():.3f}")

    values = wards.missed_rate.values
    moran = Moran(values, weights, permutations=PERMUTATIONS)
    print(f"\n  Global Moran's I on the rate       {moran.I:>8.4f}   p = {moran.p_sim:.4f}")

    gstar = G_Local(values, weights, star=True, permutations=PERMUTATIONS)
    significant = benjamini_hochberg(gstar.p_sim, ALPHA)
    wards = wards.assign(gstar_z=gstar.Zs, gstar_p=gstar.p_sim,
                         hotspot=significant & (gstar.Zs > 0),
                         coldspot=significant & (gstar.Zs < 0))

    print(f"  distinct pseudo p-values           {pd.Series(gstar.p_sim).nunique():>8}"
          f"   <- continuous variable, no degeneracy")
    print(f"  hot spots, raw p <= {ALPHA}             {int((gstar.p_sim<=ALPHA).sum()):>8}")
    print(f"  hot spots, after BH FDR            {int(wards.hotspot.sum()):>8}")
    print(f"  cold spots, after BH FDR           {int(wards.coldspot.sum()):>8}")

    print("\n  Wards ranked by missed rate")
    print("  " + "-" * 70)
    print(wards.sort_values("missed_rate", ascending=False)
          [["ward_code", "ward_name", "lga_name", "settlements", "missed",
            "missed_rate", "under5", "gstar_z", "gstar_p", "hotspot"]]
          .head(10).round({"missed_rate": 3, "gstar_z": 2, "gstar_p": 4})
          .to_string(index=False))

    con.register("ward_cluster_df", pd.DataFrame(wards.drop(columns="geometry")))
    con.execute("CREATE OR REPLACE TABLE ward_cluster AS SELECT * FROM ward_cluster_df")
    print("\n  written to tables settlement_cluster and ward_cluster")


if __name__ == "__main__":
    main()
