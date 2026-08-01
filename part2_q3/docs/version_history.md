# Form version history

One entry per publish. The analysis team reads this alongside `form_version` in
the data; knowing a record is version `20260630-ae1b89` is useless without knowing
what changed in it.

Format is fixed so it can be parsed later if it ever needs to be.

**The version is derived by the build**, not typed: release date plus a
digest of the form definition. It therefore changes whenever the form
changes and stays identical when it does not, which is what makes an entry
here correspond to exactly one instrument. See `deployment_plan.md`.

## 20260630-9c5d68 - 30 June 2026 - initial release

    Changed:  initial publication of Form HH/2026/v1 as a digital instrument
    Affects:  all fields
    Analysis: baseline version. Value crosswalk to the paper instrument is in
              codebook.md - two choice lists (6.01, 6.02) are re-based to avoid
              collisions with non-response sentinels. Concatenating a paper
              round with this one without that mapping produces nonsense.
    Known:    q4_13_medicine uses a PLACEHOLDER codelist (WHO ATC codes). The
              ministry codelist was not supplied. Records under this version
              carry ATC values and must not be pooled with any later version
              using ministry codes without an explicit crosswalk.
