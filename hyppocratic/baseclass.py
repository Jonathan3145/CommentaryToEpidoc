"""Module which will contains the basic classes used in the code

Authors: Nicolas Gruel
Copyright: IT Services, The University of Manchester
"""
import logging.config

try:
    from hyppocratic.conf import LOGGING, XML_OSS, XML_N_OFFSET, XML_OFFSET_SIZE
except ImportError:
    from conf import LOGGING, XML_OSS, XML_N_OFFSET, XML_OFFSET_SIZE

# Read logging configuration and create logger
logging.config.dictConfig(LOGGING)
# pylint: disable=locally-disabled, invalid-name
logger = logging.getLogger('hyppocratic.CommentaryToEpidoc')


# Define an Exception
class HyppocraticException(Exception):
    """Class for exception
    """
    pass


class Hyppocratic(object):
    """
    self.xml: list
        list of string which contains the XML related to the introduction
        to be include in the main XML part of the document.
    """
    def __init__(self):

        self.xml = []
        self.xml_oss = XML_OSS
        self.xml_n_offset = XML_N_OFFSET
        self.xml_offset_size = XML_OFFSET_SIZE

    def xml_main(self):
        """Method which will create the XML file.
        """
        pass

    def note_xml(self, note):
        """Method to create the apparatus note XML
        """
        self.xml.append(self.xml_oss + '<note>' + note + '</note>')

    def save_xml(self):
        """Method to save the XML in the working directory
        """
        fname = self.__class__.__name__
        with open(fname, 'w', encoding="utf-8") as f:
            for s in self.xml:
                f.write(s + '\n')
