# Q6 - Building capability in the counterpart agency

**Main response: 6 pages; Annexes A-E excluded**, per the question. The annexes
carry artefacts to be used - the session, the grid, the instrument, the datasets,
the session-by-session plan. The response carries the argument.

---

## 1. What the evidence says, before designing anything

Four findings, and three of them contradict the obvious course.

### 1.1 They know more than they can do

| | |
|---|---|
| Composite capability score | **36 / 100** |
| Objective knowledge test | **57%** across 12 items |

These do not agree, and the gap is the design brief. Recalling 57% while scoring
36 on applied capability is not a knowledge problem - **it is an application
problem.** That rules out the default response: more instruction closes a
knowledge gap, and this cohort has already met the material and cannot convert it
into work. The lever is supervised practice, which is why **95% of timetabled
minutes are participants working** (§3) and every block ends in a product rather
than a summary.

### 1.2 They cannot judge their own competence - so nothing self-reported can steer the design

A correlation of **0.11** between self-rating and tested knowledge is not weak.
It is *nothing*: knowing someone's self-assessment tells you essentially nothing
about their ability. Three consequences follow, and each removes a tool I would
normally use.

- **No streaming by self-assessment** - groups formed by confidence would be
  uncorrelated with ability. Streaming comes from the demonstrated
  pre-assessment (Annex C).
- **Stated demand is not a needs analysis.** Demand is *"near universal"*, from a
  cohort that cannot locate its own gaps: it says what is attractive, not what is
  missing, and treating it as a needs assessment produces a syllabus optimised
  for appeal.
- **Self-rated improvement is worthless as an outcome.** If self-rating is
  uninformative at baseline, a rise after training measures comfort. §5 therefore
  rests on demonstrated tasks and independent reproduction.

**It also dictates day one.** Twenty-one people will arrive believing they are
more capable than they are, and being told otherwise produces defensiveness by
mid-morning and disengagement by the afternoon. The gap must be **discovered, not
announced**: day 1 opens with a task at their stated level that they cannot
finish, followed immediately by the technique that makes it tractable. The
realisation is theirs and the recovery is immediate. Facilitator rule throughout:
**never name an individual's score, never compare two participants aloud.**

### 1.3 The binding constraint is software access - and the finding is stranger than it looks

**Zero of 21 have access to QGIS or ArcGIS.**

The important thing is that **QGIS is free**, and runs on any machine of the last
decade. This is not a budget finding. Zero access to a free tool means no
administrative rights to install; or machines too old or too few; or an IT policy
blocking installations; or no machines allocated to this work at all.

**These have entirely different remedies and nobody has established which
applies** - a single unanswered question that decides whether the constraint
lifts in two weeks or two quarters. Establishing it is action one of the 90-day
plan (§6), scheduled *before* the course.

It also settles the platform. I will not teach on software the department cannot
open on Monday; that produces a pleasant week and zero transfer. The course runs
on **QGIS Portable from USB - installs nothing, needs no administrative rights**
- and each participant keeps the stick. If the cause is rights or policy, the
constraint lifts on day one. If it is hardware, portable QGIS proves it
immediately and the escalation becomes a costed case with evidence behind it.

### 1.4 The weakest competency is also the highest-leverage one

**Documenting a reproducible cleaning workflow: 1.5 / 5** - the lowest measured
score.

Fortunate, because it is also the skill that determines whether anything else
survives: a department that cannot document a cleaning workflow cannot hand work
over, audit a number, or absorb a resignation - the same fragility as the
coordination scenario, in a different building (§7). So documentation is not a
module here. **It is the spine**, and every other block is assessed by whether
its output can be re-run by someone else.

### 1.5 The one thing they want, used rather than refused

Strongest stated demand is **map production and cartography** - not what they
most need, but refusing it would be a mistake: it is the visible end of this work
and where the department already feels ownership. **So it becomes the vehicle,
not the syllabus.** Every exercise ends in a map, and every map is accepted only
if a colleague can repeat the steps. They get what they asked for; the price of
receiving it is the thing they need.


---

## 2. Competency framework

Five levels, defined by **what a person is observed to do**, not by how much they
know. Full 6-domain grid in **Annex A**.

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

### 2.2 The target, and its limit

