# Q6 — Building capability in the counterpart agency

**Main response: 6 pages. Annexes A–D are excluded from the limit**, per the
question. The 90-minute session artefact, the full competency grid, and the
pre/post instrument are in the annexes because they are artefacts to be used,
not argument to be read.

---

## 1. What the evidence says, before designing anything

Four findings, and three of them contradict the obvious course.

### 1.1 They know more than they can do

| | |
|---|---|
| Composite capability score | **36 / 100** |
| Objective knowledge test | **57%** across 12 items |

These do not agree, and the gap is the design brief. A department that recalls
57% of what it is asked but scores 36 on applied capability does not have a
knowledge problem. **It has an application problem.**

That rules out the default response. More instruction closes a knowledge gap;
this cohort has already met the material and cannot convert it into work. The
lever is supervised practice on real tasks, not content delivery — which is why
the course below runs at **70% hands-on** and why every block ends in a product
rather than a summary.

### 1.2 They cannot judge their own competence — so nothing self-reported can steer the design

A correlation of **0.11** between self-rating and tested knowledge is not weak.
It is *nothing*: knowing someone's self-assessment tells you essentially nothing
about their ability. Three consequences follow, and each removes a tool I would
normally use.

- **No streaming by self-assessment.** Grouping by confidence would produce
  groups uncorrelated with ability. Any streaming must come from the
  **demonstrated** pre-assessment in Annex C.
- **Stated demand is not a needs analysis.** Demand is *"near universal across
  all competency areas"* — from a cohort that cannot locate its own gaps. It
  tells me what is attractive, not what is missing. Treating it as a needs
  assessment would produce a syllabus optimised for appeal.
- **Self-rated improvement is worthless as an outcome.** If self-rating is
  uninformative at baseline, a rise in it after training measures comfort, not
  capability. The evaluation in §5 therefore rests on demonstrated tasks and on
  independent reproduction.

**And it dictates day one specifically.** Twenty-one people will arrive believing
they are more capable than they are, and *being told otherwise does not work* —
it produces defensiveness in the room and disengagement by the afternoon. The
gap has to be **discovered, not announced**. Day 1 opens with a task at their
stated level that they cannot complete, followed immediately by the same task
made tractable by one technique. The realisation is theirs; the recovery is
immediate; nobody is corrected in front of colleagues.

Facilitator rule for day one, in Annex B and worth stating here: **never name an
individual's score, and never compare two participants aloud.** The diagnostic is
the room's, not a person's.

### 1.3 The binding constraint is software access — and the finding is stranger than it looks

**Zero of 21 have access to QGIS or ArcGIS.**

The important thing is that **QGIS is free.** ArcGIS costs money; QGIS costs
nothing and runs on any machine of the last decade. So this is not a budget
finding. Zero access to a free tool means one of:

- staff have no administrative rights to install software;
- the machines are too old, or there are not enough of them;
- an IT policy blocks unapproved installations;
- or there are no machines allocated to this work at all.

**These have completely different remedies, and nobody has established which
applies.** That single unanswered question governs the whole programme, because
it decides whether the constraint can be lifted in two weeks or two quarters.
Establishing it is action one of the 90-day plan (§6), scheduled *before* the
course, not after.

It also settles the training platform. I will not teach on software the
department cannot open on Monday — that produces a week of enjoyable work and
zero transfer. The course runs on **QGIS Portable from USB, which installs
nothing and requires no administrative rights**, and each participant keeps the
stick. If the cause is admin rights or IT policy, that removes the constraint on
day one. If the cause is hardware, portable QGIS will reveal it immediately and
the escalation in §6 becomes a procurement case with evidence behind it.

### 1.4 The weakest competency is also the highest-leverage one

**Documenting a reproducible cleaning workflow: 1.5 / 5** — the lowest measured
score.

This is fortunate, because it is also the skill that determines whether anything
else survives. A department that cannot document a cleaning workflow cannot hand
work over, cannot audit a number, and cannot absorb a resignation. It is the same
fragility described in the coordination scenario, in a different building (§7).

So documentation is not a module in this course. **It is the spine**, and every
other block is assessed by whether its output can be re-run by someone else.

### 1.5 The one thing they want, used rather than refused

Strongest stated demand is **map production and cartography**. It is not what
they most need — but refusing it would be a mistake. Cartography is the visible,
satisfying end of this work, and it is where the department already feels
ownership.

