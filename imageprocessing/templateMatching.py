import cv2
import numpy as np
from random import randint
from annotations.bug import Bug

class Framegroup(object):

    def __init__(self, width, height, res):
        self.width = width
        self.height = height
        self.left, self.right, self.top, self.bottom = 0.0,0.0,0.0,0.0
        self.frames = []
        self.values = res
        self.show_frame = (0,0)
        self.show_value = 0

    def add(self, frame):
        self.frames.append(frame)
        if self.show_value < self.values[frame[1], frame[0]]:
            self.show_frame = frame
            self.show_value = self.values[frame[1], frame[0]]
            self.left = frame[0]
            self.right = frame[0]+self.width
            self.top = frame[1]
            self.bottom = frame[1]+self.height

    def is_member(self, frame):
        dX = min(self.right, frame[0]+self.width) - max(self.left, frame[0])
        if dX < 0:
            return False

        dY = min(self.bottom, frame[1]+self.height) - max(self.top, frame[1])
        if dY < 0:
            return False

        return dX>self.width/4 and dY>self.height/4


class TemplateMatching(object):

    def process(self, annotator, io_helper):
        img = cv2.imread(io_helper.thumbnail())

        methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

        img_rgb = img.copy()
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(io_helper.template(),0)

        w, h = template.shape[::-1]

        res = cv2.matchTemplate(img_gray, template, eval(methods[1]))

        threshold = 0.4
        loc = np.where(res >= threshold)

        frame_groups = []
        points = zip(*loc[::-1])

        for p in points:
            group_found = False
            for frame_group in frame_groups:
                if frame_group.is_member(p):
                    frame_group.add(p)
                    group_found = True
                    break
            if not group_found:
                new_frame_group = Framegroup(w, h, res)
                new_frame_group.add(p)
                frame_groups.append(new_frame_group)

        for i in range(len(frame_groups)-1,-1,-1):
            for j in range(i-1,-1,-1):
                if frame_groups[j].is_member(frame_groups[i].show_frame):
                    for frame in frame_groups[i].frames:
                        frame_groups[j].add(frame)
                    del(frame_groups[i])
                    break

        for frame_group in frame_groups:
            frame = frame_group.show_frame
            annotator.add_bug(frame[0], frame[1], w, h)
            cv2.rectangle(img_rgb, frame, (frame[0] + w, frame[1] + h), (0,0,255), 1)

        return img_rgb


class TemplateMatchingWithThresholding(object):

    def process(self, annotator, img_file):
        img = cv2.imread(img_file)
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
