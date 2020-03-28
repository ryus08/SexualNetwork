from sexualnetwork import Partnership, PartnershipType
import re

def test_partnership_creation():
    # This is a pretty anemic test, not very valuable other than showing a sample test
    partnership = Partnership(1, 2, 3, PartnershipType.MARITAL)
    assert partnership.partnership_id == 1
    assert partnership.female_id == 2
    assert partnership.male_id == 3
    assert partnership.partnership_type == PartnershipType.MARITAL
    assert partnership.partnership_duration == 1