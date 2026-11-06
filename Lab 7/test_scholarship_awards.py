from hypothesis import given, strategies as st
from scholarship_awards import parse_applicant, marks_average, payable_award

@given(st.text() | st.none())
def test_parse_applicant_no_crash(s):

@given(st.text() | st.none())
def test_marks_average_no_crash(s):

@given(st.text() | st.none())
def test_payable_award_no_crash(s):
