"""Provides a class that contains all known data of a bug and can save it as RDF."""


class Bug(object):
    """Stores information about a found Bug."""


    def __init__(self, image_url, bounding_box):
        self.__image_url = image_url
        self.__x, self.__y, self.__w, self.__h = bounding_box

        self.order = None
        self.family = None
        self.genus = None
        self.species = None


    def bounds(self):
        """ Returns coordinates on image."""
        return self.__x, self.__y, self.__w, self.__h


    def set_taxonomic_classification(self, family, order, genus, species):
        self.order = order
        self.family = family
        self.genus = genus
        self.species = species


    def as_turtle(self):
        """Drawn a box around a bug? Tell me with this method"""
        results = []
        results.append("\n<{0}#x={1}&y={2}&w={3}&h={4}>"\
          .format(self.__image_url, self.__x, self.__y, self.__w, self.__h))
        results.append("a dwc:Organism ;")
        results.append("dwc:order {0} ;".format(self.order))
        results.append("dwc:family {0} ;".format(self.family))
        results.append("dwc:genus {0} ;".format(self.genus))
        results.append("dwc:specificEpithet {0} ;".format(self.species))
        results.append("dwc:taxonRank species .")
        return "\n    ".join(results)
