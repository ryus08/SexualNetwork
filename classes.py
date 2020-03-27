import uuid
from enum import Enum
import random

class Gender(Enum):
    MALE = 1
    FEMALE = 2

class Individual:

    maxdur = 3*12

    def __init__(self, gender, age, propconc):
        self.age = age
        self.monthage = age * 12
        self.gender = gender
        self.single = True
        self.partners = dict()
        self.numpartners = 0
        self.id = uuid.uuid1()
        self.concurrency = propconc

    def increment_age(self):
        self.monthage += 1
        if self.monthage % 12 == 0:
            self.age += 1

    def add_partner(self, key, value):
        self.partners[key] = value
        self.numpartners += 1

    def create_partnership(self, men):
        for m in men:
            if m.single:
                self.add_partner(m.id, 1)
                self.single = False
                m.numpartners += 1
                break
            else:
                rand = random.random()
                if rand < m.concurrency:
                    m.single = False
                    self.add_partner(m.id, 1)
                    self.single = False
                    m.numpartners += 1
                    break

    def dissolve_partnership(self, partnerid, man):
        del self.partners[partnerid]
        self.numpartners -= 1
        man.numpartners -= 1
        if self.numpartners == 0:
            self.single = True
        if man.numpartners == 0:
            man.single = True

    def check_relationships(self, men):
        for partnerid, partnershipdur in self.partners.items():
            if partnershipdur < self.maxdur:
                self.partners[partnerid] += 1
            else:
                index = men.id.index(partnerid)
                self.dissolve_partnership(men[index])

    def run_partnerships(self, men):
        if self.single:
            self.create_partnership(men)
        else:
            rand = random.random()
            if rand < self.concurrency:
                self.create_partnership(men)