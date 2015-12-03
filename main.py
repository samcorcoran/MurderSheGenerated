import random

import cast
from relationships import relType as rType
from cast import ConnectionStrategy
from characters import character
from characters import gender

def generateMystery():
    out = ""

    # Create graph
    c = cast.cast()
    # Add characters
    totalCharacters = random.randint(4, 15)

    characterGenders = [gender.getRandomGender() for x in range(totalCharacters)]
    out += "\n" + "TOTAL CHARACTERS: " + str(totalCharacters)
    for charGender in characterGenders:
        c.addCharacter(character(charGender))

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
    c.generateRelationshipGroupings(rType.familial, 1, numFamilies, numFamilyMembers, ConnectionStrategy.totallyConnect)
    c.generateRelationshipGroupings(rType.romantic, -1, (numRomances, numRomances), (2,2), ConnectionStrategy.totallyConnect)
    c.generateRelationshipGroupings(rType.professional, 3, numEmployers, numEmployees, ConnectionStrategy.randomlyConnect)
    c.generateRelationshipGroupings(rType.social, 3, numSocialGroups, numSocialites, ConnectionStrategy.randomlyConnect)

    # Create entities and make characters members of them
    maxFamilyMembers = (max(2, int(totalCharacters/6)), int(totalCharacters/3))
    # If familial relations can belong to different families (married off) then random.randint(min(*maxFamilyMembers), maxFamilyMembers[1]) could be used
    # If familial relations must all belong t same family, then -1 should be used, for infinite depth
    c.createTypedEntities(rType.familial, -1, strategy="bfs")
    maxCompanyMembers = (max(2, int(totalCharacters/6)), int(totalCharacters/3))
    c.createTypedEntities(rType.professional, random.randint(min(*maxCompanyMembers), maxCompanyMembers[1]), strategy="bfs")
    maxSocialGroupMembers = (max(2, int(totalCharacters/6)), int(totalCharacters/3))
    c.createTypedEntities(rType.social, random.randint(min(*maxSocialGroupMembers), maxSocialGroupMembers[1]), strategy="bfs")

    # Fill in remaining details
    c.createIsolatedTypedEntities(rType.familial)

    # Print names
    out += "\n" + "- Relationships -"
    for char in c.characters:
        out += "\n" + char.getFullName() + " [" + str(char.id) + "]"
        for relation in char.typesByRelation.keys():
            out += "\n" + "    - " + relation.getFullName() + " [" + str(relation.id) + "] " + "(" + str([x.type.name for x in char.typesByRelation[relation]]) + ")"

    return out


if __name__ == '__main__':
    generateMystery();
