import cv2
import numpy as np
from random import randint
from annotations.bug import Bug

class Framegroup(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.left, self.right, self.top, self.bottom = 0.0,0.0,0.0,0.0
        self.frames = []

    def add(self, frame):
        self.frames.append(frame)
        self.left = (self.left*(len(self.frames)-1)+frame[0])/len(self.frames)
        self.right = (self.right*(len(self.frames)-1)+frame[0]+self.width)/len(self.frames)
        self.top = (self.top*(len(self.frames)-1)+frame[1])/len(self.frames)
        self.bottom = (self.bottom*(len(self.frames)-1)+frame[1]+self.height)/len(self.frames)
        #if frame[0]<self.left:
        #    self.left = frame[0]
        #if frame[0]+self.width>self.right:
        #    self.right = frame[0]+self.width
        #if frame[1]<self.top:
        #    self.top = frame[1]
        #if frame[1]+self.height>self.bottom:
        #    self.bottom = frame[1]+self.height

    def is_member(self, frame):
        middle = [frame[0]+self.width/2, frame[1]+self.height/2]
        return middle[0]>self.left and middle[0]<self.right and middle[1]>self.top and middle[1]<self.bottom


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
        loc = np.where(res >= threshold)

        frame_groups = []
        points = zip(*loc[::-1])

        #while points:
        #    print len(points)
        #    frame_group = [points.pop()]
        #    frame_groups.append(frame_group)

        #    for frame in frame_group:
        #        for i in range(len(points)-1,-1,-1):
        #            if abs(points[i][0] - frame[0]) + abs(points[i][1] - frame[1]) <= 2:
        #                frame_group.append(points[i])
        #                del points[i]

        #frames = []
        #for frame_group in frame_groups:
        #    frames.append(tuple(np.mean(frame_group, axis=0, dtype=np.int32)))
        
        for p in points:
            group_found = False
            for frame_group in frame_groups:
                if frame_group.is_member(p):
                    frame_group.add(p)
                    group_found = True
                    break
            if not group_found:
                new_frame_group = Framegroup(w, h)
                new_frame_group.add(p)
                frame_groups.append(new_frame_group)

        frames = []
        for frame_group in frame_groups:
            best_frame = [0,0]
            best_value = 0
            for frame in frame_group.frames:
                if res[frame[1],frame[0]] > best_value:
                    best_value = res[frame[1],frame[0]]
                    best_frame = frame
            frames.append(best_frame)


        for pt in frames:
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
