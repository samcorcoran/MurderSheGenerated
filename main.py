import random

import namegen
import graph

class character(graph.vertex):
    """ Actor/agent within the story """
    def __init__(self):
        graph.vertex.__init__(self)
        self.gender = random.choice(['m','f'])
        self.name = namegen.generateFirstName(self.gender)
        # Surname is a property of family
        #self.surname = None
        self.victim = False

class relationship():
    """ Manner in which two characters are connected. An edge between vertices. """
    def __init__(self, charA, charB):
        self.type = None
        self.nature = None
        self.assignRandomType()

    def assignRandomType(self):
        self.type = random.choice(['familial', 'romantic', 'professional', 'social'])

class cast(graph.graph):
    """ Network of relationships between characters """
    def __init__(self):
        graph.graph.__init__(self)

    def addCharacter(self, c):
        self.addVertex(c)

    def createRelationship(self, charA, charB):
        rel = relationship(charA, charB)
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

# Create graph
c = cast()
# Add characters
totalCharacters = 5
for n in range(totalCharacters):
    c.addCharacter(character())
# Totally connect graph
c.totallyConnect()
# Eliminate some random edges
numEliminatedEdges = 5
for n in range(numEliminatedEdges):
    c.removeRandomRelationship()

# Print names
for char in c.edges.keys():
    print(char.name)
print(c.edges)