"""Provides a class that creates annotations out of an image analysis."""


class Annotator(object):
    """Provides methods to create annotation files."""


    def __init__(self, tools_provider):
        self.__tools_provider = tools_provider


    def save_as_turtle(self):
        """ESaves the internal data as turtle file."""
        #TODO(fhorschig): Implement.