Baseline for documentation is **1.5** - between "keeps a copy when reminded" and
"can describe it from memory today". The course targets **level 3 for the whole
cohort on one workflow**: not level 3 across all six domains, which is not
achievable in five days, and claiming it would read well and not survive the
post-assessment.

Full grid - six domains × five levels, each cell an observable behaviour - in
**Annex A**.

---

## 3. The five-day course

**Ratio: 1,245 of the 1,305 timetabled minutes are participants working - 95%.**
Instruction is four blocks, each capped at 20 minutes and each followed
immediately by the task that uses it. Annex E times every session, so the ratio
is counted rather than asserted; what it does not separately time is the
explaining and debriefing a facilitator does *inside* a working session, which
is why the felt balance in the room is nearer 70:30 than 95:5.

This follows directly from §1.1 - the cohort's deficit is application, and
lecture is the wrong instrument for an application deficit.

Learning outcomes are written at the cognitive level the evidence supports.
Nothing is set at *evaluate* or *create* on day one for a cohort scoring 36.

### Day allocation and outcomes

Full session-by-session detail - every exercise, dataset and duration - in
**Annex E**. Learning outcomes are written at the cognitive level the evidence
supports; nothing is set at *evaluate* or *create* on day one for a cohort
scoring 36.

| Day | Focus | Outcome | Hands-on |
|---|---|---|---|
| **1** | What is actually in the data | **Apply** - given an unfamiliar dataset, produce a written inventory of its defects, in counts rather than impressions, without cleaning anything | 240 / 20 min |
| **2** | Cleaning that can be checked | **Apply** - clean a dataset so every change is counted and no record is silently dropped | 240 / 20 min |
| **3** | **Reproducibility - the spine** | **Apply → analyse** - produce a record from which a colleague reproduces your cleaned dataset without speaking to you | 240 / 0 min |
| **4** | Spatial data, and the map they came for | **Apply** - produce a correctly projected, properly furnished map, and state what it does not show | 255 / 20 min |
| **5** | Their own work, and what happens next | **Apply → evaluate** - complete a real departmental product to level 3, and review a colleague's to level 4 | 270 / 0 min |

Three sessions carry the design. **Day 1 opens with a task they cannot finish**
(§1.2) and still ends in a product, so the morning's discomfort resolves the same
day. **Day 3 session 1 - "Make your work someone else's" - is the session
developed in full as Annex B**, and session 3 has the cohort draft *their own*
documentation standard, because a standard issued to this department will not be
followed and one they wrote and tested might be. **Day 5 uses the department's
real work**, since training data produces training-shaped competence and transfer
is the problem this programme exists to solve; its closing peer-reproduction
doubles as the post-assessment.

## 4. What I have chosen not to teach, and why

A five-day course promising spatial statistics, remote sensing, web mapping and
automation to a cohort scoring 36 is a design failure. Each of these was
considered and cut.

| Not taught | Why |
|---|---|
| **Spatial statistics** | Requires trust in the underlying data. This cohort cannot yet establish that a dataset is clean, so a significance test would be a confident answer resting on unexamined input - actively worse than no answer |
| **Remote sensing** | An entire discipline. Five days would produce vocabulary and no capability, and there is no departmental workflow currently demanding it |
| **Web mapping / dashboards** | Publishing is the last problem this department has. It would put unverified data in front of more people, faster |
| **Python / R automation** | The one I most wanted to include, and cutting it was the hardest call. It adds a *second* novel discipline - programming - on top of the first, reproducibility, before the first is secure. Reproducibility is achievable with the tools they have; automation is a later programme for those who reach level 4 |
| **Geodatabase administration** | No database to administer until access is resolved |
| **Advanced cartographic design** | Their strongest demand, and deliberately capped at competent-and-honest rather than beautiful. Beauty is not the department's constraint |

**The principle:** at capability 36 with the weakest score in documentation,
breadth produces people who can *name* techniques and *deliver* none. Depth on
one chain - profile, clean, document, map, hand over - produces people who can
complete a real task and prove it. Nothing here is permanently excluded; each is
a candidate for the programme after the 90 days, conditional on measured
progress.

---

## 5. Pre and post assessment

**Demonstrated capability only.** No confidence items, no satisfaction items, no
self-rating as an outcome - §1.2 disqualifies all three. Full instrument, rubric
and datasets in **Annex C**.

