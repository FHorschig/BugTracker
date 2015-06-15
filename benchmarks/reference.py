""" This class holds metadata about a Reference used for a Benchmark."""
# pylint: disable=E1101, W0141

import csv
import cv2
import os

from annotations.bug import Bug

class Reference(object):
    """ Holds data like count of bugs and checks if a bug is well encircled."""

    def __init__(self, folder, sample_name):
        self.__name = sample_name.strip('.ref')
        self.__folder = folder
        self.__bugs = self.__load_bugs()
        self.__true_positives = []
        self.__false_positives = []
        self.__false_negatives = []


    @staticmethod
    def load_from_folder(folder):
        """ Loads *.ref-Files within folder and returns Benchmark objects."""
        refs = []
        for input_file in os.listdir(folder):
            if input_file.endswith(".ref"):
                refs.append(Reference(folder, input_file))
        return refs


    def show_image(self):
        """ Were all relevant bugs found?"""
        img = cv2.imread(self.imagefile()).copy()
        Reference.__draw_bugs(img, self.__bugs, False, 1)
        Reference.__draw_bugs(img, self.__false_negatives, (0, 255, 0))
        Reference.__draw_bugs(img, self.__false_positives, (0, 0, 255))
        cv2.imshow('Image', img)
        cv2.waitKey()


    @staticmethod
    def __draw_bugs(image, bugs, color=(0, 0, 0), thickness=3):
        """ Draws the rectangles on the given image."""
        for bug in bugs:
            rect_p1 = (bug[0], bug[1])
            rect_p2 = (bug[2] + bug[0], bug[3] + bug[1])
            cv2.rectangle(image, rect_p1, rect_p2, color, thickness)

    def recall(self):
        """ Were all relevant bugs found?"""
        tpos, fneg = len(self.__true_positives), len(self.__false_negatives)
        return float(tpos) / (tpos + fneg)


    def precision(self):
        """ Which found bugs were relevant?"""
        tpos, fpos = len(self.__true_positives), len(self.__false_positives)
        return float(tpos) / (tpos + fpos)


    def compare_with(self, bugs):
        """ Which found bugs were relevant?"""
        self.__true_positives = []
        self.__false_positives = []
        self.__false_negatives = []
        for bug in bugs:
            if Reference.__has_similar_rect(bug.bounds(), self.__bugs):
                self.__true_positives.append(bug.bounds())
            else:
                self.__false_positives.append(bug.bounds())

        for bug in self.__bugs:
            if not Reference.__has_similar_rect(bug, self.__true_positives):
                self.__false_negatives.append(bug)


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
                bugs.append(tuple(map(int, line)))
        return bugs

    @staticmethod
    def __has_similar_rect(rect, rect_list):
        """ Returns true if the list contains a similar rect. """
        for ref in rect_list:
            if Reference.__is_similar(ref, rect):
                return True
        return False


    @staticmethod
    def __is_similar(rect, another):
        """ Returns true if the rects are of similar size and position. """
        x_tolerance = 0.1 * max(rect[2], another[2])
        y_tolerance = 0.1 * max(rect[3], another[3])
        return  abs(rect[0] - another[0]) < x_tolerance and \
                abs(rect[1] - another[1]) < y_tolerance
