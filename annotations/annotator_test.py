#pylint: disable=missing-docstring, invalid-name, R0904

import unittest
from annotator import Annotator
from helper.toolsprovider import ToolsProvider


class TestAnnotator(unittest.TestCase):
    def setUp(self):
        self.tools_provider = ToolsProvider()
        self.annotator = Annotator(self.tools_provider)


    def test_can_create(self):
        assert self.annotator


if __name__ == '__main__':
    unittest.main()
