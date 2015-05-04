"""Provides a class wraps tools like openCV and shared directories."""

import os

class ToolsProvider(object):
    """Provides methods to access tools and shared directories."""
    def __init__(self):
        self.__working_dir = "."
        self.__output_dir = "."
        self.__tools_dir = "."

    def set_working_directory(self, new_dir):
        """Sets working directory for temporary files."""
        self.__working_dir = new_dir


    def write_out(self, msg, filename="out.rdf"):
        """Writes a string to the default out file."""
        with open(os.path.join(self.output_dir(), filename), "w") as text_file:
            text_file.write(msg)

    def output_dir(self):
        """Returns and creates out dir if necessary."""
        ToolsProvider.__enforce_directories(self.__output_dir)
        return self.__output_dir


    def working_dir(self):
        """Returns and creates out dir if necessary."""
        ToolsProvider.__enforce_directories(self.__working_dir)
        return self.__working_dir


    def set_output_directory(self, new_dir):
        """Sets directory for final results."""
        self.__output_dir = new_dir


    def set_tools_directory(self, new_dir):
        """Sets directory for external tools."""
        self.__tools_dir = new_dir

    @staticmethod
    def __enforce_directories(directory):
        """Creates the set directory paths if they don't exist."""
        if os.path.exists(directory):
            return
        os.makedirs(directory)
