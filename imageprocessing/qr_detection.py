import cv2
import numpy as np

try:
    import zbar
except:
    print 'Zbar module not available for qr code detection.'

class QRDetection(object):

    def process(self, annotator, io_helper):

        image = cv2.cv.LoadImageM(io_helper.image(), cv2.cv.CV_LOAD_IMAGE_GRAYSCALE)

        # wrap image data
        zbar_image = zbar.Image(image.width, image.height, 'Y800', image.tostring())

        # create a reader and scan for barcodes
        scanner = zbar.ImageScanner()
        scanner.parse_config('enable')
        scanner.scan(zbar_image)

        # TODO(sten.aechtner): send results to annotator
        for symbol in zbar_image:
            # do something useful with results
            print 'Decoded', symbol.type, 'symbol', '"%s"' % symbol.data, ' at ', symbol.location
        print 'QR detection done'

        # output image with qr codes marked - remove once qr code detection is done
        result_image = cv2.imread(io_helper.image())
        for symbol in zbar_image:
            cv2.rectangle(result_image, symbol.location[0], symbol.location[2], (0, 0, 255), 20)
        return result_image
