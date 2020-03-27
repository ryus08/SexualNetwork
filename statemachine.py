import classes as Funct

CohortSize = 100
Women = []
Men = []
for x in range(CohortSize):
    Women.append(Funct.Individual("Female", 20))
    print(Women[x].id)
    Men.append(Funct.Individual("Male", 20))


