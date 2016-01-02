from enum import Enum
import random

from namegen import NameGenerator

class RelationshipType(Enum):
    familial = "familial"
    romantic = "romantic"
    professional = "professional"
    social = "social"

    def getRandomRelType(self):
        return random.choice(
            [member for name, member in RelationshipType.__members__.items()]
                            )

class Relationship:
    """ Manner in which two characters are connected. An edge between vertices. """
    def __init__(self, charA, charB, relType):
        self.members = (charA, charB)
        self.type = relType
        self.roles = list()
        self.publicKnowledge = True
        self.whoKnows = list()
        self.whoSuspects = list()

# Entities characters are members of (e.g. companies, clubs, families) keyed on associated relationship type

class Entity:
    def __init__(self, id, name, relationshipType = None):
        self.name = name
        self.type = relationshipType
        self.members = list()

    def addMember(self, newMember):
        self.members.append(newMember)

class Family(Entity):
    def __init__(self, id, name):
        super().__init__(id, name, RelationshipType.familial)

    def getLocation(self):
        return "%s residence" % self.name

class Company(Entity):
    def __init__(self, id, name):
        super().__init__(id, name, RelationshipType.professional)

    def getLocation(self):
        return "%s head offices" % self.name

class SocialGroup(Entity):
    def __init__(self, id, name):
        super().__init__(id, name, RelationshipType.social)

    def getLocation(self):
        return "%s clubhouse" % self.name

entities = {
    RelationshipType.familial: Family,
    RelationshipType.professional: Company,
    RelationshipType.social: SocialGroup
    }
