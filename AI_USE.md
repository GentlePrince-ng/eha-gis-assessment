# Declaration of AI assistance

Required by the assessment instructions. Maintained **as work proceeds**, not reconstructed
at the end.

## Tools used

| Tool | Used for |
|---|---|
| Claude (Anthropic), via Claude Code | Data profiling and defect discovery in the supplied pack; code scaffolding and review; drafting and editing of written responses; challenge and counter-argument on my analytical conclusions. |

## What it was used for, in detail

**Exploratory profiling.** The initial survey of the 160 track files, the settlement
masterlist, the e-tally and the inaccessible-settlement list was run with AI assistance —
row counts, accuracy distributions, timestamp ranges, key collisions, cross-file
disagreements. The defects listed in `part1_q1/docs/defect_register.md` were surfaced this
way. Every one has since been independently re-checked by me against the source files, and
the verification queries are in the repository.

**Code scaffolding.** Module skeletons, argument parsing, logging setup, and boilerplate
around the DuckDB spatial extension. The analytical logic — QA thresholds, the spatial
attribution method, the weights specification — is mine, and the reasoning for each is
recorded in `DECISIONS.md`.

**Drafting and editing.** Structural drafting of the written responses, and editing for
length against the stated page limits. The judgements they express are mine.

**Adversarial review.** I used the model to argue against my own conclusions — in
particular the coverage-source recommendation in Part 1 Q1 and the scope decisions in
Part 2 Q3 — in order to find where my reasoning was weakest before the walkthrough rather
than during it.

## What it was not used for

No threshold, tolerance, buffer distance, coordinate reference system, spatial weights
definition, or analytical conclusion in this submission was accepted from a model without
my deciding it and recording why. `DECISIONS.md` logs every such call, the alternative
rejected, and the reasoning. Where a value is my judgement rather than a published
standard, it says so.

## Standing commitment

Everything submitted here is work I can explain, modify live, and defend under challenge.
Where I am uncertain, the document says so rather than asserting confidence the analysis
does not support.
