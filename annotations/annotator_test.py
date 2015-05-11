#pylint: disable=missing-docstring, invalid-name, R0904, W0403, F0401

import unittest
from annotator import Annotator
from bug import Bug
from helper.iohelper import IOHelper


class TestAnnotator(unittest.TestCase):
    BUG_BOUNDING_BOX = (100, 10, 30, 50)
    PREFIXES = "@prefix dwc: <http://rs.tdwg.org/dwc/terms/#> .\n" +\
               "@prefix img: <test.jpg> .\n"

    def setUp(self):
        self.iohelper = IOHelper()
        self.annotator = Annotator(self.iohelper)
        self.iohelper.select_file('test.jpg')


    def test_can_create(self):
        assert self.annotator


    def test_creates_prefixes_without_information(self):
        self.assertEqual( \
            self.annotator.save_as_turtle(as_string=True), \
            TestAnnotator.PREFIXES)


    def test_includes_added_organism_into_turtle(self):
        self.annotator.add_bug(*TestAnnotator.BUG_BOUNDING_BOX)
        self.assertEqual(self.annotator.save_as_turtle(as_string=True), \
            TestAnnotator.PREFIXES + \
            Bug('img', TestAnnotator.BUG_BOUNDING_BOX).as_turtle())


if __name__ == '__main__':
    unittest.main()
