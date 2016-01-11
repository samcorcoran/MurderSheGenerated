import random
from enum import Enum

from namegen import NameGenerator
from graph import Vertex
from relationships import RelationshipType

class Gender(Enum):
    male = "male"
    female = "female"

    def getRandomGender():
        return random.choice([Gender.male, Gender.female])

class Character(Vertex):
    """ Actor/agent within the story """
    def __init__(self, id, name, gender):
        super().__init__(id)
        self.gender = gender
        self.name = name
        self.victim = False

        # Entity associations
        self.entities = dict()

        # Characters with relationships with this character
        self.relationsByType = {
            RelationshipType.familial :list(),
            RelationshipType.professional: list(),
            RelationshipType.social: list(),
            RelationshipType.romantic: list()
            }
        self.typesByRelation = dict()

        # Relationship objects involving
        self.relationships = {
            RelationshipType.familial: list(),
            RelationshipType.professional: list(),
            RelationshipType.social: list(),
            RelationshipType.romantic: list()
            }

    def joinEntity(self, newEntity):
        self.entities[newEntity.type] = newEntity
        newEntity.addMember(self)

    def getFullName(self):
        fullName = str(self.name)
        if RelationshipType.familial in self.entities:
            fullName += " " + str(self.entities[RelationshipType.familial].name)
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

    def printDiagnostic(self, printRelationships = True):
        print("Char {0}: {1})".format(self.id, self.getFullName()))
        print("\t{0}, Victim: {1}".format(self.gender, self.victim))
        # Optional detail regarding relationships
        if printRelationships:
            print("\tRelations:")
            # E.g. romantic (1): [(1, 'Landon')]
            for nextRelationshipType in self.relationsByType:
                relations = self.relationsByType[nextRelationshipType]
                if relations:
                    print("\t\t{0} ({1}): {2}".format(nextRelationshipType.name,
                                                             len(relations),
                                                             [(x.id, x.name) for x in relations]))
            print("\tRelationships:")
            # E.g. familial (2): [(10, 'Henrietta'), (3, 'Prudence')]
            for nextRelationshipType in self.relationships:
                rels = self.relationships[nextRelationshipType]
                tuples = []
                # Tuple formed of (relId, relation name, entity name)
                for r in rels:
                    entityName = "NONE"
                    if r.associatedEntity:
                        entityName = r.associatedEntity.name
                    tuples.append((r.id,
                                  r.getOtherParticipant(self).name,
                                  entityName))
                if rels:
                    print("\t\t{0} ({1}): {2}".format(nextRelationshipType.name,
                                                  len(rels),
                                                  tuples))

