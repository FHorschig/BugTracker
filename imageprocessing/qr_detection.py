#pylint: disable=E1101
import cv2
import Image
import zbar

class QRDetection(object):
    """ Finds & evaluates QR-Codes in images and sends results to annotator."""

    def process(self, annotator, iohelper):
        # wrap image data
        # TODO(sten.aechtner|FHorschig): Scale image.
        #     Should be param for image-function in IOHelper.
        pil = Image.fromarray(cv2.imread(iohelper.image(), 0).copy())
        width, height = pil.size
        zbar_image = zbar.Image(width, height, 'Y800', pil.tostring())

        # create a reader and scan for barcodes
        scanner = zbar.ImageScanner()
        scanner.parse_config('enable')
        scanner.scan(zbar_image)

        for symbol in zbar_image:
            # TODO(sten.aechtner): send results to annotator
            print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data, ' at ', symbol.location
        print 'QR detection done'
