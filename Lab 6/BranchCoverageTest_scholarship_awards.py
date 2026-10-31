import pytest
from scholarship_awards import award_amount, is_eligible, application_status


# ======================= award_amount =======================
# --- validation branches ---
def test_unknown_category_raises():
    with pytest.raises(ValueError, match="unknown category"):
        award_amount("music", 80, "low", False)


def test_negative_marks_raises():
    with pytest.raises(ValueError, match="invalid marks"):
        award_amount("merit", -1, "low", False)


def test_zero_marks_is_valid():
    # boundary: marks == 0 is NOT invalid
    assert award_amount("merit", 0, "low", False) == 0


# --- cutoff / renewal branches ---
def test_below_cutoff_marks():
    assert award_amount("merit", 70, "low", False) == 0


def test_exactly_at_cutoff_gives_zero():
    # boundary: above == 0 -> returns 0
    assert award_amount("merit", 75, "low", False) == 0


def test_just_above_cutoff():
    # above == 1
    assert award_amount("merit", 76, "low", False) == 100


def test_all_categories_non_renewal():
    assert award_amount("sports", 70, "low", False) == 1000   # cutoff 60
    assert award_amount("arts", 75, "low", False) == 1000     # cutoff 65


def test_renewal_non_sports_lower_cutoff():
    # merit cutoff 75 -> 70 on renewal
    assert award_amount("merit", 80, "low", True) == 1000
    # arts cutoff 65 -> 60 on renewal
    assert award_amount("arts", 70, "low", True) == 1000


def test_renewal_sports_cutoff_unchanged():
    # is_renewal True but category == sports -> cutoff stays 60
    assert award_amount("sports", 70, "low", True) == 1000


def test_renewal_below_reduced_cutoff():
    # merit renewal cutoff 70; 70 is exactly at cutoff
    assert award_amount("merit", 70, "low", True) == 0


# --- income-level / rate branches ---
def test_low_income_standard_rate():
    assert award_amount("merit", 85, "low", False) == 1000   # 10 * 100


def test_non_low_income_standard_rate():
    assert award_amount("merit", 85, "high", False) == 600   # 10 * 60


def test_unrecognised_income_level_uses_default_rate():
    assert award_amount("merit", 85, "medium", False) == 600


# --- bonus-rate branches (above > 15) ---
def test_above_exactly_15_no_bonus():
    # boundary: above == 15 -> bonus NOT applied
    assert award_amount("merit", 90, "low", False) == 1500   # 15 * 100
    assert award_amount("merit", 90, "high", False) == 900   # 15 * 60


def test_above_16_low_income_bonus():
    # above == 16: rate = 100 + 40 + 20 = 160
    assert award_amount("merit", 91, "low", False) == 2560


def test_above_16_non_low_income_bonus():
    # above == 16: rate = 60 + 40 = 100
    assert award_amount("merit", 91, "high", False) == 1600


def test_max_marks_low_income():
    assert award_amount("merit", 100, "low", False) == 4000  # 25 * 160


# ======================= is_eligible =======================
def test_is_eligible():
    assert is_eligible(90, 0, False) is True


def test_special_quota_backlogs_within_limit():
    assert is_eligible(10, 2, True) is True    # attendance ignored


def test_special_quota_backlogs_exceed_limit():
    assert is_eligible(100, 3, True) is False


def test_attendance_below_75():
    assert is_eligible(74, 0, False) is False


def test_attendance_exactly_75_passes():
    assert is_eligible(75, 1, False) is True   # boundary on both checks


def test_regular_backlogs_exceed_limit():
    assert is_eligible(90, 2, False) is False


# ===================== application_status =====================
# Non-renewal, non-paper -> cutoff 20
def test_status_new_digital():
    assert application_status(20, False, False) == "open"      # boundary
    assert application_status(19, False, False) == "closing"
    assert application_status(5, False, False) == "closing"    # boundary
    assert application_status(4, False, False) == "closed"


# Renewal, non-paper -> cutoff 30
def test_status_renewal_digital():
    assert application_status(30, True, False) == "open"
    assert application_status(29, True, False) == "closing"
    assert application_status(15, True, False) == "closing"
    assert application_status(14, True, False) == "closed"


# Non-renewal, paper -> cutoff 30
def test_status_new_paper():
    assert application_status(30, False, True) == "open"
    assert application_status(29, False, True) == "closing"
    assert application_status(15, False, True) == "closing"
    assert application_status(14, False, True) == "closed"


# Renewal, paper -> cutoff 40
def test_status_renewal_paper():
    assert application_status(40, True, True) == "open"
    assert application_status(39, True, True) == "closing"
    assert application_status(25, True, True) == "closing"
    assert application_status(24, True, True) == "closed"


def test_status_zero_days_left():
    assert application_status(0, False, False) == "closed"
