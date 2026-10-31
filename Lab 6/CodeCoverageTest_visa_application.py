import pytest

from visa_application import (
    visa_fee,
    documents_complete,
    application_status,
)


# ==================== VISA FEE TESTS ====================

def test_unknown_visa_type():
    with pytest.raises(ValueError, match="unknown visa type"):
        visa_fee("work", 2, "normal", "B")


def test_negative_entries():
    with pytest.raises(ValueError, match="invalid entries"):
        visa_fee("tourist", -1, "normal", "B")


def test_included_entries():
    assert visa_fee("tourist", 1, "normal", "B") == 0


def test_nationality_group_a_extra_included_entry():
    assert visa_fee("tourist", 2, "normal", "A") == 0


def test_student_does_not_get_nationality_bonus():
    assert visa_fee("student", 2, "normal", "A") == 0


def test_normal_processing_fee():
    assert visa_fee("tourist", 3, "normal", "B") == 80


def test_express_processing_fee():
    assert visa_fee("tourist", 3, "express", "B") == 200


def test_normal_processing_more_than_five_extra_entries():
    assert visa_fee("tourist", 7, "normal", "B") == 360


def test_express_processing_more_than_five_extra_entries():
    assert visa_fee("tourist", 7, "express", "B") == 780


# ==================== DOCUMENT TESTS ====================

def test_renewal_with_forms():
    assert documents_complete(1, 0, True) is True


def test_renewal_without_forms():
    assert documents_complete(0, 2, True) is False


def test_new_application_insufficient_photos():
    assert documents_complete(3, 1, False) is False


def test_new_application_insufficient_forms():
    assert documents_complete(2, 2, False) is False


def test_new_application_complete_documents():
    assert documents_complete(3, 2, False) is True


# ==================== APPLICATION STATUS TESTS ====================

def test_express_application_open():
    assert application_status(10, True, False) == "open"


def test_normal_application_open():
    assert application_status(30, False, False) == "open"


def test_peak_season_cutoff():
    assert application_status(45, False, True) == "open"


def test_express_peak_season_cutoff():
    assert application_status(25, True, True) == "open"


def test_application_closing():
    assert application_status(15, False, False) == "closing"


def test_application_closed():
    assert application_status(14, False, False) == "closed"