**So it becomes the vehicle, not the syllabus.** Every exercise ends in a map,
and every map is only accepted if the steps that produced it can be repeated by
a colleague. They get the thing they asked for; the price of receiving it is the
thing they need.

---

## 2. Competency framework

Five levels, defined by **what a person is observed to do**, not by how much they
know. The full 6-domain grid is **Annex A**; the documentation domain is worked
here because it is the weakest and the most load-bearing.

### 2.1 The levels

| Level | Name | The observable test |
|---|---|---|
| **0** | Not yet demonstrated | Cannot begin the task without someone performing it for them |
| **1** | Assisted | Completes the task while following a written procedure step by step. Stops when the procedure does not match what is on screen |
| **2** | Independent | Completes the task correctly from a stated objective, without a procedure. **Cannot yet be re-run by anyone else** |
| **3** | Reproducible | Output is correct **and** a colleague of the same level reproduces it from what was left behind, without asking the author a question |
| **4** | Improving | Diagnoses why someone else's workflow failed, repairs the process rather than the output, and the repair holds for the next person |

The line that matters is **between 2 and 3**, and most frameworks do not draw it.
"Can do it alone" is where training normally stops and where this department's
problem actually starts: twenty-one people at level 2 still produce a department
that cannot survive one of them leaving.

**Level 3 is testable without judgement.** Hand the artefact to a colleague, give
them the raw data, forbid them to ask the author anything, and see whether the
output matches. It either does or it does not.

### 2.2 Worked domain — Documenting a reproducible cleaning workflow

| Level | Observable behaviour |
|---|---|
| 0 | Cleans by editing cells directly in the source file. No record of what changed |
| 1 | Keeps the raw file untouched and works on a copy, when reminded to |
| 2 | Keeps raw and working copies separate and can describe the changes made, from memory, on the same day |
| 3 | Leaves a written record naming every change, the reason for it, and the number of rows affected — **and a colleague reproduces the cleaned file from the raw file using only that record** |
| 4 | Reviews a colleague's record, identifies the step that cannot be repeated, and rewrites it so the next person does not hit the same gap |

Baseline is **1.5**: between "keeps a copy when reminded" and "can describe it
from memory today". The course targets **level 3 for the whole cohort on one
workflow** — not level 3 across all domains, which is not achievable in five days
and pretending otherwise is how these programmes fail.

---

## 3. The five-day course

**Ratio: 70% hands-on, 30% instruction.** Instruction blocks are capped at 20
minutes and each is followed immediately by the task that uses it. This follows
directly from §1.1 — the cohort's deficit is application, and lecture is the
wrong instrument for an application deficit.

Learning outcomes are written at the cognitive level the evidence supports.
Nothing is set at *evaluate* or *create* on day one for a cohort scoring 36.

### Day 1 — What is actually in the data
**Outcome (apply):** Given an unfamiliar dataset, produce a written inventory of
its defects — counts, not impressions — without cleaning anything.

| Session | Min | Exercise | Dataset |
|---|---|---|---|
| The task you cannot yet do | 60 | Produce a facility map from raw data, unaided. Most will not finish | D1 (Annex D) |
| Why it failed | 20 | Facilitated, findings collected from the room, no individual named | — |
| Profiling before touching | 90 | Count rows, duplicates, blanks, out-of-range values, name variants | D1 |
| Writing a defect register | 90 | Produce a defect table: what, how many, how found | D1 |

Day 1 is the day the self-assessment gap gets closed by experience rather than by
being told. It ends with a product, so the discomfort of the morning resolves.

### Day 2 — Cleaning that can be checked
**Outcome (apply):** Clean a dataset so that every change is counted and no
record is silently dropped.

| Session | Min | Exercise | Dataset |
|---|---|---|---|
| Rules, not repairs | 20 | Instruction | — |
| Cleaning to a rule set | 120 | Fix each defect from Day 1 as a stated rule; record rows affected | D1 |
| Nothing disappears | 60 | Reconcile input rows against output rows; account for every difference | D1 |
| Ambiguous cases | 60 | Cases with no correct answer. Decide, and write down why | D1 |

### Day 3 — Reproducibility (the spine)
**Outcome (apply → analyse):** Produce a record from which a colleague
reproduces your cleaned dataset without speaking to you.

| Session | Min | Exercise | Dataset |
|---|---|---|---|
| **Make your work someone else's** | **90** | **Full artefact in Annex B** | D1 / D2 |
| Repairing the record | 60 | Rewrite the documentation that failed; re-test with a different partner | D1 |
| The department's own standard | 90 | The cohort drafts the minimum documentation standard *they* will use | — |

