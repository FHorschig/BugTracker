""" Provides benchmarking methods. """

from benchmark import Benchmark

def execute_all(method, template):
    """ Start a benchmark for the given method for every avaiable file. """
    benchmark = Benchmark(method(), template)
    benchmark.execute_all(show_images=False)
    print "Recall: " + str(benchmark.recall())
    print "Precision: " + str(benchmark.precision())
    print "F-Measure: " + str(benchmark.fmeasure())
