""" A benchmark class that executes a benchmark for a given method."""
from imageprocessing.analyzer import Analyzer
from annotations.annotator import Annotator
from helper.iohelper import IOHelper

class Benchmark(object):
    """Method in, statistics out."""

    OUTPUT_DIR = 'benchmarks/out'
    CACHE_DIR = 'benchmarks/cache'
    REFERENCES = 'benchmarks/references'

    def __init__(self, method, template):
        self.__method = method
        self.__iohelper = IOHelper()
        self.__iohelper.set_cache_directory(Benchmark.CACHE_DIR)
        self.__iohelper.set_output_directory(Benchmark.OUTPUT_DIR)
        if template:
            self.__iohelper.select_template(template)
        self.__annotator = Annotator(self.__iohelper)
        self.__analyzer = Analyzer(self.__annotator, self.__iohelper)
        self.__precision = None
        self.__recall = None


    def execute_all(self):
        """ Executes the Method against all stored reference files."""
        # TODO(fhorschig): Get actual reference files.
        # TODO(fhorschig): Compute precision.
        # TODO(fhorschig): Compute recall.
        for input_file in []:
            self.__iohelper.select_file(input_file)
            self.__analyzer.process(self.__method)
            # self.__annotator has a lot of data now. Use it!


    def recall(self):
        """ Returns how many objects were found."""
        return self.__recall


    def precision(self):
        """ Returns how many of the found objects were actually correct."""
        return self.__precision


    def fmeasure(self, precision_weight=1):
        """ Returns a harmonic mean of precision and recall."""
        weight = precision_weight * precision_weight
        return (1 + weight) * self.__precision * self.__recall / \
                (weight * self.__precision + self.__recall)
