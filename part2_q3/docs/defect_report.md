# Defects in Form HH/2026/v1, and what was done about each

The questionnaire is ethics-approved (BSHREC/2026/041) and will not be redesigned. That
constrains the response: **a defect that changes what is asked, or what a response means,
is escalated, not silently repaired.** A defect that only concerns how an answer is
captured is fixed in the digital form, because that is what the digital form is for.

Each entry states the disposition and why. Numbering follows the paper form.

---

## A. Internal contradictions

### A1 - Column (7) is "office use, leave blank", yet 3.02 asks the enumerator to read it
**Severity: high. This one stops the form working.**

The roster instruction says *"Column (7) is completed by the office and must be left blank
in the field."* Then 3.02 asks: *"**From column (7)**, how many children in this household
are aged 9 to 59 completed months?"*

The enumerator is instructed to read a total from a column they were forbidden to fill.
On paper a clerk resolves this silently. A digital form cannot.

**Disposition: resolved in the form, and it resolves itself.** Eligibility is derived from
the roster ages rather than transcribed - the count of residents with age 9-59 completed
months is calculated. 3.02 becomes a read-only calculated field, and column (7) disappears
as a field-entered concept. **Escalated as a note** because the paper instrument's
intent is ambiguous: it is not certain whether the office was meant to determine
eligibility on a different rule.

### A2 - 4.08 asks for a three-way distinction and offers a two-way code
**Severity: medium.**

*"Record whether a card, a card copy, or an electronic record was seen by you."* Coding
categories: `Card seen 1 / No card seen 2`.

The question asks the enumerator to distinguish three document types; the coding cannot
record which. Any analysis of documentation quality is impossible, and the enumerator is
left guessing whether a photographed card counts.

**Disposition: escalated, with a minimal in-form mitigation.** Changing the response
options changes what is asked, which requires ethics re-approval. The form keeps the
two-way code and adds an optional follow-up capturing document type **only when
`card_seen = 1`**, flagged in the codebook as an addition not present on paper. Recommend
the paper form be corrected at the next revision.

### A3 - Section 5 says "every eligible child", 5.01 restricts to 12 months and over
**Severity: medium.**

Section 5's instruction reads *"A stool specimen is sought from every eligible child."*
Eligible children are 9-59 months (per Section 4). But 5.01 asks *"Is the child aged 12
completed months or older?"* with `No → Section 6`.

Children aged 9-11 months are eligible for Section 4 and ineligible for a specimen. The
instruction and the filter contradict each other.

**Disposition: resolved in the form.** 5.01 is calculated from `age_months`, not asked, so
the filter governs and the contradiction cannot produce inconsistent data. The instruction
text is corrected to "every eligible child aged 12 months or older". **Escalated** so the
paper wording is fixed.

### A4 - Roster holds 12 lines; household size accepts two digits
**Severity: medium.**

3.01 records household size in a two-digit field (up to 99). The roster table has **12
rows**. A household of 15 cannot be listed, so the roster and the stated size will
disagree by construction, and the paper form gives the enumerator nowhere to put residents
13 onward.

**Disposition: resolved in the form.** The digital roster is an unbounded repeat, so the
constraint vanishes. The consistency check between 3.01 and the roster count (see F4) then
becomes meaningful rather than an artefact of table height.

### A5 - Section 4 page number is one digit; eligible-children count is two
**Severity: low.**

*"Section 4 page number ⌷ of ⌷"* allows 9 children; 3.02 accepts up to 99. Same class of
error as A4, and it disappears with a repeat group.

**Disposition: resolved in the form.** Page numbering is replaced by the repeat index.

---

## B. Missing or ambiguous skip instructions

### B1 - 5.02 has no skip instruction at all
**Severity: high. This is the missing skip the assessment refers to.**

5.02 asks *"Was a stool specimen obtained from this child?"* `Yes 1 / No 2` - and the SKIP
column is **empty**.

The following questions are 5.03 label, 5.04 time into cold box, 5.05 cold-box
temperature, then 5.06 *reason no specimen was obtained*. So:

