""" Provides benchmarking methods. """

from benchmark import Benchmark

def execute_all(method, template):
    """ Start a benchmark for the given method for every avaiable file. """
    benchmark = Benchmark(method(), template)
    benchmark.execute_all()
