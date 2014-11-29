import random

import namegen
import graph
from relationships import relType as rType

class character(graph.vertex):
    """ Actor/agent within the story """
    def __init__(self):
        graph.vertex.__init__(self)
        self.gender = random.choice(['m','f'])
        self.name = namegen.generateFirstName(self.gender)
        self.victim = False
        # Entity associations
        self.entities = dict()
        # Characters with relationships with this character
        self.relationsByType = {rType.familial:list(), rType.professional:list(), rType.social:list(), rType.romantic:list()}
        self.typesByRelation = dict()
        # Relationship objects involving
        self.relationships = {rType.familial:list(), rType.professional:list(), rType.social:list(), rType.romantic:list()}

    def joinEntity(self, newEntity):
        if newEntity.type in self.entities:
            print("ERROR: Character already member of a %s entity." % str(newEntity.type))
        self.entities[newEntity.type] = newEntity
        newEntity.addMember(self)

    def getFullName(self):
        fullName = str(self.name)
        if rType.familial in self.entities:
            fullName += " " + str(self.entities[rType.familial].surname)
        return fullName

    def addRelationship(self, charB, rel):
        if charB in self.relationsByType[rel.type]:
            print("ERROR: CharA already has this relationship with charB")
            return False
        self.relationsByType[rel.type].append(charB)
        self.relationships[rel.type].append(rel)
        # Confirm if charB is already a key
        if not charB in self.typesByRelation.keys():
            self.typesByRelation[charB] = list()
        self.typesByRelation[charB].append(rel)
        return True