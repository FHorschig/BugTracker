from analyzer import Analyzer
from thresholding import Thresholding
from templateMatching import TemplateMatching, TemplateMatchingWithThresholding
from hogTemplateMatching import HogTemplateMatching
from qr_detection import QRDetection


METHODS = {
    "THRESHOLD": Thresholding,
    "TEMPLATE": TemplateMatching,
    "HOGTEMPLATE": HogTemplateMatching,
    "TEMPLATE_THRESHOLD": TemplateMatchingWithThresholding,
    "QR_DETECTION": QRDetection,
}
