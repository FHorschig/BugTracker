#!/usr/bin/python2
#pylint: disable=missing-docstring, W0403, F0401
import os
import argparse
import imageprocessing as ip
from annotations.annotator import Annotator
from helper.iohelper import IOHelper


DIR = os.path.dirname(os.path.realpath(__file__))

DEFAULT_OUTPUT_DIR = os.path.join(DIR, 'out')
DEFAULT_CACHE_DIR = os.path.join(DIR, 'cache')
DEFAULT_METHOD = 'TEMPLATE'
DEFAULT_TEMPLATE = os.path.join(DIR, \
    'testing/test_cache_dont_delete/hesp_template.jpg')


def get_arg_parser():
    """Returns the parser for all valid arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry_run', action='store_true',
                        help='Avoids IO and downloads.')
    parser.add_argument('--test', action='store_true',
                        help='Execute all tests and exit')
    parser.add_argument('-b', '--benchmark', action='store_true',
                        help='Executes the benchmarks for the chosen method.')
    parser.add_argument('-s', '--show_intermediates', action='store_true',
                        help='Shows pictures of benchmarks and debug images.')
    parser.add_argument('-q', '--no_qr', action='store_true',
                        help='Avoids slow analysis of QR codes.')
    parser.add_argument('-c', '--cache_directory',
                        help='The directory where temporary files are stored.',
                        metavar='')
    parser.add_argument('-o', '--output_directory',
                        help='The directory where  annotations are stored.',
                        metavar='')
    parser.add_argument('-f', '--file', help='Process file or URL.')
    parser.add_argument('-m', '--method', help='Define the method to use. [' +
                        " | ".join(ip.METHODS.keys()) + ']')
    parser.add_argument('-t', '--template',
                        help='Template file for Template Matching algorithms.')
    return parser

def get_args():
    """Parses options using argparse and returns them."""
    return get_arg_parser().parse_args()


def configure_iohelper(args):
    """ Creates and sets up an IOHelper according to parsed args."""
    iohelper = IOHelper()
    if args.dry_run:
        iohelper.set_dry_run(True)
    iohelper.set_cache_directory(
        os.path.join(DIR, args.cache_directory) if args.cache_directory
        else DEFAULT_CACHE_DIR)
    iohelper.set_output_directory(
        os.path.join(DIR, args.output_directory) if args.output_directory
        else DEFAULT_OUTPUT_DIR)
    iohelper.select_file(args.file)
    iohelper.select_template(
        args.template if args.template
        else DEFAULT_TEMPLATE)
    return iohelper


def exit_on_test_initiation(args):
    """ Dispatches testing in case of present test flag."""
    if not args.test:
        return
    from bugtracker_test import execute_all_tests
    execute_all_tests()
    exit(0)


def exit_on_benchmark_initiation(args, method=DEFAULT_METHOD):
    """ Dispatches testing in case of present test flag."""
    if not args.benchmark:
        return
    from benchmarks import benchmarks
    benchmarks.execute_all(method, args.template, args.show_intermediates)
    exit(0)


def select_method(args):
    """ Parses the args for the matching method the user chose."""
    if not args.method:
        return ip.METHODS[DEFAULT_METHOD]
    if not args.method in ip.METHODS:
        print "No valid method! Possible ones:" + ", ".join(ip.METHODS.keys())
        exit(0)
    return ip.METHODS[args.method]


def main(args):
    """Function that gets called on execution."""
    exit_on_test_initiation(args)

    method = select_method(args)
    exit_on_benchmark_initiation(args, method)
    iohelper = configure_iohelper(args)
    annotator = Annotator(iohelper)
    analyzer = ip.Analyzer(annotator, iohelper)


    if not args.no_qr:
        analyzer.process(ip.METHODS["QRCODE"]())
    analyzer.process(method())

    if args.dry_run:
        exit(0)

    analyzer.show_result()
    exit(0)


if __name__ == '__main__':
    main(get_args())
