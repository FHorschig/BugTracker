#pylint: disable=missing-docstring, invalid-name, R0904

import unittest
from .toolsprovider import ToolsProvider


class TestToolsProvider(unittest.TestCase):
    def setUp(self):
        self.provider = ToolsProvider()


    def test_can_create(self):
        assert self.provider


if __name__ == '__main__':
    unittest.main()
