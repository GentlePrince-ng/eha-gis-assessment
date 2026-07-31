# Q5 — Coordinating delivery through the round

**Maximum three pages.** Day 3 of 7. Four things have arrived at once and only
one of them is actually urgent.

## 1. The first twenty-four hours

The ordering principle: **stop things getting worse, protect today's
deliverable, then diagnose.** Diagnosis before containment lets the corruption
grow while I investigate it.

| When | Action | Why here |
|---|---|---|
| 0–15 min | **Freeze writes to the settlement layer.** Read access unaffected | Cheap, reversible, and it stops the duplicate problem growing during the eight hours it takes to understand. Every hour of unrestricted editing adds records I will later have to adjudicate |
| 15–45 min | **Tell the EOC before they ask** that today's coverage figure is under verification, with a time by which I will have an answer | The discrepancy is already being discussed at national level. Arriving second to my own problem costs more credibility than the error does |
| 45 min–3 h | **Test whether the duplicate records and the coverage discrepancy are one incident, not two** | Duplicated settlements change the denominator. If that is the cause, I have one problem and one fix, not two workstreams |
| 3–6 h | Reconstruct the figure from the last known-good database state | §2 |
| 6–8 h | **Issue today's product, caveated**, or hold it with a stated reason | The EOC deploys against this daily. Silence is a decision to give them nothing |
| 8–12 h | Root cause on the concurrency failure | §3 |
| 12–16 h | Handover triage with the two departing analysts — access and credentials only | §5 |
| Within 24 h | Reply to the counterpart with **confirmed training dates** | Two minutes. Deferring it damages a contractual relationship to save nothing |

### What I deliberately do not do first

**I do not delete the duplicate records.** They are the evidence. Deleting before
establishing which edit was correct destroys the audit trail and may discard a
legitimate edit — and the duplicates are probably the cause of the discrepancy,
so removing them silently would leave a corrected figure with no explanation for
why it changed.

**I do not publish a corrected coverage figure.** The strong instinct is to
recompute and reissue within the hour. A second wrong number is far more damaging
than the first: the first is an error, the second is a pattern, and after it
nobody at national level trusts the daily product again this round.

**I do not argue the discrepancy on the merits.** I do not yet know whether the
state is wrong, and defending my figure before I have checked it is how a
technical disagreement becomes an institutional one.

**I do not start the handover documentation.** It feels productive, and it has
ten days of runway against four days of live round.

**I do not begin the partner report.** Nine days.

## 2. One authoritative coverage figure

**A single named owner, one source, one computation, one publication time.** The
absence of that is why two figures exist.

**Establishing it.** Restore the settlement layer to a point-in-time state from
before the concurrent edits, recompute my figure, then recompute *the state's*
figure from the same base using their stated method. That comparison is
diagnostic:

- **Same base, same answer** → the difference is *method*, and the fix is a
  written definition, not a data repair.
- **Same base, different answer** → the difference is *data*, and the duplicates
  are the first suspect.

**Root cause, tested in this order** — cheapest and most likely first:

1. **Definitional.** Are we computing the same quantity? Planned settlements or
   settlements with a target population; inaccessible settlements in or out;
   cumulative or daily; sync time or end of day. Most field discrepancies are
   definitional, and this costs one phone call.
2. **Duplicates.** Do the flagged duplicates change the denominator by the size
   of the gap? If the arithmetic matches, that is the cause.
3. **Latency.** Does the state hold submissions I have not received?
4. **Genuine divergence.** Only reached if the first three are excluded.

**What I say to national level before I know:**

> *Would claim:* the two figures differ by X; both are being recomputed from a
> common base; the likely causes are definitional or a known data-integrity issue
> now contained; I will have an answer by 14:00 tomorrow.

> *Would not claim:* which figure is correct; that the state is wrong; a cause;
> or a corrected number.

**Committing to a time is what buys the time.** An open-ended "we are looking
into it" invites hourly escalation; a named hour converts an incident into a
scheduled item.

## 3. Concurrent editing on the shared spatial database

Named technology: **PostgreSQL/PostGIS**. Five mechanisms, and the first matters
most because it *prevents* the conflict rather than resolving it.

**1 · Edit scope, enforced by the database.** Each analyst holds write rights to
a defined set of wards, enforced by **row-level security** with a policy on ward
ownership. Two analysts cannot edit overlapping areas because the database will
not let them. This is what actually failed here: the incident is an *assignment*
failure that a concurrency mechanism would only have detected, not avoided.

**2 · Identifier strategy.** Primary key is a **client-generated UUID**, so two
analysts creating a settlement offline cannot collide. Identity is separately
protected by a **`UNIQUE` constraint on the natural key** (settlement code within
ward) — the UUID prevents accidental collision, the unique constraint prevents
genuine duplication. The current incident is the second kind: two rows, two ids,
one settlement.

