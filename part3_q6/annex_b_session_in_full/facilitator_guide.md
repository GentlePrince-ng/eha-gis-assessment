# Facilitator guide - "Make your work someone else's"

**Day 3, session 1 · 90 minutes · 21 participants in pairs (one three)**

This is written so a colleague can deliver it without me. Where the wording
matters, it is given verbatim in quotes. Where it does not, it says so.

---

## What this session is for

Participants discover - by failing - that work they can repeat *themselves*
cannot be repeated by *anyone else*. That gap is the difference between level 2
and level 3 in the competency framework, and it is the single most important
thing in the five days.

**Do not tell them this at the start.** The whole design depends on them finding
it. If you announce the lesson, they will write good documentation for the
exercise and poor documentation for the rest of their lives.

The baseline for this competency is **1.5 out of 5** across the department. Expect
the first attempt to fail almost universally. That is the intended result, and
managing how it feels is most of your job here.

---

## Before the session

| Check | Detail |
|---|---|
| Dataset loaded | `D1_facilities_raw.csv` on every machine, in `Day3/` |
| Yesterday's work | Each participant has their own cleaned file and whatever notes they made on Day 2. **Do not let them redo the cleaning** |
| Pairing list | Prepared in advance - see pairing rule below |
| Printed briefs | One per participant. Brief A at the start; **hold Brief B back** |
| Timer | Visible to the room |
| Flip chart | Headed "What stopped us" |

**Pairing rule.** Pair across the pre-assessment range - a higher scorer with a
lower scorer - but **never announce why pairs were formed**. Same-level pairs
produce either two failures with no diagnosis, or two people who assume the tool
is broken.

**One machine per pair for the reproduction phase.** They must work on the
partner's file together; watching someone struggle with your instructions is
where the learning is.

---

## Minute by minute

### 0-8 · Framing

Say, roughly - this wording is not load-bearing:

> "Yesterday you each cleaned the facility list. This morning we are going to
> check something simple: whether the work you did is *usable by the department*
> or only usable by you."

Then, verbatim, because this line prevents the session being read as a test:

> **"Nobody's cleaning is being marked this morning. What we are testing is the
> handover, not the person."**

Hand out **Brief A**. Do not hand out Brief B.

### 8-25 · Task A - write the record (17 min)

Participants work **alone**, writing the record of what they did yesterday. Brief
A gives them the format.

**Walk the room. Do not correct anything.** You will see records that say
"cleaned the LGA names" with no list of what changed. Leave them. Correcting now
destroys the session.

If asked *"how much detail?"*, reply:

> **"Enough that someone else could do exactly what you did."**

Then leave. Do not elaborate - the ambiguity is the point, and most will resolve
it too thinly.

At 25 minutes, stop them **whether or not they have finished.** Collect nothing.

### 25-50 · Task B - reproduce your partner's work (25 min)

Hand out **Brief B**. Announce the rule, verbatim:

> **"From now until I call time, you may not speak to your partner about their
> work. Not one question. If their record does not tell you something, write down
> what it did not tell you and carry on as best you can."**

Pairs move to one machine, open the **raw** file and the **partner's record**,
and attempt to produce the partner's cleaned file.

**Enforce the no-talking rule firmly.** It will be broken within four minutes,
usually by the record's author leaning in to explain. That instinct is exactly
what the session is about. Intervene with:

> "That is the fourth thing you have had to explain. Write each one down - that
> list is your real output this morning."

**Your job in this phase is to notice, not to help.** Track which failures recur;
you will need them at 50 minutes.

At 45 minutes, ask each pair to note **row counts** for the file they produced
and the partner's original.

### 50-65 · What stopped us (15 min)

Round the room. Each pair gives **one** thing the record failed to tell them.
Write them on the flip chart, grouped as they emerge. Do not attribute to
individuals - say "a pair found", never a name.

**Expected groupings** (see the errors table below): order not stated, "cleaned"
without saying how, decisions not recorded, source file ambiguous, counts absent.

Then ask the room, and wait for the answer rather than supplying it:

> **"How many of you produced a file with the same number of rows as your
> partner's?"**

