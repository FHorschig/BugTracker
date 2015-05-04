"""Provides a class that creates annotations out of an image analysis."""

from bug import Bug


class Annotator(object):
    """Provides methods to create annotation files."""
    __PREFIXES = ["@prefix dwc: <http://rs.tdwg.org/dwc/terms/#> ."]


    def __init__(self, tools_provider):
        self.__tools_provider = tools_provider
        self.__bugs = []

    def add_bug(self, bug):
        """Drawn a box around a bug? Tel me with this method"""
        self.__bugs.append(bug)

    def save_as_turtle(self, as_string=False):
        """Saves the internal data as turtle file or prints it as String."""
        if as_string:
            return self.__get_prefixes_and_bugs()
        with open("test.txt", "w") as text_file:
            text_file.write(self.__get_prefixes_and_bugs())


    def __get_prefixes_and_bugs(self):
        """Returns prefixes and bugs concatenated and ready to save. """
        return "\n".join(Annotator.__PREFIXES) +\
               "\n" +\
               "\n".join(self.__convert_bugs_to_turtle())

    def __convert_bugs_to_turtle(self):
        """Converts the bug objects into strings."""
        return [bug.as_turtle() for bug in self.__bugs]
