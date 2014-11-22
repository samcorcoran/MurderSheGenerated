
import random
from pprint import pprint

import namegen
import graph
import cast

class character(graph.vertex):
    """ Actor/agent within the story """
    def __init__(self):
        graph.vertex.__init__(self)
        self.gender = random.choice(['m','f'])
        self.name = namegen.generateFirstName(self.gender)
        # Surname is a property of family
        #self.surname = None
        self.victim = False
        # Entity associations
        self.family = None

    def setFamily(self, newFamily):
        if self.family == None:
            print("ERROR: Character already has family.")
        self.family = newFamily

    def getFullName(self):
        return self.name + " " + self.family.surname

# Create graph
c = cast.cast()
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

# Create relationship groups
c.generateRelationshipEntities()

# Print names
print("- Relationships -")
for char in c.edges.keys():
    print(char.getFullName() + " [" + str(char.id) + "]")
    for rel in c.edges[char]:
        #pprint(vars(rel[0]))
        print("    - " + rel[0].getFullName() + " [" + str(rel[0].id) + "] " + "(" + str(rel[1].type.name) + ")")
