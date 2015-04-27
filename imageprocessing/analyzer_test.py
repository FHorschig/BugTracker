#pylint: disable=missing-docstring, invalid-name, R0904

import unittest
from .analyzer import Analyzer


class TestAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = Analyzer()


    def test_can_create(self):
        assert self.analyzer


if __name__ == '__main__':
    unittest.main()
