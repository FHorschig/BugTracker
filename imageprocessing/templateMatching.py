import cv2
import numpy as np

from random import randint

from annotations.bug import Bug
from imageprocessing.thresholding import Thresholding

from skimage.feature import hog
from skimage import data, color, exposure

from matplotlib import pyplot as plt


class Framegroup(object):

    def __init__(self):
        self.left, self.right, self.top, self.bottom, self.width, self.height = 0.0,0.0,0.0,0.0,0.0,0.0
        self.show_point = (0,0)
        self.show_value = 0

    def add(self, point, width, height, value):
        if self.show_value < value*0.8:
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

        return (intersectionWidth>width/2 or intersectionWidth>self.width/2) and (intersectionHeight>height/2 or intersectionHeight>self.height/2)


class TemplateMatching(object):

    def __init__(self):
        # self.multiscalefactors = [0.5, 0.9, 1.0, 1.2, 1.5]
        # self.multiscalefactors = [0.7, 1.0, 1.3]
        self.multiscalefactors = [1.0]

    def process(self, annotator, io_helper):
        img = cv2.imread(io_helper.thumbnail())

        methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

        img_bgr = img.copy()
        
        bgMax = [0]*3
        for i,col in enumerate(('b','g','r')):
            histr = cv2.calcHist([img_bgr],[i],None,[256],[0,256])
            maxVal = 0
            for index, value in enumerate(histr):
                if index>100 and value[0] > maxVal:
                    maxVal = value[0]
                    bgMax[i] = index

        bgRange = [(i-25, i+25) for i in bgMax]

        img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        img_gray_scikit = color.rgb2gray(img_rgb)
        # template = cv2.imread(io_helper.template(),0)
        thresh = Thresholding()
        template_bgr = thresh.extractTemplate(img)
        template_rgb = cv2.cvtColor(template_bgr, cv2.COLOR_BGR2RGB)
        template_gray = cv2.cvtColor(template_bgr, cv2.COLOR_BGR2GRAY)
        template_gray_scikit = color.rgb2gray(template_rgb)
        # cv2.imshow('Image', template_bgr)
        # cv2.waitKey()

        fd_tmp, _ = hog(template_gray_scikit, orientations=8, pixels_per_cell=(8, 8), cells_per_block=(1, 1), visualise=True)
        fd_tmp = fd_tmp / np.linalg.norm(fd_tmp)

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
                for framegroup_index in range(len(frame_groups)-1,-1,-1):
                    if frame_groups[framegroup_index].is_member(p, scaledW, scaledH):
                        if (group_found):
                            group_found.add(frame_groups[framegroup_index].show_point, frame_groups[framegroup_index].width, frame_groups[framegroup_index].height, frame_groups[framegroup_index].show_value)
                            del(frame_groups[framegroup_index])
                        else:
                            frame_groups[framegroup_index].add(p, scaledW, scaledH, res[p[1], p[0]])
                            group_found = frame_groups[framegroup_index]
                if not group_found:
                    new_frame_group = Framegroup()
                    new_frame_group.add(p, scaledW, scaledH, res[p[1], p[0]])
                    frame_groups.append(new_frame_group)

        pow_diff = lambda x,y : np.power(x-y, 2)

        final_frame_groups = []

        for frame_group in frame_groups:
            roi = img_gray_scikit[frame_group.top:frame_group.bottom , frame_group.left:frame_group.right]
            roi2 = img_bgr[frame_group.top:frame_group.bottom , frame_group.left:frame_group.right]

            roi = cv2.resize(roi, (w, h))
            fd, _ = hog(roi, orientations=8, pixels_per_cell=(8, 8), cells_per_block=(1, 1), visualise=True)
            fd = fd / np.linalg.norm(fd)

            res = np.sqrt(sum(map(pow_diff, fd, fd_tmp)))
            
            bgAvg = [0]*3
            for i,col in enumerate(('b','g','r')):
                histr = cv2.calcHist([roi2],[i],None,[256],[0,256])
                summ = 0
                for index, value in enumerate(histr):
                    bgAvg[i] += value[0]*index
                    summ += value[0]
                bgAvg[i] /= summ
            isBackGround = True
            for i in range(3):
                if not (bgRange[i][0] <= bgAvg[i] <= bgRange[i][1]):
                    isBackGround = False
                    break

            if res < 0.95 and not isBackGround:
                final_frame_groups.append(frame_group)

            # cv2.imshow('Image', roi)
            # cv2.waitKey()

        for frame_group in final_frame_groups:
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
