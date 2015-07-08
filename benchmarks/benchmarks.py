""" Provides benchmarking methods. """

from benchmark import Benchmark

def execute_all(method, template, show_images):
    """ Start a benchmark for the given method for every avaiable file. """
    benchmark = Benchmark(method(), template)
    benchmark.execute_all(show_images)
    print "Recall: " + str(benchmark.recall())
    print "Precision: " + str(benchmark.precision())
    print "F-Measure: " + str(benchmark.fmeasure())
