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

class FamilialRoles(Enum):
    sibling = "sibling"
    parent = "parent"
    child = "child"
    spouse = "spouse"

    def getAllRoles(self):
        return [member for name, member in FamilialRoles.__members__.items()]

class Relationship:
    """ Manner in which two characters are connected. An edge between vertices. """
    def __init__(self, id, charA, charB, relType):
        self.id = id
        self.members = (charA, charB)
        self.type = relType
        self.roles = None
        self.associatedEntity = None
        self.publicKnowledge = True
        self.whoKnows = list()
        self.whoSuspects = list()
        self.specifyRoles()

    def specifyRoles(self):
        if RelationshipType.familial:
            self.roles = random.choice([(FamilialRoles.sibling, FamilialRoles.sibling),
                                        (FamilialRoles.parent, FamilialRoles.child),
                                        (FamilialRoles.spouse, FamilialRoles.spouse)])

    def getOtherParticipant(self, charA):
        if self.members[0] == charA:
            return self.members[1]
        elif self.members[1] == charA:
            return self.members[0]
        else:
            return False

# Entities characters are members of (e.g. companies, clubs, families) keyed on associated relationship type

class Entity:
    def __init__(self, id, name, relationshipType = None):
        self.id = id
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
