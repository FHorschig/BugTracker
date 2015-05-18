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


def get_arg_parser():
    """Returns the parser for all valid arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry_run', action='store_true', help='Avoids IO.')
    parser.add_argument('-t', '--test', action='store_true',
                        help='Execute all tests and exit')
    parser.add_argument('-c', '--cache_directory',
                        help='The directory where temporary files are stored.',
                        metavar='')
    parser.add_argument('-o', '--output_directory',
                        help='The directory where  annotations are stored.',
                        metavar='')
    parser.add_argument('-f', '--file', help='Process file')
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
    return iohelper


def main(args):
    """Function that get called on execution."""
    if args.test:
        from bugtracker_test import execute_all_tests
        execute_all_tests()
        exit(0)

    iohelper = configure_iohelper(args)
    annotator = Annotator(iohelper)

    analyzer = ip.Analyzer(annotator, iohelper)
    if args.dry_run:
        exit(0)
    analyzer.process(method=ip.Thresholding())
    # analyzer.process(method=ip.TemplateMatching())
    # analyzer.process(method=ip.TemplateMatchingWithThresholding())

    annotator.save_as_turtle()

    exit(0)


if __name__ == '__main__':
    main(get_args())
