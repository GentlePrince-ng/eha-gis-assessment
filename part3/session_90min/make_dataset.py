"""Generate D1_facilities_raw.csv — the training dataset for Day 2 and Day 3.

Annex D, dataset specification. Generated rather than described, so a colleague
delivering the session in my absence produces exactly the dataset the model
answer expects. Fixed seed; the same file every time.

## Design requirements

The dataset has to do three things at once:

1. **Be small enough to clean in 120 minutes** by people at capability 36 —
   200 rows, 8 columns.
2. **Look like real ministry data**, because defects invented to be tidy teach
   people to spot invented defects. Every defect class below is one I have
   actually met in a facility register.
3. **Contain at least two genuine judgement calls** — defects with no single
   correct answer. This is essential: the session's most important failure
   (participants not recording their decisions) cannot occur unless there are
   decisions to record.

## Seeded defects

| # | Defect | Count | Judgement call? |
|---|---|---|---|
| 1 | LGA name variants: spacing, case, hyphenation | 34 rows across 4 LGAs | No — needs a mapping, one right answer |
| 2 | Duplicate `facility_id`, **rows differ** | 3 pairs | **Yes** — which row survives? |
| 3 | Missing coordinates | 5 rows | **Yes** — drop, or keep unmapped? |
| 4 | Latitude and longitude transposed | 2 rows | No — detectable and correctable |
| 5 | Leading/trailing whitespace in names | 21 rows | No |
| 6 | Staff count implausible (`999`) | 3 rows | **Yes** — sentinel, or a real value? |
| 7 | `facility_type` spelling variants | 18 rows | No |
| 8 | Coordinates stored as text, some with a stray `,` | 6 rows | No |

Defects 2, 3 and 6 are the ones that make the session work. Two participants
cleaning correctly will produce **different row counts**, and neither is wrong —
which is the moment reproduction fails and documentation stops being abstract.

Run:  python part3/session_90min/make_dataset.py
"""

from __future__ import annotations

import csv
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "D1_facilities_raw.csv"

SEED = 20260731
N_ROWS = 200

LGA_CANONICAL = ["Idi-Oro", "Gwarin", "Katsuma", "Ilela"]
LGA_VARIANTS = {
    "Idi-Oro": ["Idi-Oro", "Idi Oro", "IDI-ORO", "Idi-oro", "idi-oro"],
    "Gwarin": ["Gwarin", "GWARIN", "gwarin", " Gwarin"],
    "Katsuma": ["Katsuma", "Katsuma ", "KATSUMA", "Katsuma"],
    "Ilela": ["Ilela", "ILELA", "Ilela ", "ilela"],
}
TYPE_VARIANTS = {
    "Primary Health Centre": ["Primary Health Centre", "Primary Health Center",
                              "PHC", "Primary health centre"],
    "Health Post": ["Health Post", "Health post", "HEALTH POST"],
    "Cottage Hospital": ["Cottage Hospital", "Cottage hospital"],
}
NAME_STEMS = ["Uzoyosa", "Adwade", "Balawo", "Yeluwa", "Sokmiri", "Maljiwo",
              "Ngenuta", "Daibewo", "Hanjile", "Zamjidu", "Jostile", "Lokshasa",
              "Tasayi", "Dazata", "Suwade", "Kungomi", "Daberi", "Baluru"]
SUFFIXES = ["", " North", " South", " Central", " Model", " Rural"]


def main() -> None:
    rng = random.Random(SEED)
    rows = []

    for i in range(1, N_ROWS + 1):
        lga = rng.choice(LGA_CANONICAL)
        ftype = rng.choice(list(TYPE_VARIANTS))
        name = rng.choice(NAME_STEMS) + rng.choice(SUFFIXES) + " " + (
            "PHC" if ftype == "Primary Health Centre" else
            "Health Post" if ftype == "Health Post" else "Cottage Hospital")
        rows.append({
            "facility_id": f"HF{i:04d}",
            "facility_name": name,
            "facility_type": rng.choice(TYPE_VARIANTS[ftype]),
            "lga_name": rng.choice(LGA_VARIANTS[lga]),
            "ward_name": rng.choice(NAME_STEMS),
            "longitude": f"{rng.uniform(6.95, 8.43):.6f}",
            "latitude": f"{rng.uniform(10.37, 11.57):.6f}",
            "staff_total": str(rng.randint(2, 24)),
        })

    idx = list(range(N_ROWS))
    rng.shuffle(idx)

    # 2 - duplicate facility_id, rows deliberately DIFFER so that "which one
    #     survives" is a real decision the participant must record.
    for k in range(3):
        src = rows[idx[k]]
        clone = dict(src)
        clone["staff_total"] = str(int(src["staff_total"]) + rng.randint(1, 6))
        clone["facility_name"] = src["facility_name"] + " "
        rows.append(clone)

    # 3 - missing coordinates: drop them, or keep them unmapped? No right answer.
    for k in range(3, 8):
        rows[idx[k]]["longitude"] = ""
        rows[idx[k]]["latitude"] = ""

    # 4 - latitude and longitude transposed
    for k in range(8, 10):
        r = rows[idx[k]]
        r["longitude"], r["latitude"] = r["latitude"], r["longitude"]

    # 5 - whitespace
    for k in range(10, 31):
        rows[idx[k]]["facility_name"] = "  " + rows[idx[k]]["facility_name"] + " "

    # 6 - implausible staff count. Sentinel or real? The register does not say.
    for k in range(31, 34):
        rows[idx[k]]["staff_total"] = "999"

    # 8 - coordinates as text with a stray thousands comma
    for k in range(34, 40):
        r = rows[idx[k]]
        if r["longitude"]:
            r["longitude"] = r["longitude"].replace(".", ",", 1)

    rng.shuffle(rows)

    with OUT.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    dup_ids = len(rows) - len({r["facility_id"] for r in rows})
    print(f"\n  {OUT.name}")
    print(f"  rows                    {len(rows):>5}")
    print(f"  distinct facility_id    {len({r['facility_id'] for r in rows}):>5}")
    print(f"  duplicate id rows       {dup_ids:>5}")
    print(f"  missing coordinates     "
          f"{sum(1 for r in rows if not r['longitude']):>5}")
    print(f"  staff_total = 999       "
          f"{sum(1 for r in rows if r['staff_total'] == '999'):>5}")
    print(f"  names with whitespace   "
          f"{sum(1 for r in rows if r['facility_name'] != r['facility_name'].strip()):>5}")
    print(f"  lga_name variants       "
          f"{len({r['lga_name'] for r in rows}):>5}   (4 real LGAs)")
    print(f"  facility_type variants  "
          f"{len({r['facility_type'] for r in rows}):>5}   (3 real types)")
    print(f"  comma in longitude      "
          f"{sum(1 for r in rows if ',' in r['longitude']):>5}")


if __name__ == "__main__":
    main()
