import math

from hypothesis import given, strategies as st
from scholarship_awards import parse_applicant, marks_average, payable_award


# ---------- Test 1: parse_applicant must never crash ----------
@given(st.text() | st.none())
def test_parse_applicant_no_crash(s):
    try:
        parse_applicant(s)
    except Exception as e:
        assert False, f"parse_applicant crashed with: {e!r} for input {s!r}"


# ---------- Test 2: marks_average must never crash ----------
@given(st.text() | st.none())
def test_marks_average_no_crash(s):
    try:
        marks_average(s)
    except Exception as e:
        assert False, f"marks_average crashed with: {e!r} for input {s!r}"


# ---------- Test 3: payable_award must never crash ----------
@given(st.text() | st.none())
def test_payable_award_no_crash(s):
    try:
        payable_award(s)
    except Exception as e:
        assert False, f"payable_award crashed with: {e!r} for input {s!r}"


# ---------- Extra property tests (valid inputs must give sane output) ----------
@given(
    st.text(alphabet=st.characters(whitelist_categories=("L",)), min_size=1)
    .filter(lambda c: c.strip()),
    st.floats(min_value=0, max_value=100, allow_nan=False, allow_infinity=False),
)
def test_parse_applicant_valid_roundtrip(category, marks):
    result = parse_applicant(f"{category}:{marks}")
    assert result is not None
    assert result[0] == category.strip().title()
    assert result[1] == marks


@given(st.lists(st.integers(min_value=0, max_value=100), min_size=1))
def test_marks_average_within_bounds(values):
    avg = marks_average(",".join(map(str, values)))
    assert avg is not None
    assert min(values) <= avg <= max(values)


@given(
    st.floats(min_value=0, max_value=1e9, allow_nan=False),
    st.floats(min_value=0, max_value=1e9, allow_nan=False),
)
def test_payable_award_never_negative(award, deduction):
    result = payable_award(f"{award}|{deduction}")
    assert result is not None
    assert math.isfinite(result) and result >= 0
