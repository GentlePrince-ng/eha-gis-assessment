# Q3 deliverables - where each one is, and the live form

## The form is deployed and can be opened now

**https://ee.kobotoolbox.org/x/L48bzYde**

![QR code for the deployed form](part2_q3/form/form_qr.jpeg){width=38mm}

Deployed to KoboToolbox with all seven external media files attached, so the
cascades, the roster lookups, the specimen label ranges and the check digit all
resolve against real data rather than failing quietly. **A form that converts is
not a form that runs**, and this question is largely about the difference.

Worth knowing before opening it:

- **Sign in with an enumerator code and PIN.** `ENU001` with PIN `9384` works;
  every code and PIN is in `form/media/staff_roster.csv`.
- **1.02 offers only the LGA that enumerator is assigned.** ENU001 is assigned
  Gwarin. That constraint is defect E5 - the supplied roster records the LGA
  *label* where every other file keys on the *code*, which blocked all 96
  enumerators until it was fixed.
- **The form is in Hausa by default**, with English available from the language
  selector, because interviews are conducted in Hausa and 38% of enumerators are
  not confident readers of English.
- **1.13 behaves differently by settlement.** The previous-round lookup covers
  1,565 of 2,524 settlements, so in the other 959 the list is legitimately empty
  and a typed fallback appears instead. Bijidu (Ekduru ward, Idi-Oro) is one such
  settlement; most settlements in the same ward are not.

## The fourteen deliverables

| | Deliverable | Artefact |
|---|---|---|
| **F1** | The form, converting without error | `form/bansara_hh_2026.xlsx`, `.xml`, `conversion_log.txt` |
| **F2** | Constraint register | `constraint_register.md` - generated; the build fails if a rule has no documented source |
| **F3** | Sentinel handling and collisions | `coding_scheme.md`, found by `scan_sentinels.py` rather than by reading |
| **F4** | Cross-question consistency | `consistency_checks.md` |
| **F5** | Questionnaire defect report | `defect_report.md` - 20 findings |
| **F6** | 2,524 settlements on a 2 GB device | `external_data.md` |
| **F7** | Check digit, with transposition tests | `tests/test_check_digit.py` - 14 tests |
| **F8** | Cross-submission label reuse | `label_reuse.md` |
| **F9** | Test plan | `test_plan.md`, executed by `run_test_plan.py` |
| **F10** | Deployment and version control | `deployment_plan.md`, `version_history.md` |
| **F11** | Fabrication detection | `fabrication_detection.md`, `daily_qa.py` |
| **F12** | Data protection | `data_protection.md` |
| **F13** | Codebook | `codebook.md` - generated from the form |
| **F14** | Deliberate scope | `deliberate_scope.md` |

## What has been validated, and how far

| Check | Result |
|---|---|
| Conversion, pyxform 4.5.0 | SUCCESS, versions recorded by the build itself |
| XForm structure and XPath, ODK Validate on OpenJDK 21 | SUCCESS |
| External references resolve, values join, cross-references exist | PASSED, 5 checks |
| Every printed question implemented or declared | PASSED, 58 accounted for |
| Check-digit expression **taken from the built XForm and evaluated** | 21,600 serials, 0 disagreements; 22,160 transpositions, 0 escaping |
| Test plan | **43 of 54 cases executed, all passing**, including all seven the question names as required |
| Deployed and opened on a real server | **Yes** - the link above |

**The honest boundary.** The 11 remaining test cases need a device or a server
in ways an expression evaluator cannot reach: form navigation and repeat
behaviour, `last-saved` across submissions, sync, and encryption. They are
reported as not run rather than counted as passing.

Four defects were found by deploying this form and working through it, after
every static check was already passing - the 1.02 join, the 1.13 dead end, the
1.14 note pointing at a question that had been removed, and four builds shipping
one version string. Each is now covered by an automatic check. That sequence is
the argument for deploying rather than validating.
