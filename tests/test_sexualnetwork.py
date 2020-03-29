from sexualnetwork import Partnership, PartnershipType, Women, Men, Gender, Individual
import re

def test_partnership_creation():
    # This is a pretty anemic test, not very valuable other than showing a sample test
    partnership = Partnership(1, 2, 3, PartnershipType.MARITAL)
    assert partnership.partnership_id == 1
    assert partnership.female_id == 2
    assert partnership.male_id == 3
    assert partnership.partnership_type == PartnershipType.MARITAL
    assert partnership.partnership_duration == 1

def test_partnership_max_dur_calculation_marital():
    partnership = Partnership(1, 2, 3, PartnershipType.MARITAL, lambda x: x)
    assert partnership.maxdur == 480

def test_partnership_max_dur_calculation_short():
    partnership = Partnership(1, 2, 3, PartnershipType.SHORT_TERM, lambda x: x)
    assert partnership.maxdur == 36

def test_partnership_max_dur_calculation_casual():
    partnership = Partnership(1, 2, 3, PartnershipType.CASUAL, lambda x: x)
    assert partnership.maxdur == 12