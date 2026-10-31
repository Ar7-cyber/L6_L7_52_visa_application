import pytest

from visa_application import (
    visa_fee,
    documents_complete,
    application_status,
)


# ==================== VISA FEE BRANCH TESTS ====================

def test_unknown_visa_type():
    with pytest.raises(ValueError):
        visa_fee("work", 2, "normal", "B")


def test_valid_visa_types():
    assert visa_fee("tourist", 1, "normal", "B") == 0
    assert visa_fee("business", 3, "normal", "B") == 0
    assert visa_fee("student", 2, "normal", "B") == 0


def test_negative_entries():
    with pytest.raises(ValueError):
        visa_fee("tourist", -1, "normal", "B")


def test_nationality_group_a_non_student():
    assert visa_fee("tourist", 2, "normal", "A") == 0


def test_nationality_group_a_student():
    assert visa_fee("student", 3, "normal", "A") == 40


def test_nationality_group_b():
    assert visa_fee("tourist", 2, "normal", "B") == 40


def test_no_extra_entries():
    assert visa_fee("tourist", 1, "normal", "B") == 0


def test_normal_speed():
    assert visa_fee("tourist", 3, "normal", "B") == 80


def test_express_speed():
    assert visa_fee("tourist", 3, "express", "B") == 200


def test_extra_entries_equal_five():
    assert visa_fee("tourist", 6, "normal", "B") == 200


def test_extra_entries_above_five_normal():
    assert visa_fee("tourist", 7, "normal", "B") == 360


def test_extra_entries_above_five_express():
    assert visa_fee("tourist", 7, "express", "B") == 780


# ==================== DOCUMENT BRANCH TESTS ====================

def test_renewal_true_with_forms():
    assert documents_complete(1, 0, True) is True


def test_renewal_true_without_forms():
    assert documents_complete(0, 2, True) is False


def test_non_renewal_insufficient_photos():
    assert documents_complete(3, 1, False) is False


def test_non_renewal_sufficient_photos_insufficient_forms():
    assert documents_complete(2, 2, False) is False


def test_non_renewal_complete():
    assert documents_complete(3, 2, False) is True


# ==================== APPLICATION STATUS BRANCH TESTS ====================

def test_express_cutoff():
    assert application_status(10, True, False) == "open"


def test_normal_cutoff():
    assert application_status(30, False, False) == "open"


def test_peak_season_true():
    assert application_status(45, False, True) == "open"


def test_peak_season_false():
    assert application_status(30, False, False) == "open"


def test_express_peak_season():
    assert application_status(25, True, True) == "open"


def test_closing_status():
    assert application_status(15, False, False) == "closing"


def test_closed_status():
    assert application_status(14, False, False) == "closed"


def test_closing_boundary():
    assert application_status(9, True, False) == "closing"
