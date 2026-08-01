"""Verify that every headline number quoted in the write-ups still matches the
artefacts, after a clean rebuild.

The write-ups quote a lot of figures. Any of them can go stale the moment a
threshold changes, and a submission whose prose disagrees with its own outputs
is worse than one that quotes nothing. This is the same anti-drift principle as
the generated constraint register, test plan and codebook - applied to the
narrative rather than the tables.

Run after any change to a threshold or a stage:

    python verify_claims.py
"""
import duckdb, re, sys, pathlib
sys.path.insert(0, "part1_q1/src")
import config

con = duckdb.connect(str(config.DB_PATH)); con.execute("INSTALL spatial; LOAD spatial;")
q = lambda s: con.execute(s).fetchone()[0]

checks = []
def check(label, actual, claimed):
    checks.append((label, actual, claimed, actual == claimed))

check("points stored",            q("SELECT count(*) FROM track_point"), 929733)
check("usable for coverage",      q("SELECT count(*) FROM track_qa WHERE use_for_coverage"), 150940)
check("outside campaign window",  q("SELECT count(*) FROM track_qa WHERE qa01_out_of_window"), 633207)
check("settlements visited >=5m", q("""SELECT count(*) FROM (SELECT settlement_id FROM settlement_visit
                                       GROUP BY 1 HAVING sum(dwell_minutes)>=5)"""), 797)
check("settlements claimed",      q("SELECT count(DISTINCT settlement_id) FROM etally"), 2023)
check("claims confirmed",         q("SELECT count(*) FROM claim_reconciliation WHERE cause_class='confirmed'"), 556)
check("claims team_elsewhere",    q("SELECT count(*) FROM claim_reconciliation WHERE cause_class='team_elsewhere'"), 1336)
check("doses reported",           int(q("SELECT sum(doses_reported) FROM ward_coverage")), 170104)
check("hot-spot wards",           q("SELECT count(*) FROM ward_cluster WHERE hotspot"), 3)
check("under-5 in hot spots",     int(q("SELECT sum(under5) FROM ward_cluster WHERE hotspot")), 31950)
check("missed, both sources",     q("SELECT count(*) FROM settlement_cluster WHERE missed=1 AND NOT inaccessible"), 444)

xml = pathlib.Path("part2_q3/form/bansara_hh_2026.xml").read_text(encoding="utf-8")
check("form constraint messages", xml.count("jr:constraintMsg"), 64)
check("form relevance rules",     len(re.findall(r"relevant=", xml)), 38)

reg = pathlib.Path("part2_q3/docs/constraint_register.md").read_text(encoding="utf-8")
check("register rules documented", int(re.search(r"(\d+) rules documented", reg).group(1)), 22)
plan = pathlib.Path("part2_q3/docs/test_plan.md").read_text(encoding="utf-8")
check("test plan cases",           int(re.search(r"\*\*(\d+) cases\*\*", plan).group(1)), 54)

# ---------------------------------------------------------------------------
# Part 3 Q6 - the training dataset against the figures quoted in the annexes.
#
# Stricter than the checks above, and deliberately so. Those compare an
# artefact against a literal in this file, which still leaves the literal free
# to drift from the prose. These parse the number out of the annex itself, so
# the only way to pass is for the document and the data to agree.
#
# This gate exists because they once did not: the model answer quoted 61 rows
# for the lga_name mapping where the file says 98, and the generator's own
# docstring said 34. Three numbers for one count, none of them checked.
# ---------------------------------------------------------------------------
import csv
sys.path.insert(0, "part3_q6/annex_b_session_in_full")
import make_dataset as md

D1 = list(csv.DictReader(
    open("part3_q6/annex_b_session_in_full/D1_facilities_raw.csv", encoding="utf-8")))

def num(v):
    v = v.replace(",", ".").strip()
    return float(v) if v else None

