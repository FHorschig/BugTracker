"""Provides a class that creates annotations out of an image analysis."""

import csv

from bug import Bug
from qr_code import QRCode


class Annotator(object):
    """Provides methods to create annotation files."""
    __PREFIXES = ["@prefix dwc: <http://rs.tdwg.org/dwc/terms/#> ."]


    def __init__(self, iohelper):
        self.__iohelper = iohelper
        self.__bugs = []
        self.__qr_codes = []
        self.__common_features_qr_code = None


    def bugs(self, ref_image=None):
        """ Returns the list of saved bugs. Needed esp. for Benchmarking."""
        if not ref_image:
            return self.__bugs
        from cv2 import imread
        height, width, _ = imread(ref_image).shape
        return [bug.new_for_reference(height, width) for bug in self.__bugs]


    def add_bug(self, x, y, width, height):
        """Drawn a box around a bug? Tel me with this method"""
        relative_coordinates = self.__iohelper.transform(x, y, width, height)
        bug = Bug('img', relative_coordinates)
        self.__add_taxon_information(bug)
        self.__bugs.append(bug)


    def __add_taxon_information(self, bug):
        if self.__common_features_qr_code:
            code = self.__common_features_qr_code 
            bug.set_taxonomic_classification(code.order, code.family, code.genus, code.species)


    def reset_bugs(self):
        """ Empties the list of known bugs."""
        self.__bugs = []


    def add_qr_code(self, symbol):
        code = QRCode(symbol.data, symbol.location)

        taxonomic_information = self.__get_qr_code_data(code.get_species_id())

        if taxonomic_information:
            order = taxonomic_information[0]
            family = taxonomic_information[1]
            species = taxonomic_information[2]
            genus = species[:species.find(' ')] # genus is the first word of a species name
            code.set_taxonomic_classification(order, family, genus, species)

        self.__qr_codes.append(code)
        self.__update_common_features_qr_code(code)


    def __get_qr_code_data(self, species_id):
        with open(self.__iohelper.species_csv(), 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='\"')
            for row in reader:
                if row[3] == species_id: # 4th column contains the id of a species
                    return row


    def __update_common_features_qr_code(self, code):
        if not self.__common_features_qr_code:
            self.__common_features_qr_code = QRCode(None, None)
            self.__common_features_qr_code.set_taxonomic_classification(code.order, code.family, code.genus, code.species)
            return

        common_code = self.__common_features_qr_code
        if common_code.species and code.species and common_code.species != code.species:
            common_code.species = None
        if common_code.genus and code.genus and common_code.genus != code.genus:
            common_code.genus = None
        if common_code.family and code.family and common_code.family != code.family:
            common_code.family = None
        if common_code.order and code.order and common_code.order != code.order:
            common_code.order = None


    def save_as_turtle(self, as_string=False):
        """Saves the internal data as turtle file or prints it as String."""
        if as_string:
            return self.__get_prefixes_and_bugs()
        self.__iohelper.write_out(self.__get_prefixes_and_bugs())


    def __get_prefixes_and_bugs(self):
        """Returns prefixes and bugs concatenated and ready to save. """
        return "\n".join(Annotator.__PREFIXES) +\
               "\n@prefix img: <" + self.__iohelper.uri() + "> ."+\
               "\n" +\
               "\n".join(self.__convert_bugs_to_turtle())


    def __convert_bugs_to_turtle(self):
        """Converts the bug objects into strings."""
        return [bug.as_turtle() for bug in self.__bugs]
