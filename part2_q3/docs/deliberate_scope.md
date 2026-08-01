# What I deliberately did not implement, and why (F14)

The question says *"a defensible scope scores better than an exhaustive one."*
This is that scope. Each item was reachable and was left out for a stated
reason, and every one is cross-referenced to where it is discussed.

## Left out because the input does not exist

### The real medicine codelist
4.13 says *"record from the medicine list"* and the pack README claims one is
supplied. It is not - verified by searching every file in the pack, and inside
the `.docx` for embedded objects. A clearly-marked WHO ATC placeholder is
implemented instead, so the mechanism is demonstrable and the real list drops in
by replacing one CSV.

**Why not invent two-digit codes:** the paper form expects them, so invented
codes would be indistinguishable from real ones and would silently recode the
AMR variable. ATC codes cannot be mistaken for a two-digit local code, which
makes any placeholder data self-identifying. → `defect_report.md` E1

### A real encryption keypair
`public_key` in settings is a labelled placeholder. Submissions encrypted to it
cannot be decrypted, so the real key is a deployment gate rather than a form
change. The round-trip is untestable until the keypair is issued.
→ `data_protection.md`

## Left out because the decision is not mine

### Per-team partitioning of the media files
`previous_round_households.csv` ships **3,982 households with initials, structure
numbers and GPS to all 120 devices**, and `staff_roster.csv` ships **all 120
PINs to all 120 devices**. Both should be partitioned per team - exposure drops
from 3,982 households to roughly 300-400, and from 120 PINs to five.

`prepare_media.py` already builds these files, so partitioning is a change to
that script rather than to the form. **Not implemented because it turns one
media set into twenty-four**, which changes the deployment model, the
provisioning QR codes and the update procedure. That is the survey manager's
call, not a technical detail I should decide unilaterally. → `data_protection.md`

### Removing 4.02, the child's name
Recommended for removal: 4.01 already identifies the child by roster line, and
the name is never used analytically. **Not removed**, because dropping a field
from an ethics-approved instrument changes what is collected and requires
committee approval. Escalated with a recommendation rather than done.

### Wiring `consent_to_follow_up` into 1.13
The previous-round file carries a follow-up consent flag that nothing checks, so
a household that declined can still be selected. Implementing the filter is two
lines. **Not implemented** because a household refusing follow-up and then being
visited anyway is a governance question - someone must decide whether the flag is
authoritative - and silently enforcing it could suppress legitimate revisits
that were consented verbally. Escalated as the second of three items for the
ethics committee.

## Left out because it is impossible in the medium

### Cross-submission duplicate label detection
A self-contained form cannot check a label against every earlier submission,
because it has no writable store outliving the instance. Three layers are
implemented - allocation range, within-submission uniqueness, and the
`last-saved` instance - and the write-up states plainly which errors still get
through. ODK Entities would solve it for a connected deployment and is **wrong
here**, because entity updates propagate on sync and these devices are offline up
to nine days. → `label_reuse.md`

### Hashing the PIN
XForms has no hash function, so an in-form PIN check must compare against a
value shipped in the media. The fix is architectural - Central per-user accounts
- not a form change. → `data_protection.md`

## Left out because it needs a device or a person

### Executing the test plan
54 cases specified, **none executed against a running instance**, because no ODK
Central project was available in the window. The check-digit logic behind case
S09 *is* executed exhaustively in `tests/test_check_digit.py`. Everything else
is a specification. → `test_plan.md`

### Native-speaker review of the Hausa
Every label and constraint message is bilingual with Hausa as the default,
because an English-only message is a message that does not exist for the 38% of
enumerators who are not confident readers of English. **The strings are mine and
are indicative.** Whether an enumerator with six years of schooling understands
a given message is a cognitive-interview question, not a translation one, and
both need doing before deployment.

### Device testing under memory pressure
A 40-person roster with eight eligible children on a 2 GB tablet needs a real
device. The external-media design exists precisely to keep memory pressure low -
2,524 settlements queried from SQLite rather than parsed into RAM - but the claim
is reasoned, not measured. → `prepare_media.py`

## Left out on judgement

### A GPS geofence on 1.11
No constraint that the household falls inside the selected settlement. A
settlement centroid is not a household location, and a boundary rule would block
legitimate dwellings at the edge of a settlement - which are disproportionately
the poorest. Out-of-area points are better surfaced as a back-office flag than
blocked at a doorstep. → `consistency_checks.md`

### Blocking on clinically implausible measurements
Weight and height carry hard bounds that are typo guards, deliberately wider
than clinical plausibility, with WHO-based implausibility raised as a warning. A
clinical range enforced as a block would delete the severely malnourished
children the survey exists to count. → `constraint_register.md`

### Converting 4.13 to select-multiple
The single most valuable analytical fix available - an AMR survey that records
only the most recent antibiotic is discarding its central measurement. **Not
done**, because it changes what the variable means and requires re-approval. One
added yes/no lets analysis know when the code is incomplete, without altering
4.13 itself. → `defect_report.md` C1

## What I would do first with another day

1. Partition the media files per team. Largest risk reduction per hour of work.
2. Execute the test plan on a real device, since Central access resolves it.
3. Get the Hausa reviewed.

Everything else on this list is either blocked on someone else's decision or
correctly out of scope.
