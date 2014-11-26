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

    def createFamilialRelationships(self, family):
        if family == None:
            print("ERROR: No family supplied to createFamilialRelationships")
            return
        for charA in family.members:
            for charB in family.members:
                if charA == charB:
                    continue
                # Create relationship
                self.createRelationship(charA, charB, rship.relType.familial)

    # Vestigial?
    def generatePlotFamilies(self, rangeFamilies, rangeFamilyMembers):
        """
        Creates parameterised number of families with parameterised numbers of members by creating family
        entities and selecting members.
        :param rangeFamilies: tuple of min, max number of familes desired
        :param rangeFamilyMembers: tuple of min, max number of members of each family
        :return: None
        """
        candidates = self.getFamilyCandidates()
        numFamilies = random.randint(*rangeFamilies)
        # If player count can't support 2-member families at min family count, reduce numFamilies so it can
        if len(candidates) < numFamilies*2:
            print("WARNING: Player count cannot sustain num families. Reducing num family min/max.")
            numFamilies = random.randint(0, int(len(candidates)/2))
        print("- Families (" + str(numFamilies) + ") -")
        if len(candidates) < rangeFamilyMembers[0]*numFamilies:
            print("ERROR: Less family candidates than min member count allows")
        # Create desired number of multi-member plot families
        for n in range(numFamilies):
            remainingFamilies = numFamilies - n
            if len(candidates) < remainingFamilies * 2:
                print("ERROR: Less family candidates than desired families")
                break
            newFamily = rship.family()
            # Cap possible family members so to-be created families have minimum of two members each
            numSpareCandidates = len(candidates) - (remainingFamilies * 2)
            # Used desired min/max, unless there aren't enough
            minAdditionalMembers = min(rangeFamilyMembers[0]-2, numSpareCandidates)
            maxAdditionalMembers = min(rangeFamilyMembers[1]-2, numSpareCandidates)
            numMembers = 2 + random.randint(minAdditionalMembers, maxAdditionalMembers)
            print("New Family: " + newFamily.surname + "(" + str(numMembers) + ")")
            for m in range(numMembers):
                member = candidates.pop()
                member.setFamily(newFamily)
                print(member.getFullName())
            # Create familial relationships
            self.createFamilialRelationships(newFamily)

    def generateNonPlotFamilies(self):
        """ Create single-member non-plot families """
        candidates = self.getFamilyCandidates()
        for charA in candidates:
            newFamily = rship.family()
            charA.family = newFamily

    # Vestigial, and needs replacing in usage?
    def getFamilyCandidates(self):
        """ Returns list of all characters eligible to be added to a family """
        candidates = list()
        for charA in self.characters:
            if charA.family == None:
                candidates.append(charA)
        return candidates

    def generateRomanticEntanglements(self, numRomances):
        """ Creates romantic relationships between characters """
        for n in range(numRomances):
            # Perform number of attempts, to attempt to guarantee numRomances
            numAttempts = 10
            for attemptNumber in range(numAttempts):
                charA = random.choice(self.characters)
                candidates = self.getRomanceCandidates(charA)
                if candidates:
                    self.createRelationship(charA, random.choice(candidates), rship.relType.romantic)
                    break
                else:
                    # Pick another charA if this one has no romance candidates
                    continue

    def getRomanceCandidates(self, charA):
        candidates = list(self.characters)
        # Avoid self-romance
        candidates.remove(charA)
        for charB in candidates:
            # Avoid duplicate romances
            if charB in charA.relationsByType[rType.romantic]:
                candidates.remove(charB)
                continue
        return candidates

    def generateRelationshipGroupings(self, relationshipType, numAllowed, numGroupsMinMax, groupSizeMinMax, connectionStrategy):
        """ Gathers candidates and forms groups connected by typed relationships based on parameters """
        numGroups = random.randint(*numGroupsMinMax)
        print("Num [" + relationshipType.name + "] groups: " + str(numGroups))
        for groupNum in range(numGroups):
            candidates = self.gatherCandidates(relationshipType, numAllowed)
            if not candidates:
                return
            # Create a new group
            groupMembers = list()
            groupSize = random.randint(*groupSizeMinMax)
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
            for charA in groupMembers:
                if not alreadyConnected:
                    alreadyConnected.append(charA)
                else:
                    # Connect to existing member of 'in-group'
                    self.createRelationship(charA, random.choice(alreadyConnected), relationshipType)
                # Track character as member of in-group
                groupMembers.remove(charA)
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

    def createRelationshipEntities(self):
        # Familial
        for charA in self.characters:
            if charA.family:
                continue
            if charA.relationsByType[rType.familial]:
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

    def gatherConnectedRelTypeMembers(self, charA, desiredType, members):
        members.append(charA)
        for charB in charA.relationsByType[desiredType]:
            if not charB in members:
                # Extend search to matching character's relationships
                self.gatherConnectedRelTypeMembers(charB, desiredType, members)
        return members