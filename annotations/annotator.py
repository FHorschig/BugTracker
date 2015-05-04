"""Provides a class that creates annotations out of an image analysis."""

from bug import Bug


class Annotator(object):
    """Provides methods to create annotation files."""


    def __init__(self, tools_provider):
        self.__tools_provider = tools_provider
        self.__PREFIXES = ["@prefix dwc: <http://rs.tdwg.org/dwc/terms/#> .\n"]
        self.__bugs = []

    def add_found_bug(self, image_file, x, y, w, h):
        """Drawn a box around a bug? Tel me with this method"""
        self.__bugs.append(Bug(image_file, x, y, w, h).as_turtle())

    def save_as_turtle(self, as_string=True):
        """Saves the internal data as turtle file."""
        #TODO(fhorschig): Use only needed prefixes.
        out = "".join(self.__PREFIXES)
        out = out + "\n".join(self.__bugs)
        if as_string:
            return out
        #TODO(fhorschig): Create file in tools_provider out-dir.
