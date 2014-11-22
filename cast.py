import random

import graph
import relationships as rship
from relationships import relType

class cast(graph.graph):
    """ Network of relationships between characters """
    def __init__(self):
        graph.graph.__init__(self)
        self.allRelationships = list()
        self.plotFamilies = list()

    def addCharacter(self, c):
        self.addVertex(c)

    def createRelationship(self, charA, charB):
        rel = rship.relationship(charA, charB)
        self.allRelationships.append(rel)
        self.addRelationship(charA, charB, rel)

    def addRelationship(self, charA, charB, rel):
        self.edges[charA].append((charB, rel))
        self.edges[charB].append((charA, rel))

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

    def totallyConnect(self):
        """ Create a relationship between every pair of vertices """
        for charA in self.edges:
            for charB in self.edges:
                if charA != charB:
                    # Confirm relationship doesn't already exist
                    exists = False
                    for rel in self.edges[charA]:
                        if rel[0] == charB:
                            exists = True
                            break
                    if not exists:
                        self.createRelationship(charA, charB)

    def gatherConnectedRelTypeMembers(self, charA, desiredType, members):
        members.append(charA)
        for rel in self.edges[charA]:
            if rel[1].type == desiredType and not rel[0] in members:
                # Extend search to matching character's relationships
                self.gatherConnectedRelTypeMembers(rel[0], desiredType, members)
        return members

    def generateRelationshipEntities(self):
        for charA in self.edges.keys():
            for edge in self.edges[charA]:
                rel = edge[1]
                if rel.type == relType.familial:
                    # Check for no existing family
                    if rel.members[0].family == None:
                        newFamily = rship.family()
                        self.plotFamilies.append(newFamily)
                        self.connectFamily(rel.members[0], newFamily)
            # Create single-member non-plot families
            if charA.family == None:
                charA.family = rship.family()

    def connectFamily(self, charA, family):
        global c #cast
        familyMembers = list()
        self.gatherConnectedRelTypeMembers(charA, relType.familial, familyMembers)
        print("New family:")
        for m in familyMembers:
            m.family = family
            print(m.name + " " + family.surname)