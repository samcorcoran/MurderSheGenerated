from enum import Enum
import itertools
import random

from graph import Graph
from characters import Character, Gender
from namegen import NameGenerator
from relationships import Relationship, RelationshipType, Family, entities


def getRelationship(char, relation):
    out = dict()
    out["character"] = {
        "name": relation.getFullName(),
        "id": relation.id
        }
    out["types"] = [x.type.name for x in char.typesByRelation[relation]]
    return out

def getCharacter(char, relationships=True):
    out = {
        "id": char.id,
        "name": char.getFullName(),
        "gender": char.gender.name
    }
    if char.id == 0:
        out["victim"] = True
    if relationships:
        out["relationships"] = [getRelationship(char, r) for r in char.typesByRelation.keys()]
    return out

def getMurderer(char):
    c = getCharacter(char)
    c["murderer"] = True
    return c

def getEntity(e, type):
    return {
      "name": e.name,
      "type": type.name,
      "members": [getCharacter(c, relationships=False) for c in e.members]
      }

def getEntities(type, entities):
    return [getEntity(e, type) for e in entities[type]]

class ConnectionStrategy(Enum):
    totallyConnect = "total"
    randomlyConnect = "random"
    stringConnect = "string"

class Cast():
    """ Network of relationships between characters """
    def __init__(self):
        self.characters = list()
        self.namegen = NameGenerator()
        # Lists of relationship objects, keyed by type
        self.relationships = {
            RelationshipType.familial: list(),
            RelationshipType.professional:list(),
            RelationshipType.social:list(),
            RelationshipType.romantic:list()
            }
        # Lists of relationship objects, keyed by participants
        self.relationshipsByParticipants = dict()

        self.entities = dict()

    def addEntity(self, entity):
        if not entity.type in self.entities:
            self.entities[entity.type] = list()
        self.entities[entity.type].append(entity)

    def totalTypedEntities(self, relationshipType):
        if not relationshipType in self.entities:
            self.entities[relationshipType] = list()
        return len(self.entities[relationshipType])

    def getAllRelationships(self):
        return [item for sublist in self.relationships.values() for item in sublist]

    def getAllEntities(self):
        return [item for sublist in self.entities.values() for item in sublist]

    def addCharacter(self, name = None, gender = None):
        if gender == None:
            gender = Gender.getRandomGender()
        if name == None:
            name = self.namegen.generateFirstName(gender)
        c = Character(len(self.characters), name, gender)
        self.characters.append(c)

    def createRelationship(self, charA, charB, relType):
        totalRelationships = self.getTotalRelationships()
        charATotalTypedRelationships = len(charA.relationships[relType])
        charBTotalTypedRelationships = len(charB.relationships[relType])
        totalRelationshipsByParticipantsKeys = len(
            [x for x in self.relationshipsByParticipants.values() for item in x]
            )
        # Create relationship object (does not affect state - not binding relationship
        # until stored somewhere)
        rel = Relationship(self.getTotalRelationships(), charA, charB, relType)
        # Don't add relationship if already related
        if charB in charA.relationsByType[rel.type]:
            print("WARNING: Attempted to create duplicate relationship ",
                "({0}) between {1} and {2}".format(rel.type.name, charA.name, charB.name))
            return False
        # Store relationship object keyed by relationship type
        self.relationships[rel.type].append(rel)
        # Also store rel obj keyed by participant tuples (in both orderings)
        self.storeRelationshipByParticipants(charA, charB, rel)
        # Store in characters
        charA.addRelationship(charB, rel)
        charB.addRelationship(charA, rel)
        # Test relationship creation did not have problems
        if (totalRelationships+1 != self.getTotalRelationships()):
            print("ERROR: Relationship not correctly added to total set")
        if (charATotalTypedRelationships+1 != len(charA.relationships[relType])):
            print("ERROR: Relationship not correctly added to charA")
        if (charBTotalTypedRelationships+1 != len(charB.relationships[relType])):
            print("ERROR: Relationship not correctly added to charB")
        if (totalRelationshipsByParticipantsKeys+2 != len([x for x in self.relationshipsByParticipants.values() for item in x])):
            print("ERROR: Relationship not correctly added, keyed by participants")
        return True

    def getTotalRelationships(self):
        return len(self.getAllRelationships())

    def getTotalEntities(self):
        return len(self.getAllEntities())

    def storeRelationshipByParticipants(self, charA, charB, rel):
        """ Store relationship object keyed on participants (in both orderings) """
        # Ensure character pairing exists as dictionary key
        if not (charA, charB) in self.relationshipsByParticipants:
            self.relationshipsByParticipants[(charA, charB)] = list()
        if not (charB, charA) in self.relationshipsByParticipants:
            self.relationshipsByParticipants[(charB, charA)] = list()
        # Store relationship object under both keys
        self.relationshipsByParticipants[(charA, charB)].append(rel)
        self.relationshipsByParticipants[(charB, charA)].append(rel)

    def removeDirectedRelationship(self, charA, charB):
        """ Removes v2 from v1 edge list """
        for to in self.edges[charA]:
            if to[0] == charB:
                self.edges[charA].remove(to)

    def removeReciprocalRelationship(self, charA, charB):
        self.removeDirectedRelationship(charA, charB)
        self.removeDirectedRelationship(charB, charA)

    def removeRandomRelationship(self):
        if not self.edges:
            print("ERROR: No relationships to be removed")
            return
        charA = None
        charB = None
        while charB == None:
            charA = random.choice(list(self.edges.keys()))
            if self.edges[charA]:
                charB = random.choice(self.edges[charA])[0]
        self.removeReciprocalRelationship(charA, charB)

    def generateRelationshipGroupings(self, relationshipType, maxAllowed, numGroupsMinMax,
                                      groupSizeMinMax, connectionStrategy):
        """ Gathers candidates and forms groups connected by typed relationships """
        numGroups = random.randint(*sorted(numGroupsMinMax))
        print("Num [" + relationshipType.name + "] groups: " + str(numGroups))
        for groupNum in range(numGroups):
            candidates = self.gatherCandidates(relationshipType, maxAllowed)
            if not candidates:
                return
            # Create a new group
            groupMembers = list()
            groupSize = random.randint(*sorted(groupSizeMinMax))
            for memberNum in range(groupSize):
                # Select new member
                if not candidates:
                    break
                member = candidates.pop()
                groupMembers.append(member)
            # Connect members of group
            print("Group size: " + str(len(groupMembers)))
            self.connectCandidates(groupMembers, connectionStrategy, relationshipType)
            if not candidates:
                break
        pass

    def connectCandidates(self, groupMembers, strategy, relationshipType):
        """ Relationships (of relType) are created between group members based strategy """
        if strategy == ConnectionStrategy.totallyConnect:
            # Every member is related to every other
            for pairing in itertools.combinations(groupMembers, 2):
                self.createRelationship(pairing[0], pairing[1], relationshipType)
        elif strategy == ConnectionStrategy.stringConnect:
            # Members form a line (e.g. o-o-o-o-o)
            for n in range(len(groupMembers)-1):
                self.createRelationship(groupMembers[n], groupMembers[n+1], relationshipType)
        elif strategy == ConnectionStrategy.randomlyConnect:
            # All members are randomly connected to existing member of the in-group
            alreadyConnected = list()
            while len(groupMembers) > 0:
                charA = groupMembers.pop()
                if not alreadyConnected:
                    alreadyConnected.append(charA)
                else:
                    # Connect to existing member of 'in-group'
                    self.createRelationship(
                        charA,
                        random.choice(alreadyConnected),
                        relationshipType
                        )
                # Track character as member of in-group
                alreadyConnected.append(charA)
        else:
            print("ERROR: Connection strategy unknown")

    def gatherCandidates(self, relationshipType, numAllowed):
        """ Given criteria, possible relations are listed and returned """
        candidates = list(self.characters)
        # Disqualify by number of existing typed relationships, if necessary
        if numAllowed != -1:
            candidates = [x for x in candidates if len(x.relationsByType[relationshipType]) < numAllowed ]
        random.shuffle(candidates)
        return candidates

    def createEntity(self, relationshipType):
        newEntity = entities[relationshipType](self.getTotalEntities(),
                                               self.namegen.generateName(relationshipType.name))
        # Immediately register new entity with cast object
        self.addEntity(newEntity)
        return newEntity

    def createTypedEntitiesForRelationships(self, relationshipType, maxMembers, strategy = "bfs"):
        """ Finds characters with relationships missing typed entity and creates one """
        # Aggregate relationships of given type
        matchingRelationships = list()
        for character in self.characters:
            # Every relationship is included only once
            charRel = character.relationships[relationshipType]
            if charRel in matchingRelationships:
                continue
            matchingRelationships.extend(charRel)
        # Randomise order to avoid bias in initiators of BF (or otherwise) searches
        random.shuffle(matchingRelationships)
        # Ensure all relationships have an entity
        for nextRelationship in matchingRelationships:
            if not nextRelationship.associatedEntity:
                # This relationship does not have an entity associated so one will be created and associated with
                # the two characters in this relationship. Then using the desired search rules, other characters
                # connected by relationships will also be made associated with the Entity through their relationships
                newEntity = self.createEntity(relationshipType)
                # Associate entity with the relationship it was created for
                nextRelationship.associatedEntity = newEntity
                members = list()
                rels = list()
                if strategy == "bfs":
                    members, rels = self.gatherConnectedRelTypeMembersBreadthFirst(random.choice(nextRelationship.members), relationshipType, maxMembers)
                elif strategy == "dfs":
                    members = self.gatherConnectedRelTypeMembersDepthFirst(random.choice(nextRelationship.members), relationshipType, members, maxMembers)
                for member in members:
                    member.joinEntity(newEntity)
                for rel in rels:
                    rel.associatedEntity = newEntity

    def createIsolatedTypedEntities(self, relationshipType):
        for charA in self.characters:
            # Find characters who don't already have a typed entity
            if not relationshipType in charA.entities.keys():
                newEntity = entities[relationshipType](self.getTotalEntities(), self.namegen.generateName(relationshipType.name))
                self.addEntity(newEntity)
                charA.joinEntity(newEntity)

    def gatherConnectedRelTypeMembersDepthFirst(self, charA, desiredType, members, maxMembers=-1):
        members.append(charA)
        for charB in charA.relationsByType[desiredType]:
            # Character accepted if not already accepted and doesn't already have typed entity
            if not charB in members and not desiredType in charB.entities:
                # Recursively extend search to matching character's relationships
                self.gatherConnectedRelTypeMembersDepthFirst(charB, desiredType, members)
        return members

    def gatherConnectedRelTypeMembersBreadthFirst(self, charA, desiredType, maxMembers=-1, totallyConnect=True):
        """ Creates breadth-first expanding set of typed relations to charA and returns characters and relationships """
        leaves = [charA]
        relationships = list()
        for leafCharacter in leaves:
            edges = leafCharacter.relationships[desiredType]
            ##Debug:
            ##print("Next leaf is '{0}' with {1} {2} relationships ({3})".format(leafCharacter.name,
            ##                                                            len(edges),
            ##                                                           desiredType.name,
            ##                                                            [x.getOtherParticipant(leafCharacter).name for x in edges]))
            for nextRelationship in edges:
                # Get the other participant of the relationship with leafCharacter
                leafRelation = nextRelationship.getOtherParticipant(leafCharacter)
                # Character accepted if not already accepted and doesn't already have typed entity
                if leafRelation not in leaves:
                    leaves.append(leafRelation)
                    relationships.append(nextRelationship)
                    if totallyConnect:
                        # Check if new member has any other relationships of this type with existing members which must
                        # be added to achieve total connectivity for these characters
                        for existingMember in leaves:
                            for possibleInternalConnection in existingMember.relationships[desiredType]:
                                if possibleInternalConnection.getOtherParticipant(existingMember) != leafRelation:
                                    continue
                                if possibleInternalConnection in relationships:
                                    continue
                                relationships.append(possibleInternalConnection)
                    if (0 <= maxMembers <= len(leaves)):
                        # Return early if maximum is reached
                        return leaves, relationships
        ## Debug:
        ##print("Gathered {0} characters and {1} relationships in BFS".format(len(leaves), len(relationships)))
        # Return full set if no maximum was set
        return leaves, relationships

    def mostCommonConnection(self, L):
        groups = itertools.groupby(sorted(L))
        def auxfun(item):
            return len(list(item[1])), -L.index(item[0])
        return max(groups, key=auxfun)[0]

    def toDict(self):
        groups = [getEntities(type, self.entities) for type in self.entities.keys() if type.name != "familial"]
        id = self.mostCommonConnection(
            [c["character"]["id"] for c in getCharacter(self.characters[0])["relationships"]]
            )
        murderer = getCharacter([c for c in self.characters if c.id == id][0])
        characters = [getMurderer(c) if c.id == murderer["id"] else getCharacter(c) for c in self.characters]
        return {
            "characters": characters,
            "groups": [item for sublist in groups for item in sublist],
            "investigator": self.investigator,
            "murderer": murderer
            }

    def generateLocation(self):
        return self.namegen.generateLocation()

    def generateScene(self, location):
        victim = self.characters[0]
        types = [etype for etype in self.entities.keys() if etype.name != "familial" and etype.name != "romantic"]
        groups = [self.entities[etype] for etype in types]
        investigator_title = random.choice(self.namegen.investigatorTitles)
        investigator_surname = random.choice(self.namegen.surnames)
        self.investigator = "{0} {1}".format(investigator_title, investigator_surname)
        return self.namegen.generateScene(
            location,
            victim,
            investigator_title,
            investigator_surname,
            [item for sublist in groups for item in sublist]
            )

    def generateTitle(self):
        return "The {0} of {1}".format(
            self.namegen.generateTitle(),
            self.characters[0].getFullName()
        )

    def printDiagnostic(self):
        print("--- CAST DIAGNOSTICS ---")
        print("Character diagnostics (total: {0})".format(len(self.characters)))
        for charA in self.characters:
            charA.printDiagnostic()
        print("Relationship diagnostics (total: {0})".format(self.getTotalRelationships()))
        for nextRelationshipType in self.relationships:
            print("\t{0} relationships (total: {1})".format(nextRelationshipType.name, len(self.relationships[nextRelationshipType])))
            for rel in self.relationships[nextRelationshipType]:
                rel.printDiagnostic()
        print("Entity diagnostics (total: {0})".format(self.getTotalEntities()))
        for nextEntityType in self.entities:
            print("\t{0} entities (total: {1})".format(nextEntityType.name, len(self.entities[nextEntityType])))
            for nextEntity in self.entities[nextEntityType]:
                nextEntity.printDiagnostic()

