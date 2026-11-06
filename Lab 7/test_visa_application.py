import math

from hypothesis import given, strategies as st

from visa_application import (
    parse_application,
    processing_average,
    payable_fee
)


# Test 1: Visa application parser
@given(st.text() | st.none())
def test_parse_application_no_crash(s):
    result = parse_application(s)

    assert isinstance(result, tuple)
    assert len(result) == 2
    assert isinstance(result[0], str)
    assert isinstance(result[1], int)


@given(
    visa=st.text(min_size=1).filter(lambda x: ':' not in x),
    entries=st.integers()
)
def test_parse_application_valid_input(visa, entries):
    result = parse_application(f"{visa}:{entries}")

    assert result == (visa.strip().title(), entries)


# Test 2: Processing average
@given(st.text() | st.none())
def test_processing_average_no_crash(s):
    result = processing_average(s)

    assert isinstance(result, int)


@given(st.lists(st.integers(), min_size=1))
def test_processing_average_correctness(days):
    csv_input = ",".join(map(str, days))

    expected = sum(days) // len(days)

    assert processing_average(csv_input) == expected


# Test 3: Payable fee
@given(st.text() | st.none())
def test_payable_fee_no_crash(s):
    result = payable_fee(s)

    assert isinstance(result, float)
    assert result >= 0


@given(
    fee=st.floats(min_value=0, max_value=1000000, allow_nan=False, allow_infinity=False),
    discount=st.floats(min_value=0, max_value=1000000, allow_nan=False, allow_infinity=False)
)
def test_payable_fee_correctness(fee, discount):
    result = payable_fee(f"{fee}|{discount}")

    expected = max(fee * 1.18 - discount, 0)

    assert math.isclose(result, expected, rel_tol=1e-9, abs_tol=1e-9)