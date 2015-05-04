"""Provides a class contains all known data of a bug and can save it as RDF."""


class Bug(object):
    """Stores information about a found Bug."""


    def __init__(self, image_url, x, y, w, h):
        self.__image_url = image_url
        self.__x = x
        self.__y = y
        self.__w = w
        self.__h = h


    def as_turtle(self):
        """Drawn a box around a bug? Tel me with this method"""
        return "<" + self.__image_url + \
                   "#x=" + str(self.__x) +\
                   "&y=" + str(self.__y) +\
                   "&w=" + str(self.__w) +\
                   "&h=" + str(self.__h) + ">" + " a dwc:Organism ."
