"""Provides a that class contains all known data of a bug and can save it as RDF."""


class QRCode(object):
    """Stores information about a found QR code."""


    def __init__(self, data, location):
        self.uri = data
        self.location = location

        self.order = None
        self.family = None
        self.genus = None
        self.species = None

    def get_species_id(self):
        return self.uri[(self.uri.rfind('/') + 1) : self.uri.rfind('\.')]


    def set_taxonomic_classification(self, order, family, genus, species):
        self.order = order
        self.family = family
        self.genus = genus
        self.species = species
