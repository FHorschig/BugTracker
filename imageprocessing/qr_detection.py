import cv2
import numpy as np
import zbar

class QRDetection(object):

    def process(self, annotator, img_file):
        image = cv2.cv.LoadImageM(img_file, cv2.cv.CV_LOAD_IMAGE_GRAYSCALE)

        # wrap image data
        zbar_image = zbar.Image(image.width, image.height, 'Y800', image.tostring())

        # create a reader and scan for barcodes
        scanner = zbar.ImageScanner()
        scanner.parse_config('enable')
        scanner.scan(zbar_image)

        # TODO(sten.aechtner): send results to annotator
        for symbol in zbar_image:
            # do something useful with results
            print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data, ' at ', symbol.location
        print 'QR detection done'
