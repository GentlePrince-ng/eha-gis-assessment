# Q5 - Coordinating delivery through the round

Day 3 of 7. Four things have arrived at once and only one is genuinely urgent.

## 1. The first twenty-four hours

Ordering principle: **contain, protect today's deliverable, then diagnose.**
Diagnosing first lets the corruption grow while I investigate it.

**0-15 min · Freeze writes to the settlement layer**, reads unaffected, and
**scoped down or lifted at the three-hour mark** when the one-incident test
reports. Cheap and reversible; every hour of open editing adds records I must
later adjudicate.

**15-45 min · Tell the EOC before they ask** that the figure is under
verification, with a time for the answer. It is already being discussed
nationally, and arriving second to my own problem costs more than the error
does.

**45 min-3 h · Test whether the duplicates and the discrepancy are one
incident.** Duplicated settlements change the denominator. If that is the cause
I have one problem and one fix, not two workstreams.

**3-8 h · Reconstruct the figure** from the last known-good state (§2), then
**issue today's product caveated, or hold it with a stated reason.** The EOC
deploys against this daily; silence is a decision to give them nothing.

**8-16 h ·** Root cause on the concurrency failure (§3), then handover triage -
credentials and access only (§5).

**Within 24 h · Confirm the counterpart's training dates.** Two minutes.
Deferring damages a contractual relationship to save nothing.

**What I deliberately do not do first.** Not **delete the duplicates**: they are
the evidence and probably the cause, and removing them before establishing which
edit was correct destroys the audit trail and leaves a corrected figure with no
explanation for why it moved. Not **publish a corrected figure**: a second wrong
number is far worse than the first, because the first is an error and the second
is a pattern. Not **argue the discrepancy on the merits** before checking my own
figure - that turns a technical disagreement into an institutional one. And not
the **handover documentation or the partner report**: both feel productive, both
have over a week of runway against four days of live round.

## 2. One authoritative coverage figure

**One named owner, one source, one computation, one publication time.** The
absence of that is why two figures exist.

Restore the layer to a point-in-time state from before the concurrent edits,
recompute my figure, then recompute *the state's* from the same base using their
method. **Same answer** means the difference is *method*, and the fix is a
written definition rather than a data repair. **Different answer** means it is
*data*, and the duplicates are the first suspect.

Root cause, cheapest first: **definitional** - same quantity? planned
settlements or those with a target, inaccessible in or out, cumulative or daily,
sync time or end of day (most field discrepancies are definitional, and this
costs one phone call); then **duplicates** - do they change the denominator by
the size of the gap; then **latency** - does the state hold submissions I have
not received; then **genuine divergence**, only if the first three are excluded.

**To national level, before I know** - *would claim:* the figures differ by X,
both are being recomputed from a common base, the likely causes are definitional
or a contained integrity issue, and I will have an answer by 14:00 tomorrow.
*Would not claim:* which figure is correct, that the state is wrong, a cause, or
a corrected number.

**Committing to a time is what buys the time.** "We are looking into it" invites
hourly escalation; a named hour converts an incident into a scheduled item.

## 3. Concurrent editing on the shared database

**PostgreSQL/PostGIS.** Five mechanisms; the first matters most because it
*prevents* the conflict rather than resolving it.

**1 · Edit scope enforced by the database.** Each analyst holds write rights to
a defined set of wards via **row-level security** on ward ownership, so two
analysts cannot edit overlapping areas at all. This is what actually failed
here: the incident is an *assignment* failure, which a concurrency mechanism
would only have detected, not avoided.

**2 · Identifiers.** **Client-generated UUID** primary keys, so two analysts
creating a settlement offline cannot collide, with identity separately protected
by a **`UNIQUE` constraint on the natural key** (settlement code within ward).
The UUID prevents accidental collision; the constraint prevents genuine
duplication. The current incident is the second kind - two rows, two ids, one
settlement.

**3 · Conflict detection and resolution by optimistic concurrency, not
locking.** Every feature carries a `version`; an update supplies the version it
read and applies only if it still matches. A stale write is **rejected and
returned to its author**, never silently applied. Locking is rejected because
analysts are intermittently connected, and a lock held from a disconnected
session blocks a whole ward.