- if a specimen **was** obtained, 5.06 should not be asked, and it has no filter;
- if a specimen was **not** obtained, 5.03-5.05 are unanswerable, and there is no skip.

On paper, a clerk diagonal-lines the inapplicable boxes. In a digital form this must be
explicit or the data is uninterpretable.

**Disposition: resolved in the form.** `5.02 = 1` → 5.03-5.05 required, 5.06-5.07 hidden.
`5.02 = 2` → 5.03-5.05 hidden, 5.06 required. This does not change what is asked of any
respondent; it enforces the logic the paper form leaves to a clerk.

### B2 - 5.01 skips to Section 6, abandoning the remaining children
**Severity: high.**

5.01 `No → Section 6`. Section 5 is completed **per child**; Section 6 is household-level
and terminal. So a household whose first eligible child is under 12 months sends the
enumerator to the household section, and every remaining child's module is never reached.

The skip target is wrong: it should be *next child*, not *Section 6*.

**Disposition: resolved in the form.** Sections 4 and 5 sit inside one per-child repeat, so
"skip" means "end this child's iteration". The paper defect cannot occur. **Escalated**,
because on paper this will already have cost data in previous rounds.

### B3 - 2.01 records that consent was not read, and proceeds anyway
**Severity: high - ethical, not just structural.**

2.01 *"Consent statement read aloud to the respondent in full?"* `Yes 1 / No 2`, no skip.
A `No` is recorded and the interview continues to 2.02, where consent may then be "given".

Consent recorded after an unread consent statement is not informed consent.

**Disposition: escalated, and blocked in the form.** The form prevents progression while
`2.01 = 2`, with a message instructing the enumerator to read the statement and then
record `Yes`. This is the one place a hard block is used rather than a warning, because
the alternative is collecting biological specimens from children under defective consent.
Flagged to the ethics committee as a paper-form correction.

---

## C. Data the paper design permits that cannot be analysed

### C1 - 4.13 discards multiple antibiotics in an antimicrobial resistance survey
**Severity: high, analytically.**

*"Which antibiotic was taken? ... Where more than one was taken, record the most recent."*

This is an AMR survey. Concurrent or sequential multiple-antibiotic exposure is among the
most important things such a survey could measure, and the instrument deliberately
discards it, keeping one drug with no record that others existed.

**Disposition: escalated, not changed.** Converting to select-multiple changes what is
asked and what the variable means, so it cannot be done unilaterally on an approved
instrument. The form adds **one** yes/no - *was more than one antibiotic taken?* - which
does not alter 4.13 but lets the analysis know when the single code is incomplete.
Recommended as a priority correction before the next round.

### C2 - 6.07 allows "None of these" together with owned assets
**Severity: medium.**

*"Which of the following does this household own? Record all that apply."* Options A-G are
assets; **H is "None of these"**. Nothing prevents H being marked alongside D.

**Disposition: resolved in the form.** H is made exclusive by constraint. This corrects a
logical impossibility rather than changing the question.

### C3 - 5.05 cannot record a cold-chain failure
**Severity: medium, and easy to miss.**

Cold-box temperature is captured as `⌷ . ⌷ °C` - one digit and one decimal, so 0.0 to 9.9.

The acceptable range is roughly 2-8 °C, so the field holds valid readings comfortably. It
**cannot record a failure**: a box at 15.0 °C, or one that has frozen below zero, has no
representable value. The field can only record success, which makes it useless as a
quality control.

**Disposition: escalated, and widened in the form** to accept −20.0 to 40.0 with a warning
outside 2-8. Widening a measurement range does not change what is asked.

### C4 - 1.05 collects an alternative settlement name as free text
**Severity: low.**

Useful operationally, unanalysable as supplied, and it will produce spelling variants.
**Disposition: kept as free text, flagged in the codebook** as an operational field not
intended for analysis.

---

## D. Sentinel codes colliding with real values

The completion notes define: **8 / 98** = does not know; **9 / 99** = asked, no answer
obtained; **96** = Other. Three collisions follow from that rule.

