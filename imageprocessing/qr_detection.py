import cv2
import numpy as np
import Image
import zbar

class QRDetection(object):

    def process(self, annotator, iohelper):
        # image = cv2.cv.LoadImageM(img_file, cv2.cv.CV_LOAD_IMAGE_GRAYSCALE)

        img = cv2.imread(iohelper.image(), 0)
        image = img.copy()
        # wrap image data
        pil = Image.fromarray(image)
        w, h = pil.size
        raw = pil.tostring()

        zbar_image = zbar.Image(w, h, 'Y800', raw)

        # create a reader and scan for barcodes
        scanner = zbar.ImageScanner()
        scanner.parse_config('enable')
        scanner.scan(zbar_image)

        # TODO(sten.aechtner): send results to annotator
        for symbol in zbar_image:
            # do something useful with results
            print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data, ' at ', symbol.location
        print 'QR detection done'
