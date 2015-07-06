"""Provides a class that creates annotations out of an image analysis."""

from bug import Bug


class Annotator(object):
    """Provides methods to create annotation files."""
    __PREFIXES = ["@prefix dwc: <http://rs.tdwg.org/dwc/terms/#> ."]


    def __init__(self, iohelper):
        self.__iohelper = iohelper
        self.__bugs = []


    def bugs(self):
        """ Returns the list of saved bugs. Needed esp. for Benchmarking."""
        return self.__bugs


    def reset_bugs(self):
        """ Empties the list of known bugs."""
        self.__bugs = []


    def add_bug(self, x, y, width, height):
        """Drawn a box around a bug? Tel me with this method"""
        relative_coordinates = self.__iohelper.transform(x, y, width, height)
        self.__bugs.append(Bug('img', relative_coordinates))


    def save_as_turtle(self, as_string=False):
        """Saves the internal data as turtle file or prints it as String."""
        if as_string:
            return self.__get_prefixes_and_bugs()
        self.__iohelper.write_out(self.__get_prefixes_and_bugs())


    def __get_prefixes_and_bugs(self):
        """Returns prefixes and bugs concatenated and ready to save. """
        return "\n".join(Annotator.__PREFIXES) +\
               "\n@prefix img: <" + self.__iohelper.uri() + "> ."+\
               "\n" +\
               "\n".join(self.__convert_bugs_to_turtle())


    def __convert_bugs_to_turtle(self):
        """Converts the bug objects into strings."""
        return [bug.as_turtle() for bug in self.__bugs]
