#pylint: disable=missing-docstring, invalid-name, R0904

import unittest
from bug import Bug


class TestBug(unittest.TestCase):
    TEST_IMG = "http://gbif.naturkundemuseum-berlin.de/hackathon/Thumbs/" + \
               "mfnb_col_buprestidae_julodinae_d011.jpg"

    def setUp(self):
        self.bug = Bug(TestBug.TEST_IMG, 100, 10, 30, 50)


    def test_includes_organism_into_turtle(self):
        self.assertEqual(self.bug.as_turtle(), \
            "<" + TestBug.TEST_IMG + "#x=100&y=10&w=30&h=50> a dwc:Organism .")


if __name__ == '__main__':
    unittest.main()
