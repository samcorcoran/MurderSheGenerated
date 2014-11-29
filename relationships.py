
from enum import Enum
import random
from pprint import pprint

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

# Entities characters are members of (e.g. companies, clubs, families) keyed on associated relationship type
entities = dict()

def addEntity(entity):
    if not entity.type in entities:
        entities[entity.type] = list()
    entities[entity.type].append(entity)

def totalTypedEntities(relationshipType):
    if not relationshipType in entities:
        entities[relationshipType] = list()
    return len(entities[relationshipType])

class entity():
    def __init__(self, relationshipType = None):
        self.type = relationshipType
        self.id = totalTypedEntities(self.type)
        addEntity(self)
        self.members = list()

    def addMember(self, newMember):
        self.members.append(newMember)

class family(entity):
    def __init__(self):
        entity.__init__(self, relType.familial)
        self.surname = namegen.generateSurname()

class company(entity):
    def __init__(self):
        entity.__init__(self, relType.professional)
        self.companyName = namegen.generateCompanyName()

class socialGroup(entity):
    def __init__(self):
        entity.__init__(self, relType.social)
        self.socialGroupName = "unnamed";

createEntity = {relType.familial: family, relType.professional: company, relType.social: socialGroup}
