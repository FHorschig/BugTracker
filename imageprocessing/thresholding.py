import cv2
import numpy as np
import os
from annotations.bug import Bug



class Thresholding(object):
    """Uses thresholding and contour detection to segment given image."""

    def process(self, annotator, iohelper):
        img = cv2.imread(iohelper.thumbnail())
        image = img.copy()

        # Preprocessing like gray-scaling, thresholding, closing
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray_blur = cv2.GaussianBlur(gray, (9, 9), 0)
        thresh = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 31, 11)
        kernel = np.ones((3, 3), np.uint8)
        closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

        # Contour detection
        cont_img = closing.copy()
        if int(cv2.__version__[0]) < 3:
            contours, _ = cv2.findContours(\
                    cont_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        else:
            _, contours, _ = cv2.findContours(\
                    cont_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw rectangles and add found bug to annotator.
        i = 0
        for cnt in contours:
            area = cv2.contourArea(cnt)
            ellipse = cv2.fitEllipse(cnt)
            center, axes, angle = ellipse
            rect_area = axes[0] * axes[1]
            rect = np.round(np.float64(cv2.cv.BoxPoints(ellipse))).astype(np.int64)
            annotator.add_bug(*rect)
            color = (255,0,0)
            cv2.drawContours(image, [rect], 0, color, 1)
            i = (i + 30) % 255

        return image

    # Approach to remove blue label-like segments from a set of contours
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

    # Remove contours which deviate in size a lot from the average contour size
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

    # Debug output
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


    # Debug output
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

    # Method to extract a suitable template from an image, which represents the occuring insect species in that image
    def extractTemplate(self, img, demo):
        image = img.copy()
        if demo:
            cv2.imshow('Image', image)
            cv2.waitKey()

        # Preprocessing like gray-scaling, thresholding, closing
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray_blur = cv2.GaussianBlur(gray, (9, 9), 0)
        thresh = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 31, 11)
        kernel = np.ones((3, 3), np.uint8)
        closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

        # Contour detection
        cont_img = closing.copy()
        if int(cv2.__version__[0]) < 3:
            contours, _ = cv2.findContours(\
                    cont_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        else:
            _, contours, _ = cv2.findContours(\
                    cont_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Cut edges away if only found one contour around the box
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

        if demo:
            cv2.imshow('Image', thresh)
            cv2.waitKey()
            cv2.imshow('Image', closing)
            cv2.waitKey()
        # self.showContourBubbles(image, contours)
        # self.showContourRects(image, contours)

        if demo:
            self.showContourRects(image, contours)

        # Reduce the number of possible templates in multiple steps:

        # 1. Remove all contours that are VERY small
        contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 50]
        # 2. Try to remove blue labels
        contours = self.removeLabelContours(contours, image)

        # 3. Cut away edge-cases in width and height
        tenpercent = len(contours)/20
        contours.sort(key=lambda x: max([p[0][0] for p in x])-min([p[0][0] for p in x]))
        contours = contours[tenpercent:len(contours)-tenpercent]
        contours.sort(key=lambda x: max([p[0][1] for p in x])-min([p[0][1] for p in x]))
        contours = contours[tenpercent:len(contours)-tenpercent]

        # 4. Remove contours that are far away from average size
        contours = self.removeExtremes(contours, 5, 2)

        if demo:
            self.showContourRects(image, contours)

        # Prepare template matching of contours with each other
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

        # Add mannually cropped-out templates to improve the scores
        negativeSamples = [cv2.imread('templates/negatives/' + image) for image in os.listdir('templates/negatives')]
        positiveSamples = [cv2.imread('templates/positives/' + image) for image in os.listdir('templates/positives')]
        resized_templates = []
        for tmp in templates:
            resized_templates.append(cv2.resize(tmp, (max_width, max_height)))
        resized_positives = []
        for tmp in positiveSamples:
            resized_positives.append(cv2.resize(tmp, (max_width, max_height)))
        resized_negatives = []
        for tmp in negativeSamples:
            resized_negatives.append(cv2.resize(tmp, (max_width, max_height)))

        # Template matching with contours against each other
        match_values = [0] * len(resized_templates)
        for i in range(len(resized_templates)):
            for j in range(i):#+1, len(resized_templates)):
                im1 = resized_templates[i]
                im2 = resized_templates[j]
                res = cv2.matchTemplate(im1, im2, cv2.TM_CCOEFF_NORMED)
                match_values[i] += res[0][0]
                match_values[j] += res[0][0]

        # Template matching with contours against positive samples
        for i in range(len(resized_templates)):
            for j in range(len(resized_positives)):
                im1 = resized_templates[i]
                im2 = resized_positives[j]
                res = cv2.matchTemplate(im1, im2, cv2.TM_CCOEFF_NORMED)
                match_values[i] += res[0][0]

        # Template matching with contours against negative samples
        for i in range(len(resized_templates)):
            for j in range(len(resized_negatives)):
                im1 = resized_templates[i]
                im2 = resized_negatives[j]
                res = cv2.matchTemplate(im1, im2, cv2.TM_CCOEFF_NORMED)
                match_values[i] -= res[0][0]

        # Get the best template (highest score)
        best_template_index = match_values.index(max(match_values))
        if demo:
            cv2.imshow('Image', templates[best_template_index])
            cv2.waitKey()

        return templates[best_template_index]
