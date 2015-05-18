#pylint: disable=missing-docstring, invalid-name, R0904, W0403, F0401

import unittest
from bug import Bug
from testing.testfiles import TestFiles

class TestBug(unittest.TestCase):

    def setUp(self):
        self.bug = Bug(TestFiles.IMG, TestFiles.BOUNDING_BOX)


    def test_includes_organism_into_turtle(self):
        self.assertEqual(self.bug.as_turtle(), TestFiles.RDF_SINGLE_BUG)


if __name__ == '__main__':
    unittest.main()
