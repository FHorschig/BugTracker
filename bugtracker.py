#!/usr/bin/python2
#pylint: disable=missing-docstring, W0403, F0401
import os
import argparse
import imageprocessing as ip
from annotations.annotator import Annotator
from helper.toolsprovider import ToolsProvider


DIR = os.path.dirname(os.path.realpath(__file__))

DEFAULT_OUTPUT_DIR = os.path.join(DIR, 'out')
DEFAULT_WORKING_DIR = os.path.join(DIR, 'out')
DEFAULT_TOOLS_DIR = '~/opencv'


def get_arg_parser():
    """Returns the parser for all valid arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry_run', action='store_true', help='Avoids IO.')
    parser.add_argument('-t', '--test', action='store_true',
                        help='Execute all tests and exit')
    parser.add_argument('-w', '--working_directory',
                        help='The directory where temporary files are stored.',
                        metavar='')
    parser.add_argument('-o', '--output_directory',
                        help='The directory where  annotations are stored.',
                        metavar='')
    parser.add_argument('--tools_directory',
                        help='The directory where tools are located.',
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

    tools_provider = ToolsProvider()
    tools_provider.set_working_directory(
        os.path.join(DIR, args.working_directory) if args.working_directory
        else DEFAULT_WORKING_DIR)
    tools_provider.set_output_directory(
        os.path.join(DIR, args.output_directory) if args.output_directory
        else DEFAULT_OUTPUT_DIR)
    tools_provider.set_tools_directory(
        os.path.join(DIR, args.tools_directory) if args.tools_directory
        else DEFAULT_TOOLS_DIR)

    annotator = Annotator(tools_provider)

    analyzer = ip.Analyzer(annotator)
    method = ip.Thresholding()
    # method = ip.TemplateMatching()
    # method = ip.TemplateMatchingWithThresholding()
    file = os.path.join(DIR, args.FILE)

    analyzer.process(file, method)
    annotator.save_as_turtle()


if __name__ == '__main__':
    main(get_args())
