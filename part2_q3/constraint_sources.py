"""Where every rule in the form came from.

This is the other half of the constraint register. `build_form.py` holds the
rules; this holds the justification for each. `build_register.py` joins them and
**fails if any rule in the form has no entry here**, so a constraint cannot be
added without stating where its value came from.

That check is the point. The assessment says a form full of sensible constraints
with no register is worth less than a smaller form with a defended one, and
lists "thresholds, buffers, or tolerances asserted without justification" as an
automatic loss of marks. A register maintained by hand beside a form is wrong
within a day; this one cannot be.

`source` is one of:
  * **paper form** - the value is stated or implied by Form HH/2026/v1
  * **reference data** - the value comes from a supplied lookup file
  * **published standard** - named, external, checkable
  * **judgement** - mine, with the reasoning given. Never left unlabelled.
"""

SOURCES: dict[str, dict[str, str]] = {

    # ---------------------------------------------------------------- sign-in
    "pin_entered": dict(
        prevents="One enumerator submitting under another's code, which is the "
                 "precondition for the fabrication pattern described in the "
                 "operating conditions (94 interviews, 4-minute mean).",
        source="reference data",
        detail="4-digit PIN held per enumerator in staff_roster.csv. The paper "
               "form has no equivalent: 1.08 is a code anyone can write.",
    ),
    "q1_02_lga": dict(
        prevents="Work recorded in an LGA the enumerator was not assigned to, "
                 "which corrupts both the sampling frame and workload tracking.",
        source="reference data",
        detail="staff_roster.csv assigned_lga. Relaxed for supervisors, who "
               "legitimately move between LGAs.",
    ),
    "q0_label_range": dict(
        prevents="A team working from another team's label book. The check digit "
                 "cannot detect this - a label from the wrong book is internally "
                 "valid - so only the allocation range catches it.",
        source="reference data",
        detail="specimen_label_allocation.csv, filtered to the signed-in team.",
    ),

    # -------------------------------------------------------- identification
    "q1_06_structure": dict(
        prevents="A mistyped structure number that cannot be traced back to a "
                 "dwelling on revisit.",
        source="paper form",
        detail="1.06 provides three coding boxes, so 1-999.",
    ),
    "q1_07_hh_serial": dict(
        prevents="A household serial outside the range the paper form can hold, "
                 "breaking comparability with paper rounds.",
        source="paper form",
        detail="1.07 provides three coding boxes, so 1-999.",
    ),
    "q1_10_visit_date": dict(
        prevents="A visit dated outside the approved fieldwork window - most "
                 "often a device with the wrong date, or a form completed later "
                 "from notes.",
        source="paper form",
        detail="Header states 'Fieldwork period 1 to 30 June 2026'. The operating "
               "conditions say fieldwork runs 14 days, which is narrower. The "
               "ETHICS-APPROVED window is enforced as the hard constraint and the "
               "14-day expectation is a soft warning, because a hard 14-day rule "
               "would reject legitimate submissions if the schedule shifts.",
    ),

    # --------------------------------------------------------------- consent
    "q2_01_statement_read": dict(
        prevents="An interview proceeding, and biological specimens being taken "
                 "from children, after the consent statement was not read.",
        source="judgement",
        detail="The paper form records 'No' and continues to 2.02, where consent "
               "may then be given. Consent recorded after an unread statement is "
               "not informed consent. This is the ONLY hard block in the form; "
               "every other rule warns. Escalated to the ethics committee as a "
               "paper-form correction. See defect B3.",
    ),

    # ---------------------------------------------------------------- roster
    "q3_01_hh_size": dict(
        prevents="A household size that is a typo rather than a count, and the "
                 "runaway repeat it would generate.",
        source="judgement",
        detail="Upper bound 40. The paper field accepts two digits (to 99) and "
               "the paper roster holds 12 lines, so the instrument itself is "
               "inconsistent (defect A4). 40 is set well above any plausible "
               "single household while still catching a slipped digit. It is my "
               "judgement, not a published figure. A household above 40 is "
               "referred to the supervisor rather than silently truncated.",
    ),
    "r_age_years": dict(
        prevents="An under-five recorded in years, which would make the child "
                 "invisible to the eligibility calculation and lose them from "
                 "the survey entirely.",
        source="paper form",
        detail="Roster instruction: ages in YEARS for residents five and over, "
               "MONTHS for under-fives. Lower bound 5 enforces that split. Upper "
               "bound 120 is my judgement as an implausibility guard.",
    ),
    "r_age_months": dict(
        prevents="A child of 60 months or more recorded in the months column, "
                 "which would wrongly make them eligible.",
        source="paper form",
        detail="Roster instruction, column (6): 'under 5 only', so 0-59 completed "
               "months.",
    ),

    # ----------------------------------------------------------- child module
    "q4_01_line": dict(
        prevents="A child module pointing at an adult, at a line that does not "
                 "exist, or at a resident outside 9-59 months.",
        source="paper form",
        detail="4.01 asks for the roster line number. The paper form cannot check "
               "it; indexed-repeat() validates against the roster itself.",
    ),
    "q4_05_weight_kg": dict(
        prevents="A transposed or slipped digit at data entry - 152 kg for 15.2.",
        source="judgement",
        detail="Hard bounds 2.0-30.0 kg are a TYPO guard, deliberately wider than "
               "clinical plausibility, so that a genuinely severely wasted child "
               "is never blocked from being recorded. Clinical implausibility is "
               "handled by a separate soft warning against WHO Child Growth "
               "Standards, which flags rather than blocks. Blocking on clinical "
               "range would delete the very cases the survey exists to find.",
    ),
    "q4_06_height_cm": dict(
        prevents="A transposed or slipped digit - 811 cm for 81.1.",
        source="judgement",
        detail="Hard bounds 45.0-130.0 cm on the same principle as weight: a typo "
               "guard, not a clinical filter, with WHO-based implausibility "
               "raised as a warning.",
    ),
    "q4_07_position_warn": dict(
        prevents="Length and height being recorded against the wrong convention, "
                 "which biases every derived z-score by roughly 0.7 cm.",
        source="published standard",
        detail="WHO Child Growth Standards: recumbent length below 24 months, "
               "standing height at 24 months and above. Warns rather than blocks, "
               "because a child who cannot stand is legitimately measured "
               "recumbent at any age.",
    ),
    "weight_implausible_warn": dict(
        prevents="A weight that is possible to type but not to observe, passing "
                 "unnoticed into analysis.",
        source="published standard",
        detail="WHO Child Growth Standards, approximately -4 SD to +4 SD across "
               "9-59 months. Warns; never blocks.",
    ),
    "height_implausible_warn": dict(
        prevents="A height outside any observed value for the age band.",
        source="published standard",
        detail="WHO Child Growth Standards, approximately -4 SD to +4 SD across "
               "9-59 months. Warns; never blocks.",
    ),

    # -------------------------------------------------------------- specimen
    "q5_03_label_serial": dict(
        prevents="A specimen recorded against a label from outside the team's "
                 "allocation, which the laboratory cannot reconcile - and an "
                 "unreconcilable specimen is discarded and the child revisited.",
        source="reference data",
        detail="range_start and range_end per team in "
               "specimen_label_allocation.csv. Six digits enforced by regex.",
    ),
    "q5_03_check_digit": dict(
        prevents="A mis-keyed or transposed specimen serial reaching the "
                 "laboratory. Modulus 11 detects every single-digit error and "
                 "every transposition of two adjacent digits.",
        source="reference data",
        detail="Scheme stated in specimen_label_allocation.csv: 'Modulus 11, "
               "weights 2 to 7 applied right to left, remainder 10 recorded as "
               "X'. The check character field accepts X as well as 0-9, which the "
               "paper form's digit box cannot (defect E3).",
    ),
    "q5_05_coldbox_temp": dict(
        prevents="A cold-chain failure being unrecordable. The paper field is one "
                 "digit and one decimal, so 0.0-9.9: a box at 15 degrees or a "
                 "frozen box has no representable value, and the field can only "
                 "record success.",
        source="judgement",
        detail="Widened to -20.0 to 40.0 as a device-range guard. The acceptable "
               "2-8 degree range is enforced as a WARNING that tells the "
               "enumerator to notify their supervisor, not as a block - blocking "
               "would leave the failure unrecorded, which is the defect being "
               "fixed. See defect C3.",
    ),

    # ----------------------------------------------------------- environment
    "q6_07_assets": dict(
        prevents="'None of these' being selected alongside owned assets, a "
                 "logical impossibility the paper form permits.",
        source="judgement",
        detail="Standard exclusivity rule for a none-of-the-above option. See "
               "defect C2.",
    ),

    "q4_13_placeholder_warning": dict(
        prevents="Placeholder medicine codes being collected without the "
                 "enumerator, the supervisor or the analyst realising the "
                 "codelist is not the real one.",
        source="judgement",
        detail="The medicine list referenced by 4.13 is absent from the data "
               "pack (defect E1). The substitute uses WHO ATC codes, which "
               "cannot be confused with the two-digit local codes the paper form "
               "expects, so placeholder data is self-identifying. This banner is "
               "the second guard: the substitution is visible at the point of "
               "capture, not only in documentation nobody reads in the field.",
    ),

    # ------------------------------------------------- cross-question checks
    "roster_mismatch_note": dict(
        prevents="A roster that disagrees with the stated household size passing "
                 "unnoticed until data entry, weeks after the household could be "
                 "revisited.",
        source="judgement",
        detail="Required by the question: reconcile stated household size against "
               "the roster. Implemented as a WARNING, not a block: the two "
               "legitimately differ when a usual resident is absent and the "
               "enumerator cannot obtain their details. Blocking would push "
               "enumerators to invent a line to clear the error.",
    ),
    "q3_02_note": dict(
        prevents="The count of eligible children being transcribed from an "
                 "office-use column the enumerator was instructed to leave blank "
                 "(defect A1).",
        source="paper form",
        detail="Derived from roster ages, so the stated number of eligible "
               "children and the number of child modules cannot disagree - they "
               "are the same quantity. This is the second consistency check the "
               "question requires, satisfied by construction rather than by rule.",
    ),
    "q5_05_temp_warn": dict(
        prevents="A cold-chain excursion being recorded and then ignored.",
        source="published standard",
        detail="2-8 degrees C is the standard specimen cold-chain range. Warns "
               "and instructs the enumerator to notify the supervisor immediately.",
    ),
}