Drafting the standard themselves is deliberate. A standard issued to this
department will not be followed; one they wrote and immediately tested might be.

### Day 4 — Spatial data, and the map they came for
**Outcome (apply):** Produce a correctly projected, properly furnished map from a
cleaned dataset, and state what it does not show.

| Session | Min | Exercise | Dataset |
|---|---|---|---|
| Coordinates, joins, and why maps lie | 20 | Instruction | — |
| Joining and checking | 90 | Join facilities to wards; find and count the failures | D2 |
| Projection, in practice not theory | 45 | Measure the same distance in three CRS; see the answers differ | D2 |
| Map production | 120 | Full cartographic furniture; every map states its projection and source | D2 |

The projection block teaches by consequence, not by theory. Measuring one
distance three ways and getting three answers takes fifteen minutes and is
remembered; a lecture on datums is not.

### Day 5 — Their own work, and what happens next
**Outcome (apply → evaluate):** Complete a real departmental product to level 3,
and review a colleague's to level 4.

| Session | Min | Exercise | Dataset |
|---|---|---|---|
| Bring your own task | 150 | Each participant works a real, current departmental task | Their own |
| Peer reproduction | 60 | Exchange and attempt to reproduce. This is the post-assessment (§5) | Their own |
| The 90 days | 60 | Each participant leaves with a named product, a date, and a reviewer | — |

Day 5 uses the department's real work deliberately. Training data produces
training-shaped competence, and the transfer problem is the one this programme
exists to solve.

---

## 4. What I have chosen not to teach, and why

A five-day course promising spatial statistics, remote sensing, web mapping and
automation to a cohort scoring 36 is a design failure. Each of these was
considered and cut.

| Not taught | Why |
|---|---|
| **Spatial statistics** | Requires trust in the underlying data. This cohort cannot yet establish that a dataset is clean, so a significance test would be a confident answer resting on unexamined input — actively worse than no answer |
| **Remote sensing** | An entire discipline. Five days would produce vocabulary and no capability, and there is no departmental workflow currently demanding it |
| **Web mapping / dashboards** | Publishing is the last problem this department has. It would put unverified data in front of more people, faster |
| **Python / R automation** | The one I most wanted to include, and cutting it was the hardest call. It adds a *second* novel discipline — programming — on top of the first, reproducibility, before the first is secure. Reproducibility is achievable with the tools they have; automation is a later programme for those who reach level 4 |
| **Geodatabase administration** | No database to administer until access is resolved |
| **Advanced cartographic design** | Their strongest demand, and deliberately capped at competent-and-honest rather than beautiful. Beauty is not the department's constraint |

**The principle:** at capability 36 with the weakest score in documentation,
breadth produces people who can *name* techniques and *deliver* none. Depth on
one chain — profile, clean, document, map, hand over — produces people who can
complete a real task and prove it. Nothing here is permanently excluded; each is
a candidate for the programme after the 90 days, conditional on measured
progress.

---

## 5. Pre and post assessment

**Demonstrated capability only.** No confidence items, no satisfaction items, no
self-rating as an outcome — §1.2 disqualifies all three. Full instrument,
rubric and both datasets in **Annex C**.

### Structure

**A practical task, scored against the level definitions in §2** — identical in
structure at both administrations, on **parallel datasets** (D-PRE and D-POST)
built to the same specification with the same defect classes at the same
frequencies, but different values. Same difficulty, no memorisation.

Eight tasks, each scored **0–4** against the framework: 32 points. Tasks span
profiling, cleaning, documentation, joining, projection, map production, and
stating a limitation.

### The item that carries the whole design

**Task 8 is not performed by the participant.** Their submitted work is given to
an assessor who has not seen it, with the raw data and no access to the author.
The score is whether the output is reproduced.

This measures the thing the course is for, and it cannot be faked, coached, or
inflated by a confident participant. It is also the only item that tests level 3
directly.

### Comparability

Same rubric, same eight tasks, same time limit, parallel datasets, and **blind
marking** — assessors see submissions without names or administration order, so
the same marker cannot unconsciously reward improvement they expect.

### One secondary measure, and it is not an outcome

The self-rating item is retained at both administrations — **not as a measure of
capability, but of calibration.** Baseline correlation between self-rating and
tested score is 0.11. If it rises, participants have learned to judge their own
competence, which is a real and separately valuable result: a department that
knows what it cannot do asks for help before it produces a wrong number.

