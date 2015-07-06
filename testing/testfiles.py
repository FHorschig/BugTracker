#pylint: disable=F0401
""" Simple collection of test constants and freuquently used test methods. The
Objects created in here (for example IOHelper) won't use internet connection."""

class TestFiles(object):
    """Provides methods to create test objects."""

    OUT_DIR = "./testing/out/"
    CACHE_DIR = "./testing/test_cache_dont_delete/"

    IMG_NAME = "MFNB_Col_Buprestidae_Julodinae_D011.jpg"
    IMG = "http://gbif.naturkundemuseum-berlin.de/hackathon/Thumbs/" + IMG_NAME
    IMG_PATH = CACHE_DIR + IMG_NAME

    TEMPLATE = CACHE_DIR + 'hesp_template.jpg'

    RDF_SINGLE_BUG = "\n<" + IMG + "#x=0.5&y=0.5&w=0.5&h=0.25> a dwc:Organism ."
    PREFIXES = "@prefix dwc: <http://rs.tdwg.org/dwc/terms/#> .\n" +\
               "@prefix img: <" + IMG + "> .\n"

    BOUNDING_BOX = (81, 100, 81, 50)
    RELATIVE_BOUNDING_BOX = (0.5, 0.5, 0.5, 0.25)

    def __init__(self):
        self.__uri = None


    @staticmethod
    def make_bug():
        """ Returns a test bug."""
        from annotations.bug import Bug
        return Bug('img', TestFiles.RELATIVE_BOUNDING_BOX)


    @staticmethod
    def make_rdf_file():
        """ Returns a test bug."""
        return TestFiles.PREFIXES + TestFiles.make_bug().as_turtle()


    @staticmethod
    def make_io_helper():
        """ Returns a helper that points to a filled cache of small files."""
        from helper.iohelper import IOHelper

        iohelper = IOHelper(True)
        iohelper.set_output_directory(TestFiles.OUT_DIR)
        TestFiles.check_test_path_exists(iohelper.output_dir())

        iohelper.set_dry_run(True) # The following paths should already exist.

        iohelper.set_cache_directory(TestFiles.CACHE_DIR)
        TestFiles.check_test_path_exists(iohelper.cache_dir())
        iohelper.select_file(TestFiles.IMG)
        TestFiles.check_test_path_exists(iohelper.thumbnail())
        TestFiles.check_test_path_exists(iohelper.image())

        return iohelper

    @staticmethod
    def check_test_path_exists(filepath):
        """ Asserts the existence of paths that are required for testing."""
        from os import path
        if not path.exists(filepath):
            print "The path " + filepath + " has to be accessed for tests."
            assert False

