""" This class holds metadata about a Reference used for a Benchmark."""
# pylint: disable=E1101, W0141

import csv
import cv2
import os

from annotations.bug import Bug

class Reference(object):
    """ Holds data like count of bugs and checks if a bug is well encircled."""

    TOLERANCE = 0.3  # Bounding boxes can be 30% bigger or smaller
    DIFF_OUT = 'diffs'

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
        """ Shows the diff between ideal and calculated bugs."""
        cv2.imshow('Image', self.__diff_image())
        cv2.waitKey()


    def store_image(self):
        """ Saves the diff between ideal and calculated bugs to a file."""
        cv2.imwrite(self.__diff_filename(), self.__diff_image())


    def __diff_filename(self):
        """ Creates a filename for the diff image."""
        diff_dir = os.path.join(self.__folder, Reference.DIFF_OUT)
        if not os.path.exists(diff_dir):
            os.makedirs(diff_dir)
        return os.path.join(diff_dir, self.__name  +'.jpg')


    def __diff_image(self):
        """ Creates diff between ideal and calculated bugs."""
        img = cv2.imread(self.imagefile()).copy()
        Reference.__draw_bugs(img, self.__true_positives, False, 1)
        Reference.__draw_bugs(img, self.__false_negatives, (0, 255, 0))
        Reference.__draw_bugs(img, self.__false_positives, (0, 0, 255))
        return img


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
        x_tolerance = Reference.TOLERANCE * max(rect[2], another[2])
        y_tolerance = Reference.TOLERANCE * max(rect[3], another[3])
        return  abs(rect[0] - another[0]) < x_tolerance and \
                abs(rect[1] - another[1]) < y_tolerance
