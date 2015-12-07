import random

from cast import Cast, ConnectionStrategy
from relationships import RelationshipType
from characters import Character, Gender

def generateMystery(characters):
    out = ""

    # Create graph
    c = Cast()

    # Add characters
    if characters is not None:
        totalCharacters = characters
    else:
        totalCharacters = random.randint(4, 15)
    [c.addCharacter() for x in range(totalCharacters)]
    out += "\nTOTAL CHARACTERS: %d" % len(c.characters)

    # GENERATE FAMILIAL RELATIONSHIP NETWORK
    numFamilies = (int(totalCharacters/6), int(totalCharacters/3))
    numFamilyMembers = (max(2, int(totalCharacters/6)), int(totalCharacters/3))
    if (numFamilies[1] * numFamilyMembers[1] > totalCharacters):
        out += "\n" + "WARNING: May have too few characters for max possible families and members"
    out += "\n" + "Family parameters: number" + str(numFamilies) + ", size" + str(numFamilyMembers)

    # GENERATE ROMANTIC RELATIONSHIP NETWORK
    numRomances = int(0.5 * totalCharacters)

    # GENERATE PROFESSIONAL RELATIONSHIP NETWORK
    numEmployers = (int(totalCharacters/6), int(totalCharacters/3))
    numEmployees = (max(2, int(totalCharacters/6)), int(totalCharacters/3))
    if (numEmployers[1] * numEmployees[1] > totalCharacters):
        out += "\n" + "WARNING: May have too few characters for max possible professional relationships"
    out += "\n" + "Professional parameters: number" + str(numEmployers) + ", size" + str(numEmployees)

    # GENERATE SOCIAL RELATIONSHIP NETWORK
    numSocialGroups = (int(totalCharacters/6), int(totalCharacters/3))
    numSocialites = (max(2, int(totalCharacters/6)), int(totalCharacters/3))
    if (numSocialGroups[1] * numSocialites[1] > totalCharacters):
        out += "\n" + "WARNING: May have too few characters for max possible social relationships"
    out += "\n" + "Social parameters: number" + str(numSocialGroups) + ", size" + str(numSocialites)

    # Create typed relationships between characters
    c.generateRelationshipGroupings(RelationshipType.familial, 1, numFamilies, numFamilyMembers, ConnectionStrategy.totallyConnect)
    c.generateRelationshipGroupings(RelationshipType.romantic, -1, (numRomances, numRomances), (2,2), ConnectionStrategy.totallyConnect)
    c.generateRelationshipGroupings(RelationshipType.professional, 3, numEmployers, numEmployees, ConnectionStrategy.randomlyConnect)
    c.generateRelationshipGroupings(RelationshipType.social, 3, numSocialGroups, numSocialites, ConnectionStrategy.randomlyConnect)

    # Create entities and make characters members of them
    maxFamilyMembers = (max(2, int(totalCharacters/6)), int(totalCharacters/3))
    # If familial relations can belong to different families (married off) then random.randint(min(*maxFamilyMembers), maxFamilyMembers[1]) could be used
    # If familial relations must all belong t same family, then -1 should be used, for infinite depth
    c.createTypedEntities(RelationshipType.familial, -1, strategy="bfs")
    maxCompanyMembers = (max(2, int(totalCharacters/6)), int(totalCharacters/3))
    c.createTypedEntities(RelationshipType.professional, random.randint(min(*maxCompanyMembers), maxCompanyMembers[1]), strategy="bfs")
    maxSocialGroupMembers = (max(2, int(totalCharacters/6)), int(totalCharacters/3))
    c.createTypedEntities(RelationshipType.social, random.randint(min(*maxSocialGroupMembers), maxSocialGroupMembers[1]), strategy="bfs")

    # Fill in remaining details
    c.createIsolatedTypedEntities(RelationshipType.familial)

    return (c, out)

if __name__ == '__main__':
    generateMystery();