ids       = [r["facility_id"] for r in D1]
no_coord  = {r["facility_id"] for r in D1 if not r["longitude"].strip()}
swapped   = [r for r in D1
             if num(r["longitude"]) is not None and num(r["latitude"]) is not None
             and md.LAT_RANGE[0] <= num(r["longitude"]) <= md.LAT_RANGE[1]
             and md.LON_RANGE[0] <= num(r["latitude"])  <= md.LON_RANGE[1]]
ws        = lambda col: sum(1 for r in D1 if r[col] != r[col].strip())
noncanon  = lambda col, ok: sum(1 for r in D1 if r[col].strip() not in ok)

truth = {
    "rows in":            len(D1),
    "distinct id":        len(set(ids)),
    "duplicate rows":     len(ids) - len(set(ids)),
    "rows out":           len(set(ids)),
    "mappable":           len(set(ids)) - len(no_coord),
    "missing coords":     len(no_coord),
    "ws facility_name":   ws("facility_name"),
    "ws lga_name":        ws("lga_name"),
    "ws total":           ws("facility_name") + ws("lga_name"),
    "lga variants":       len({r["lga_name"] for r in D1}),
    "lga canonical":      len(md.LGA_CANONICAL),
    "lga rows":           noncanon("lga_name", set(md.LGA_CANONICAL)),
    "type variants":      len({r["facility_type"] for r in D1}),
    "type canonical":     len(md.TYPE_VARIANTS),
    "type rows":          noncanon("facility_type", set(md.TYPE_VARIANTS)),
    "decimal commas":     sum(1 for r in D1 if "," in r["longitude"]),
    "transposed":         len(swapped),
    "staff_total = 999":  sum(1 for r in D1 if r["staff_total"].strip() == "999"),
}

ANNEX_B = pathlib.Path(
    "part3_q6/annex_b_session_in_full/model_answer.md").read_text(encoding="utf-8")
ANNEX_D = pathlib.Path(
    "part3_q6/annex_d_dataset_spec.md").read_text(encoding="utf-8")

def quoted(doc, pattern, groups=1):
    """Pull the figure(s) an annex states. Absent means the prose was reworded
    and the gate no longer covers it - which is a failure, not a pass."""
    m = re.search(pattern, doc)
    if not m:
        return None if groups == 1 else (None,) * groups
    return int(m.group(1)) if groups == 1 else tuple(int(g) for g in m.groups())

# the exemplar record, where the drift happened
ws_tot, ws_fn, ws_lg = quoted(ANNEX_B, r"(\d+) values changed - (\d+) in facility_name, (\d+) in lga_name", 3)
# Steps 2 and 3 state the same shape of sentence. Take them in order rather
# than by a distinguishing pattern - re.search would return step 2 for both.
_reduced = re.findall(r"(\d+) distinct values reduced to (\d+)\. (\d+) rows changed", ANNEX_B)
(lga_v, lga_c, lga_r), (typ_v, typ_c, typ_r) = (
    tuple(int(g) for g in _reduced[0]), tuple(int(g) for g in _reduced[1]))

