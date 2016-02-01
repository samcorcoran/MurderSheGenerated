__author__ = 'Sam'

import unittest
import random

import cast
from cast import ConnectionStrategy
from relationships import RelationshipType
from relationships import Family

class TestCast(unittest.TestCase):

    def setUp(self):
        self.c = cast.Cast()
        self.totalMembers = 5
        # Add characters
        for x in range(self.totalMembers):
            self.c.addCharacter()

    def test_non_empty(self):
        self.assertTrue(len(self.c.characters) > 0)

    def test_gathering_all_candidates(self):
        maxAllowed = -1
        # Assert all cast members are candidates
        self.assertEqual(len(self.c.gatherCandidates(RelationshipType.familial, maxAllowed)), self.totalMembers)

    def test_connecting_all_candidates(self):
        # Send entire cast of characters for total connection
        self.c.connectCandidates(self.c.characters, ConnectionStrategy.totallyConnect, RelationshipType.familial)
        for charA in self.c.characters:
            # Assert relations total to same as sum of all other cast members
            self.assertEqual(charA.getTotalRelations(), len(self.c.characters)-1)
            # Assert character has enough relationships for there to be one for every other cast member
            self.assertEqual(charA.getTotalRelationships(), len(self.c.characters)-1)
            # Assert there are no duplicates in relations or relationships
            self.assertEqual(len(charA.getAllRelations()), len(set(charA.getAllRelations())))
            self.assertEqual(len(charA.getAllRelationships()), len(set(charA.getAllRelationships())))

    def create_all_family_relations(self):
        numFamilies = (1,1)
        numFamilyMembers = (self.totalMembers, self.totalMembers*2)
        self.c.generateRelationshipGroupings(RelationshipType.familial,
                                             1,
                                             numFamilies,
                                             numFamilyMembers,
                                             ConnectionStrategy.totallyConnect)

    def test_dfs_gathering_all(self):
        # Ensure all characters are related by family
        self.create_all_family_relations()
        # Gather all connected family members of a random starting character
        startingMembers = list()
        leaves = self.c.gatherConnectedRelTypeMembersDepthFirst(random.choice(self.c.characters),
                                                                  RelationshipType.familial,
                                                                  startingMembers,
                                                                  maxMembers = -1)
        # Assert all characters are included in gathered set
        self.assertEqual(len(leaves), len(self.c.characters))

    def test_all_joining_entity(self):
        newFamily = self.c.createEntity(RelationshipType.familial)
        for char in self.c.characters:
            char.joinEntity(newFamily)
        self.assertEqual(len(self.c.characters), len(newFamily.members))
        self.assertEqual(len(self.c.entities), 1)