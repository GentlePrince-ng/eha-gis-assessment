"""The specimen label check digit — one definition, two consumers.

The scheme is stated in `specimen_label_allocation.csv`:

    "Modulus 11, weights 2 to 7 applied right to left, remainder 10 recorded as X"

So for a six-digit serial `d1 d2 d3 d4 d5 d6` read left to right, the weights
applied right to left are:

    d6 x 2,  d5 x 3,  d4 x 4,  d3 x 5,  d2 x 6,  d1 x 7

check = (sum) mod 11, with 10 written as `X`.

Why this module exists
----------------------
The check runs in two places: as an XPath expression inside the XForm, and in
Python inside the test suite. If those are written separately they will
eventually disagree, and the tests would then be proving something true of the
tests rather than of the form.

So the weights are declared **once**, here. `xpath_expression()` generates the
expression that `build_form.py` puts into the form, and `compute()` is what the
tests exercise. `tests/test_check_digit.py` additionally asserts that the
expression generated here appears verbatim in the built XForm — which closes the
loop: passing tests are evidence about the deployed form, not about this file.
"""

from __future__ import annotations

SERIAL_LENGTH = 6

# Weight applied to each digit, left to right. The scheme says weights 2 to 7
# right to left, which reversed is 7,6,5,4,3,2 left to right.
WEIGHTS: tuple[int, ...] = (7, 6, 5, 4, 3, 2)

MODULUS = 11
REMAINDER_TEN = "X"


def compute(serial: str) -> str:
    """Return the check character for a six-digit serial."""
    if len(serial) != SERIAL_LENGTH or not serial.isdigit():
        raise ValueError(f"serial must be {SERIAL_LENGTH} digits, got {serial!r}")
    total = sum(int(d) * w for d, w in zip(serial, WEIGHTS))
    remainder = total % MODULUS
    return REMAINDER_TEN if remainder == 10 else str(remainder)


def is_valid(label_serial: str, check_char: str) -> bool:
    """Whether a serial and check character agree."""
    try:
        return compute(label_serial) == check_char.upper()
    except ValueError:
        return False


def xpath_expression(field: str) -> str:
    """Generate the ODK/JavaRosa expression that computes the check character.

    `field` is the XLSForm reference to the serial, e.g. '${q5_03_label_serial}'.

    Written as XPath 1.0 plus JavaRosa extensions only. `upper-case()` is XPath
    2.0 and is not available - that mistake was caught by ODK Validate on the
    first build and is why `translate()` is used at the call site.
    """
    terms = " + ".join(
        f"{w} * number(substr({field},{i},{i + 1}))"
        for i, w in enumerate(WEIGHTS)
    )
    total = f"({terms})"
    return (
        f"if({total} mod {MODULUS} = 10, "
        f"'{REMAINDER_TEN}', "
        f"string({total} mod {MODULUS}))"
    )


def detects_all_transpositions() -> tuple[bool, str]:
    """Whether the weight set detects every transposition of two digits.

    Swapping digits at positions i and j changes the weighted sum by
    (d_i - d_j)(w_i - w_j). The error escapes detection only when that product
    is divisible by the modulus.

    With a prime modulus of 11, and |d_i - d_j| <= 9 and |w_i - w_j| <= 5,
    neither factor can be divisible by 11 and neither can their product. So
    every transposition of two *different* digits changes the check character -
    not only adjacent ones. The test suite verifies this exhaustively rather
    than relying on the argument.
    """
    max_digit_diff = 9
    max_weight_diff = max(WEIGHTS) - min(WEIGHTS)
    ok = MODULUS > max_digit_diff and MODULUS > max_weight_diff
    reason = (
        f"modulus {MODULUS} is prime and exceeds both the largest digit "
        f"difference ({max_digit_diff}) and the largest weight difference "
        f"({max_weight_diff}), so no transposition product can be divisible "
        f"by it"
    )
    return ok, reason
