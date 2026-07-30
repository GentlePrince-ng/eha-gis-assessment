# Declaration of AI assistance

Required by the assessment instructions. Written and maintained **as the work
proceeded**, not reconstructed at the end.

## Tools

| Tool | Used for |
|---|---|
| Claude (Anthropic), via Claude Code CLI | Data profiling and defect discovery; code scaffolding and review; drafting and editing of written responses; adversarial challenge against my own conclusions |
| pyxform 4.5.0 + ODK Validate (OpenJDK 21) | XLSForm conversion and XForm validation |
| Python 3.12 · DuckDB · GeoPandas · libpysal/esda · matplotlib | The analysis itself |

The commit history carries `Co-Authored-By` trailers on AI-assisted commits.
They are left in place deliberately: this file and the history should agree.

## How the work was actually structured

This matters more than the tool list, so it is stated plainly rather than left
to be inferred.

I used the model as a fast analyst and code author working under my direction,
and I kept three things for myself: **which questions to attempt, every threshold
and analytical decision, and verification of anything the model asserted.**

**Every judgement call in this submission is mine.** Each was made by choosing
between measured options with the costs of each in front of me, and each is
recorded in `DECISIONS.md` with its rejected alternative:

| Decision | What I chose | What I rejected |
|---|---|---|
| Duty-hours window | 07:00–16:59, evidence-led | 06:00–18:59; per-team-day |
| Positional accuracy | **No exclusion**; tolerance scales with reported error | Any fixed cut — it would have removed 62% of eight teams' tracks |
| Fix-sequence gaps | 5 min interruption, 15 min outage | — |
| Projected CRS | EPSG:32632 (WGS 84 / UTM 32N) | Minna Mid Belt, on datum grounds; Web Mercator; Albers |
| Attribution tolerance | 50 m + 2 × reported accuracy | Fixed 100 m |
| Dwell threshold for "visited" | 5 distinct minutes, calibrated at the elbow | 3, 10, 15 |
| Transposed coordinates | Correct **only where corroborated** within 500 m | Exclude all; correct all |
| Submission sequencing | Q1 → Q3 → Q6 → Q5, map last | — |

Where a value is my judgement rather than a published standard, the constraint
register says so in those words. Eight of its twenty-two entries are labelled
**my judgement**.

## The verification discipline, and why it is built into the code

Work produced quickly needs checking harder, not less. Three mechanisms exist
specifically so that AI-assisted output could not be self-confirming:

- **`build_register.py` fails the build** if any constraint in the form has no
  documented source. A rule cannot be added without stating where its value came
  from. It caught an undocumented rule on its first run.
- **`test_check_digit.py` T0 asserts the tested algorithm appears in the built
  XForm.** Without it, a passing suite would be evidence about the test file
  rather than the deployed form.
- **`validate_media.py`** checks that every external reference resolves to a real
  file and column. It was written after I found such a defect by hand, on the
  principle that a defect found once should be found automatically thereafter.
  It then caught a second instance of the same class.

**Every defect discovered with AI assistance was independently re-checked against
the source data**, and the verification queries are in the repository. Four
findings did not survive that check and were corrected:

1. The ~36 m accuracy cohort was initially read as urban multipath. Spatial join
   and stationary-scatter measurement showed it follows the **logger**, not the
   ground. Corrected in `qa_rule_options.md` C-1.
2. T14's logger failure was first stated from a single file's row count, which
   understated the day because the files overlap. Corrected in C-2.
3. `near_miss` was computed from a table that by construction only held matched
   points, so the class could never fire and every near miss was being swept into
   `team_elsewhere` — the one class implying a team was not where it said it was.
   Fixed in stage 04a; it moved 66 claims out of the accusatory class.
4. The sentinel collision list, written from reading the questionnaire, named
   three collisions. `scan_sentinels.py` found **six**. The defect report now
   records the correction and points at the scan as the authority.

Two further things I found by testing the artefact rather than trusting the
tooling: the form fails to load in XLSForm Online because external media cannot
be attached there — which exposed an undeclared instance that both pyxform and
ODK Validate had passed, and that would have rejected every valid specimen label
in the field.

## What was not accepted from a model

No threshold, tolerance, buffer, coordinate reference system, spatial weights
definition, dwell rule or analytical conclusion was accepted without my deciding
it and recording why. Where the analysis could not decide something — the 1,336
uncorroborated claims — it says so and routes the question to a field check
rather than resolving it by assumption.

Two results were **discarded** rather than reported: the settlement-level Gi\*
cold spots, which were an artefact of a degenerate permutation distribution, and
the point-level cluster analysis as a whole, which does not survive at that unit.
Both were the more eye-catching output.

## Standing commitment

Everything here is work I can explain, modify live, and defend under challenge.
Where I am uncertain — the circularity in calibrating the dwell threshold against
the e-tally, the assumption that reported GPS accuracy is a 1-sigma error, the
test plan specified but not yet executed against a live instance — the documents
say so rather than asserting confidence the analysis does not support.
