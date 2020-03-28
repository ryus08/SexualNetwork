import uuid
from enum import Enum
import random
import configparser
import numpy as np

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
DUR_MARITAL = int(run001["DUR_MARITAL"])
DUR_CASUAL = int(run001["DUR_CASUAL"])
DUR_SHORT_TERM = int(run001["DUR_SHORT_TERM"])
SIM_MONTHS = SIM_YEARS * CYCLE_LENGTH

# Create empty dictionary of men, women and list of partnerships

Women = dict()
Men = dict()
Partnerships = dict()

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

    def __init__(self, partnershipid, womanid, manid, partnershiptype):
        self.partnership_id = partnershipid
        self.male_id = manid
        self.female_id = womanid
        self.partnership_duration = 1
        self.partnership_type = partnershiptype
        if self.partnership_type == PartnershipType.MARITAL:
            self.maxdur = 12 * np.random.poisson(DUR_MARITAL, 1)
        elif self.partnership_type == PartnershipType.SHORT_TERM:
            self.maxdur = 12 * np.random.poisson(DUR_SHORT_TERM, 1)
        elif self.partnership_type == PartnershipType.CASUAL:
            self.maxdur = 12 * np.random.poisson(DUR_CASUAL, 1)

    def check_relationships(self):
        if self.partnership_type == PartnershipType.INSTANTANEOUS:
            del self
        elif self.partnership_duration < self.maxdur:
            self.partnership_duration += 1
        else:
            Women[self.female_id].numpartners -= 1
            Men[self.male_id].numpartners -= 1
            del self


class Individual:
    single = True
    numpartners = 0

    def __init__(self, gender, age, propconc, id):
        self.age = age
        self.monthage = age * 12
        self.gender = gender
        self.concurrency = propconc
        self.id = id

    def increment_age(self):
        self.monthage += 1
        if self.monthage % 12 == 0:
            self.age += 1

    def add_partner(self, partnerid, partnershiptype):
        partnership_id = uuid.uuid1()
        Partnerships[partnership_id] = Partnership(partnership_id, self.id, partnerid, partnershiptype)
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
    woman_id = uuid.uuid1()
    Women[woman_id] = Individual(Gender.FEMALE, 20, CONCURRENCY_FEMALE, woman_id)
    man_id = uuid.uuid1()
    Men[man_id] = Individual(Gender.MALE, 20, CONCURRENCY_MALE, man_id)

# Starting simulation

for months in range(SIM_MONTHS):
    for _, w in Women.items():
        w.run_partnerships(Men)

    for _, p in Partnerships.items():
        p.check_relationships()
