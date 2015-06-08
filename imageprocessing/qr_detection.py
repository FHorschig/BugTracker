#pylint: disable=E1101
import cv2

try:
    from PIL import Image
except:
    pass

try:
    import Image
except:
    pass

try:
    import zbar
except:
    print 'Zbar module not available for qr code detection.'


class QRDetection(object):
    """ Finds & evaluates QR-Codes in images and sends results to annotator."""

    def process(self, annotator, io_helper):
        # wrap image data
        image = cv2.imread(io_helper.image(), cv2.IMREAD_GRAYSCALE)
        pil_image = Image.fromarray(image)
        width, height = pil_image.size

        zbar_image = zbar.Image(width, height, 'Y800', pil_image.tostring())

        # create a reader and scan for barcodes
        scanner = zbar.ImageScanner()
        scanner.parse_config('enable')
        scanner.scan(zbar_image)

        for symbol in zbar_image:
            print 'Decoded', symbol.type, 'symbol', '"%s"' % symbol.data, ' at ', symbol.location
        print 'QR detection done'

        # output image with qr codes marked
        result_image = cv2.imread(io_helper.image())
        for symbol in zbar_image:
            cv2.rectangle(result_image, symbol.location[0], symbol.location[2], (0, 0, 255), 20)
        return result_image
