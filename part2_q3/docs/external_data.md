# Serving 2,524 settlements to a 2 GB tablet (F6)

The question rules out the easy answer in advance: *"A choices worksheet is not
an acceptable answer, and saying so is not sufficient; describe the mechanism
you used instead."*

## The mechanism

The settlement list is delivered as an **external CSV attached to the form as
media**, and referenced with **`select_one_from_file settlements.csv`**. The
cascade from LGA to ward to settlement is expressed as a `choice_filter` on
those external files.

The difference from a choices worksheet is architectural, not cosmetic:

| | Choices worksheet | External CSV media |
|---|---|---|
| Where the options live | Compiled into the form definition itself | A separate file attached to the form |
| What happens on open | ODK Collect **parses the whole codelist into memory** | Nothing - the file was imported once |
| First use | - | Collect imports the CSV into its local **SQLite** database |
| Every use after | Walks an in-memory list | **Indexed query** against SQLite |
| Memory cost during the interview | The entire 2,524-row list, held for the whole session | A query result - the handful of rows that match the filter |
| Cascade filtering | Evaluated in the form engine | Evaluated by the database |

On a 2 GB device shared with the operating system, Collect, the camera and
whatever else the tablet is doing, the distinction is the difference between
carrying a codelist for the length of every interview and holding a few rows for
the length of one question.

## What that costs, and what it buys

Columns are trimmed to those the form actually references, because unused
columns cost import time and storage on every device, 120 times over:

| File | Rows | As supplied | Prepared |
|---|---|---|---|
| `settlements.csv` | 2,524 | 212.5 KB | **88.6 KB** |
| `previous_round_households.csv` | 3,982 | 328.8 KB | 289.3 KB |
| `wards.csv` | 40 | 1.1 KB | 1.1 KB |
| `staff_roster.csv` | 120 | 6.5 KB | 7.3 KB |
| `specimen_label_allocation.csv` | 24 | 2.5 KB | 1.3 KB |
| `medicines.csv` | 23 | - | 1.9 KB |
| `lgas.csv` | 4 | 0.1 KB | 0.1 KB |
| **Total shipped to each device** | | 551.4 KB | **389.6 KB** |

Built by `prepare_media.py`, which reads the supplied reference files and
**never modifies them**.

## What I rejected, and why

### 1. Putting the settlements on the `choices` worksheet

**Rejected on memory.** This is the option the question names, and the reason is
above: 2,524 rows compiled into the form definition and parsed into RAM at open,
for the whole interview, on a 2 GB device.

There is a second reason worth stating. A choices worksheet is **part of the
form**, so correcting a settlement name means publishing a new form version -
and with devices offline for up to nine days, a form version change mid-round is
the most disruptive thing you can do (see `deployment_plan.md`). An external CSV
is a **media file**: it can be replaced without touching the form's logic.

### 2. The `search()` appearance

The older ODK idiom for pulling options from a CSV. **Rejected because it is
deprecated** and was never fully supported in Enketo, so a form built on it
behaves differently on a tablet and in a browser preview. `select_one_from_file`
is the supported replacement and works in both.

### 3. Splitting the survey into four LGA-specific forms

Each form would carry only its own settlements - roughly 600 rows instead of
2,524.

**Rejected**, for three reasons that compound:

- It creates **four datasets, not one.** Every analysis then begins with a union,
  and the analysis team must remember that four form IDs are the same instrument.
- It **multiplies the mid-round change problem by four.** The operating
  conditions say a mid-round change is likely; four forms means four
  publications and four opportunities for a device to be running the wrong one.
- It solves a problem the external-file approach has already solved, at the cost
  of a structural complication that lasts for the whole round.

### 4. A live server lookup

Query the settlement list from a server as the enumerator types.

**Rejected outright by the operating conditions.** Nine consecutive days offline.
Anything requiring connectivity at the moment of data entry is not a candidate.
Recording this because it is the answer that a reviewer used to connected
deployments might expect.

### 5. Pre-filtering each device's list to its own team

Ship each team only the settlements in its assigned wards - about 100 rows per
device instead of 2,524.

**This one I did not reject on the merits**, and it is worth being precise about
why it is not implemented. On memory grounds it is strictly better. On data
protection grounds it is *considerably* better, and
`data_protection.md` recommends exactly this for
`previous_round_households.csv`, which currently ships 3,982 households with
initials and GPS to every tablet.

What stopped it is **operational, not technical**: one media set becomes
twenty-four. That changes provisioning, the update procedure, and what happens
when an enumerator is reassigned mid-round - a supervisor moving someone to
another ward would need to reprovision the device rather than just tell them.
That is the survey manager's decision, not mine, so it is recorded as a
recommendation in `deliberate_scope.md` rather than made unilaterally.

**At 389 KB total, memory is not the binding reason to do it. Data protection
is.**

## The check that keeps this honest

External media introduces a failure mode that a choices worksheet does not have:
**the form can reference a file that is not there, or a column that does not
exist, and still convert and validate cleanly.**

That happened twice in this build. `validate_media.py` now checks, on every
rebuild, that every `instance()` call resolves to a declared instance, every
declared media file exists, each has the `name` and `label` columns
`select_one_from_file` requires, and every column named in a path is present in
that CSV. See `validation.md`.
