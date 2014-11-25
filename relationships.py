
from enum import Enum
import random

import namegen

class relType(Enum):
    familial = "familial"
    romantic = "romantic"
    professional = "professional"
    social = "social"

    def getRandomRelType():
        return random.choice([relType.familial, relType.romantic, relType.professional, relType.social])

class relationship():
    """ Manner in which two characters are connected. An edge between vertices. """
    def __init__(self, charA, charB, relType):
        self.members = (charA, charB)
        self.type = relType
        self.nature = None
        self.publicKnowledge = True


totalFamilies = 0
class family():
    def __init__(self):
        global totalFamilies
        self.id = totalFamilies
        totalFamilies += 1
        self.surname = namegen.generateSurname()
        self.members = list()

    def addMember(self, newMember):
        self.members.append(newMember)