**3 · Conflict detection: optimistic concurrency, not locking.** Every feature
carries a `version` integer. An update supplies the version it read, and the
write applies only if it still matches — compare-and-swap. A stale write is
**rejected and returned to its author**, never silently applied. Pessimistic
locking is rejected: analysts are intermittently connected, and a held lock from
a disconnected state blocks a whole ward.

**4 · Staged merge, validated before acceptance.** Analysts write to a personal
staging schema, not to trunk. A merge runs the validation suite in §4 and is
applied only if it passes. Nothing enters the authoritative layer unvalidated —
which is the property that would have stopped this incident reaching the daily
product.

**5 · Audit trail: append-only, by trigger.** Every change writes a history row —
who, when, before, after, and which merge accepted it. **Records are superseded,
never deleted.** That is what makes "which of these two edits was correct" a
question with an answer, and it is why my first action was a freeze rather than a
cleanup.

## 4. Automated data quality rules

**Blocked** — the change is rejected, because accepting it produces data that is
meaningless or unrecoverable:

- Invalid geometry (self-intersecting polygon, null geometry on a required layer)
- Settlement point outside the ward it declares
- Duplicate natural key within a ward
- Referential integrity failure — a ward code with no parent
- Coordinates outside the state boundary
- A version conflict (§3)

**Flagged for review** — applied, recorded, and queued, because the change may
well be correct:

- A settlement moved more than 200 m from its previous position
- Target population changed by more than 20%
- A new settlement created in a ward that has never had one
- A route line whose length is implausible for one team-day
- Any edit made outside working hours

**The reasoning behind the split.** Block only where the data would be *wrong in
a way nobody can later untangle*. Everything else flags — because **a block an
analyst cannot satisfy honestly is a block they will satisfy dishonestly.**
Refuse a settlement that has genuinely moved, and it gets created under a
different code, and the duplicate problem returns wearing a new hat.

**The bar for blocking is higher mid-round than between rounds.** A rule that
halts a state analyst on day 4 of a 7-day campaign is an operational failure even
when it is technically correct. Anything not on the blocked list above waits for
the inter-round window.

## 5. Handover in ten days, with the round live

**Do not ask them to write documentation.** Written from memory under notice, it
describes what they believe they do. Instead: **their successor performs the
task while the departing analyst watches and corrects.** Faster, and it produces
a procedure that is known to work because it has just been used.

The handover is complete when the successor completes the daily product **without
asking a question** — the same test as level 3 in the counterpart competency
framework, and not a coincidence (§Q6).

| Days | Protect |
|---|---|
| 1–2 | **Credentials, access, and anything only they can log into.** If this is missed, nothing else matters |
| 3–5 | **The daily EOC product.** Successor runs it shadowed; the analyst corrects but does not touch the keyboard |
| 6–8 | **Reverse-shadow.** Successor runs it unaided. Every question asked is a gap in the written procedure and gets written down |
| 9–10 | The known-issues list: which settlements are known-bad, which local contacts answer, which manual steps exist and why |

**What I accept losing.** Their relationships with state counterparts, their
tacit sense of which numbers in their state look wrong, and the historical
rationale for past decisions. Ten days cannot transfer these and pretending
otherwise produces four thin handovers instead of two solid ones. I would rather
lose the context knowingly than lose the pipeline by accident.

## 6. Delegating without becoming the single point of failure

**Four problems, four named owners, four deadlines.** Not "the team will look at
it": the coverage figure to a named central analyst; the database integrity fix
to the data engineer who found it; the handover to the two state supervisors; the
partner report to a central analyst starting on day 5.

**I own two things only** — the sequencing decision, and communication to
national level. Both are genuinely mine and neither is delegable mid-incident.

**Supervision without reviewing every output.** Per-record checking is what §4's
automated rules are for; a coordinator repeating them by eye is the bottleneck,
not the control. So:

- **I review exceptions, not passes.** The flagged queue, not the accepted edits.
- **Peer review is paired and rotating**, so review capacity scales with the team
  rather than with me.
- **A 15-minute daily stand-up on exceptions only** — what is blocked, what is
  flagged, what is late.
- **A named deputy for the coverage figure**, who publishes it when I am
  unavailable.

**The test I would hold myself to:** if I am uncontactable for 48 hours, does the
daily product still ship and does the partner report still progress? If the
answer is no, I have not delegated — I have distributed tasks while keeping the
dependencies.

**And the connection to the other half of this scenario:** two resignations
threaten delivery only because knowledge lived in two people rather than in a
process. That is the same finding as the counterpart department's 1.5 out of 5
for documenting a reproducible workflow. The handover method in §5 and the
standard the counterpart drafts on day 3 of the training are the same artefact,
and building it once, in the open, serves both.
