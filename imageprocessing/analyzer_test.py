#pylint: disable=missing-docstring, invalid-name, R0904, W0403, F0401
import unittest
from analyzer import Analyzer
from annotations.annotator import Annotator
from helper.toolsprovider import ToolsProvider

class TestAnalyzer(unittest.TestCase):
    def setUp(self):
        self.tools_provider = ToolsProvider()
        self.annotator = Annotator(self.tools_provider)
        self.analyzer = Analyzer(self.annotator)


    def test_can_create(self):
        assert self.analyzer


if __name__ == '__main__':
    unittest.main()
