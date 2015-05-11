import cv2
import numpy as np
from annotations.bug import Bug

class TemplateMatching(object):

    def process(self, annotator, img):
        methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']


        img_rgb = img.copy()
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('hesp_template.jpg',0)

        w, h = template.shape[::-1]

        res = cv2.matchTemplate(img_gray, template, eval(methods[1]))

        threshold = 0.4
        loc = np.where( res >= threshold)

        for pt in zip(*loc[::-1]):
            annotator.add_bug(pt[0], pt[1], w, h)
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 1)

        return img_rgb


class TemplateMatchingWithThresholding(object):

    def process(self, annotator, img):
        image = img.copy()

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray_blur = cv2.GaussianBlur(gray, (15, 15), 0)
        thresh = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 1)

        kernel = np.ones((3, 3), np.uint8)
        closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=3)

        methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']



        template = cv2.imread('hesp_template.jpg', 0)
        template_gray_blur = cv2.GaussianBlur(template, (15, 15), 0)
        template_thresh = cv2.adaptiveThreshold(template_gray_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 1)

        w, h = template.shape[::-1]

        res = cv2.matchTemplate(closing, template_thresh, eval(methods[1]))

        threshold = 0.3
        loc = np.where( res >= threshold)

        for pt in zip(*loc[::-1]):
            annotator.add_bug(pt[0], pt[1], w, h)
            cv2.rectangle(image, pt, (pt[0] + w, pt[1] + h), (0,0,255), 1)


        # cv2.imshow('Image', closing)
        # cv2.waitKey()

        return image
