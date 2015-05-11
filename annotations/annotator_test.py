#pylint: disable=missing-docstring, invalid-name, R0904, W0403, F0401

import unittest
from annotator import Annotator
from bug import Bug
from helper.toolsprovider import ToolsProvider


class TestAnnotator(unittest.TestCase):
    BUG = Bug("bug.jpg", 100, 10, 30, 50)
    PREFIXES = "@prefix dwc: <http://rs.tdwg.org/dwc/terms/#> .\n"

    def setUp(self):
        self.tools_provider = ToolsProvider()
        self.annotator = Annotator(self.tools_provider)


    def test_can_create(self):
        assert self.annotator


    def test_creates_prefixes_without_information(self):
        self.assertEqual( \
            self.annotator.save_as_turtle(as_string=True), \
            TestAnnotator.PREFIXES)


    def test_includes_added_organism_into_turtle(self):
        self.annotator.add_bug(TestAnnotator.BUG)
        self.assertEqual(self.annotator.save_as_turtle(as_string=True), \
            TestAnnotator.PREFIXES + \
            TestAnnotator.BUG.as_turtle())


if __name__ == '__main__':
    unittest.main()