A **practical task**: 8 items scored 0-4 against the level definitions, 32
points, 3 hours, blind marked. Identical tasks and rubric at both administrations
on **parallel datasets** - same defect specification, same frequencies, different
values, so the difficulty matches and the post-test cannot be passed from memory.
The parallel-form claim is *verified rather than asserted*: the dataset generator
compares defect profiles across the files and fails if they differ.

**Task 8 carries the design, and the participant does not perform it.** Their
submitted work goes to an assessor who has not seen it, with the raw data and no
access to the author; the score is whether the output reproduces. It is the only
item that tests level 3 directly, and the only one that cannot be faked, coached
or inflated by a confident participant. Someone can score well on tasks 1-7 and
**zero on 8** - which is precisely this department's present condition, so the
instrument has to be able to detect it.

**One secondary measure, never an outcome.** The self-rating item is retained
only to recompute the 0.11 correlation as a measure of *calibration*. If it
rises, participants have learned to judge their own competence - and a department
that knows what it cannot do asks for help before producing a wrong number.
Reported on its own line, never as evidence of capability.

---

## 6. The ninety days after the course

Training that ends when the course ends is the failure mode this section exists
to prevent.

### Days −14 to 0 - before the course: resolve the binding constraint

**This runs before day one, not after.** Nothing transfers if participants cannot
open the software on the Monday afterwards.

1. **Establish why access is zero.** One conversation with the agency's IT
   function and one attempt to install QGIS on a departmental machine
   distinguishes admin rights from hardware from policy. Until this is known,
   every remedy is a guess.
2. **Deploy QGIS Portable on USB** to all 21. No administrative rights, no
   installation - it removes the constraint immediately if the cause is rights or
   policy, and demonstrates it hard if the cause is hardware.
3. **Escalate with evidence, not a request.** If hardware is the cause, the ask
   to the counterpart's management is specific and costed, and carries the
   finding: a department contractually committed to geospatial output with zero
   capacity to run geospatial software.

### Days 1-30 - applied work under review

Each participant leaves day 5 with **one named real product, a delivery date and
a named reviewer.** Fortnightly 60-minute remote clinics - not teaching;
participants bring work that is stuck. Every product passes **peer reproduction**
before acceptance, so the level-3 test becomes routine practice rather than an
assessment event.

### Days 31-60 - the standard becomes binding

The documentation standard drafted on day 3 is **formally adopted** by the
department head, having been tested on 30 days of real work rather than issued
from outside. Two or three participants reaching level 4 take over **reviewing**
others' work - capability transfers when the review stops being mine. **Access is
resolved or formally escalated**; if neither, the programme reports it as a
failure of the commitment rather than of the training, and that distinction
belongs on the record.

### Days 61-90 - measure, and decide what is next

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
  available to participants who reach level 4 - earned by demonstration, not by
  attendance. A cohort that has not reached level 3 gets a repeat of this
  programme, and saying so at the outset is what makes level 3 mean something.

---

## 7. Why this is the same problem as the coordination scenario

The scenario presents two obligations competing for my time. They are one
problem.

Two of six state analysts resign and delivery is threatened - true only because
their knowledge was never written down. The counterpart department scores **1.5
out of 5 on documenting a reproducible workflow.** The same finding in two
organisations: capability living in individuals rather than in the process, so
competence is exactly as durable as staffing.

That is why documentation is the spine of this course, and why level 3 - *a
colleague reproduces it without asking you* - is the threshold the programme is
built around. It is the operational definition of knowledge that has left
someone's head.

It is also why the two obligations do not compete as the scenario implies. The
handover protocol for my own departing analysts and the standard this department
drafts on day 3 are **the same artefact**, and building it once, in the open,
with the counterpart participating, serves both.

**The honest caveat:** this is a genuine connection, not a universal one. If the
counterpart's real constraint proves to be hardware rather than knowledge, no
documentation standard fixes it and the two problems come apart completely. The
90-day plan's first action exists because the answer decides whether this
argument holds.


### Annexes (excluded from the page limit)

**A** competency framework · **B** the 90-minute session in full - facilitator
guide, participant briefs, model answer and dataset generator · **C** pre/post
assessment instrument · **D** dataset specifications · **E** session-by-session
course plan
