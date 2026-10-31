import pytest
from scholarship_awards import award_amount, is_eligible, application_status


# ---------------- award_amount ----------------
def test_below_cutoff_marks():
    assert award_amount("merit", 70, "low", False) == 0


def test_unknown_category_raises():
    with pytest.raises(ValueError, match="unknown category"):
        award_amount("music", 80, "low", False)


def test_negative_marks_raises():
    with pytest.raises(ValueError, match="invalid marks"):
        award_amount("merit", -1, "low", False)


def test_low_income_standard_rate():
    # above = 10, rate = 100
    assert award_amount("merit", 85, "low", False) == 1000


def test_other_income_standard_rate():
    # above = 10, rate = 60
    assert award_amount("merit", 85, "high", False) == 600


def test_low_income_high_marks_bonus():
    # above = 20, rate = 100 + 40 + 20 = 160
    assert award_amount("merit", 95, "low", False) == 3200


def test_other_income_high_marks_bonus():
    # above = 20, rate = 60 + 40 = 100
    assert award_amount("merit", 95, "high", False) == 2000


def test_renewal_non_sports_lower_cutoff():
    # cutoff 75 -> 70, above = 10
    assert award_amount("merit", 80, "low", True) == 1000


def test_renewal_sports_cutoff_unchanged():
    # sports cutoff stays 60, above = 10
    assert award_amount("sports", 70, "low", True) == 1000


# ---------------- is_eligible ----------------
def test_is_eligible():
    assert is_eligible(90, 0, False) is True


def test_special_quota_eligible():
    assert is_eligible(50, 2, True) is True


def test_low_attendance_not_eligible():
    assert is_eligible(70, 0, False) is False


def test_too_many_backlogs_not_eligible():
    assert is_eligible(90, 2, False) is False


# ---------------- application_status ----------------
def test_status_open():
    assert application_status(25, False, False) == "open"


def test_status_closing():
    assert application_status(10, False, False) == "closing"


def test_status_closed():
    assert application_status(2, False, False) == "closed"


def test_status_renewal_and_paper():
    # cutoff = 30 + 10 = 40
    assert application_status(40, True, True) == "open"
