import cv2
import numpy as np

from random import randint

from annotations.bug import Bug
from imageprocessing.thresholding import Thresholding


class Framegroup(object):

    def __init__(self):
        self.left, self.right, self.top, self.bottom, self.width, self.height = 0.0,0.0,0.0,0.0,0.0,0.0
        self.show_point = (0,0)
        self.show_value = 0

    def add(self, point, width, height, value):
        if self.show_value < value:
            self.show_point = (point)
            self.show_value = value
            self.left = point[0]
            self.right = point[0]+width
            self.top = point[1]
            self.bottom = point[1]+height
            self.width = width
            self.height = height

    def is_member(self, point, width, height):
        intersectionWidth = min(self.right, point[0]+width) - max(self.left, point[0])
        if intersectionWidth < 0:
            return False

        intersectionHeight = min(self.bottom, point[1]+height) - max(self.top, point[1])
        if intersectionHeight < 0:
            return False

        return (intersectionWidth>width/3 or intersectionWidth>self.width/3) and (intersectionHeight>height/3 or intersectionHeight>self.height/3)


class TemplateMatching(object):

    def __init__(self):
        self.multiscale = False
        self.multiscalefactors = [0.5, 1.0, 1.5, 3.0]
        # self.multiscalefactors = [1.0]

    def process(self, annotator, io_helper):
        img = cv2.imread(io_helper.thumbnail())

        methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

        img_bgr = img.copy()
        img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        # template = cv2.imread(io_helper.template(),0)
        thresh = Thresholding()
        template_bgr = thresh.extractTemplate(img)
        template_gray = cv2.cvtColor(template_bgr, cv2.COLOR_BGR2GRAY)
        # cv2.imshow('Image', template_bgr)
        # cv2.waitKey()

        w, h = template_gray.shape[::-1]
        
        frame_groups = []
        for factor in self.multiscalefactors:
            scaledW = int(w * factor)
            scaledH = int(h * factor)

            scaledTemplate = cv2.resize(template_gray, (scaledW, scaledH))

            res = cv2.matchTemplate(img_gray, scaledTemplate, eval(methods[1]))

            threshold = 0.41
            loc = np.where(res >= threshold)

            points = zip(*loc[::-1])

            for p in points:
                group_found = False
                for frame_group in frame_groups:
                    if frame_group.is_member(p, scaledW, scaledH):
                        frame_group.add(p, scaledW, scaledH, res[p[1], p[0]])
                        group_found = True
                        break
                if not group_found:
                    new_frame_group = Framegroup()
                    new_frame_group.add(p, scaledW, scaledH, res[p[1], p[0]])
                    frame_groups.append(new_frame_group)

        # for i in range(len(frame_groups)-1,-1,-1):
        #     for j in range(i-1,-1,-1):
        #         if frame_groups[j].is_member(frame_groups[i].show_frame):
        #             for frame in frame_groups[i].frames:
        #                 frame_groups[j].add(frame)
        #             del(frame_groups[i])
        #             break

        for frame_group in frame_groups:
            point = frame_group.show_point
            annotator.add_bug(point[0], point[1], frame_group.width, frame_group.height)
            cv2.rectangle(img_bgr, point, (point[0] + frame_group.width, point[1] + frame_group.height), (0,0,255), 1)

        return img_bgr


class TemplateMatchingWithThresholding(object):

    def process(self, annotator, iohelper):
        img = cv2.imread(iohelper.thumbnail())
        image = img.copy()

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray_blur = cv2.GaussianBlur(gray, (15, 15), 0)
        thresh = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 1)

        kernel = np.ones((3, 3), np.uint8)
        closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=3)

        methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

        template = cv2.imread(iohelper.template(), 0)
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
