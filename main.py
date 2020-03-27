from classes import Gender
from classes import Individual

COHORT_SIZE = 100
SIM_YEARS = 5
CYCLE_LENGTH = 12
SIM_MONTHS = SIM_YEARS * CYCLE_LENGTH
CONCURRENCY_MALE = 0.2
CONCURRENCY_FEMALE = 0.1

## Create empty list of men and women

Women = []
Men = []

## Initialize list of men and women

for x in range(COHORT_SIZE):
    Women.append(Individual(Gender.FEMALE, 20, CONCURRENCY_FEMALE))
    Men.append(Individual(Gender.MALE, 20, CONCURRENCY_MALE))

for months in range(SIM_MONTHS):

    for w in Women:
        w.run_partnerships(Men)
        w.check_relationships(Men)
