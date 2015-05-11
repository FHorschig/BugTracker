#pylint: disable=missing-docstring, invalid-name, R0904, W0403, F0401
"""Provides a function that runs all known tests."""

import unittest

from bugtracker import main
from bugtracker import get_arg_parser
from annotations.annotator_test import TestAnnotator
from annotations.bug_test import TestBug
from imageprocessing.analyzer_test import TestAnalyzer
from helper.iohelper_test import TestIOHelper


class TestBugTracker(unittest.TestCase):
    def test_exits_normally_on_dry_run(self):
        with self.assertRaises(SystemExit):
            main(get_arg_parser().parse_args(["--dry_run"]))


def execute_all_tests():
    """Runs all known tests."""
    unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(TestBugTracker),
        unittest.TestLoader().loadTestsFromTestCase(TestBug),
        unittest.TestLoader().loadTestsFromTestCase(TestAnnotator),
        unittest.TestLoader().loadTestsFromTestCase(TestAnalyzer),
        unittest.TestLoader().loadTestsFromTestCase(TestIOHelper)]))


if __name__ == '__main__':
    execute_all_tests()