### D1 - 6.02 codes 8 AND 9 both collide
**Severity: high.**

**Corrected after a systematic scan.** This entry originally named code 9 only.
`scan_sentinels.py` checks every coding category against the declared sentinels
and found **six collisions across four questions**, not three - code `8` also
collides in both 6.01 and 6.02 (`Bucket` and `Unprotected spring` respectively).
Written from reading, the first pass missed them. See `docs/coding_scheme.md`
for the full table; the scan is now the authority.

6.02 has nine categories and its ninth is `No facility or bush . . . 9`. In a single-digit
field, 9 is the standard no-answer sentinel. **Open defecation - the single most important
category in a sanitation question - is indistinguishable from a missing answer.**

**Disposition: resolved in storage, not in the question.** The category set and the numbers
read to the respondent are unchanged. The digital form stores the response and the
non-response reason in **separate fields**, so `9` always means "no facility or bush" and
missingness is carried elsewhere. Escalated for paper renumbering.

### D2 - 6.01 code 9 is "Rainwater", with an 11-category list
**Severity: medium.**

Same mechanism. The list runs to 11, so the field is arguably two-digit and the sentinel
would be 99 - but the form does not say so, and `9` is genuinely ambiguous between
"rainwater" and "no answer" for anyone applying the completion note literally.

**Disposition: as D1.** Sentinels never share a field with substantive values.

### D3 - 99 is both "Not measured" and a plausible child height
**Severity: high. This is the sentinel-inside-a-measurement case the brief warns about.**

4.06 records length or height as `⌷⌷⌷ . ⌷ cm` with `Not measured . . . 99`.

**99 cm is an entirely ordinary height for a three-year-old.** A child measured at 99.0 cm
and a child not measured at all are recorded identically. 4.05 weight carries the same
`99` convention; 99 kg is implausible for a child so the collision is latent there, but
present.

**Disposition: resolved in storage.** Measurement and measurement-status are separate
fields: `not measured` is a boolean, and the measurement is null when it is true. No
sentinel is ever stored inside a numeric measurement. This is the single most important
storage decision in the form.

---

## E. Problems with the external files, not the questionnaire

### E1 - The medicine list does not exist
**Severity: high. Blocking.**

4.13 says *"Record from the medicine list."* The data pack README states the reference
files support *"a settlement list, **a medicine list**, a staff roster and pre-printed
specimen labels."*

`reference_media/` contains seven files: `lgas.csv`, `wards.csv`, `settlements.csv`,
`settlements.geojson`, `previous_round_households.csv`, `staff_roster.csv`,
`specimen_label_allocation.csv`. **There is no medicine list.**

**Disposition: escalated, with a documented stand-in.** 4.13 cannot be implemented as a
coded lookup without the codelist. The form implements it as a coded select against a
**placeholder list built from the WHO AWaRe classification**, clearly marked as a
substitute, so the mechanism is demonstrable and the real list can be dropped in by
replacing one CSV. Every occurrence is flagged in the codebook. **The real list must be
obtained before deployment** - a substituted codelist would silently recode the AMR
variable.

### E2 - Code-box widths do not match the identifiers they hold
**Severity: low, but it affects validation.**

1.02 LGA `Code ⌷⌷⌷` against actual `LGA02` (five characters); 1.03 Ward `⌷⌷⌷` against
`W018` (four); 1.04 Settlement `⌷⌷⌷⌷⌷⌷` against `S01324` (six, fits).

The boxes plausibly hold the numeric part with the prefix implied, but the form does not
say so. **Disposition: resolved.** All three become cascading selects from the reference
files, so codes are chosen rather than typed and the width question disappears.

### E3 - The check digit can be `X`, and the paper form provides a digit box
**Severity: medium.**

`specimen_label_allocation.csv` gives the scheme as *"Modulus 11, weights 2 to 7 applied
right to left, remainder 10 recorded as X"*. Label format at 5.03 is `BSN ⌷⌷⌷⌷⌷⌷ - ⌷`.

Roughly one label in eleven carries a check character of `X`, which a digit box cannot
hold. **Disposition: resolved in the form** - the check character field accepts `0-9` and
`X`. Escalated for the paper form.