Typically two or three pairs of ten. Let the silence sit. **This is the moment
the session exists for.** Do not rescue it, and do not lecture. Say only:

> "So the work was right, and it did not survive the handover."

### 65-83 · Repair and re-test (18 min)

Participants take back their own record and rewrite it using the flip chart.
**10 minutes.**

Then **re-pair with a different partner** and give **8 minutes** to attempt
reproduction again. Eight minutes is not enough to finish, and it does not need
to be - what is being tested is whether the second reader gets *further*, not
whether they finish.

Ask for a show of hands: **"Who got further this time?"** Near-universal, and it
is the first evidence they have that the fix is achievable.

### 83-90 · Consolidate

Ask the room for the minimum a record must contain. Take five or six items only.
You will get most of the model answer back; supply nothing they do not offer,
and do not correct omissions - Day 3 session 3 is where they draft the full
standard, and it must be theirs.

Close, verbatim:

> **"Your cleaning was not the problem. Every one of you could repeat your own
> work. The department cannot, and that is a different skill - it is the one we
> are building this week."**

---

## Common errors, and how to intervene

Ranked by how often they occur. **Interventions are all delayed to the 50-minute
discussion unless flagged otherwise** - correcting during Task B removes the
evidence.

| # | What you will see | Why it happens | Intervention |
|---|---|---|---|
| 1 | *"Removed duplicates"* - no key, no count, no rule for which was kept | Deduplication feels self-evident to the person who did it | At 50 min: "Which of the two rows survived? Did your partner keep the same one?" |
| 2 | Steps in the wrong order, or no order at all | They remember the *set* of actions, not the sequence | Ask a pair to state what happens if trimming spaces comes after grouping names. Let them work it out |
| 3 | *"Corrected the LGA names"* with no mapping | The variants were obvious on the day | "Your partner has seen `Idi Oro`, `IDI-ORO` and `Idi-oro`. Which is correct, and how would they know?" |
| 4 | No row counts anywhere | Counting feels bureaucratic until reproduction fails | This is why the row-count check at 45 min exists. Let the numbers make the argument |
| 5 | Source file ambiguous - several files named `facilities_final` | Nobody names a file for a reader | Ask which file the partner opened. Often the wrong one, and everything after was wasted |
| 6 | Judgement calls not recorded at all | The 5 facilities with no coordinates were dropped, or kept, and it seemed obvious | The most important error in the session. "You made a decision. Your partner made the opposite one. Neither of you is wrong - but the numbers now differ and nobody knows why" |
| 7 | The record describes *intent*, not *action* - "made the data consistent" | Writing about work is a different skill from doing it | "Read that sentence and tell me the first thing your partner should click" |
| 8 | Author explains verbally, then insists the record was fine | The gap is genuinely invisible from inside | **Intervene immediately.** "Stop - write down what you just said. That sentence is the missing line" |

### Two situations that need handling on the spot

**A pair reproduces the file exactly.** It happens once or twice, and it is a
genuine level-3 result. Do not make an example of them in a way that isolates the
room. Ask the *reproducer*, not the author: *"What did their record have that
made this possible?"* Their answer goes on the flip chart and carries more weight
than anything you say.

**A participant becomes defensive** - usually a senior one whose record failed
publicly. Redirect to the artefact, never the person: *"The record is the thing
we are fixing, not the cleaning. Your cleaning was correct."* If it persists,
move them into the repair phase early and let them succeed at the rewrite.

---

## If you are running short of time

Cut in this order:

1. **The second re-pair at 75 min** - shorten to 5 minutes. Getting further is
   the point; finishing is not.
2. **The consolidation at 83 min** - Day 3 session 3 covers it.
3. **Never cut the reproduction attempt or the row-count check.** Without them the
   session is a lecture about documentation, which is what the department has
   already had and has not acted on.

## What success looks like

Not a room that has written good documentation. **A room that has felt the gap.**

The measurable outcome is at 83 minutes: *"who got further this time?"* If most
hands go up, they have learned that the fix is small and achievable, which is
what makes them do it next week when nobody is watching.
