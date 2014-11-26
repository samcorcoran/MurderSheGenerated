import random

import cast
from relationships import relType as rType
from cast import ConnectionStrategy
from characters import character

# Create graph
c = cast.cast()
# Add characters
totalCharacters = random.randint(4, 15)
#totalCharacters = 4
print("TOTAL CHARACTERS: " + str(totalCharacters))
for n in range(totalCharacters):
    c.addCharacter(character())

# GENERATE FAMILIAL RELATIONSHIP NETWORK
numFamilies = (int(totalCharacters/6), int(totalCharacters/3))
numFamilyMembers = (max(2, int(totalCharacters/6)), int(totalCharacters/3))
if (numFamilies[1] * numFamilyMembers[1] > totalCharacters):
    print("WARNING: May have too few characters for max possible families and members")
print("Family parameters: number" + str(numFamilies) + ", size" + str(numFamilyMembers))

# GENERATE ROMANTIC RELATIONSHIP NETWORK
numRomances = int(0.5 * totalCharacters)

# GENERATE PROFESSIONAL RELATIONSHIP NETWORK
numEmployers = (int(totalCharacters/6), int(totalCharacters/3))
numEmployees = (max(2, int(totalCharacters/6)), int(totalCharacters/3))
if (numEmployers[1] * numEmployees[1] > totalCharacters):
    print("WARNING: May have too few characters for max possible professional relationships")
print("Professional parameters: number" + str(numEmployers) + ", size" + str(numEmployees))

# GENERATE SOCIAL RELATIONSHIP NETWORK
numSocialGroups = (int(totalCharacters/6), int(totalCharacters/3))
numSocialites = (max(2, int(totalCharacters/6)), int(totalCharacters/3))
if (numSocialGroups[1] * numSocialites[1] > totalCharacters):
    print("WARNING: May have too few characters for max possible social relationships")
print("Social parameters: number" + str(numSocialGroups) + ", size" + str(numSocialites))

c.generateRelationshipGroupings(rType.familial, 1, numFamilies, numFamilyMembers, ConnectionStrategy.totallyConnect)
c.generateRelationshipGroupings(rType.romantic, -1, (numRomances, numRomances), (2,2), ConnectionStrategy.totallyConnect)
c.generateRelationshipGroupings(rType.professional, 3, numEmployers, numEmployees, ConnectionStrategy.randomlyConnect)
c.generateRelationshipGroupings(rType.social, 3, numSocialGroups, numSocialites, ConnectionStrategy.randomlyConnect)
# Generate non-plot families (wip)
#c.generateRelationshipGroupings(rType.familial, 1, (totalCharacters,totalCharacters), (1,1), ConnectionStrategy.totallyConnect)

c.createRelationshipEntities()

# Fill in remaining details
c.generateNonPlotFamilies()

# Print names
print("- Relationships -")
for char in c.characters:
    print(char.getFullName() + " [" + str(char.id) + "]")
    for relation in char.typesByRelation.keys():
        print("    - " + relation.getFullName() + " [" + str(relation.id) + "] " + "(" + str([x.type.name for x in char.typesByRelation[relation]]) + ")")
