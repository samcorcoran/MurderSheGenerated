
import cast
from relationships import relType as rType
from cast import ConnectionStrategy
from characters import character

# Create graph
c = cast.cast()
# Add characters
#totalCharacters = random.randint(4, 15)
totalCharacters = 4
print("TOTAL CHARACTERS: " + str(totalCharacters))
for n in range(totalCharacters):
    c.addCharacter(character())

# GENERATE FAMILIAL RELATIONSHIP NETWORK
numFamilies = (2,3)#(2, 4)
numFamilyMembers = (3,3)#(2, 5)
if (numFamilies[1] * numFamilyMembers[1] > totalCharacters):
    print("WARNING: May have too few characters for max possible families and members")
print("Family parameters: number" + str(numFamilies) + ", size" + str(numFamilyMembers))
#c.generatePlotFamilies(numFamilies, numFamilyMembers)

# GENERATE ROMANTIC RELATIONSHIP NETWORK
numRomances = int(0.5 * totalCharacters)
#c.generateRomanticEntanglements(numRomances)

c.generateRelationshipGroupings(rType.familial, 1, numFamilies, numFamilyMembers, ConnectionStrategy.totallyConnect)
#c.generateRelationshipGroupings(rType.romantic, -1, (numRomances, numRomances), (2,2), ConnectionStrategy.totallyConnect)

c.createRelationshipEntities()

# Fill in remaining details
c.generateNonPlotFamilies()

# Print names
print("- Relationships -")
for char in c.characters:
    print(char.getFullName() + " [" + str(char.id) + "]")
    for relation in char.typesByRelation.keys():
        print("    - " + relation.getFullName() + " [" + str(relation.id) + "] " + "(" + str([x.type.name for x in char.typesByRelation[relation]]) + ")")
