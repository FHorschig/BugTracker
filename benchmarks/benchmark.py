""" A benchmark class that executes a benchmark for a given method."""
# pylint: disable=F0401


from annotations.annotator import Annotator
from reference import Reference
from helper.iohelper import IOHelper
from imageprocessing.analyzer import Analyzer

class Benchmark(object):
    """Method in, statistics out."""

    OUTPUT_DIR = 'benchmarks/out'
    REFERENCES = 'benchmarks/references'


    def __init__(self, method, template):
        self.__method = method
        self.__iohelper = IOHelper()
        self.__iohelper.set_cache_directory(Benchmark.REFERENCES)
        self.__iohelper.set_output_directory(Benchmark.OUTPUT_DIR)
        if template:
            self.__iohelper.select_template(template)
        self.__annotator = Annotator(self.__iohelper)
        self.__analyzer = Analyzer(self.__annotator, self.__iohelper)
        self.__precision = None
        self.__recall = None
        self.__references = Reference.load_from_folder(Benchmark.REFERENCES)


    def execute_all(self):
        """ Executes the Method against all stored reference files."""
        recalls = 0
        precs = 0
        for reference in self.__references:
            self.__iohelper.select_file(reference.imagefile())
            self.__analyzer.process(self.__method)
            recalls = recalls + reference.recall_for(self.__annotator.bugs())
            precs = precs + reference.precision_for(self.__annotator.bugs())
        self.__recall = recalls / len(self.__references)
        self.__precision = precs / len(self.__references)


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