annex_b_checks = [
    ("B source rows",      truth["rows in"],           quoted(ANNEX_B, r"D1_facilities_raw\.csv, (\d+) rows")),
    ("B ws total",         truth["ws total"],          ws_tot),
    ("B ws facility_name", truth["ws facility_name"],  ws_fn),
    ("B ws lga_name",      truth["ws lga_name"],       ws_lg),
    ("B lga variants",     truth["lga variants"],      lga_v),
    ("B lga canonical",    truth["lga canonical"],     lga_c),
    ("B lga rows changed", truth["lga rows"],          lga_r),
    ("B type variants",    truth["type variants"],     typ_v),
    ("B type canonical",   truth["type canonical"],    typ_c),
    ("B type rows changed",truth["type rows"],         typ_r),
    ("B decimal commas",   truth["decimal commas"],    quoted(ANNEX_B, r'in longitude\. (\d+) values fixed')),
    ("B transposed",       truth["transposed"],        quoted(ANNEX_B, r"Found (\d+) rows where longitude")),
    ("B staff 999",        truth["staff_total = 999"], quoted(ANNEX_B, r"read 999 \((\d+) rows\)")),
    ("B duplicates",       truth["duplicate rows"],    quoted(ANNEX_B, r"Removed (\d+) duplicate facility_id rows")),
    ("B rows in",          truth["rows in"],           quoted(ANNEX_B, r"Rows in:\s+(\d+)")),
    ("B rows out",         truth["rows out"],          quoted(ANNEX_B, r"Rows out:\s+(\d+)")),
    ("B mappable",         truth["mappable"],          quoted(ANNEX_B, r"Facilities mappable: (\d+)")),
    ("B not mappable",     truth["missing coords"],    quoted(ANNEX_B, r"Not mappable: (\d+)")),
    # the reconciliation table a facilitator scores against
    ("B tbl rows raw",     truth["rows in"],           quoted(ANNEX_B, r"Rows in raw file \| \*\*(\d+)")),
    ("B tbl distinct id",  truth["distinct id"],       quoted(ANNEX_B, r"Distinct `facility_id` \| \*\*(\d+)")),
    ("B tbl rows out",     truth["rows out"],          quoted(ANNEX_B, r"Rows out, following the model \| \*\*(\d+)")),
    ("B tbl mappable",     truth["mappable"],          quoted(ANNEX_B, r"Mappable facilities \| \*\*(\d+)")),
    ("B tbl ws name",      truth["ws facility_name"],  quoted(ANNEX_B, r"Whitespace in `facility_name` \| \*\*(\d+)")),
    ("B tbl ws lga",       truth["ws lga_name"],       quoted(ANNEX_B, r"Whitespace in `lga_name` \| \*\*(\d+)")),
    ("B tbl transposed",   truth["transposed"],        quoted(ANNEX_B, r"Transposed coordinate pairs \| \*\*(\d+)")),
]

d_lga_v, d_lga_c, d_lga_r = quoted(ANNEX_D, r"(\d+) variants → (\d+) real LGAs, (\d+) rows", 3)
d_typ_v, d_typ_c, d_typ_r = quoted(ANNEX_D, r"(\d+) variants → (\d+) real types, (\d+) rows", 3)

annex_d_checks = [
    ("D lga variants",     truth["lga variants"],      d_lga_v),
    ("D lga canonical",    truth["lga canonical"],     d_lga_c),
    ("D lga rows",         truth["lga rows"],          d_lga_r),
    ("D type variants",    truth["type variants"],     d_typ_v),
    ("D type canonical",   truth["type canonical"],    d_typ_c),
    ("D type rows",        truth["type rows"],         d_typ_r),
    ("D duplicate pairs",  truth["duplicate rows"],    quoted(ANNEX_D, r"rows differ\*\* \| (\d+) pairs")),
    ("D missing coords",   truth["missing coords"],    quoted(ANNEX_D, r"Missing coordinates \| (\d+) rows")),
    ("D transposed",       truth["transposed"],        quoted(ANNEX_D, r"transposed \| (\d+) rows")),
    ("D ws facility_name", truth["ws facility_name"],  quoted(ANNEX_D, r"whitespace in `facility_name` \| (\d+) rows")),
    ("D staff 999",        truth["staff_total = 999"], quoted(ANNEX_D, r"`staff_total = 999` \| (\d+) rows")),
    ("D decimal commas",   truth["decimal commas"],    quoted(ANNEX_D, r"Decimal comma in `longitude` \| (\d+) rows")),
]

for label, actual, claimed in annex_b_checks + annex_d_checks:
    check(label, actual, claimed if claimed is not None else -1)

print("\n  Claim verification against rebuilt artefacts")
print("  " + "-" * 62)
bad = 0
for label, actual, claimed, ok in checks:
    if not ok: bad += 1
    print(f"  {'OK ' if ok else 'DRIFT'}  {label:28s} artefact={actual:>9,}  doc={claimed:>9,}")
print("  " + "-" * 62)
print(f"  {len(checks)-bad}/{len(checks)} match" + ("" if not bad else f"   <<< {bad} DRIFTED"))
sys.exit(1 if bad else 0)
