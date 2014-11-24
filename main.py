
import random
from pprint import pprint

import namegen
import graph
import cast
import relationships as rship
from relationships import relType as rType

class character(graph.vertex):
    """ Actor/agent within the story """
    def __init__(self):
        graph.vertex.__init__(self)
        self.gender = random.choice(['m','f'])
        self.name = namegen.generateFirstName(self.gender)
        self.victim = False
        # Entity associations
        self.family = None
        # Characters with relationships with this character
        self.relationsByType = {rType.familial:list(), rType.professional:list(), rType.social:list(), rType.romantic:list()}
        self.typesByRelation = dict()
        # Relationship objects involving
        self.relationships = {rType.familial:list(), rType.professional:list(), rType.social:list(), rType.romantic:list()}

    def setFamily(self, newFamily):
        if self.family != None:
            print("ERROR: Character already has family.")
        self.family = newFamily
        self.family.addMember(self)

    def getFullName(self):
        return str(self.name) + " " + str(self.family.surname)

    def addRelationship(self, charB, rel):
        self.relationsByType[rel.type].append(charB)
        self.relationships[rel.type].append(rel)
        if not charB in self.typesByRelation:
            self.typesByRelation[charB] = list()
        self.typesByRelation[charB].append(rel)

# Create graph
c = cast.cast()
# Add characters
#totalCharacters = random.randint(4, 15)
totalCharacters = 6
print("TOTAL CHARACTERS: " + str(totalCharacters))
for n in range(totalCharacters):
    c.addCharacter(character())

# GENERATE FAMILIAL RELATIONSHIP NETWORK
numFamilies = (2, 4)
numFamilyMembers = (2, 5)
if (numFamilies[1] * numFamilyMembers[1] > totalCharacters):
    print("WARNING: May have too few characters for max possible families and members")
print("Family parameters: number" + str(numFamilies) + ", size" + str(numFamilyMembers))
c.generatePlotFamilies(numFamilies, numFamilyMembers)
c.generateNonPlotFamilies()

# GENERATE ROMANTIC RELATIONSHIP NETWORK
numRomances = int(0.8 * totalCharacters)
numRomances = 20
c.generateRomanticEntanglements(numRomances)

# Print names
print("- Relationships -")
for char in c.edges.keys():
    print(char.getFullName() + " [" + str(char.id) + "]")
    for relation in char.typesByRelation.keys():
        print("    - " + relation.getFullName() + " [" + str(relation.id) + "] " + "(" + str([x.type.name for x in char.typesByRelation[relation]]) + ")")
