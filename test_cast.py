__author__ = 'Sam'

import unittest

import cast
from cast import ConnectionStrategy
from relationships import RelationshipType

class TestCast(unittest.TestCase):

    def setUp(self):
        self.c = cast.Cast()
        self.totalMembers = 1
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
