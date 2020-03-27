from classes import Gender
from classes import Individual
import configparser

config = configparser.ConfigParser()
config.read('example.ini')
run001 = config['run001']

COHORT_SIZE = int(run001["COHORT_SIZE"])
SIM_YEARS = int(run001["SIM_YEARS"])
CYCLE_LENGTH = int(run001["CYCLE_LENGTH"])
SIM_MONTHS = SIM_YEARS * CYCLE_LENGTH
CONCURRENCY_MALE = float(run001["CONCURRENCY_MALE"])
CONCURRENCY_FEMALE = float(run001["CONCURRENCY_FEMALE"])

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