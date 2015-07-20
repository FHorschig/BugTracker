import cv2
import numpy as np
import os
from annotations.bug import Bug
from imageprocessing.thresholding import Thresholding

import matplotlib.pyplot as plt

from skimage.feature import hog
from skimage import data, color, exposure
from sklearn import svm



class HogTemplateMatching(object):

    def process(self, annotator, io_helper):
        img_bgr = cv2.imread(io_helper.thumbnail())
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

        thresh = Thresholding()
        tmp_bgr = thresh.extractTemplate(img_bgr)
        tmp_rgb = cv2.cvtColor(tmp_bgr, cv2.COLOR_BGR2RGB)

        img_gray = color.rgb2gray(img_rgb)
        tmp_gray = color.rgb2gray(tmp_rgb)

        template_bgr = cv2.imread(io_helper.template())
        template_bgr = cv2.imread('templates/positives/buprestidae_julodinae.png')
        template_rgb = cv2.cvtColor(template_bgr, cv2.COLOR_BGR2RGB)
        template_gray = color.rgb2gray(template_rgb)

        height, width = template_bgr.shape[:2]
        img_gray = cv2.resize(img_gray, (width, height))
        tmp_gray = cv2.resize(tmp_gray, (width, height))

        positiveSamples = [tmp_bgr]
        negativeSamples = [cv2.imread('templates/negatives/' + image) for image in os.listdir('templates/negatives')]

        X = []
        y = [1] * len(positiveSamples) + [0] * len(negativeSamples)
        
        for sample_bgr in positiveSamples + negativeSamples:
            sample_rgb = cv2.cvtColor(sample_bgr, cv2.COLOR_BGR2RGB)
            sample_gray = color.rgb2gray(sample_rgb)
            sample = cv2.resize(sample_gray, (width, height))
            fd, _ = hog(sample, orientations=8, pixels_per_cell=(8, 8), cells_per_block=(1, 1), visualise=True)
            X.append(fd)

        clf = svm.SVC(kernel='linear', C = 1.0)
        clf.fit(X,y)

        fd_img, hog_img = hog(img_gray, orientations=8, pixels_per_cell=(8, 8), cells_per_block=(1, 1), visualise=True)
        fd_tmp, hog_tmp = hog(tmp_gray, orientations=8, pixels_per_cell=(8, 8), cells_per_block=(1, 1), visualise=True)
        fd_template, hog_template = hog(template_gray, orientations=8, pixels_per_cell=(8, 8), cells_per_block=(1, 1), visualise=True)

        print(clf.predict(fd_template))
        # print(clf.predict(fd_img))

        label_rgb = cv2.cvtColor(cv2.imread("templates/negatives/blue_label_template.jpg"), cv2.COLOR_BGR2RGB)
        label_rgb = cv2.resize(label_rgb, (width, height))
        label_gray = color.rgb2gray(label_rgb)
        fd_label, hog_label = hog(label_gray, orientations=8, pixels_per_cell=(8, 8), cells_per_block=(1, 1), visualise=True)

        pow_diff = lambda x,y : np.power(x-y, 2)
        
        fd_tmp = fd_tmp / np.linalg.norm(fd_tmp)
        fd_template = fd_template / np.linalg.norm(fd_template)
        fd_img = fd_img / np.linalg.norm(fd_img)
        fd_label = fd_label / np.linalg.norm(fd_label)

        dist_sme = np.sqrt(sum(map(pow_diff, fd_tmp, fd_tmp)))
        dist_tmp = np.sqrt(sum(map(pow_diff, fd_tmp, fd_template)))
        dist_img = np.sqrt(sum(map(pow_diff, fd_tmp, fd_img)))
        dist_lbl = np.sqrt(sum(map(pow_diff, fd_tmp, fd_label)))

        print dist_sme
        print dist_tmp
        print dist_img
        print dist_lbl

        # fd_tmp, hog_tmp = hog(img_gray, orientations=8, pixels_per_cell=(16, 16), cells_per_block=(1, 1), visualise=True)

        # fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
        # hog_template_rescaled = exposure.rescale_intensity(hog_template, in_range=(0, 0.02))

        # ax1.axis('off')
        # ax1.imshow(hog_template_rescaled, cmap=plt.cm.gray)
        # ax1.set_title('Input image')

        # Rescale histogram for better display
        # hog_img_rescaled = exposure.rescale_intensity(hog_img, in_range=(0, 0.02))
        # hog_tmp_rescaled = exposure.rescale_intensity(hog_tmp, in_range=(0, 0.02))

        # ax2.axis('off')
        # ax2.imshow(hog_tmp_rescaled, cmap=plt.cm.gray)
        # ax2.set_title('Histogram of Oriented Gradients')
        # plt.show()


        return img_bgr
