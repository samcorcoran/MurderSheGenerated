import random
from pprint import pprint
from enum import Enum
import itertools

import graph
import relationships as rship
from relationships import relType as rType

class ConnectionStrategy(Enum):
    totallyConnect = "total"
    randomlyConnect = "random"
    stringConnect = "string"

class cast():
    """ Network of relationships between characters """
    def __init__(self):
        self.characters = list()
        # Lists of relationship objects, keyed by type
        self.relationships = {rType.familial:list(), rType.professional:list(), rType.social:list(), rType.romantic:list()}
        # Lists of relationship objects, keyed by participants
        self.relationshipsByParticipants = dict()

    def getAllRelationships(self):
        return [item for sublist in self.relationships for item in sublist]

    def addCharacter(self, c):
        self.characters.append(c)

    def createRelationship(self, charA, charB, relType):
        totalRelationships = self.getTotalRelationships()
        charATotalTypedRelationships = len(charA.relationships[relType])
        charBTotalTypedRelationships = len(charB.relationships[relType])
        totalRelationshipsByParticipantsKeys = len(self.relationshipsByParticipants.keys())
        # Create relationship object (does not affect state - not binding relationship until stored somewhere)
        rel = rship.relationship(charA, charB, relType)
        # Don't add relationship if already related
        if charB in charA.relationsByType[rel.type]:
            print("WARNING: Attempted to create duplicate relationship (" + relType.name + ")")
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
        if (totalRelationshipsByParticipantsKeys+2 != len(self.relationshipsByParticipants.keys())):
            print("ERROR: Relationship not correctly added, keyed by participants")
        return True

    def getTotalRelationships(self):
        return len([item for sublist in self.relationships.values() for item in sublist])

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

    def generateNonPlotFamilies(self):
        """ Create single-member non-plot families """
        candidates = self.gatherCandidates(rType.familial, 1)
        for charA in candidates:
            charA.family = rship.family()

    def generateRelationshipGroupings(self, relationshipType, numAllowed, numGroupsMinMax, groupSizeMinMax, connectionStrategy):
        """ Gathers candidates and forms groups connected by typed relationships based on parameters """
        numGroups = random.randint(min(*numGroupsMinMax), numGroupsMinMax[1])
        print("Num [" + relationshipType.name + "] groups: " + str(numGroups))
        for groupNum in range(numGroups):
            candidates = self.gatherCandidates(relationshipType, numAllowed)
            if not candidates:
                return
            # Create a new group
            groupMembers = list()
            groupSize = random.randint(min(*groupSizeMinMax), groupSizeMinMax[1])
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
        """ Relationships (of relType) are created between group members based on given strategy """
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
                    self.createRelationship(charA, random.choice(alreadyConnected), relationshipType)
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

    def createFamilyEntities(self):
        for charA in self.characters:
            if charA.family and charA.relationsByType[rType.familial]:
                # Has familial relations, needs family
                newFamily = rship.family()
                familyMembers = list()
                self.gatherConnectedRelTypeMembers(charA, rType.familial, familyMembers)
                for member in familyMembers:
                    member.setFamily(newFamily)
                # Check if totally connected (because family should be)
                for member in familyMembers:
                    if len(member.relationsByType[rType.familial]) < len(familyMembers)-1:
                        print("ERROR: Family not totally connected")
                        break

    def createCompanyEntities(self, maxCompanyMembers):
        for charA in self.characters:
            if charA.family and charA.relationsByType[rType.professional]:
                # Has professional relations, needs company
                newCompany = rship.company()
                companyMembers = list()
                # Gathered results are a breadth first search???
                self.gatherConnectedRelTypeMembers(charA, rType.professional, companyMembers)
                maxCompanyMembers = min(companyMembers, maxCompanyMembers)
                for n in range(maxCompanyMembers):
                    companyMembers[n].setCompany(newCompany)

    def gatherConnectedRelTypeMembers(self, charA, desiredType, members):
        members.append(charA)
        for charB in charA.relationsByType[desiredType]:
            if not charB in members:
                # Extend search to matching character's relationships
                self.gatherConnectedRelTypeMembers(charB, desiredType, members)
        return members