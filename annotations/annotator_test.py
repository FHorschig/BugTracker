#pylint: disable=missing-docstring, invalid-name, R0904

import unittest
from .annotator import Annotator


class TestAnnotator(unittest.TestCase):
    def setUp(self):
        self.annotator = Annotator()


    def test_can_create(self):
        assert self.annotator


if __name__ == '__main__':
    unittest.main()