Reported separately, and never as evidence of capability.

---

## 6. The ninety days after the course

Training that ends when the course ends is the failure mode this section exists
to prevent.

### Days −14 to 0 — before the course: resolve the binding constraint

**This runs before day one, not after.** Nothing in the course transfers if
participants cannot open the software on the Monday after.

1. **Establish why access is zero.** A 30-minute conversation with the agency's
   IT function and one attempt to install QGIS on a departmental machine
   distinguishes admin rights from hardware from policy. Until this is known,
   every remedy is a guess.
2. **Deploy QGIS Portable on USB** to all 21 participants. Requires no
   administrative rights and no installation. It removes the constraint
   immediately if the cause is rights or policy, and demonstrates it hard if the
   cause is hardware.
3. **Escalate with evidence, not a request.** If hardware is the cause, the ask
   to the counterpart's management is specific and costed, and carries the
   assessment finding: a department contractually committed to geospatial output
   with zero capacity to run geospatial software.

### Days 1–30 — applied work under review

- Each participant leaves day 5 with **one named real product, a delivery date,
  and a named reviewer.**
- Fortnightly 60-minute clinics, remote. Not teaching — **participants bring work
  that is stuck.**
- Every product goes through **peer reproduction** before it is accepted. The
  level-3 test becomes routine practice rather than an assessment event.

### Days 31–60 — the department's own standard becomes binding

- The documentation standard drafted on day 3 is **adopted formally** by the
  department head, having been tested on 30 days of real work rather than issued
  from outside.
- Two or three participants reaching level 4 take over **reviewing** others'
  work. Capability transfers to the department when the review stops being mine.
- **Access is resolved or formally escalated.** If neither, the programme reports
  it as a failure of the commitment rather than of the training — that
  distinction is the honest one and it belongs on the record.

### Days 61–90 — measure, and decide what is next

- **Post-assessment**, including the independent reproduction task.
- **Capability transfer measured**, not satisfaction:

| Indicator | Measures |
|---|---|
| % of participants with working GIS software on their own machine | Whether the binding constraint was actually lifted |
| Number of real departmental products delivered to level 3 | Whether skills reached real work |
| Independent reproduction success rate | Whether the core skill transferred |
| Number of reviews conducted **by the department**, not by me | Whether capability is now self-sustaining |
| Change in tested score, pre to post | Capability |
| Change in self-rating/tested correlation | Calibration, reported separately |

**Not measured, deliberately:** satisfaction, self-rated confidence, attendance,
or number trained. Every one of them can be excellent while nothing changed.

- **The next programme is conditional.** Automation and spatial statistics become
  available to participants who reach level 4 — earned by demonstration, not by
  attendance. A cohort that has not reached level 3 gets a repeat of this
  programme, and saying so at the outset is what makes level 3 mean something.

---

## 7. Why this is the same problem as the coordination scenario

The scenario has two failures presented as separate obligations, and they are one
problem.

Two of six state analysts resign and delivery is threatened — which is only true
because their knowledge was never written down. The counterpart department scores
1.5 out of 5 on documenting a reproducible workflow. **These are the same finding
in two organisations.** In both, capability lives in individuals rather than in
the process, so the organisation's competence is exactly as durable as its
staffing.

That is why documentation is the spine of this course rather than a module in it,
and why level 3 — *"a colleague reproduces it without asking you"* — is the
threshold the whole programme is built around. It is the operational definition
of knowledge that has left someone's head.

It is also why the two obligations do not compete for my time in the way the
scenario implies. The handover protocol I would impose on my own departing
analysts and the standard this department drafts on day 3 are **the same
artefact**. Building it once, in the open, with the counterpart participating,
serves both — and a counterpart that has watched me handle a live coordination
failure has learned something no five-day course delivers.

**The honest caveat:** this is a genuine connection, not a universal one. If the
counterpart's real constraint turns out to be hardware rather than knowledge,
then no documentation standard fixes it, and the two problems come apart
completely. The 90-day plan's first action exists precisely because the answer to
that question determines whether this argument holds.

---

### Annexes (excluded from the page limit)

- **Annex A** — Full competency framework, 6 domains × 5 levels
- **Annex B** — The 90-minute session, in full: facilitator guide, participant
  brief, model answer, expected errors and interventions
- **Annex C** — Pre/post instrument: 8 tasks, rubric, scoring, parallel datasets
- **Annex D** — Training dataset specifications D1, D2, D-PRE, D-POST
