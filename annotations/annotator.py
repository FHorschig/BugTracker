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


    def add_qr_code(self, symbol):
        code = QRCode(symbol.data, symbol.location)

        taxonomic_information = self.__get_qr_code_data(code.get_species_id())
        if taxonomic_information:
            order = taxonomic_information[0]
            family = taxonomic_information[1]
            species = taxonomic_information[2]
            genus = species[:species.find(' ')] # genus is the first part of a species name
            code.set_taxonomic_classification(order, family, genus, species)

        self.__qr_codes.append(code)


    def bugs(self):
        """ Returns the list of saved bugs. Needed esp. for Benchmarking."""
        return self.__bugs


    def reset_bugs(self):
        """ Empties the list of known bugs."""
        self.__bugs = []


    def add_bug(self, x, y, width, height):
<<<<<<< HEAD
        """Drawn a box around a bug? Tel me with this method"""
        relative_coordinates = self.__iohelper.transform(x, y, width, height)
        self.__bugs.append(Bug('img', relative_coordinates))
        self.__add_taxon_information(bug)
        self.__bugs.append(bug)


    def __get_qr_code_data(self, species_id):
        with open(self.__iohelper.species_csv(), 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='\"')
            for row in reader:

                # row[3] contains the id of a species
                if row[3] == species_id:
                    return row


    def __add_taxon_information(self, bug):
        qr_codes = self.__qr_codes
        
        # TODO: find best matching qr code once we have relative coordinates

        if qr_codes:
            code = qr_codes[0]
            bug.set_taxonomic_classification(code.order, code.family, code.genus, code.species)


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
