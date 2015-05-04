#pylint: disable=missing-docstring, invalid-name, R0904

import unittest
from annotator import Annotator
from helper.toolsprovider import ToolsProvider


class TestAnnotator(unittest.TestCase):
    TEST_IMG = "http://gbif.naturkundemuseum-berlin.de/hackathon/Thumbs/" + \
               "mfnb_col_buprestidae_julodinae_d011.jpg"

    def setUp(self):
        self.tools_provider = ToolsProvider()
        self.annotator = Annotator(self.tools_provider)


    def test_can_create(self):
        assert self.annotator


    def disabled_test_creates_empty_string_without_information(self):
        assert self.annotator.save_as_turtle() == ""


    def test_includes_organism_into_turtle(self):
        img = TestAnnotator.TEST_IMG
        self.annotator.add_found_bug(img, 100, 10, 30, 50)
        self.assertEqual(self.annotator.save_as_turtle(), \
            "@prefix dwc: <http://rs.tdwg.org/dwc/terms/#> .\n" + \
            "<" + img + "#x=100&y=10&w=30&h=50> a dwc:Organism .")


if __name__ == '__main__':
    unittest.main()
