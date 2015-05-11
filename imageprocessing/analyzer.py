"""Provides a class that analyzes images for bugs."""

import cv2


class Analyzer(object):
    """Provides methods to extract regions with bugs from images."""


    def __init__(self, annotator, iohelper):
        self.__annotator = annotator
        self.__iohelper = iohelper


    def process(self, method):
        """Extracts features and stores findings into given annotator."""

        image = cv2.imread(self.__iohelper.thumbnail())
        result = method.process(self.__annotator, image)

        cv2.imshow('Image', result)
        cv2.waitKey()

