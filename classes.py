import uuid

class Individual:

    def __init__(self, gender, age):
        self.age = age
        self.gender = gender
        self.single = True
        self.partners = []
        self.id = uuid.uuid1()


