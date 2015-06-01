from analyzer import Analyzer
from thresholding import Thresholding
from templateMatching import TemplateMatching, TemplateMatchingWithThresholding
METHODS = {
    "THRESHOLD": Thresholding,
    "TEMPLATE": TemplateMatching,
    "TEMPLATE_THRESHOLD": TemplateMatchingWithThresholding,
}
