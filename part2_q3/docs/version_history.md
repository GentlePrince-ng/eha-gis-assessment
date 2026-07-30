# Form version history

One entry per publish. The analysis team reads this alongside `form_version` in
the data; knowing a record is version `2026063002` is useless without knowing
what changed in `002`.

Format is fixed so it can be parsed later if it ever needs to be.

## 2026063001 — 30 June 2026 — initial release

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
