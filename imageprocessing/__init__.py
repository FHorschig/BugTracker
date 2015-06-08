from analyzer import Analyzer
from thresholding import Thresholding
from templateMatching import TemplateMatching, TemplateMatchingWithThresholding
from qr_detection import QRDetection

METHODS = {
    "THRESHOLD": Thresholding,
    "TEMPLATE": TemplateMatching,
    "TEMPLATE_THRESHOLD": TemplateMatchingWithThresholding,
    "QR_DETECTION": QRDetection,
}
