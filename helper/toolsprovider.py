"""Provides a class wraps tools like openCV and shared directories."""


class ToolsProvider(object):
    """Provides methods to access tools and shared directories."""
    def __init__(self):
        self.__working_dir = "."
        self.__output_dir = "."
        self.__tools_dir = "."

    def set_working_directory(self, new_dir):
        """Sets working directory for temporary files."""
        self.__working_dir = new_dir


    def set_output_directory(self, new_dir):
        """Sets directory for final results."""
        self.__output_dir = new_dir


    def set_tools_directory(self, new_dir):
        """Sets directory for external tools."""
        self.__tools_dir = new_dir

    def enforce_directories(self):
        """Creates the set directory paths if they don't exist."""
        #TODO(fhorschig): Implement.
