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


def main(args):
    """Function that get called on execution."""
    if args.dry_run:
        exit(0)

    if args.test:
        from bugtracker_test import execute_all_tests
        execute_all_tests()
        exit(0)

    iohelper = IOHelper()
    iohelper.set_cache_directory(
        os.path.join(DIR, args.cache_directory) if args.cache_directory
        else DEFAULT_CACHE_DIR)
    iohelper.set_output_directory(
        os.path.join(DIR, args.output_directory) if args.output_directory
        else DEFAULT_OUTPUT_DIR)
    iohelper.select_file(args.file)

    annotator = Annotator(iohelper)

    analyzer = ip.Analyzer(annotator, iohelper)
    method = ip.Thresholding()
    # method = ip.TemplateMatching()
    # method = ip.TemplateMatchingWithThresholding()

    analyzer.process(method)
    annotator.save_as_turtle()


if __name__ == '__main__':
    main(get_args())
