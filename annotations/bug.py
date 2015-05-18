"""Provides a class contains all known data of a bug and can save it as RDF."""


class Bug(object):
    """Stores information about a found Bug."""


    def __init__(self, image_url, bounding_box):
        self.__image_url = image_url
        self.__x, self.__y, self.__w, self.__h = bounding_box


    def as_turtle(self):
        """Drawn a box around a bug? Tell me with this method"""
        return "\n<" + self.__image_url + \
                   "#x=" + str(self.__x) +\
                   "&y=" + str(self.__y) +\
                   "&w=" + str(self.__w) +\
                   "&h=" + str(self.__h) + ">" + " a dwc:Organism ."
