"""How stable is the ward hot-spot set under the permutation seed?

Stage 05 reports three hot-spot wards holding 31,950 children under 5. That
figure is the output of a permutation test, and a permutation test is a random
procedure: run it again and the pseudo p-values move a little.

Usually that does not matter. Here it does, because the Benjamini-Hochberg step
turns a continuous p-value into a binary decision, and the wards sit close to the
threshold. Before stage 05 was seeded, repeated runs of identical code returned
both three hot-spot wards and two - and because one of the three holds 85% of
the children, the headline moved between 31,950 and 4,813.

Seeding stage 05 makes the reported figure **reproducible**. It does not make it
**stable**, and reporting a seeded number as though it were settled would be the
more misleading of the two failures. This script measures the instability so it
can be stated.

    python part1_q1/src/seed_stability.py [n_seeds]

Ward level only. The settlement-level analysis is not reported as a result
(see docs/cluster_analysis.md), so its stability is not load-bearing.
"""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config  # noqa: E402
from stage05_cluster import (  # noqa: E402
    ALPHA, K_NEIGHBOURS, PERMUTATIONS, PROJECTED_CRS, SEED,
    benjamini_hochberg, load_settlements,
)


def main(n_seeds: int = 200) -> None:
    import geopandas as gpd
    import libpysal
    from esda.getisord import G_Local

    con = duckdb.connect(str(config.DB_PATH))
    con.execute("INSTALL spatial; LOAD spatial;")
    settlements = load_settlements(con)
    analysed = settlements[~settlements.inaccessible].reset_index(drop=True)

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
    values = wards.missed_rate.values

    print(f"\n  Seed stability of the ward hot-spot set")
    print(f"  {n_seeds} seeds, {PERMUTATIONS:,} permutations each, "
          f"BH FDR at alpha = {ALPHA}")
    print("=" * 74)

    hits = Counter()
    counts = Counter()
    under5_totals = []

    for i in range(n_seeds):
        np.random.seed(1000 + i)
        gstar = G_Local(values, weights, star=True, permutations=PERMUTATIONS)
        sig = benjamini_hochberg(gstar.p_sim, ALPHA) & (gstar.Zs > 0)
        names = set(wards.ward_name[sig])
        hits.update(names)
        counts[int(sig.sum())] += 1
        under5_totals.append(int(wards.under5[sig].sum()))

    print("\n  How often each ward is returned as a hot spot")
    print("  " + "-" * 70)
    print(f"  {'ward':14s} {'LGA':10s} {'under 5':>9s} {'selected':>10s}   share")
    for name, n in hits.most_common():
        row = wards[wards.ward_name == name].iloc[0]
        bar = "#" * int(round(30 * n / n_seeds))
        print(f"  {name:14s} {row.lga_name:10s} {int(row.under5):9,} "
              f"{n:6,}/{n_seeds:<4} {100*n/n_seeds:5.1f}%  {bar}")

    print("\n  Size of the reported hot-spot set")
    print("  " + "-" * 70)
    for k in sorted(counts):
        print(f"  {k} ward(s){'':4s} {counts[k]:6,}/{n_seeds:<4} "
              f"{100*counts[k]/n_seeds:5.1f}%")

    u = pd.Series(under5_totals)
    print("\n  Children under 5 in the reported set")
    print("  " + "-" * 70)
    print(f"  min {u.min():>8,}   median {int(u.median()):>8,}   max {u.max():>8,}")
    print(f"  the seeded run (SEED = {SEED}) reports 31,950")

    print("\n  Reading this")
    print("  " + "-" * 70)
    print("  A ward selected in nearly every run is a finding. A ward selected in")
    print("  half of them is a candidate for verification, not a conclusion, and")
    print("  the brief should not spend mop-up capacity on it as though it were")
    print("  settled. The instability is a property of the data, not of the seed.")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 200)
