import uuid
from enum import Enum
import random
import configparser
import numpy as np
import pandas as pd

config = configparser.ConfigParser()
config.read('example.ini')
run001 = config['run001']
COHORT_SIZE: int = int(run001["COHORT_SIZE"])
SIM_YEARS: int = int(run001["SIM_YEARS"])
CYCLE_LENGTH: int = int(run001["CYCLE_LENGTH"])
CONCURRENCY_MALE: float = float(run001["CONCURRENCY_MALE"])
CONCURRENCY_FEMALE: float = float(run001["CONCURRENCY_FEMALE"])
PROB_MARITAL: float = float(run001["PROB_MARITAL"])
PROB_CASUAL: float = float(run001["PROB_CASUAL"])
PROB_SHORT_TERM: float = float(run001["PROB_SHORT_TERM"])
PROB_INSTANTANEOUS: float = float(run001["PROB_INSTANTANEOUS"])
DUR_MARITAL: int = int(run001["DUR_MARITAL"])
DUR_CASUAL: int = int(run001["DUR_CASUAL"])
DUR_SHORT_TERM: int = int(run001["DUR_SHORT_TERM"])
SEXUAL_DEBUT_AGE: int = int(run001["SEXUAL_DEBUT_AGE"])
BACKGROUND_MORTALITY_FEMALE = pd.read_csv(run001["BACKGROUND_MORTALITY_FEMALE_FILE"])
BACKGROUND_MORTALITY_MALE = pd.read_csv(run001["BACKGROUND_MORTALITY_MALE_FILE"])
AGE_OF_PARTNER = pd.read_csv(run001["AGE_OF_PARTNER_FILE"])
PARTNERSHIP_FORMATION = pd.read_csv(run001["PARTNERSHIP_FORMATION_FILE"])
INITIAL_POPULATION = pd.read_csv(run001["INITIAL_POPULATION_FILE"])

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
            self.maxdur = 12 * np.random.poisson(DUR_MARITAL, None)
        elif self.partnership_type == PartnershipType.SHORT_TERM:
            self.maxdur = 12 * np.random.poisson(DUR_SHORT_TERM, None)
        elif self.partnership_type == PartnershipType.CASUAL:
            self.maxdur = 12 * np.random.poisson(DUR_CASUAL, None)

    def check_relationships(self):
        if Women[self.female_id].alive and Men[self.male_id].alive:
            if self.partnership_type == PartnershipType.INSTANTANEOUS:
                self.dissolve_relationship()
            elif self.partnership_duration < self.maxdur:
                self.partnership_duration += 1
            else:
                self.dissolve_relationship()
        else:
            self.dissolve_relationship()

    def dissolve_relationship(self):
        Women[self.female_id].numpartners -= 1
        Men[self.male_id].numpartners -= 1
        del self


class Individual:
    single = True
    numpartners = 0
    alive = True

    def __init__(self, gender, age, propconc, identifier):
        self.age = age
        self.month_age = age * 12
        self.gender = gender
        self.concurrency = propconc
        self.id = identifier

    def natural_history(self, mortality):
        rand = random.random()
        if rand < mortality.iloc[self.age]["mASR"]:
            self.alive = False
        else:
            self.month_age += 1
            if self.month_age % 12 == 0:
                self.age += 1

    def add_partner(self, partnerid, partnershiptype):
        partnership_id = uuid.uuid1()
        Partnerships[partnership_id] = Partnership(partnership_id, self.id, partnerid, partnershiptype)
        self.numpartners += 1
        Men[partnerid].numpartners += 1

    def create_partnership(self):
        for _, m in Men.items():
            if (AGE_OF_PARTNER.iloc[self.age]["mean"] + AGE_OF_PARTNER.iloc[self.age]["SD"]) >= m.age >= (AGE_OF_PARTNER.iloc[self.age]["mean"] - AGE_OF_PARTNER.iloc[self.age]["SD"]):
                if m.single:
                    relationship_type = self.assign_partnership_type(True)
                    self.add_partner(m.id, relationship_type)
                    m.single = False
                    self.single = False
                    self.numpartners += 1
                    m.numpartners += 1
                    break
                else:
                    rand = random.random()
                    if rand < m.concurrency:
                        relationship_type = self.assign_partnership_type(False)
                        self.add_partner(m.id, relationship_type)
                        m.single = False
                        self.numpartners += 1
                        self.single = False
                        m.numpartners += 1
                        break

    @staticmethod
    def assign_partnership_type(single):
        if single:
            rand = random.random()
            if rand < PROB_CASUAL:
                return PartnershipType.CASUAL
            elif rand < (PROB_CASUAL + PROB_MARITAL):
                return PartnershipType.MARITAL
            elif rand < (PROB_CASUAL + PROB_MARITAL + PROB_SHORT_TERM):
                return PartnershipType.SHORT_TERM
            else:
                return PartnershipType.INSTANTANEOUS
        else:
            rand = random.random()
            if rand < PROB_CASUAL:
                return PartnershipType.CASUAL
            else:
                return PartnershipType.INSTANTANEOUS

    def run_partnerships(self):
        if self.age >= SEXUAL_DEBUT_AGE:
            if self.single:
                rand = random.random()
                if rand < PARTNERSHIP_FORMATION.iloc[self.age]["Female"]:
                    self.create_partnership()
            else:
                rand = random.random()
                if rand < self.concurrency:
                    self.create_partnership()


# Initialize men and women

NumMen = []
NumWomen = []
ModelAges = INITIAL_POPULATION.shape[0]

for k in range(ModelAges):
    NumMen.append(int(INITIAL_POPULATION.iloc[k]["MALE"] * COHORT_SIZE))
    NumWomen.append(int(INITIAL_POPULATION.iloc[k]["FEMALE"] * COHORT_SIZE))

age = 1
for x in NumWomen:
    for i in range(x):
        woman_id = uuid.uuid1()
        Women[woman_id] = Individual(Gender.FEMALE, age, CONCURRENCY_FEMALE, woman_id)
    age += 1

age = 1
for x in NumMen:
    for i in range(x):
        man_id = uuid.uuid1()
        Men[man_id] = Individual(Gender.MALE, age, CONCURRENCY_MALE, man_id)
    age += 1

# Starting simulation

for months in range(SIM_MONTHS):
    for _, w in Women.items():
        w.natural_history(BACKGROUND_MORTALITY_FEMALE)

    for _, m in Men.items():
        m.natural_history(BACKGROUND_MORTALITY_MALE)

    for _, w in Women.items():
        w.run_partnerships()

    for _, p in Partnerships.items():
        p.check_relationships()
