import cv2
import numpy as np

class TemplateMatching(object):

    def process(self, img):
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
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 1)
            
        return img_rgb