import cv2
import numpy as np
import os
from annotations.bug import Bug



class Thresholding(object):

    def process(self, annotator, iohelper):
        img = cv2.imread(iohelper.thumbnail())
        image = img.copy()

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray_blur = cv2.GaussianBlur(gray, (9, 9), 0)
        thresh = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 31, 11)

        kernel = np.ones((3, 3), np.uint8)
        closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

        cont_img = closing.copy()
        if int(cv2.__version__[0]) < 3:
            contours, _ = cv2.findContours(\
                    cont_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        else:
            _, contours, _ = cv2.findContours(\
                    cont_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)



        i = 0
        for cnt in contours:

            area = cv2.contourArea(cnt)
            # if area < 500 or area > 4000:
            #     continue

            #if len(cnt) < 50:
            #    continue

            ellipse = cv2.fitEllipse(cnt)
            # cv2.ellipse(image, ellipse, (0,255,0), 2)
            center, axes, angle = ellipse
            rect_area = axes[0] * axes[1]
            rect = np.round(np.float64(cv2.cv.BoxPoints(ellipse))).astype(np.int64)

            # rect = cv2.boundingRect(cnt)

            annotator.add_bug(*rect)
            # for point in cnt:
            #     cv2.circle(image, tuple(point[0]), 2, (255-i,(120+i)%255,i))

            color = (255,0,0)

            # cv2.rectangle(image, (rect[0], rect[1]), (rect[2], rect[3]), (0,255,0))

            cv2.drawContours(image, [rect], 0, color, 1)

            i = (i + 30) % 255



        # cv2.imshow('Image', gray)
        # cv2.waitKey()
        # cv2.imshow('Image', gray_blur)
        # cv2.waitKey()
        # cv2.imshow('Image', thresh)
        # cv2.waitKey()
        # cv2.imshow('Image', closing)
        # cv2.waitKey()
        # cv2.imshow('Image', cont_img)
        # cv2.waitKey()
        return image

    def removeLabelContours(self, contours, image):
        result = []
        blue_label_template = cv2.imread("templates/negatives/blue_label_template.jpg")
        template_h, template_w = blue_label_template.shape[:2]

        for cnt in contours:
            x,y,w,h = cv2.boundingRect(cnt)
            roi = image[y:y+h , x:x+w]
            roi_h, roi_w = roi.shape[:2]

            new_size = (max(roi_w, template_w), max(roi_h, template_h))

            resized_roi = cv2.resize(roi, new_size)
            resized_template = cv2.resize(blue_label_template, new_size)

            value = cv2.matchTemplate(resized_roi, resized_template, cv2.TM_CCOEFF_NORMED)

            if value < 0.2:
                result.append(cnt)

        return result

    def removeExtremes(self, contours, iterations, dev):
        ret = contours
        
        for i in range(iterations):
            # print len(ret)
            contouravg = sum([cv2.contourArea(cnt) for cnt in ret]) / len(ret)
            newContours = []
            for cnt in ret:
                area = cv2.contourArea(cnt)
                deviation = contouravg / dev
                if area < contouravg - deviation or area > contouravg + deviation:
                    continue
                newContours.append(cnt)
            ret = newContours

        return ret


    def showContourRects(self, image, contours):
        img = image.copy()
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < 5:
                continue
            # ellipse = cv2.fitEllipse(cnt)
            # center, axes, angle = ellipse
            # rect_area = axes[0] * axes[1]
            # rect = np.round(np.float64(cv2.cv.BoxPoints(ellipse))).astype(np.int64)
            color = (255,0,0)

            x,y,w,h = cv2.boundingRect(cnt)

            cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)
            # cv2.drawContours(img, [rect], 0, color, 2)
        cv2.imshow('Image', img)
        cv2.waitKey()


    def showContourBubbles(self, image, contours):
        img = image.copy()
        i = 0
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < 5:
                continue
            for point in cnt:
                cv2.circle(img, tuple(point[0]), 2, (255-i,(120+i)%255,i))
            color = (255,0,0)
            i = (i + 30) % 255
        cv2.imshow('Image', img)
        cv2.waitKey()


    def extractTemplate(self, img):
        image = img.copy()
        # cv2.imshow('Image', image)
        # cv2.waitKey()

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray_blur = cv2.GaussianBlur(gray, (9, 9), 0)
        thresh = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 31, 11)

        kernel = np.ones((3, 3), np.uint8)
        closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

        cont_img = closing.copy()
        if int(cv2.__version__[0]) < 3:
            contours, _ = cv2.findContours(\
                    cont_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        else:
            _, contours, _ = cv2.findContours(\
                    cont_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        ## cut edges away if only found one contour around the box
        cont_img = closing.copy()
        while len(contours) <= 2:
            height, width = cont_img.shape[:2]
            newHeight = height - height/20
            newWidth = width - width/20
            cont_img = cont_img[0:newHeight, 0:newWidth]
            copy = cont_img.copy()
            if int(cv2.__version__[0]) < 3:
                contours, _ = cv2.findContours(\
                        copy, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            else:
                _, contours, _ = cv2.findContours(\
                        copy, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # cv2.imshow('Image', thresh)
        # cv2.waitKey()
        # cv2.imshow('Image', closing)
        # cv2.waitKey()
        # cv2.imshow('Image', cont_img)
        # cv2.waitKey()
        # self.showContourBubbles(image, contours)
        # self.showContourRects(image, contours)


        contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 50]

        # self.showContourRects(image, contours)

        contours = self.removeLabelContours(contours, image)

        # self.showContourRects(image, contours)


        tenpercent = len(contours)/20

        contours.sort(key=lambda x: max([p[0][0] for p in x])-min([p[0][0] for p in x]))
        contours = contours[tenpercent:len(contours)-tenpercent]

        # self.showContourRects(image, contours)

        contours.sort(key=lambda x: max([p[0][1] for p in x])-min([p[0][1] for p in x]))
        contours = contours[tenpercent:len(contours)-tenpercent]



        # self.showContourRects(image, contours)

        contours = self.removeExtremes(contours, 1, 1.5)

        # self.showContourRects(image, contours)


        templates = []
        max_height = -1
        max_width = -1

        for cnt in contours:
            x,y,w,h = cv2.boundingRect(cnt)
            roi = image[y:y+h , x:x+w]
            height, width = roi.shape[:2]
            templates.append(roi)
            max_height = max(max_height, height)
            max_width = max(max_width, width)


        negativeSamples = [cv2.imread('templates/negatives/' + image) for image in os.listdir('templates/negatives')]
        positiveSamples = [cv2.imread('templates/positives/' + image) for image in os.listdir('templates/positives')]

        # templates.extend(positiveSamples)

        resized_templates = []
        for tmp in templates:
            resized_templates.append(cv2.resize(tmp, (max_width, max_height)))

        resized_positives = []
        for tmp in positiveSamples:
            resized_positives.append(cv2.resize(tmp, (max_width, max_height)))

        resized_negatives = []
        for tmp in negativeSamples:
            resized_negatives.append(cv2.resize(tmp, (max_width, max_height)))

        match_values = [0] * len(resized_templates)
        for i in range(len(resized_templates)):
            for j in range(i):#+1, len(resized_templates)):
                im1 = resized_templates[i]
                im2 = resized_templates[j]

                res = cv2.matchTemplate(im1, im2, cv2.TM_CCOEFF_NORMED)

                match_values[i] += res[0][0]
                match_values[j] += res[0][0]
        
        for i in range(len(resized_templates)):
            for j in range(len(resized_positives)):
                im1 = resized_templates[i]
                im2 = resized_positives[j]

                res = cv2.matchTemplate(im1, im2, cv2.TM_CCOEFF_NORMED)

                match_values[i] += res[0][0]

        for i in range(len(resized_templates)):
            for j in range(len(resized_negatives)):
                im1 = resized_templates[i]
                im2 = resized_negatives[j]

                res = cv2.matchTemplate(im1, im2, cv2.TM_CCOEFF_NORMED)

                match_values[i] -= res[0][0]
            

        best_template_index = match_values.index(max(match_values))
        # cv2.imshow('Image', templates[best_template_index])
        # cv2.waitKey()

        return templates[best_template_index]
