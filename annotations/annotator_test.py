#pylint: disable=missing-docstring, invalid-name, R0904, W0403, F0401

import unittest
from annotator import Annotator
from testing.testfiles import TestFiles


class TestAnnotator(unittest.TestCase):
    def setUp(self):
        self.annotator = Annotator(TestFiles.make_io_helper())


    def test_can_create(self):
        assert self.annotator


    def test_creates_prefixes_without_information(self):
        self.assertEqual(self.annotator.save_as_turtle(as_string=True), \
                         TestFiles.PREFIXES)


    def test_includes_added_organism_into_turtle(self):
        self.annotator.add_bug(*TestFiles.BOUNDING_BOX)
        self.assertEqual(self.annotator.save_as_turtle(as_string=True), \
                         TestFiles.make_rdf_file())


if __name__ == '__main__':
    unittest.main()
