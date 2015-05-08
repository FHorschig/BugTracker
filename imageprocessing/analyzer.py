"""Provides a class that analyzes images for bugs."""

import cv2
import numpy as np


class Analyzer(object):
    """Provides methods to extract regions with bugs from images."""


    def __init__(self, annotator):
        self.__annotator = annotator


    def process(self, file):
        """Extracts features and stores findings into given annotator."""

        image = cv2.imread(file)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray_blur = cv2.GaussianBlur(gray, (15, 15), 0)
        thresh = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 1)

        kernel = np.ones((3, 3), np.uint8)
        closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

        cont_img = closing.copy()
        contours, hierarchy = cv2.findContours(cont_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


        i = 0
        for cnt in contours:

            area = cv2.contourArea(cnt)
            if area < 500 or area > 4000:
                continue

            if len(cnt) < 5:
                continue

            # ellipse = cv2.fitEllipse(cnt)
            # cv2.ellipse(image, ellipse, (0,255,0), 2)

            for point in cnt:
                cv2.circle(image, tuple(point[0]), 2, (255-i,(120+i)%255,i))

            i = (i + 30) % 255


        # cv2.imshow('Image', gray_blur)
        # cv2.imshow('Image', thresh)
        # cv2.imshow('Image', closing)
        # cv2.imshow('Image', cont_img)
        cv2.imshow('Image', image)
        cv2.waitKey()
