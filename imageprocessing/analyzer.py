"""Provides a class that analyzes images for bugs."""

import cv2
import numpy


max_output_width = 1000
max_output_height = 760

class Analyzer(object):
    """Provides methods to extract regions with bugs from images."""

    def __init__(self, annotator, iohelper):
        self.__annotator = annotator
        self.__iohelper = iohelper

        self.result_image = None
        self.qr_codes = []


    def process(self, method):
        """Extracts features and stores findings into given annotator."""

        self.result_image = method.process(self.__annotator, self.__iohelper)


    def show_result(self):
        if self.result_image is None:
            return

        self.__annotator.save_as_turtle()

        if isinstance(self.result_image, numpy.ndarray):
            result_image = self.result_image
            
            height, width = result_image.shape[:2]
            if width > max_output_width or height > max_output_height:
                resize_factor = min(float(max_output_width) / width, float(max_output_height) / height)
                result_image = cv2.resize(result_image, (0, 0), fx=resize_factor, fy=resize_factor)

            print 'Displaying result image'

            cv2.imshow('Image', result_image)
            cv2.waitKey()
