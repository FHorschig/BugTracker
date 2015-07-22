"""Provides a class that contains all data of a qr code."""


class QRCode(object):
    """Stores information about a found QR code."""


    def __init__(self, data, location):
        self.url = data
        self.location = location

        self.order = None
        self.family = None
        self.genus = None
        self.species = None


    def get_species_id(self):
        return self.url[(self.url.rfind('/') + 1):]


    def set_taxonomic_classification(self, order, family, genus, species):
        self.order = order
        self.family = family
        self.genus = genus
        self.species = species
