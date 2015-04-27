#!/usr/bin/python2
"""This script parses command line flags to easily use the pgpimporter class."""

import getopt
from sys import argv
from imageprocessing.analyzer import Analyzer
from annotations.annotator import Annotator
from helper.toolsprovider import ToolsProvider


DEFAULT_OUTPUT_DIR = "/out"
DEFAULT_WORKING_DIR = "/out"
DEFAULT_TOOLS_DIR = "~/opencv"


def get_options():
    """Parses options using getopt and returns them if no error occured."""
    options = None
    try:
        options, _ = getopt.getopt(argv[1:], "f:hw:o:ht:", [
            "file=", "help", "working_directory=", "output_directory=",
            "tools_directory=", "test"])
    except getopt.GetoptError:
        print "ERROR: Unknown flags! Use python " + argv[0] + " -h for options."
        exit(1)

    return options


def check_options_for_tests(options):
    """Checks if the --test flag is present and executes tests in this case."""
    for opt, _ in options:
        if opt in ("-t", "--test"):
            from bugtracker_test import execute_all_tests
            execute_all_tests()
            exit(0)


def check_directory_options(tools_provider, options):
    """Checks additional flags and sets working and out directories."""
    working_dir_set = out_dir_set = tools_dir_set = False
    for opt, arg in options:
        if opt in ("-w", "--working_directory"):
            tools_provider.set_working_directory(arg)
            working_dir_set = True
        elif opt in ("-o", "--output_directory"):
            tools_provider.set_output_directory(arg)
            out_dir_set = True
        elif opt == "--tools_directory":
            tools_provider.set_tools_directory(arg)
            tools_dir_set = True

    if not working_dir_set:
        tools_provider.set_working_directory(DEFAULT_WORKING_DIR)
    if not out_dir_set:
        tools_provider.set_output_directory(DEFAULT_OUTPUT_DIR)
    if not tools_dir_set:
        tools_provider.set_tools_directory(DEFAULT_TOOLS_DIR)
    tools_provider.enforce_directories()


def configure_annotator(annotator, options):
    """Set up annotator according to flags."""
    for opt, arg in options:
        if opt in ("-f", "--file"):
            annotator.process_file(arg)
            exit(0)
        elif opt in ("-h", "--help"):
            usage(argv)


def configure_analyzer(analyzer, options):
    """Set up analyzer according to flags."""


def usage(args):
    """Prints all possible flags if the user didn't pass useful ones."""
    print "usage: python " + args[0] + " [options] [-f <file>" | \
           " --test] [-o <output-directory>] [-w working-directory>]"
    print "   -f --file <filename in working-dir>  "\
           "Process the given file within the working directory."
    print "\n"
    print "   -w --working_directory <working-dir> "\
           "The directory where temporary files are stored."
    print "   -o --output_directory <dir>          "\
           "The directory where the annotation files should be stored to."
    print "   --tools_directory <dir>              "\
           "The directory where tools like openCV are located."
    print "\n"
    print "   -h --help                            "\
           "Displays this message."
    print "\n"
    print "   --test                               "\
          "Executes all tests. Works offline and without DB."\
          " Ignores other options."
    print "   --no_log                               "\
          "Doesn't print anything to std out."
    exit()


def main(options):
    """Parses user inputs and passes them to an PGP importer."""
    check_options_for_tests(options)

    tools_provider = ToolsProvider()
    check_directory_options(tools_provider, options)
    annotator = Annotator(tools_provider)
    configure_annotator(annotator, options)
    analyzer = Analyzer(tools_provider, annotator)
    configure_analyzer(analyzer, options)

    analyzer.start_processing()
    annotator.save_as_turtle()


if __name__ == '__main__':
    main(get_options())
