"""Provides a function that runs all known tests."""

import unittest


from annotations.annotator_test import TestAnnotator
from imageprocessing.analyzer_test import TestAnalyzer
from helper.toolsprovider_test import TestToolsProvider

def execute_all_tests():
    """Runs all known tests."""
    unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(TestAnnotator),
        unittest.TestLoader().loadTestsFromTestCase(TestAnalyzer),
        unittest.TestLoader().loadTestsFromTestCase(TestToolsProvider)]))


if __name__ == '__main__':
    execute_all_tests()
