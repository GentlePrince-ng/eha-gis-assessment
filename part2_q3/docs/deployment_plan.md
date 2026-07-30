# Deployment and version control (F10)

**120 enumerators, 24 teams, 4 LGAs, 14 days, offline for up to 9 consecutive
days.** The operating conditions also state that a mid-round change to the
instrument is likely, because it has happened in every previous round.

So this plan assumes a mid-round change rather than hoping to avoid one.

## The versioning scheme

| Element | Value | Rule |
|---|---|---|
| `form_id` | `bansara_hh_2026` | **Never changes.** Changing it creates a *different form* on Central, and submissions against the old id become an orphaned dataset |
| `version` | `2026063001` — `yyyymmddnn` | Increments on every publish, including a one-character label fix |
| `form_version` | a calculate holding the same string | Stamped into the **data**, not only the metadata |

The last row matters more than it looks. Central records the version against each
submission, but metadata is the first thing lost when someone reshapes an export
in Excel — and a mixed-version round is precisely when that happens. A field in
the record itself survives the reshaping.

## What may and may not change mid-round

This is the part that determines whether a change is safe, and it is not
negotiable by urgency.

### Safe

- **Adding a field.** Records from earlier versions have it null, which the
  codebook explains as "not collected under version *n*". No existing value moves.
- **Loosening a constraint.** Data already collected remains valid.
- **Fixing a label, hint or translation.** No stored value changes.
- **Correcting a relevance rule** so a question appears where it should have.
- **Replacing a media file** — for example the real medicine list arriving. New
  attachment, new version, no form logic change.

### Unsafe — do not do mid-round

- **Renaming a field.** Central treats it as delete-plus-add. The old column
  stops and a new one starts, and the analysis team must union two columns that
  mean the same thing. If a name is wrong, live with it until the next round.
- **Changing a choice *value*.** Every record collected under the old value now
  means something different. This is the failure that recodes a variable
  silently. Change the *label* freely; never the value.
- **Tightening a constraint.** Records already saved under the looser rule cannot
  be revalidated, and drafts on devices may become unfinishable — the enumerator
  cannot advance and cannot save.
- **Removing a field**, or making an optional field required.

**The rule in one line:** *add and loosen freely; never rename, never re-value,
never tighten.*

## Pushing a change to devices that are offline

The nine-day window means a change does not arrive when it is published. It
arrives when each device next syncs, which is staggered and partly outside
anyone's control.

### Sequence

1. **Publish as a draft on Central and test it** against the test plan on two
   devices before it reaches anyone else. A mid-round change is the highest-risk
   moment in a round; it deserves the same testing as the original.
2. **Publish the new version.** Central serves it to any device that syncs.
3. **Tell people out of band.** Devices are offline; phones usually are not. A
   phone tree through the 24 team supervisors reaches 120 people faster than a
   sync does, and tells them *why* the update matters.
4. **Do not force an update.** ODK Collect finalises a form under the version it
   was **started** with. Forcing a refresh mid-interview is how a partially
   completed submission is lost.
5. **Accept a mixed-version round.** For a period — potentially the full nine
   days — some records are version *n* and some *n+1*. That is not a failure
   state to be prevented; it is the normal consequence of offline work, and the
   design has to make it analysable rather than avoid it.

### What protects data already collected

- **Finalised submissions are immutable on the device** and queue for upload.
  A form update does not touch them.
- **Drafts in progress stay on their original version.** This is the reason not
  to tighten constraints: a draft cannot be revalidated against a rule that did
  not exist when it was started.
- **Encryption is per-submission**, so a version change does not affect
  decryptability of anything already saved.
- **Media replacement is versioned with the form**, so a device that has not
  synced continues to use the media it has. It does not get the new medicine list
  and the old form logic, or vice versa.

## How the analysis team distinguishes versions

Three mechanisms, deliberately redundant, because the first two can be lost in
handling:

1. **`form_version` in every record.** Survives any export, reshape or merge.
2. **Central's submission metadata**, which records the version served.
3. **A published change log** — `docs/version_history.md`, one entry per publish:
   version, date, what changed, which fields affected, and what the analysis team
   must do about it.

The third is the one that actually matters. Knowing a record is version
`2026063002` is useless without knowing what changed in `002`.

### The change log entry format

```
## 2026063002 — 8 June 2026
Changed:  q4_13_medicine — placeholder list replaced with the ministry codelist
Affects:  child.q4_13_medicine
Analysis: records with form_version = 2026063001 carry WHO ATC codes;
          records from 2026063002 carry ministry two-digit codes.
          Crosswalk in codebook.md. DO NOT concatenate without mapping.
```

## Device provisioning

- **Central project QR code** configures server, project and credentials in one
  scan. No enumerator types a URL.
- **Per-user accounts, not a shared one.** A shared login makes `device_id` the
  only identity in the data, which defeats the fabrication checks.
- **Media pre-loaded before deployment.** 389 KB across seven files — trivial on
  arrival, painful over a rural connection on day one.
- **Storage headroom checked**: photographs at `max-pixels=1024` are roughly
  150 KB each; a 2 GB device with the OS and Collect installed has room for a
  full round, but not if the device is also used for anything else.

## What this plan does not solve

- **A device lost or broken before syncing** loses every unsynced submission.
  Nothing in the form prevents it. The mitigation is procedural: supervisors
  collect and sync at every opportunity, not only at the end of the offline
  window.
- **A change that genuinely requires a rename or re-value** cannot be done safely
  mid-round. The honest answer is to carry the defect to the end of the round and
  fix it in the next version, documenting the defect in the meantime.
- **Ethics re-approval** for anything altering what is asked. That is a
  timeline, not a technical step, and it is why the escalated defects in
  `defect_report.md` are escalated rather than fixed.
