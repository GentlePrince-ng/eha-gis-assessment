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

print("\n  Claim verification against rebuilt artefacts")
print("  " + "-" * 62)
bad = 0
for label, actual, claimed, ok in checks:
    if not ok: bad += 1
    print(f"  {'OK ' if ok else 'DRIFT'}  {label:28s} artefact={actual:>9,}  doc={claimed:>9,}")
print("  " + "-" * 62)
print(f"  {len(checks)-bad}/{len(checks)} match" + ("" if not bad else f"   <<< {bad} DRIFTED"))
sys.exit(1 if bad else 0)
