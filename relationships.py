from enum import Enum
import random

import namegen

class RelationshipType(Enum):
    familial = "familial"
    romantic = "romantic"
    professional = "professional"
    social = "social"

    def getRandomRelationshipType():
        return random.choice([
          RelationshipType.familial,
          RelationshipType.romantic,
          RelationshipType.professional,
          RelationshipType.social
          ])

class Relationship:
    """ Manner in which two characters are connected. An edge between vertices. """
    def __init__(self, charA, charB, relType):
        self.members = (charA, charB)
        self.type = relType
        self.nature = None
        self.publicKnowledge = True

# Entities characters are members of (e.g. companies, clubs, families) keyed on associated relationship type

class Entity:
    def __init__(self, id, name, relationshipType = None):
        self.name = name
        self.type = relationshipType
        self.members = list()

    def addMember(self, newMember):
        self.members.append(newMember)

class Family(Entity):
    def __init__(self, id):
        super().__init__(
            id,
            namegen.generateSurname(),
            RelationshipType.familial
            )

class Company(Entity):
    def __init__(self, id):
        super().__init__(
            id,
            namegen.generateCompanyName(),
            RelationshipType.professional
            )

class SocialGroup(Entity):
    def __init__(self, id):
        super().__init__(
            id,
            namegen.generateSocialClubName(),
            RelationshipType.social
            )

entities = {
    RelationshipType.familial: Family,
    RelationshipType.professional: Company,
    RelationshipType.social: SocialGroup
    }
