"""Provides easy access to filenames, URIs and shared directories."""

import csv
import os
import urllib2

class IOHelper(object):
    __IMAGE_LIST = "http://gbif.naturkundemuseum-berlin.de/"\
                   "hackathon/hackathon_list.csv"


    """Provides methods to access filenames, URIs and shared directories."""
    def __init__(self):
        self.__cache_dir = "."
        self.__output_dir = "."
        self.__uri = None
        self.__thumb = None


    def select_file(self, external_file=None):
        index = 0
        rows = []
        if external_file:
            self.__uri = self.__thumb = external_file
            return

        image_list = self.__download_if_not_cached(IOHelper.__IMAGE_LIST)

        with open(image_list, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';', quotechar='\n')
            for row in spamreader:
                rows.append(row)
                if index > 0:
                    print "[" + str(index) + "] " + row[4]
                index += 1
                if index % 20 == 0:
                    i = raw_input("Select a number or press enter for more: ")
                    if i != '':
                        _, _, _, _, _, self.__uri, self.__thumb = rows[int(i)]
                        print self.__uri + ", " + self.__thumb
                        return
            i = raw_input("Select a number or press enter to end: ")
            if i != '':
                _, _, _, _, _, self.__uri, self.__thumb = rows[int(i)]
                print self.__uri + ", " + self.__thumb
                return
            exit(0)


    def thumbnail(self):
        return self.__download_if_not_cached(self.__thumb, True)


    def image(self):
        return self.__download_if_not_cached(self.__uri)


    def __download_if_not_cached(self, url, thumb=False):
        if os.path.exists(url):
            return url
        path = os.path.join(self.cache_dir(), "thumb_" + os.path.basename(url))
        if os.path.exists(path):
            return path
        req = urllib2.urlopen(url)
        dl_f = open(path, 'wb')
        meta = req.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        print "Downloading: %s Bytes: %s" % (path, file_size)

        dl_size = 0
        block_sz = 8192
        while True:
            buf = req.read(block_sz)
            if not buf:
                break

            dl_size += len(buf)
            dl_f.write(buf)
            status = r"%10d  [%3.2f%%]" % (dl_size, dl_size * 100. / file_size)
            status = status + chr(8)*(len(status)+1)
            print status,

        dl_f.close()
        return path

    def set_cache_directory(self, new_dir):
        """Sets cache directory for temporary and downloaded files."""
        self.__cache_dir = new_dir


    def write_out(self, msg, filename=None):
        """Writes a string to the default out file."""
        if not filename:
            filename = os.path.basename(self.__uri) + ".rdf"
        with open(os.path.join(self.output_dir(), filename), "w") as text_file:
            text_file.write(msg)

    def output_dir(self):
        """Returns and creates out dir if necessary."""
        IOHelper.__enforce_directories(self.__output_dir)
        return self.__output_dir


    def cache_dir(self):
        """Returns and creates cache dir if necessary."""
        IOHelper.__enforce_directories(self.__cache_dir)
        return self.__cache_dir


    def uri(self):
        """The stable URI for the currently processed image."""
        return self.__uri


    def set_output_directory(self, new_dir):
        """Sets directory for final results."""
        self.__output_dir = new_dir

    @staticmethod
    def __enforce_directories(directory):
        """Creates the set directory paths if they don't exist."""
        if os.path.exists(directory):
            return
        os.makedirs(directory)
