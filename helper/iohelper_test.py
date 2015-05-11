#pylint: disable=missing-docstring, invalid-name, R0904

import unittest
from os import path
from shutil import rmtree

from .iohelper import IOHelper


class TestIOHelper(unittest.TestCase):
    TEST_DIR = ".test"
    TEST_OUT = ".test/test.jpg.rdf"

    def setUp(self):
        rmtree(TestIOHelper.TEST_DIR, ignore_errors=True)
        self.iohelper = IOHelper()


    def tearDown(self):
        rmtree(TestIOHelper.TEST_DIR, ignore_errors=True)


    def test_can_create(self):
        assert self.iohelper


    def test_returns_valid_out_path(self):
        self.iohelper.set_output_directory(TestIOHelper.TEST_DIR)
        assert path.exists(self.iohelper.output_dir())


    def test_returns_valid_work_path(self):
        self.iohelper.set_cache_directory(TestIOHelper.TEST_DIR)
        assert path.exists(self.iohelper.output_dir())


    def test_writes_to_default_out_file(self):
        self.iohelper.set_output_directory(TestIOHelper.TEST_DIR)
        self.iohelper.select_file('test.jpg')
        self.iohelper.write_out("")
        assert path.exists(TestIOHelper.TEST_OUT)


if __name__ == '__main__':
    unittest.main()
