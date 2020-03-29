from sexualnetwork import Partnership, Marriage, ShortTermRelationship, CasualRelationship, InstantaneousRelationship, Women, Men, Gender, Individual
import re

def test_partnership_creation():
    # This is a pretty anemic test, not very valuable other than showing a sample test
    partnership = Marriage(1, 2, 3)
    assert partnership.partnership_id == 1
    assert partnership.female_id == 2
    assert partnership.male_id == 3
    assert partnership.partnership_duration == 1

def test_partnership_max_dur_calculation_marital():
    partnership = Marriage(1, 2, 3, lambda x: x)
    assert partnership.maxdur == 480

def test_partnership_max_dur_calculation_short():
    partnership = ShortTermRelationship(1, 2, 3, lambda x: x)
    assert partnership.maxdur == 36

def test_partnership_max_dur_calculation_casual():
    partnership = CasualRelationship(1, 2, 3, lambda x: x)
    assert partnership.maxdur == 12

def test_partnership_max_dur_calculation_instantaneous():
    partnership = InstantaneousRelationship(1, 2, 3, lambda x: x)
    assert partnership.maxdur == 0