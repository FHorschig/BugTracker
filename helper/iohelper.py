"""Provides easy access to filenames, URIs and shared directories."""

import csv
import os
import urllib2

class IOHelper(object):
    """Provides methods to access filenames, URIs and shared directories."""

    __IMAGE_LIST = "http://gbif.naturkundemuseum-berlin.de/"\
                   "hackathon/hackathon_list.csv"


    def __init__(self, silent=False):
        self.__silent = silent
        self.__dry = False
        self.__cache_dir = "."
        self.__output_dir = "."
        self.__uri = None
        self.__thumb = None


    def select_file(self, external_file=None, input_func=raw_input):
        """ Loads the image list if none is passed and lets the user choose."""
        if external_file:
            self.__uri = self.__thumb = external_file
            return

        with open(self.__download_if_not_cached(IOHelper.__IMAGE_LIST), 'rb') \
                as csvfile:
            if self.__ask_user_for_image(
                    csv.reader(csvfile, delimiter=';', quotechar='\n'),
                    input_func):
                return
        exit(0)


    def set_dry_run(self, dry):
        """ If in running dry, neither files nor pathes are created. """
        self.__dry = dry


    def thumbnail(self):
        """ Returns path for downloaded thumbnail of the selected file."""
        return self.__download_if_not_cached(self.__thumb, True)


    def image(self):
        """ Returns path for downloaded image of the selected file."""
        return self.__download_if_not_cached(self.__uri)


    def write_out(self, msg="", filename=None):
        """Creates empty default file without parameters. """
        if self.__dry:
            return
        if not filename:
            filename = os.path.basename(self.__uri) + ".rdf"
        with open(os.path.join(self.output_dir(), filename), "w") as text_file:
            text_file.write(msg)


    def set_output_directory(self, new_dir):
        """Sets directory for final results."""
        self.__output_dir = new_dir


    def set_cache_directory(self, new_dir):
        """Sets cache directory for temporary and downloaded files."""
        self.__cache_dir = new_dir


    def output_dir(self):
        """Returns and creates out dir if necessary."""
        self.__enforce_directories(self.__output_dir)
        return self.__output_dir


    def cache_dir(self):
        """Returns and creates cache dir if necessary."""
        self.__enforce_directories(self.__cache_dir)
        return self.__cache_dir


    def uri(self):
        """The stable URI for the currently processed image."""
        return self.__uri


    def __enforce_directories(self, directory):
        """Creates the set directory paths if they don't exist."""
        if self.__dry or os.path.exists(directory):
            return
        os.makedirs(directory)


    def __ask_user_for_image(self, reader, input_func):
        """ Returns if the user has chosen a line from the reader."""
        index = 0
        rows = []
        for row in reader:
            rows.append(row)
            if index > 0 and not self.__silent:
                print "[" + str(index) + "] " + row[4]
            index += 1
            if index % 20 != 0:
                continue
            if self.__set_uri_by_user_choice(" for more", rows, input_func):
                return True
        return self.__set_uri_by_user_choice(" to end", rows, input_func)


    def __set_uri_by_user_choice(self, msg_appendix, rows, input_func):
        """ Sets the uri to the index of the rwos that the user chose from.
        Returns True if a choice was made. """
        i = input_func("Select a number or press enter" + msg_appendix + ": ")
        if i == '':
            return False
        _, _, _, _, _, self.__uri, self.__thumb = rows[int(i)]
        if not self.__silent:
            print self.__uri + ", " + self.__thumb
        return True


    def __local_filename(self, url, is_thumb):
        """ Returns the filename of the given url within the cache."""
        filename = os.path.basename(url)
        if is_thumb:
            filename = "thumb_" + filename
        return os.path.join(self.cache_dir(), filename)


    def __download_if_not_cached(self, url, is_thumb=False):
        """ Returns path to downloaded file. Downloads if not in cache."""
        if os.path.exists(url):
            return url
        path = self.__local_filename(url, is_thumb)
        if os.path.exists(path):
            return path
        if self.__dry:
            return None
        self.__download(url, path)
        return path


    def __download(self, url, path):
        """ Downloads a file from an url to a path while showing progress."""
        if self.__dry:
            print "Tried to download a file while running dry!"
            return
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
