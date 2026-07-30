# DECISION BRIEF — where to deploy 24 hours of mop-up

**To:** Incident Manager, Bansara State SIA
**From:** Data and GIS Analytics
**Date:** 14 March 2026 · **Round:** 9–13 March 2026
**Decision required:** where to send the available mop-up capacity, today.

---

## Recommendation

**Deploy to Daberi and Kungomi wards (Katsuma LGA) first, then Baluru ward (Idi-Oro).**

| Priority | Ward | LGA | Settlements missed | Under-5 in ward | Why |
|---|---|---|---|---|---|
| **1** | Daberi + Kungomi | Katsuma | 20 | 4,813 | Adjacent wards, statistically confirmed cluster — one team can work both in a day |
| **2** | Baluru | Idi-Oro | 31 | 27,137 | Largest child population at risk of any hot spot; urban, so travel time is low |
| **3** | Suwade | Katsuma | 16 | 2,593 | Worst missed rate in the state (34%), but isolated — a ward problem, not an area problem |

Daberi and Kungomi share a boundary. Treat them as one deployment, not two.

---

## What we found

Of **2,487 settlements** in the plan (excluding 75 classified inaccessible on security
grounds), **444 have no evidence of being reached** — no doses reported and no GPS track
placing a team there. That is **17.9%**.

Those missed settlements are **not scattered evenly**. Three wards form a statistically
significant cluster of high missed rates, confirmed after correcting for the fact that
testing 40 wards will throw up false alarms by chance alone.

**Suwade is the trap in this data.** It has the highest missed rate in the state, and it is
*not* part of a cluster — its neighbours performed normally. Sending an area-level response
there would waste capacity. It needs a single-ward fix, and it is third priority only
because its child population is small.

---

## The thing you need to know before you trust this

**We can only confirm that 27.5% of reported activity actually happened.**

The teams' GPS loggers corroborate **556 of 2,023** reported settlement visits. For
**1,336** of them, the team's own logger places it **a median of 3.5 km away** at the time,
and no other team went there either.

**This does not mean the vaccinations did not happen.** We measured where *loggers* were,
not where *people* were. A logger left in a vehicle, switched off during work, or carried
by one member of a team that split up would all produce exactly this pattern. We tested and
ruled out the innocent data explanations — mismatched team numbers, wrong dates, faulty
settlement coordinates — but we cannot rule out these operational ones from the data alone.

**What it means for your decision:** the 444 confirmed-missed settlements are the *floor*,
not the ceiling. If a meaningful share of those 1,336 unverified visits did not happen, the
real gap is larger and may sit in different wards than this map shows.

---

## What we recommend alongside the deployment

1. **Send supervisors to spot-check 30 of the 1,336 unverified claims**, chosen at random,
   while mop-up runs. That single action will tell you more than any further analysis. If
   most check out, this map is your targeting tool. If they do not, the round needs a
   different conversation.
2. **Reported coverage is 170,104 doses against a planned target of 255,931 — 66.5%.**
   Treat that as unverified until the spot-check returns.
3. **Five settlements classified inaccessible reported doses anyway.** Either the security
   classification is out of date or the reporting is wrong. Worth a phone call today.

---

## What this brief does not tell you

- **Nothing about any individual child.** No vaccination status was measured.
- **Nothing reliable about any individual settlement.** The cluster finding holds at ward
  level. A settlement inside a hot-spot ward may have been covered perfectly.
- **Nothing about why.** We can say where the gaps concentrate, not whether the cause is
  terrain, insecurity, team assignment, or reporting.
- **Nothing about any individual team's honesty.** Low corroboration is a statement about a
  logger, not about the people carrying it.

---

## Confidence

| Finding | Confidence |
|---|---|
| 444 settlements have no evidence of coverage from either source | **High** — both sources agree |
| Those settlements cluster in Daberi, Kungomi and Baluru | **High** — significant after correction for multiple testing |
| Suwade is a poor performer but not part of a cluster | **High** |
| Reported coverage of 66.5% | **Low** — two-thirds of it is uncorroborated |
| The true missed total is 444 | **Low** — this is a floor; the ceiling is unknown |

*Analysis: 956,702 GPS fixes from 160 logger files, of which 150,940 (16.2%) were usable
after quality control. Full method and its limitations in the accompanying technical note.*
