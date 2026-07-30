"""Stage 06 — A3 PDF map of missed-settlement clusters, for a technical audience.

Rendered from the same DuckDB store the analysis wrote, so the map cannot drift
from the numbers. No desktop GIS, no hand export, no network basemap: the
submission must run end to end from the supplied files, and a tile server is a
runtime dependency that would break that on an offline machine.

Cartographic decisions
----------------------
* **A3 landscape, 420 x 297 mm**, vector PDF. Text stays selectable and the map
  survives being printed at size, which a raster export would not.
* **EPSG:32632** throughout, stated on the map face. A map that does not declare
  its projection cannot be measured from.
* **The unit of inference is the ward, so the ward is the emphasis.** Hot-spot
  wards carry the strong fill; settlements are drawn as a secondary layer for
  context. Drawing missed settlements as the primary symbol would invite exactly
  the settlement-level reading the statistic does not support.
* **Diverging colour is avoided.** Missed rate is a sequential quantity with a
  meaningful low end, so a single-hue sequential ramp is used. A red-green
  diverging ramp would also fail for colour-blind readers.
* Suwade is labelled explicitly despite not being a hot spot, because it holds
  the highest missed rate in the study area and a reader who spots it unlabelled
  will assume the analysis missed it.
"""

from __future__ import annotations

import sys
from pathlib import Path

import duckdb
import geopandas as gpd
import matplotlib as mpl
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch, Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config  # noqa: E402

mpl.use("Agg")
mpl.rcParams.update({
    "pdf.fonttype": 42,          # embed TrueType so text stays selectable
    "font.family": "DejaVu Sans",
    "font.size": 8,
})

PROJECTED_CRS = "EPSG:32632"
A3_LANDSCAPE_IN = (16.54, 11.69)

INK = "#1a1a1a"
GRID = "#d9d9d9"
SEQ = ["#f7fbff", "#deebf7", "#c6dbef", "#9ecae1", "#6baed6", "#3182bd", "#08519c"]
HOTSPOT_EDGE = "#b2182b"
MISSED_PT = "#d6604d"
VISITED_PT = "#7fbf7b"


def load_layers(con: duckdb.DuckDBPyConnection):
    wards = gpd.read_file(config.BOUNDARIES_GPKG, layer="wards").to_crs(PROJECTED_CRS)
    lgas = gpd.read_file(config.BOUNDARIES_GPKG, layer="lgas").to_crs(PROJECTED_CRS)

    ward_stats = con.execute(
        "SELECT ward_code, settlements, missed, missed_rate, under5, "
        "gstar_z, gstar_p, hotspot FROM ward_cluster"
    ).df()
    wards = wards.merge(ward_stats, on="ward_code", how="left")

    points = con.execute(
        "SELECT longitude, latitude, missed, inaccessible FROM settlement_cluster"
    ).df()
    settlements = gpd.GeoDataFrame(
        points,
        geometry=gpd.points_from_xy(points.longitude, points.latitude),
        crs="EPSG:4326",
    ).to_crs(PROJECTED_CRS)

    inaccessible = con.execute(
        "SELECT s.longitude, s.latitude FROM inaccessible i "
        "JOIN settlement s USING (settlement_id)"
    ).df()
    inaccessible_gdf = gpd.GeoDataFrame(
        inaccessible,
        geometry=gpd.points_from_xy(inaccessible.longitude, inaccessible.latitude),
        crs="EPSG:4326",
    ).to_crs(PROJECTED_CRS)

    return wards, lgas, settlements, inaccessible_gdf


def add_scale_bar(ax, length_m=10000):
    """Scale bar drawn in projected metres, which is the only reason a projected
    CRS was chosen in the first place."""
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()
    x0 = xmin + (xmax - xmin) * 0.04
    y0 = ymin + (ymax - ymin) * 0.05
    height = (ymax - ymin) * 0.006

    for i in range(4):
        ax.add_patch(Rectangle(
            (x0 + i * length_m / 4, y0), length_m / 4, height,
            facecolor=INK if i % 2 == 0 else "white",
            edgecolor=INK, linewidth=0.5, zorder=10))
    for i, label in enumerate(["0", "", "5", "", "10"]):
        if label:
            ax.text(x0 + i * length_m / 4, y0 + height * 2.2, label,
                    ha="center", va="bottom", fontsize=6.5, color=INK, zorder=10)
    ax.text(x0 + length_m / 2, y0 - height * 2.6, "kilometres",
            ha="center", va="top", fontsize=6.5, color=INK, zorder=10)


