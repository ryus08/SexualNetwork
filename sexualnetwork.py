import uuid
from enum import Enum
import random
import configparser

config = configparser.ConfigParser()
config.read('example.ini')
run001 = config['run001']
COHORT_SIZE = int(run001["COHORT_SIZE"])
SIM_YEARS = int(run001["SIM_YEARS"])
CYCLE_LENGTH = int(run001["CYCLE_LENGTH"])
CONCURRENCY_MALE = float(run001["CONCURRENCY_MALE"])
CONCURRENCY_FEMALE = float(run001["CONCURRENCY_FEMALE"])
PROB_MARITAL = float(run001["PROB_MARITAL"])
PROB_CASUAL = float(run001["PROB_CASUAL"])
PROB_SHORT_TERM = float(run001["PROB_SHORT_TERM"])
PROB_INSTANTANEOUS = float(run001["PROB_INSTANTANEOUS"])
SIM_MONTHS = SIM_YEARS * CYCLE_LENGTH

# Create empty list of men, women and partnerships

Women = []
Men = []
Partnerships = []

# Defining classes and variables


class Gender(Enum):
    MALE = 1
    FEMALE = 2


class PartnershipType(Enum):
    MARITAL = 1
    SHORT_TERM = 2
    CASUAL = 3
    INSTANTANEOUS = 4


class Partnership:
    maxdur_SHORT_TERM = 3 * 12
    maxdur_MARITAL = 40 * 12
    maxdur_CASUAL = 1 * 12

    def __init__(self, womanid, manid, partnershiptype):
        self.partnership_id = uuid.uuid1()
        self.male_id = manid
        self.female_id = womanid
        self.partnership_duration = 1
        self.partnership_type = partnershiptype

    def check_relationships(self):
        if self.partnership_type == PartnershipType.MARITAL:
            if self.partnership_duration < self.maxdur_MARITAL:
                self.partnership_duration += 1
            else:
                self.dissolve_partnership()
        elif self.partnership_type == PartnershipType.SHORT_TERM:
            if self.partnership_duration < self.maxdur_SHORT_TERM:
                self.partnership_duration += 1
            else:
                self.dissolve_partnership()
        elif self.partnership_type == PartnershipType.CASUAL:
            if self.partnership_duration < self.maxdur_CASUAL:
                self.partnership_duration += 1
            else:
                self.dissolve_partnership()
        elif self.partnership_type == PartnershipType.INSTANTANEOUS:
            self.dissolve_partnership()

    def dissolve_partnership(self):
        del self


class Individual:

    def __init__(self, gender, age, propconc):
        self.age = age
        self.monthage = age * 12
        self.gender = gender
        self.single = True
        self.numpartners = 0
        self.id = uuid.uuid1()
        self.concurrency = propconc

    def increment_age(self):
        self.monthage += 1
        if self.monthage % 12 == 0:
            self.age += 1

    def add_partner(self, partnerid, partnershiptype):
        Partnerships.append(Partnership(self.id, partnerid, partnershiptype))
        self.numpartners += 1

    def create_partnership(self, men):
        random.shuffle(men)
        for m in men:
            if m.single:
                rand = random.random()
                if rand < PROB_CASUAL:
                    self.add_partner(m.id, PartnershipType.CASUAL)
                elif rand < (PROB_CASUAL + PROB_MARITAL):
                    self.add_partner(m.id, PartnershipType.MARITAL)
                elif rand < (PROB_CASUAL + PROB_MARITAL + PROB_SHORT_TERM):
                    self.add_partner(m.id, PartnershipType.SHORT_TERM)
                else:
                    self.add_partner(m.id, PartnershipType.INSTANTANEOUS)
                m.single = False
                self.single = False
                self.numpartners += 1
                m.numpartners += 1
                break
            else:
                rand = random.random()
                if rand < m.concurrency:
                    rand = random.random()
                    if rand < PROB_CASUAL:
                        self.add_partner(m.id, PartnershipType.CASUAL)
                    elif rand < (PROB_CASUAL + PROB_SHORT_TERM):
                        self.add_partner(m.id, PartnershipType.SHORT_TERM)
                    else:
                        self.add_partner(m.id, PartnershipType.INSTANTANEOUS)
                    m.single = False
                    self.numpartners += 1
                    self.single = False
                    m.numpartners += 1
                    break

    def run_partnerships(self, men):
        if self.single:
            self.create_partnership(men)
        else:
            rand = random.random()
            if rand < self.concurrency:
                self.create_partnership(men)


# Initialize list of men and women

for x in range(COHORT_SIZE):
    Women.append(Individual(Gender.FEMALE, 20, CONCURRENCY_FEMALE))
    Men.append(Individual(Gender.MALE, 20, CONCURRENCY_MALE))

# Starting simulation

for months in range(SIM_MONTHS):
    for w in Women:
        w.run_partnerships(Men)

    for p in Partnerships:
        p.check_relationships()
