"""Provides a class that analyzes images for bugs."""


class Analyzer(object):
    """Provides methods to extract regions with bugs from images."""


    def __init__(self, tools_provider, annotator):
        self.__tools_provider = tools_provider
        self.__annotator = annotator


    def start_processing(self):
        """Extracts features and stores findings into given annotator."""
        #TODO(fhorschig): Implement.
