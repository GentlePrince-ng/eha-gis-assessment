# Designing for fabrication detection (F11)

The operating conditions state the failure this has to prevent:

> In the last round one enumerator submitted 94 interviews with a mean duration
> of 4 minutes and almost no vaccination cards sighted. **This was discovered
> only after fieldwork had closed.**

The detection was not the problem — the pattern is obvious once you look. The
*timing* was. Ninety-four households were spent and the round could not be
repaired. So the requirement is not "can this be detected" but "is it detected
while there is still something to do about it".

**Implemented and demonstrated**: `daily_qa.py` flags the planted pattern at the
**end of day 2, on 22 submissions**, against a 14-day round. Run
`python part2_q3/daily_qa.py --demo`.

## Fields that exist solely to enable back-office QA

These answer no survey question. They are in the form because the paper form
cannot have them, and they are what makes daily detection possible at all.

| Field | Type | What it enables |
|---|---|---|
| `start_time` | `start` | Interview duration — the primary fabrication signal |
| `end_time` | `end` | as above |
| `interview_duration_min` | calculated | Duration in minutes, so no analyst has to derive it consistently |
| `device_id` | `deviceid` | Detects one device submitting under several enumerator codes |
| `audit` | `audit` with `track-changes`, `identify-user`, `track-changes-reasons` | Per-question timing and a change log. Reveals a form filled in one pass with no back-navigation, which real interviews do not look like |
| `today_date` | `today` | Device date, comparable against `q1_10_visit_date` — catches back-dating |
| `pin_entered` | text, masked | Binds a submission to a person, not just to a typed code |

**Dual-purpose fields** — operationally necessary, and also QA evidence:
`q1_11_gps` (household location; also reveals a stationary enumerator),
`q4_08_card` (a substantive coverage variable; also the second signal in the
described pattern), `q4_16_photo` (medicine packaging; also independently
verifiable evidence a visit occurred).

## The daily check

Run each evening against submissions received so far. Output is a ranked list a
supervisor acts on the next morning.

### Indicators

| Indicator | Compared against | Detects |
|---|---|---|
| Median interview duration | Cohort median | Interviews too short to have happened |
| Card sighting rate | Cohort median | Documentation not actually being asked for |
| Submissions per day | Cohort median | Volume no one could physically achieve |
| Distinct GPS locations | Absolute (≤2 across ≥8 submissions) | An enumerator not moving between households |
| Non-completion rate | Cohort median | Refusals being manufactured to skip work |

### Three design decisions

**Robust statistics, not fixed thresholds.** "Flag anything under 10 minutes" is
wrong on day one of a different survey, and wrong in an LGA with small
households. Each indicator is a modified z-score against the *cohort's own*
median using median absolute deviation. MAD rather than standard deviation
specifically because a fabricator's extreme values inflate the SD and help hide
them inside their own outlier; the median and MAD are unmoved by contamination
up to half the sample.

**Conjunction, not any-single-signal.** Short interviews alone are weak — a
household of two with no eligible children is legitimately quick. Low card
sighting alone is weak — some settlements genuinely have few cards. The
described pattern is *both, at high volume, from one person*. Requiring signals
to co-occur is what keeps the list short enough that supervisors actually work
it. A flag list nobody reads is worse than no flag list, because it looks like
control.

**A volume gate.** Below 8 submissions there is no stable median, so those
enumerators are reported as **"insufficient data"** and never as clean. The
distinction matters: silence about someone is not evidence about them.

### Demonstrated result

Nineteen enumerators behaving normally, one planted with the described pattern:

```
ENU020   3 indicator(s)   ESCALATE TODAY
   * interviews far shorter than the cohort
     median 4.1 min (cohort 22.3), z=-11.4
   * vaccination cards sighted far less often
     4% of children (cohort 64%), z=-5.7
   * submission volume far above the cohort
     11.0/day (cohort 6.8), z=3.8
```

**Flagged end of day 2 on 22 submissions.** Zero false positives among the
other nineteen. Against the round described in the operating conditions, that is
22 households at risk instead of 94, with twelve days left to act.

## What the report says, and deliberately does not say

Every escalation carries the same action:

> Supervisor accompanies this enumerator tomorrow and re-interviews three
> households already submitted. **Do not confront on the basis of this report
> alone — it is evidence for a visit, not a finding.**

That wording is deliberate. These indicators identify an enumerator whose data
*looks* different, which has innocent explanations: a dense urban ward with
small households, an area where cards genuinely are rare, a fast and experienced
worker. The check produces a **priority order for supervision**, and the finding
is made by a person who went and looked.

The same discipline applies as in the campaign-tracking analysis: where the data
can decide, it decides; where it cannot, the uncertainty is named and routed to
someone who can resolve it.

## What this does not catch

- **A careful fabricator.** Someone who idles the form for twenty minutes,
  varies durations, and occasionally records a card will not cross these
  thresholds. The check raises the effort required; it does not make fabrication
  impossible.
- **Whole-team collusion.** Every indicator is relative to the cohort. If a
  whole team fabricates together, they become the cohort. Cross-LGA comparison
  partly mitigates this and is not implemented — noted as a limitation rather
  than claimed.
- **Fabrication that produces plausible data.** Nothing here inspects whether
  the answers are true, only whether the process that produced them looks like
  interviewing.
- **Anything, if nobody runs it.** This is a script, not a control. The control
  is a named person opening it each evening. That belongs in the supervision
  plan, not in the code.
