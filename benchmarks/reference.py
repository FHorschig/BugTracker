""" This class holds metadata about a Reference used for a Benchmark."""
# pylint: disable=

import csv
import os

class Reference(object):
    """ Holds data like count of bugs and checks if a bug is well encircled."""

    def __init__(self, folder, sample_name):
        self.__name = sample_name.strip('.ref')
        self.__folder = folder
        self.__bugs = self.__load_bugs()


    @staticmethod
    def load_from_folder(folder):
        """ Loads *.ref-Files within folder and returns Benchmark objects."""
        refs = []
        for input_file in os.listdir(folder):
            if input_file.endswith(".ref"):
                refs.append(Reference(folder, input_file))
        return refs


    def recall_for(self, bugs):
        """ Were all relevant bugs found?"""
        return 0.123  # TODO(fhorschig): Implement.


    def precision_for(self, bugs):
        """ Which found bugs were relevant?"""
        return 0.321  # TODO(fhorschig): Implement.


    def reffile(self):
        """ Returns complete path to reference file."""
        return os.path.join(self.__folder, self.__name + '.ref')


    def imagefile(self):
        """ Returns complete path to reference file."""
        return os.path.join(self.__folder, self.__name + '.jpg')


    def __load_bugs(self):
        """ Loads the positions where bugs where found. """
        bugs = []
        with open(self.reffile(), 'rb') as reffile:
            reader = csv.reader(reffile, delimiter=';', quotechar='\n')
            for line in reader:
                bugs.append(line)
        return bugs
