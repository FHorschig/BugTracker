"""Provides a class contains all known data of a bug and can save it as RDF."""


class Bug(object):
    """Stores information about a found Bug."""


    def __init__(self, image_url, bounding_box):
        self.__image_url = image_url
        self.__x, self.__y, self.__w, self.__h = bounding_box


    def bounds(self):
        """ Returns (relative) coordinates on image."""
        return self.__x, self.__y, self.__w, self.__h


    def new_for_reference(self, width, height):
        """ Returns bug with absolute coordinates on image."""
        return Bug(self.__image_url, (
                          int(self.__x * width),
                          int(self.__y * height),
                          int(self.__w * width),
                          int(self.__h * height)))


    def as_turtle(self):
        """Drawn a box around a bug? Tell me with this method"""
        return "\n<" + self.__image_url + \
                   "#x=" + str(self.__x) +\
                   "&y=" + str(self.__y) +\
                   "&w=" + str(self.__w) +\
                   "&h=" + str(self.__h) + ">" + " a dwc:Organism ."
