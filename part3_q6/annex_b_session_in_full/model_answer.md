## Model answer - "Make your work someone else's"

For the facilitator. **Do not distribute.** Participants draft the standard
themselves in Day 3 session 3, and handing them the answer removes the reason
they would follow it.

---

## Part 1 - What a level-3 record looks like

This is the exemplar, not a template to issue. Compare participant records
against it to judge *what is missing*, not to mark them.

```
SOURCE FILE
    D1_facilities_raw.csv, 203 rows, as received 2 June 2026.
    Not modified. All work done on a copy.

STEPS, in this order
    1. Trimmed leading and trailing spaces from facility_name and lga_name.
       54 values changed - 24 in facility_name, 30 in lga_name.
       (Done FIRST - grouping before trimming leaves " Gwarin" as its own group.)

    2. Mapped lga_name to 4 canonical values using this table:
           Idi-Oro   <- "Idi Oro", "IDI-ORO", "Idi-oro", "idi-oro"
           Gwarin    <- "GWARIN", "gwarin"
           Katsuma   <- "KATSUMA"
           Ilela     <- "ILELA", "ilela"
       16 distinct values reduced to 4. 98 rows changed.

    3. Mapped facility_type to 3 canonical values:
           Primary Health Centre <- "Primary Health Center", "PHC",
                                    "Primary health centre"
           Health Post           <- "Health post", "HEALTH POST"
           Cottage Hospital      <- "Cottage hospital"
       9 distinct values reduced to 3. 120 rows changed.

    4. Replaced "," with "." in longitude. 6 values fixed.
       These were text like "7,914882" - a decimal comma, not a thousands
       separator. Checked: all 6 fall inside the state bounding box afterwards.

    5. Found 2 rows where longitude was between 10.37 and 11.57 and latitude
       between 6.95 and 8.43 - outside the state, but inside it when swapped.
       Swapped them. Flagged both in a column `coord_swapped`.

    6. Set staff_total to blank where it read 999 (3 rows). See DECISIONS.

    7. Removed 3 duplicate facility_id rows. See DECISIONS.

DECISIONS
    D1. staff_total = 999 in 3 rows.
        999 is not a plausible staff count for any facility in this register
        (max otherwise 24). Treated as a non-response sentinel, not a value.
        Set to blank rather than deleted, so the facility is retained.
        ALTERNATIVE: it could be a real data-entry error for 99 or 9. I could
        not distinguish these from the register alone. Flagged for the ministry.

    D2. 3 facility_ids appear twice, and the two rows DIFFER (staff_total).
        Kept the row with the HIGHER staff_total, on the assumption that the
        later entry is an update.
        ALTERNATIVE: keeping the first occurrence is equally defensible. This
        changes staff totals by 11 across the register.

    D3. 5 facilities have no coordinates.
        KEPT them in the cleaned file, with coordinates blank.
        They are real facilities; dropping them would silently reduce the
        facility count and understate coverage. They cannot be mapped, and any
        map made from this file must state that 5 of 200 are absent.
        ALTERNATIVE: dropping them makes the file directly mappable but
        changes the denominator without saying so.

RESULT
    Rows in:   203
    Rows out:  200
    Difference explained: 3 duplicate facility_id rows removed (D2).
    Facilities mappable: 195. Not mappable: 5 (D3).
```

## Part 2 - The numbers

Use these to check whether a pair actually reproduced the file.

| | |
|---|---|
| Rows in raw file | **203** |
| Distinct `facility_id` | **200** |
| Rows out, following the model | **200** |
| Mappable facilities | **195** |
| `lga_name` variants → canonical | 16 → **4** |
| `facility_type` variants → canonical | 9 → **3** |
| Whitespace values corrected | **24** |
| Decimal-comma longitudes | **6** |
| Transposed coordinate pairs | **2** |
| `staff_total = 999` | **3** |

**A pair has reproduced the work when the row count matches and the same
facilities are present.** Exact column-by-column equality is not the standard -
the standard is that the department would report the same numbers.

## Part 3 - Why participants get different answers, and why that is the lesson

Three defects have **no single correct treatment**: D1, D2 and D3 above.

Two participants can both clean this file competently and arrive at:

- **200 rows** (duplicates removed, missing coordinates kept), or
- **195 rows** (missing coordinates also dropped), or
- **203 rows** (duplicates kept as separate facilities)

**All three are defensible. None is reproducible unless the decision was
written down.**

This is the point of the whole session, and it is why the dataset was built with
judgement calls in it. A dataset with only mechanical defects would teach
participants that documentation means listing steps. It does not. **It means
recording the choices**, because the steps are usually recoverable by inspection
and the choices never are.

If the discussion at minute 50 reaches this on its own, the session has done
more than it needed to. If it does not, do not supply it - Day 3 session 3 is
where they will reach it while drafting their own standard, and it lands harder
there.

## Part 4 - What to look for when judging level 3

Not a mark scheme. A prompt for what to notice while walking the room.

| Signal | Level |
|---|---|
| Record describes intent - "made the data consistent" | 1 |
| Steps listed, no counts, no order stated | 2 |
| Steps in order, with counts, no decisions recorded | 2 (the most common outcome) |
| Steps, counts, order **and** decisions with their alternatives | **3** |
| The above, plus notes on what the *next* person should check | 4 |

**Expect the whole room at 2 or below on the first attempt.** The department's
measured baseline for this competency is 1.5 out of 5, and a single morning does
not move a department to level 3. What it moves is their understanding of what
level 3 requires - the remaining distance is closed over the 90 days, on real
work, under review.
