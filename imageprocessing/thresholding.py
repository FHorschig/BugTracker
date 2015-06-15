import cv2
import numpy as np
from annotations.bug import Bug



class Thresholding(object):

    def process(self, annotator, iohelper):
        img = cv2.imread(iohelper.thumbnail())
        image = img.copy()

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray_blur = cv2.GaussianBlur(gray, (9, 9), 0)
        thresh = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 31, 11)
        #thresh = cv2.adaptiveThreshold(thresh1, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 31, 11)
        #retval, thresh = cv2.threshold(gray_blur, 150, 255, cv2.THRESH_BINARY_INV)

        kernel = np.ones((3, 3), np.uint8)
        closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

        cont_img = closing.copy()
        # if int(cv2.__version__[0]) < 3:
        #     contours, _ = cv2.findContours(\
        #             cont_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # else:
        #     _, contours, _ = cv2.findContours(\
        #             cont_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        contours, _ = cv2.findContours(cont_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


############
        contourareas = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < 50 or area > 5000:
                continue
            contourareas.append(area)

        contourareas.sort()
        contourmed = contourareas[len(contourareas)/2]
        contouravg = sum(contourareas)/len(contourareas)

        newContours = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            deviation = contouravg / 2
            if area < contouravg - deviation or area > contouravg + deviation:
                continue
            newContours.append(cnt)

        contourareas = []
        for cnt in newContours:
            area = cv2.contourArea(cnt)
            if area < 50 or area > 5000:
                continue
            contourareas.append(area)

        contourareas.sort()
        contourmed = contourareas[len(contourareas)/2]
        contouravg = sum(contourareas)/len(contourareas)

        newNewContours = []
        for cnt in newContours:
            area = cv2.contourArea(cnt)
            deviation = contouravg / 16
            if area < contouravg - deviation or area > contouravg + deviation:
                continue
            newNewContours.append(cnt)


        templates = []
        max_height = -1
        max_width = -1
        for cnt in newNewContours:
            area = cv2.contourArea(cnt)
            ellipse = cv2.fitEllipse(cnt)
            center, axes, angle = ellipse
            rect_area = axes[0] * axes[1]
            rect = np.round(np.float64(cv2.cv.BoxPoints(ellipse))).astype(np.int64)

            roi_b = max(rect[2][1], rect[3][1])
            roi_l = min(rect[0][0], rect[3][0])
            roi_t = min(rect[0][1], rect[1][1])
            roi_r = max(rect[1][0], rect[2][0])

            roi = image[roi_t:roi_b , roi_l:roi_r]

            height, width = roi.shape[:2]
            templates.append(roi)
            max_height = max(max_height, height)
            max_width = max(max_width, width)

        resized_templates = []
        for tmp in templates:
            resized_templates.append(cv2.resize(tmp, (max_width, max_height)))

        # for tmp in resized_templates:
        #     cv2.imshow('Image', tmp)
        #     cv2.waitKey()

        match_values = [0] * len(resized_templates)
        for i in range(len(resized_templates)):
            for j in range(i):#+1, len(resized_templates)):
                im1 = resized_templates[i]
                im2 = resized_templates[j]

                res = cv2.matchTemplate(im1, im2, cv2.TM_CCOEFF_NORMED)

                match_values[i] += res[0][0]
                match_values[j] += res[0][0]

        best_template_index = match_values.index(max(match_values))
        cv2.imshow('Image', templates[best_template_index])
        cv2.waitKey()

############



        i = 0
        for cnt in newNewContours:

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

    def extractTemplate(self, img):
        image = img.copy()

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray_blur = cv2.GaussianBlur(gray, (9, 9), 0)
        thresh = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 31, 11)
        #thresh = cv2.adaptiveThreshold(thresh1, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 31, 11)
        #retval, thresh = cv2.threshold(gray_blur, 150, 255, cv2.THRESH_BINARY_INV)

        kernel = np.ones((3, 3), np.uint8)
        closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

        cont_img = closing.copy()
        # if int(cv2.__version__[0]) < 3:
        #     contours, _ = cv2.findContours(\
        #             cont_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # else:
        #     _, contours, _ = cv2.findContours(\
        #             cont_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        contours, _ = cv2.findContours(cont_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


############
        contourareas = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < 50 or area > 5000:
                continue
            contourareas.append(area)

        contourareas.sort()
        contourmed = contourareas[len(contourareas)/2]
        contouravg = sum(contourareas)/len(contourareas)

        newContours = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            deviation = contouravg / 2
            if area < contouravg - deviation or area > contouravg + deviation:
                continue
            newContours.append(cnt)

        contourareas = []
        for cnt in newContours:
            area = cv2.contourArea(cnt)
            if area < 50 or area > 5000:
                continue
            contourareas.append(area)

        contourareas.sort()
        contourmed = contourareas[len(contourareas)/2]
        contouravg = sum(contourareas)/len(contourareas)

        newNewContours = []
        for cnt in newContours:
            area = cv2.contourArea(cnt)
            deviation = contouravg / 16
            if area < contouravg - deviation or area > contouravg + deviation:
                continue
            newNewContours.append(cnt)


        templates = []
        max_height = -1
        max_width = -1
        im_h, im_w = image.shape[:2]
        for cnt in newNewContours:
            area = cv2.contourArea(cnt)
            ellipse = cv2.fitEllipse(cnt)
            center, axes, angle = ellipse
            rect_area = axes[0] * axes[1]
            rect = np.round(np.float64(cv2.cv.BoxPoints(ellipse))).astype(np.int64)

            roi_b = min(im_h, max([rect[i][1] for i in range(4)]))
            roi_t = max(0, min([rect[i][1] for i in range(4)]))
            roi_l = max(0, min([rect[i][0] for i in range(4)]))
            roi_r = min(im_w, max([rect[i][0] for i in range(4)]))

            roi = image[roi_t:roi_b , roi_l:roi_r]

            height, width = roi.shape[:2]
            templates.append(roi)
            max_height = max(max_height, height)
            max_width = max(max_width, width)

        resized_templates = []
        for tmp in templates:
            resized_templates.append(cv2.resize(tmp, (max_width, max_height)))

        # for tmp in resized_templates:
        #     cv2.imshow('Image', tmp)
        #     cv2.waitKey()

        match_values = [0] * len(resized_templates)
        for i in range(len(resized_templates)):
            for j in range(i):#+1, len(resized_templates)):
                im1 = resized_templates[i]
                im2 = resized_templates[j]

                res = cv2.matchTemplate(im1, im2, cv2.TM_CCOEFF_NORMED)

                match_values[i] += res[0][0]
                match_values[j] += res[0][0]

        best_template_index = match_values.index(max(match_values))
        # cv2.imshow('Image', templates[best_template_index])
        # cv2.waitKey()
        return templates[best_template_index]
