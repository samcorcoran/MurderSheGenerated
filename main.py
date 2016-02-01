import json
import random

from cast import Cast, ConnectionStrategy
from relationships import RelationshipType
from characters import Character, Gender

def generateMystery(num_players = None, num_male = None, num_female = None):
    # Create graph
    c = Cast()

    # Add characters
    if num_players is not None:
        chars = [Gender.getRandomGender() for x in range(num_players)]
    elif num_male is not None and num_female is not None:
        chars = [Gender.male for x in range(num_male)] + [Gender.female for x in range(num_female)] + [Gender.getRandomGender()]
    else:
        chars = [Gender.getRandomGender() for x in range(random.randint(5, 15))]

    [c.addCharacter(gender=gender) for gender in chars]
    totalCharacters = len(chars)

    # GENERATE FAMILIAL RELATIONSHIP NETWORK
    numFamilies = [int(totalCharacters/6), int(totalCharacters/3)]
    numFamilyMembers = [max(2, int(totalCharacters/6)), int(totalCharacters/3)]
    if (numFamilies[1] * numFamilyMembers[1] > totalCharacters):
        print("WARNING: May have too few characters for max possible families and members")
    print("Family parameters: number {0}, size {1}".format(numFamilies, numFamilyMembers))

    # GENERATE ROMANTIC RELATIONSHIP NETWORK
    numRomances = int(0.5 * totalCharacters)

    # GENERATE PROFESSIONAL RELATIONSHIP NETWORK
    numEmployers = [int(totalCharacters/6), int(totalCharacters/3)]
    numEmployees = [max(2, int(totalCharacters/6)), int(totalCharacters/3)]
    if (numEmployers[1] * numEmployees[1] > totalCharacters):
        print("WARNING: May have too few characters for max possible professional relationships")
    print("Professional parameters: number {0}, size {1}".format(numEmployers, numEmployees))

    # GENERATE SOCIAL RELATIONSHIP NETWORK
    numSocialGroups = [int(totalCharacters/6), int(totalCharacters/3)]
    numSocialites = [max(2, int(totalCharacters/6)), int(totalCharacters/3)]
    if (numSocialGroups[1] * numSocialites[1] > totalCharacters):
        print("WARNING: May have too few characters for max possible social relationships")
    print("Social parameters: number {0}, size {1}".format(numSocialGroups, numSocialites))

    # Create typed relationships between characters
    c.generateRelationshipGroupings(RelationshipType.familial, 1, numFamilies, numFamilyMembers, ConnectionStrategy.totallyConnect)
    c.generateRelationshipGroupings(RelationshipType.romantic, -1, (numRomances, numRomances), (2,2), ConnectionStrategy.totallyConnect)
    c.generateRelationshipGroupings(RelationshipType.professional, 3, numEmployers, numEmployees, ConnectionStrategy.randomlyConnect)
    c.generateRelationshipGroupings(RelationshipType.social, 3, numSocialGroups, numSocialites, ConnectionStrategy.randomlyConnect)

    # Create entities and make characters members of them
    maxFamilyMembers = (max(2, int(totalCharacters/6)), int(totalCharacters/3))
    # If familial relations can belong to different families (married off) then random.randint(min(*maxFamilyMembers), maxFamilyMembers[1]) could be used
    # If familial relations must all belong t same family, then -1 should be used, for infinite depth
    c.createTypedEntitiesForRelationships(RelationshipType.familial, -1, strategy="bfs")
    maxCompanyMembers = (max(2, int(totalCharacters/6)), int(totalCharacters/3))
    c.createTypedEntitiesForRelationships(RelationshipType.professional, random.randint(*sorted(maxCompanyMembers)), strategy="bfs")
    maxSocialGroupMembers = (max(2, int(totalCharacters/6)), int(totalCharacters/3))
    c.createTypedEntitiesForRelationships(RelationshipType.social, random.randint(*sorted(maxSocialGroupMembers)), strategy="bfs")

    # Fill in remaining details
    c.createIsolatedTypedEntities(RelationshipType.familial)

    title = c.generateTitle()
    location = c.generateLocation()
    scene = c.generateScene(location)

    return (c, title, location, scene)

if __name__ == '__main__':
    cast, title, location, scene = generateMystery()
    print(
        json.dumps({
            "cast": cast.toDict(),
            "title": title,
            "location": location,
            "scene": scene
            })
        )
    cast.printDiagnostic()
