"""Provides a class contains all known data of a bug and can save it as RDF."""


class Bug(object):
    """Stores information about a found Bug."""


    def __init__(self, image_url, bounding_box):
        self.__image_url = image_url
        self.__x, self.__y, self.__w, self.__h = bounding_box


    def bounds(self):
        """ Returns coordinates on image."""
        return self.__x, self.__y, self.__w, self.__h


    def as_turtle(self):
        """Drawn a box around a bug? Tell me with this method"""
        results = []
        results.append("\n<{0}#x={1}&y={2}&w={3}&h={4}>"\
          .format(self.__image_url, self.__x, self.__y, self.__w, self.__h))
        results.append("a dwc:Organism ;")
        results.append("dwc:order x ;")
        results.append("dwc:family x ;")
        results.append("dwc:genus x ;")
        results.append("dwc:specificEpithet x ;")
        results.append("dwc:taxonRank species .")
        return "\n    ".join(results)
