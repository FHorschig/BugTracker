"""Provides a class that analyzes images for bugs."""


class Analyzer(object):
    """Provides methods to extract regions with bugs from images."""


    def __init__(self, annotator):
        self.__annotator = annotator


    def process(self, file):
        """Extracts features and stores findings into given annotator."""
        #TODO(fhorschig): Implement.