### E4 - Supervisor codes legitimately use the `ENU` prefix
**Not a defect. Recorded so it is not "fixed".**

7.04 labels the supervisor field `ENU ⌷⌷⌷`, which looks like a copy-paste error from 1.08.
It is not: `staff_roster.csv` shows team supervisors carry `ENU###` identifiers
(e.g. `ENU005`, role *Team supervisor*). The form validates 7.04 against roster members
whose role is supervisor, and leaves the prefix alone.

### E5 - `staff_roster.assigned_lga` holds a label where every other file holds a code

**Found by deploying the form to a live server and trying to use it**, which is
the only way it could have been found.

`lgas.csv` keys on `name` = `LGA02` with `label` = `Gwarin`. `wards.csv` and
`settlements.csv` both carry `lga_code` = `LGA02`. **`staff_roster.csv` carries
`assigned_lga` = `Gwarin`** - the label, in a column every other supplied file
expresses as a code.

Question 1.02 constrains the selected LGA to the one the enumerator is assigned.
Comparing the selection (`LGA02`) against the roster column (`Gwarin`) is a code
against a label: **never equal, so the constraint rejected every selection and
all 96 enumerators were stopped at the first question of the form.** The 24 team
supervisors were unaffected, because the constraint exempts non-enumerators by
role - which is what made it present as a permissions problem rather than a join
problem.

**Disposition: fixed in the form's own media build.** `prepare_media.py` derives
`assigned_lga_code` by joining the roster's label to `lgas.csv`, and the
constraint compares code to code. The supplied file is not edited, and an
unmatched label fails the build rather than shipping a roster that silently
blocks somebody.

**Rejected: resolving the label inside the constraint.** It is expressible as a
nested predicate, but it puts a second `instance()` lookup into an expression
JavaRosa evaluates on every keystroke, and this form has already been bitten
twice by lookups that convert cleanly and resolve to nothing at runtime (see
`validation.md`).

**Escalated as well as fixed.** The mismatch is in the supplied reference data,
so it will recur every round until the roster is issued with a code column. The
form now tolerates it; the source should be corrected.

**What this cost, and what it changed.** Three tools reported success on a form
that could not be used: pyxform converted it, ODK Validate passed it, and
`validate_media.py` confirmed the referenced column existed. **All three were
right, and the form was still broken** - because a column existing is not the
same as its values meaning what they are compared against. `validate_media.py`
now checks five cross-file value domains and fails if a child column holds a
value absent from its parent. **A reference that resolves and joins to nothing
is worse than a broken one, because every tool in the chain reports success.**

---

## F. Tension between the questionnaire and the stated operating conditions

### F1 - The form says fieldwork runs 1-30 June; the operating conditions say 14 days
The header reads *"Fieldwork period 1 to 30 June 2026."* The brief states fieldwork runs
14 days.

**Disposition:** the date constraint uses **1-30 June**, the ethics-approved window, since
narrowing it could reject a legitimate submission if the 14 days shift. The 14-day
expectation is enforced as a **soft warning**, not a block. Recorded in the constraint
register as a deliberate choice with the reasoning.

### F2 - Names are collected where line numbers would serve
Roster column (2) and 4.02 both collect *"name or initials"*, alongside GPS to six decimal
places at the dwelling entrance, structure number, and the previous round's household
identifier.

Together these identify a specific dwelling and the children in it. **Disposition: raised
under data protection** (see the data protection note) rather than as a form defect. The
recommendation is that 4.02 be dropped entirely - it duplicates the roster line reference
at 4.01, which is sufficient to link child to roster.

---

## Summary of dispositions

| Resolved in the form | Escalated | Both |
|---|---|---|
| A1, A4, A5, B1, B2, C2, D1, D2, D3, E2, E3 | C1, F2 | A2, A3, B3, C3, E1 |

**Escalated items are listed for the survey manager and the ethics committee in a single
memo** rather than left inside a technical document, because escalation that nobody reads
is the same as a silent fix.
