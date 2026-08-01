# Reconciliation: track-derived coverage against the reported e-tally

## The discrepancy

| Measure | Settlements | % of 2,562 planned |
|---|---|---|
| Planned in the masterlist | 2,562 | 100% |
| **Confirmed visited by tracks** (dwell ≥ 5 min) | **797** | 31.1% |
| **Claimed in the e-tally** | **2,023** | 79.0% |
| Classified inaccessible before the round | 75 | 2.9% |

Doses: **170,104 reported against a planned under-5 target of 255,931 - 66.5%.** Eight
settlements carry no denominator at all and are excluded from that ratio rather than
counted as zero.

## Why each claim is or is not corroborated

Every e-tally claim (team × settlement × day) is classified by evidence already in the
store. First match wins.

| Cause class | Claims | % | Doses |
|---|---|---|---|
| `confirmed` - tracks put the claiming team there ≥ 5 min | 556 | 27.5% | 34,286 |
| **`team_elsewhere`** - team had ample tracking that day, none near this settlement | **1,336** | **66.0%** | 123,653 |
| `near_miss` - a usable fix within 250 m, just outside tolerance | 66 | 3.3% | 6,930 |
| `brief_presence` - team was there, below the dwell threshold | 37 | 1.8% | 2,955 |
| `logger_failed` - claiming team had < 60 usable fixes that day | 16 | 0.8% | 2,207 |
| `not_in_masterlist` - settlement has no coordinate; unverifiable by construction | 7 | 0.3% | 300 |
| `security_excluded` - classified inaccessible, yet doses reported | 5 | 0.2% | 73 |

## Three alternative explanations, tested and rejected

The 66% is a serious number, so the innocent explanations were tested before it was
allowed to stand.

**1. Are the team identifiers mismatched between the two sources?** If `T04` in the e-tally
were `T11` in the tracks, real work would be misfiled as absence. Rejected: of the 1,336
`team_elsewhere` claims, **exactly one** was visited by *any other* team on the same day
(0.1%), while 100% of `confirmed` claims match. A scrambled identifier would not produce
that pattern.

**2. Did somebody else cover those settlements on another day?** Rejected as a general
explanation: only **192 of 1,336** (14.4%) were visited by any team on any day of the
round. Coverage is genuinely absent, not merely misdated.

**3. Are the masterlist coordinates systematically offset?** A datum or digitisation shift
would push every track just outside tolerance. Rejected: where tracks *do* match, the
median distance to the settlement centroid is **11.3 m**. A systematic offset would show as
a distance cluster at the offset value, not at 11 m.

**How far away were they?** For the `team_elsewhere` claims, the claiming team's nearest
usable fix that day sits a median of **3.47 km** from the settlement (p25 1.44 km, p75
9.68 km, max 101.8 km). This is not a tolerance argument.

## What this does and does not license

**Supported:** two-thirds of reported claims have no supporting track evidence; the
claiming team was kilometres away; no other team covered those settlements; and the gap is
not explained by identifier error, date shift, coordinate offset, or the analyst's
thresholds - it persists at every dwell value from 1 to 15 minutes.

**Not supported:** that the doses were not administered. The analysis observes where
*loggers* were, not where *people* were. At least three benign mechanisms would produce the
same pattern and cannot be separated with the data supplied:

- the logger stayed with a vehicle or a team leader while members worked on foot;
- the logger was switched off during work and on during transit - plausible given eight
  loggers ran continuously for three weeks, showing switching discipline was not uniform;
- one logger per team was issued, but teams split to cover more ground.

**Nothing here licenses a statement about any individual team, and nothing licenses a
statement about any individual child.** A team with a low confirmation rate is a team whose
logger did not corroborate its report, which is not the same as a team that did not work.

## Which source goes to the Incident Manager

**Neither alone. The e-tally as the operational figure, with the track data as a
verification overlay - and the disagreement reported, not resolved.**

The reasoning:

- **The e-tally is the only source that measures the outcome.** Tracks record presence;
  only the e-tally records doses. An Incident Manager deciding on mop-up needs children
  vaccinated, and no GPS pipeline can supply that.
- **The tracks cannot be the headline** because they under-detect by construction. Only
  16.2% of the supplied points survived QA, and 83.7% of survivors sit more than a
  tolerance away from any planned settlement. A figure derived from them is a lower bound
  on presence, not a measure of coverage.
- **But the e-tally cannot go up unqualified.** It reports doses exceeding the target
  population in 201 records, names 7 settlements that do not exist in the masterlist, and
  reports doses against 5 settlements the programme itself had classified inaccessible.
- **The overlay is where the value is.** The 1,336 uncorroborated claims are not a coverage
  estimate; they are a **verification worklist**, ranked by doses at stake. That is
  actionable in a way neither source is alone.

**What I would put in front of the Incident Manager:** reported coverage of 66.5% of the
under-5 target, flagged as unverified; 797 settlements with independent presence evidence;
and 1,336 claims requiring supervisory confirmation before the round is signed off - with
the honest statement that the tracking data can neither confirm nor refute them, and that
the fastest route to an answer is a supervisor spot-check of a sample, not more analysis.
