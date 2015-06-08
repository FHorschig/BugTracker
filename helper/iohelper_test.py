#pylint: disable=missing-docstring, invalid-name, R0904, F0401

import unittest
from os import path
from shutil import rmtree

from .iohelper import IOHelper
from testing.testfiles import TestFiles


class TestIOHelper(unittest.TestCase):
    TEST_DIR = ".test-folder-that-shouldnt-exist-very-long"
    TEST_FILENAME = "strange_name_for_a_test_file.jpg"
    TEST_OUT = TEST_DIR + "/" + TEST_FILENAME + ".rdf"


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
        assert path.exists(self.iohelper.cache_dir())


    def test_writes_to_default_out_file(self):
        self.iohelper.set_output_directory(TestIOHelper.TEST_DIR)
        self.iohelper.select_file(TestIOHelper.TEST_FILENAME)
        self.iohelper.write_out()
        assert path.exists(TestIOHelper.TEST_OUT)


    def test_doesnt_write_on_dry_run(self):
        self.iohelper.set_output_directory(TestIOHelper.TEST_DIR)
        self.iohelper.set_dry_run(True)
        self.iohelper.select_file(TestIOHelper.TEST_FILENAME)
        self.iohelper.write_out()
        assert not path.exists(TestIOHelper.TEST_OUT)


    def test_first_file_selection(self):
        self.iohelper = TestFiles.make_io_helper()
        self.iohelper.select_file(None, (lambda echo: "1")) # user choice nr. 1
        self.assertEqual(self.iohelper.image(), TestFiles.IMG_PATH)


if __name__ == '__main__':
    unittest.main()
