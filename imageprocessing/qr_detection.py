import cv2
import numpy as np
import zbar

class QRDetection(object):

    def process(self, img_file):
        cv_image = cv2.cv.LoadImageM(img_file, cv2.cv.CV_LOAD_IMAGE_GRAYSCALE)

        width = cv_image.width
        height = cv_image.height
        raw = cv_image.tostring()

        # wrap image data
        image = zbar.Image(width, height, 'Y800', raw)

        # create a reader and scan for barcodes
        scanner = zbar.ImageScanner()
        scanner.parse_config('enable')
        scanner.scan(image)

        # TODO(sten.aechtner): send results to annotator
        for symbol in image:
            # do something useful with results
            print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data
        print 'QR detection done'
