#pylint: disable=missing-docstring, invalid-name, R0904

import unittest
from os import path
from shutil import rmtree

from .toolsprovider import ToolsProvider


class TestToolsProvider(unittest.TestCase):
    TEST_DIR = ".test"
    TEST_OUT = ".test/out.rdf"

    def setUp(self):
        rmtree(TestToolsProvider.TEST_DIR, ignore_errors=True)
        self.provider = ToolsProvider()


    def tearDown(self):
        rmtree(TestToolsProvider.TEST_DIR, ignore_errors=True)


    def test_can_create(self):
        assert self.provider


    def test_returns_valid_out_path(self):
        self.provider.set_output_directory(TestToolsProvider.TEST_DIR)
        assert path.exists(self.provider.output_dir())


    def test_returns_valid_work_path(self):
        self.provider.set_working_directory(TestToolsProvider.TEST_DIR)
        assert path.exists(self.provider.output_dir())


    def test_writes_to_default_out_file(self):
        self.provider.set_output_directory(TestToolsProvider.TEST_DIR)
        self.provider.write_out("")
        assert path.exists(TestToolsProvider.TEST_OUT)


if __name__ == '__main__':
    unittest.main()