**4 · Staged merge - branch versioning, assembled rather than bought.** Analysts
write to a personal staging schema; a merge applies only if the §4 validation
passes, so nothing enters the authoritative layer unvalidated - the property
that would have stopped this incident reaching the daily product.

**5 · Append-only audit by trigger.** Who, when, before, after, which merge
accepted it. **Records are superseded, never deleted** - which is what makes
*"which of these two edits was correct"* answerable, and why my first action was
a freeze rather than a cleanup.

## 4. Automated data quality rules

**Blocked** - rejected, because accepting produces data nobody can later
untangle: invalid geometry; a settlement outside its declared ward; a duplicate
natural key; referential integrity failure; coordinates outside the state
boundary; a version conflict.

**Flagged** - applied, recorded and queued, because the change may be correct: a
settlement moved more than **200 m** - 3.4x the worst single-fix accuracy in
this round's own tracks (58 m), so it is not GPS jitter; **target population
changed by more than 20%** - my judgement, not a standard: a fifth of a
settlement's under-5 population appearing or disappearing between rounds is a
resurvey trigger rather than a keying slip; a first settlement created in a
ward; a team-day route beyond the 95th percentile of the round to date; any edit
outside working hours.

**Every threshold above is either measured from the round in progress or
labelled judgement.** None is inherited from another programme, and a rule whose
number cannot be sourced does not go in.

**The reasoning.** Block only where the data would be wrong irrecoverably.
Everything else flags, because **a block an analyst cannot satisfy honestly is a
block they will satisfy dishonestly** - refuse a settlement that genuinely moved
and it reappears under a new code, and the duplicate problem returns wearing a
different hat. **The bar is higher mid-round than between rounds:** a rule that
halts a state analyst on day 4 of 7 is an operational failure even when
technically correct.

## 5. Handover in ten days, round live

**Do not ask them to write documentation.** Written from memory under notice, it
records what they believe they do. Instead the **successor performs the task
while the departing analyst watches and corrects** - faster, and it produces a
procedure known to work because it has just been used. The handover is complete
when the successor completes the daily product **without asking a question** -
deliberately the same test as level 3 in the counterpart competency framework
(Q6).

**Days 1-2: credentials and access** - miss this and nothing else matters.
**Days 3-5: the daily EOC product**, successor running it shadowed while the
analyst corrects but does not touch the keyboard. **Days 6-8: reverse-shadow**,
successor unaided, every question asked marking a gap in the procedure that gets
written down. **Days 9-10:** the known-issues list - which settlements are
known-bad, which contacts answer, which manual steps exist and why.

**What I accept losing:** their counterpart relationships, their tacit sense of
which numbers in their state look wrong, and the rationale behind past
decisions. Ten days cannot transfer these, and pretending otherwise produces
four thin handovers instead of two solid ones. Better to lose the context
knowingly than the pipeline by accident.

## 6. Delegating without becoming the single point of failure

**Four problems, four named owners, four deadlines** - not "the team will look
at it". Coverage figure to a named central analyst; the integrity fix to the
data engineer who found it; handover to the two state supervisors; partner
report to a central analyst from day 5. **I keep two things only:** the
sequencing decision and communication to national level, neither delegable
mid-incident.

**Supervision without reviewing every output.** Per-record checking is what §4's
rules are for, and a coordinator repeating them by eye is the bottleneck rather
than the control. So I review **exceptions, not passes**; peer review is paired
and rotating, so capacity scales with the team rather than with me; a 15-minute
daily stand-up covers only what is blocked, flagged or late; and a **named
deputy publishes the coverage figure** when I am unavailable.

**The test I hold myself to:** if I am uncontactable for 48 hours, does the
daily product still ship and the partner report still progress? If not, I have
distributed tasks while keeping the dependencies.

**And the connection to the other half of this scenario:** two resignations
threaten delivery only because knowledge lived in two people rather than in a
process - the same finding as the counterpart department's 1.5 out of 5 for
documenting a reproducible workflow. The handover method above and the standard
that department drafts on day 3 of its training are the same artefact, and
building it once, in the open, serves both.
