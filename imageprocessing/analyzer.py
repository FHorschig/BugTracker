"""Provides a class that analyzes images for bugs."""

import cv2
import numpy


class Analyzer(object):
    """Provides methods to extract regions with bugs from images."""


    def __init__(self, annotator, iohelper):
        self.result = None

        self.__annotator = annotator
        self.__iohelper = iohelper


    def process(self, method):
        """Extracts features and stores findings into given annotator."""

        # image = cv2.imread(self.__iohelper.thumbnail())
        img_file = self.__iohelper.thumbnail()
        self.result = method.process(self.__annotator, img_file)


    def show_result(self):
        if self.result is None:
            return

        if isinstance(self.result, numpy.ndarray):
            cv2.imshow('Image', self.result)
            cv2.waitKey()

