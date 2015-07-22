#pylint: disable=E1101
import cv2
from scipy import ndimage

try:
    import zbar
except:
    print 'Zbar module not available for qr code detection.'


# Import Image from PIL depending on installed library
try:
    from PIL import Image
except:
    pass

try:
    import Image
except:
    pass


class QRDetection(object):
    """ Finds & evaluates QR-Codes in images and sends results to annotator."""

    def __init__(self):
        self.scanner = zbar.ImageScanner()
        self.scanner.parse_config('enable')

    def process(self, annotator, io_helper):
        image = cv2.imread(io_helper.image(), cv2.IMREAD_GRAYSCALE)
        small = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)
        symbols = self._scan_image(small)
        for symbol in symbols:
            annotator.add_qr_code(symbol)

        # Output image with qr codes marked
        # result_image = small
        # for symbol in symbols:
        #     cv2.rectangle(result_image, symbol.location[0], symbol.location[2], (0, 0, 255), 20)
        # return result_image

    def process_alternative(self, annotator, io_helper):
        image = cv2.imread(io_helper.image(), cv2.IMREAD_GRAYSCALE)
        step_size = 1000
        step_overlap = step_size + 100

        height, width = image.shape[:2]
        for x in range(width / step_size):
            for y in range(height / step_size):
                sub_image = image[(y * step_size):(y * step_size + step_overlap), (x * step_size):(x * step_size + step_overlap)]
                symbols = self._scan_image(image)
                for symbol in symbols:
                    annotator.add_qr_code(symbol)

        print 'All qr codes found. Zbar should be finished at this point.'




    def find(self, annotator, image):
        """ Finds a single QR-Code in an image and returns it."""

    # Test values for image 30
    # def process(self, annotator, io_helper):
        # whole_image = cv2.imread(io_helper.image(), cv2.IMREAD_GRAYSCALE)
        # image_unrotated = whole_image[11800:12500, 16100:16800] #img[y1:y2, x1:x2]
        # image = ndimage.rotate(image_unrotated, 0)

        symbols = self._scan_image(image)
        if symbols:
            symbol = symbols[0]
            print 'Decoded', symbol.type, 'symbol', '"%s"' % symbol.data, ' at ', symbol.location
            return symbol


    def _scan_image(self, image):
        pil_image = Image.fromarray(image)
        width, height = pil_image.size
        zbar_image = zbar.Image(width, height, 'Y800', pil_image.tostring())
        self.scanner.scan(zbar_image)
        return [symbol for symbol in zbar_image]
