"""Provides a function that runs all known tests."""

import unittest


from annotations.annotator_test import TestAnnotator
from annotations.bug_test import TestBug
from imageprocessing.analyzer_test import TestAnalyzer
from helper.toolsprovider_test import TestToolsProvider
from bugtracker import main


class TestBugTracker(unittest.TestCase):
    def test_executes_without_error(self):
        main([])
        assert True


def execute_all_tests():
    """Runs all known tests."""
    unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(TestBugTracker),
        unittest.TestLoader().loadTestsFromTestCase(TestBug),
        unittest.TestLoader().loadTestsFromTestCase(TestAnnotator),
        unittest.TestLoader().loadTestsFromTestCase(TestAnalyzer),
        unittest.TestLoader().loadTestsFromTestCase(TestToolsProvider)]))


if __name__ == '__main__':
    execute_all_tests()
