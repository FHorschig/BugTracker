"""Provides a class that analyzes images for bugs."""

import cv2


class Analyzer(object):
    """Provides methods to extract regions with bugs from images."""


    def __init__(self, annotator):
        self.__annotator = annotator


    def process(self, file, method):
        """Extracts features and stores findings into given annotator."""

        image = cv2.imread(file)
        result = method.process(self.__annotator, image)

        cv2.imshow('Image', result)
        cv2.waitKey()

