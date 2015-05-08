#!/usr/bin/python2

import os
import argparse
import imageprocessing as ip
from annotations.annotator import Annotator
from helper.toolsprovider import ToolsProvider


DIR = os.path.dirname(os.path.realpath(__file__))

DEFAULT_OUTPUT_DIR = os.path.join(DIR, 'out')
DEFAULT_WORKING_DIR = os.path.join(DIR, 'out')
DEFAULT_TOOLS_DIR = '~/opencv'


def get_args():
    """Parses options using argparse and returns them."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', action='store_true', help='Execute all tests and exit')
    parser.add_argument('-w', '--working_directory', help='The directory where temporary files are stored', metavar='')
    parser.add_argument('-o', '--output_directory', help='The directory where the annotation files should be stored', metavar='')
    parser.add_argument('--tools_directory', help='The directory where tools like openCV are located', metavar='')
    parser.add_argument('FILE', help='Process file')
    args = parser.parse_args()

    return args


def main():
    args = get_args()

    if args.test:
        from bugtracker_test import execute_all_tests
        execute_all_tests()
        exit(0)

    tools_provider = ToolsProvider()
    tools_provider.set_working_directory(os.path.join(DIR, args.working_directory) if args.working_directory else DEFAULT_WORKING_DIR)
    tools_provider.set_output_directory(os.path.join(DIR, args.output_directory) if args.output_directory else DEFAULT_OUTPUT_DIR)
    tools_provider.set_tools_directory(os.path.join(DIR, args.tools_directory) if args.tools_directory else DEFAULT_TOOLS_DIR)

    annotator = Annotator(tools_provider)

    analyzer = ip.Analyzer(annotator)
    # method = ip.Thresholding()
    method = ip.TemplateMatching()
    # method = ip.TemplateMatchingWithThresholding()
    file = os.path.join(DIR, args.FILE)

    analyzer.process(file, method)
    annotator.save_as_turtle()


if __name__ == '__main__':
    main()
