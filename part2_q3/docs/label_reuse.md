# Rejecting a specimen label already used in an earlier submission (F8)

## The plain answer

**No. A self-contained form cannot enforce this.**

Not because ODK lacks a feature, but because of what "self-contained" means. A
form instance is a document. It is filled, saved and submitted, and it has no
writable store that outlives it. Detecting reuse against *every* earlier
submission requires state that persists across instances and is consulted before
the current one is saved — which is, definitionally, not something the form
holds.

Anything claiming otherwise is either checking a narrower thing (the last
submission, this submission) or relying on a server the form cannot reach for
nine days.

## What was implemented anyway, and what each layer actually catches

Three layers are enforceable on the device. Their coverage is uneven and it is
worth being precise about which error each one stops.

| Layer | Rule | Catches | Misses |
|---|---|---|---|
| **1. Allocation range** | serial within the signed-in team's `range_start`–`range_end` | A label from another team's book — which the **check digit cannot detect**, because such a label is internally valid | Reuse within the team's own range |
| **2. Within this submission** | `count(/data/child/s5_specimen[q5_03_label_serial = current()/.]) = 1` | The same label entered for two children in the same household — the most common real duplicate, since both entries happen minutes apart from one book | Anything from an earlier household |
| **3. Previous submission** | `count(${last-saved#q5_03_label_serial}[. = current()/.]) = 0` | Re-entering the label from the household just completed, typically because the enumerator re-read the same sticker | Submission *n−2* and earlier |

Layer 3 uses ODK's `last-saved` instance, which holds **only the immediately
preceding submission**. It is genuinely useful — consecutive re-entry is a common
slip — but it is one step of history, not a ledger. Describing it as duplicate
detection would be overclaiming.

**A note on how this was found.** The first implementation called
`instance('last-saved')` directly. pyxform exposes the previous submission only
through its own `${last-saved#field}` syntax and names the instance
`__last-saved`, so the raw call converted cleanly, passed ODK Validate, and
would have resolved to an empty nodeset in the field — making the constraint
pass unconditionally and silently disabling layer 3. `validate_media.py` caught
it. That is the second time the same class of defect has appeared in this form,
which is why the check is automated rather than remembered.

## What the requirement is really about

The labels are **pre-printed and physically affixed** — 5.03 says *"Affix the
specimen label in the box."* A physical sticker can be applied to exactly one
container. So a duplicated label number in the data is, in the overwhelming
majority of cases, **a transcription error rather than genuine reuse**: the
enumerator read the wrong line of the book, or typed the previous child's serial
from memory.

That matters, because transcription errors are precisely what layers 1–3 and the
check digit are good at. Genuine reuse — the same sticker on two containers —
is a physical impossibility unless labels were reprinted, which is a printing
control problem, not a form design problem.

The requirement should therefore be read as *"do not let a label be recorded
twice"*, and most of that is achievable on the device.

## The architecture that can enforce it fully

### Server-side uniqueness at submission — the authoritative layer

A `UNIQUE` constraint on the specimen identifier in the receiving store, applied
when a submission arrives. This is the only layer that is genuinely complete: it
sees every submission from every device, needs no device state, and cannot be
outrun by an enumerator who reinstalls the app.

**On ODK Central this is a validation step behind the submission endpoint**, not
a Central feature in itself — Central accepts submissions and does not reject on
content. In practice: submissions stream to a store, a job asserts uniqueness on
`specimen_label_full`, and a duplicate raises a flag on both submissions for
supervisor resolution. The laboratory then receives a reconciled list rather
than a raw one.

**It is detective, not preventive.** By the time it fires, the team has moved on.
It cannot stop the collection of a duplicate; it can stop a duplicate reaching
the laboratory, which is what the requirement asks for.

### ODK Entities — preventive, but defeated by the offline window

ODK Entities let a submission create or update a shared dataset that later form
downloads receive as an attachment. A `used_labels` entity list would make prior
labels visible to the form itself.

**It does not survive the operating conditions.** Entity updates propagate on
sync, and these devices are offline for **up to nine consecutive days**. A device
that has not synced has an entity list up to nine days stale, and two devices
that never sync during the round can never see each other's labels. It is the
right architecture for a connected deployment and the wrong one here.

Recording that explicitly, because "use Entities" is the fashionable answer and
it is wrong for this fieldwork.

### Procedural control — the layer that actually prevents

The one control that operates at the moment of the error: **the label book
itself.** Serials are issued to a team as a physical range; the enumerator
strikes through each label as it is used. A struck-through label cannot be
selected twice without the enumerator noticing.

This is cheap, needs no connectivity, and is the only layer that acts before the
data is recorded rather than after. It is also the layer most likely to be
skipped under time pressure, which is why the digital layers exist alongside it
rather than instead of it.

### Laboratory reconciliation — the backstop that already exists

The operating conditions state that the laboratory reconciles against the form
data and that an unmatched specimen is discarded and the child revisited. That
is a real, working duplicate detector — with a cost of one wasted specimen and
one revisit per occurrence. Every layer above exists to reduce how often that
cost is paid.

## Summary

| Layer | Preventive or detective | Works offline | Complete |
|---|---|---|---|
| Label book strike-through | **Preventive** | Yes | No — depends on discipline |
| Form: allocation range | Preventive | Yes | No — within-range reuse passes |
| Form: within submission | Preventive | Yes | No — this household only |
| Form: last-saved | Preventive | Yes | No — one submission of history |
| Server-side uniqueness | Detective | **No** | **Yes** |
| Laboratory reconciliation | Detective | Yes | Yes — at the cost of a revisit |

**No single layer satisfies the requirement.** The form contributes the three it
can, and the write-up says plainly which errors still get through — because a
supervisor who believes the form prevents duplicates will stop checking the
label book, and that trade is a net loss.
