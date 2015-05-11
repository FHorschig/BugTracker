#pylint: disable=missing-docstring, invalid-name, R0904, W0403, F0401
import unittest
from analyzer import Analyzer
from annotations.annotator import Annotator
from helper.iohelper import IOHelper

class TestAnalyzer(unittest.TestCase):
    def setUp(self):
        self.iohelper = IOHelper()
        self.annotator = Annotator(self.iohelper)
        self.analyzer = Analyzer(self.annotator, self.iohelper)


    def test_can_create(self):
        assert self.analyzer


if __name__ == '__main__':
    unittest.main()