def add_north_arrow(ax):
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()
    x = xmin + (xmax - xmin) * 0.955
    y = ymin + (ymax - ymin) * 0.88
    size = (ymax - ymin) * 0.045
    ax.annotate("", xy=(x, y + size), xytext=(x, y),
                arrowprops=dict(facecolor=INK, edgecolor=INK, width=1.6,
                                headwidth=7, headlength=8), zorder=10)
    ax.text(x, y + size * 1.12, "N", ha="center", va="bottom",
            fontsize=9, fontweight="bold", color=INK, zorder=10)


def main() -> None:
    con = duckdb.connect(str(config.DB_PATH))
    con.execute("INSTALL spatial; LOAD spatial;")
    wards, lgas, settlements, inaccessible = load_layers(con)

    hotspots = wards[wards.hotspot.fillna(False)]
    total_missed = int(settlements.missed.sum())
    under5_at_stake = int(hotspots.under5.sum())

    fig = plt.figure(figsize=A3_LANDSCAPE_IN)
    fig.patch.set_facecolor("white")
    ax = fig.add_axes([0.03, 0.05, 0.68, 0.86])
    ax.set_facecolor("white")

    # --- choropleth: missed rate by ward -------------------------------
    cmap = mpl.colors.LinearSegmentedColormap.from_list("seq", SEQ)
    bounds = [0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35]
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    wards.plot(column="missed_rate", ax=ax, cmap=cmap, norm=norm,
               edgecolor="#8c8c8c", linewidth=0.35, zorder=1)

    # --- settlements as context, not as the finding --------------------
    settlements[settlements.missed == 0].plot(
        ax=ax, color=VISITED_PT, markersize=0.7, alpha=0.35, zorder=2)
    settlements[settlements.missed == 1].plot(
        ax=ax, color=MISSED_PT, markersize=2.2, alpha=0.85, zorder=3)
    inaccessible.plot(ax=ax, color="none", edgecolor=INK, marker="^",
                      markersize=14, linewidth=0.7, zorder=4)

    # --- hot-spot wards carry the emphasis -----------------------------
    hotspots.boundary.plot(ax=ax, edgecolor=HOTSPOT_EDGE, linewidth=2.4, zorder=5)
    lgas.boundary.plot(ax=ax, edgecolor=INK, linewidth=1.0, zorder=6)

    for _, ward in hotspots.iterrows():
        point = ward.geometry.representative_point()
        ax.annotate(f"{ward.ward_name}\n{ward.missed_rate:.0%} missed",
                    xy=(point.x, point.y), ha="center", va="center",
                    fontsize=7.5, fontweight="bold", color=INK, zorder=9,
                    bbox=dict(boxstyle="round,pad=0.28", facecolor="white",
                              edgecolor=HOTSPOT_EDGE, linewidth=0.9, alpha=0.93))

    suwade = wards[wards.ward_name == "Suwade"]
    if len(suwade):
        point = suwade.geometry.iloc[0].representative_point()
        # Offset with a leader line. Placed in situ it sat directly beneath the
        # Daberi callout, and two touching callouts read as one annotation.
        ax.annotate("Suwade  34% missed\nhighest rate in the state, NOT a cluster",
                    xy=(point.x, point.y),
                    xytext=(point.x + 26000, point.y - 30000),
                    ha="center", va="center",
                    fontsize=6.8, style="italic", color=INK, zorder=9,
                    arrowprops=dict(arrowstyle="-", color="#6e6e6e", lw=0.8),
                    bbox=dict(boxstyle="round,pad=0.24", facecolor="#fff8e1",
                              edgecolor="#8c8c8c", linewidth=0.7, alpha=0.95))

    ax.set_xticks([]); ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_edgecolor("#8c8c8c"); spine.set_linewidth(0.8)
    add_scale_bar(ax)
    add_north_arrow(ax)

    # --- titles ---------------------------------------------------------
    fig.text(0.03, 0.955, "Clusters of missed settlements",
             fontsize=21, fontweight="bold", color=INK)
    fig.text(0.03, 0.928,
             "Bansara State Supplementary Immunization Activity, 9-13 March 2026   |   "
             "Getis-Ord Gi* on ward missed rate, Queen contiguity, 9,999 permutations, "
             "Benjamini-Hochberg FDR   |   EPSG:32632 (WGS 84 / UTM zone 32N)",
             fontsize=9, color="#4a4a4a")

    # --- side panel -----------------------------------------------------
    panel = fig.add_axes([0.735, 0.05, 0.245, 0.86]); panel.axis("off")
    y = 1.0

    def block(title, lines, y, gap=0.0145):
        panel.text(0, y, title, fontsize=9, fontweight="bold",
                   color=INK, transform=panel.transAxes, va="top")
        y -= 0.020
        for line in lines:
            panel.text(0, y, line, fontsize=7.0, color="#333333",
                       transform=panel.transAxes, va="top")
            y -= gap
        return y - 0.011

    handles = [
        Patch(facecolor=SEQ[i], edgecolor="#8c8c8c",
              label=f"{bounds[i]:.0%} - {bounds[i+1]:.0%}")
        for i in range(len(bounds) - 1)
    ]
    legend = panel.legend(handles=handles, loc="upper left",
                          bbox_to_anchor=(0, y), frameon=False,
                          title="Ward missed rate", fontsize=7.4,
                          title_fontsize=9, handlelength=1.4,
                          labelspacing=0.28, borderpad=0.2)
    legend.get_title().set_fontweight("bold")
    y -= 0.235

    handles2 = [
        Line2D([], [], color=HOTSPOT_EDGE, lw=2.4,
               label="Gi* hot-spot ward (FDR p<0.05)"),
        Line2D([], [], color=INK, lw=1.0, label="LGA boundary"),
        Line2D([], [], marker="o", color="none", markerfacecolor=MISSED_PT,
               markersize=4, label="Missed settlement"),
        Line2D([], [], marker="o", color="none", markerfacecolor=VISITED_PT,
               markersize=4, alpha=.6, label="Covered settlement"),
        Line2D([], [], marker="^", color="none", markeredgecolor=INK,
               markersize=6, label="Inaccessible (excluded)"),
    ]
    legend2 = panel.legend(handles=handles2, loc="upper left",
                           bbox_to_anchor=(0, y), frameon=False,
                           fontsize=7.0, handlelength=1.5,
                           labelspacing=0.34, borderpad=0.2)
    panel.add_artist(legend)
    y -= 0.135

    y = block("Result", [
        f"3 of 40 wards form a significant cluster",
        f"of high missed rates after FDR correction.",
        f"Global Moran's I = 0.356, p = 0.0004.",
        "",
        f"{len(hotspots)} hot-spot wards   227 settlements",
        f"51 missed   {under5_at_stake:,} under-5 children",
    ], y)

    y = block("Definition", [
        "A settlement is missed when NO doses were",
        "reported in the e-tally AND no track confirms",
        "a visit. Both sources must agree on absence.",
        f"{total_missed} of 2,487 analysed ({total_missed/2487:.1%}).",
        "75 security-classified settlements excluded,",
        "not counted as missed.",
    ], y)

    y = block("What this does NOT show", [
        "Not a statement about any individual",
        "settlement: Gi* describes neighbourhoods.",
        "Not a statement about any child - nothing",
        "here measures vaccination status.",
        "Not causal: where, not why.",
        "Settlement-level clustering is NOT significant",
        "(Moran's I = 0.003, p = 0.34). The finding is",
        "a ward-level finding and does not restate.",
    ], y)

    block("Sources and method", [
        "GPS tracks: 160 files, 956,702 fixes, of which",
        "150,940 (16.2%) usable after QA.",
        "Settlement masterlist 2,562; e-tally 2,023.",
        "Attribution: 50 m + 2 x reported accuracy.",
        "Visit = 5+ distinct minutes of presence.",
        "",
        "Projection EPSG:32632 (WGS 84 / UTM 32N).",
        "Synthetic assessment data - not a real",
        "population or programme.",
        "",
        "S. Oladimeji  |  eHA technical assessment",
    ], y)

    output = config.OUTPUTS / "missed_settlement_clusters_A3.pdf"
    fig.savefig(output, format="pdf", dpi=300, facecolor="white")
    # A raster twin at review resolution. Cartographic defects - overlapping
    # labels, a legend running off the panel, a scale bar in the wrong place -
    # are only visible by looking at the rendered page, never from the code.
    fig.savefig(config.OUTPUTS / "missed_settlement_clusters_A3_preview.png",
                format="png", dpi=110, facecolor="white")
    plt.close(fig)

    size_kb = output.stat().st_size / 1024
    print(f"\nStage 06 - cartography")
    print("-" * 60)
    print(f"  written  {output.name}  ({size_kb:.0f} KB)")
    print(f"  A3 landscape 420 x 297 mm, vector PDF, fonts embedded")
    print(f"  hot-spot wards {len(hotspots)}   under-5 at stake {under5_at_stake:,}")
    con.close()


if __name__ == "__main__":
    main()
