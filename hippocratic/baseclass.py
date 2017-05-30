"""Module which will contains the basic classes used in the code

:Authors: Nicolas Gruel <nicolas.gruel@manchester.ac.uk>

:Copyright: IT Services, The University of Manchester
"""
# pylint: disable=locally-disabled, invalid-name
try:
    from .conf import (logger, XML_OSS, XML_N_OFFSET, XML_OFFSET_SIZE,
                       TEMPLATE_FNAME, RELAXNG_FNAME)
except ImportError:
    from conf import (logger, XML_OSS, XML_N_OFFSET, XML_OFFSET_SIZE,
                      TEMPLATE_FNAME, RELAXNG_FNAME)


# Define an Exception
class HippocraticException(Exception):
    """Class for exception
    """
    pass


class Hippocratic(object):
    """Basic class used for the software.

    Attributes
    ----------
    xml : list, optional
        list of string which contains the XML related to the introduction
        to be include in the main XML part of the document.

    xml_n_offset : int, optional
        define the number of time the oss string is used (see above)
        default: 3

    xml_offset_size : int, optional
        define the number of times the same string is used to indent.
        Default: 4

    xml_oss : str, optional
        define the string used to indent xml statement.
        default ' ' * XML_OFFSET_SIZE.
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

        Parameters
        ----------
        note : str
            contains the string to consider as a note in the XML
        """
        self.xml.append(self.xml_oss + '<note>' + note + '</note>')

    def save_xml(self, fname=None, xml=None):
        """Method to save the XML in the working directory
        """
        if fname is None:
            fname = self.__class__.__name__ + '.xml'

        if xml is None:
            if self.xml is list:
                xml = '\n'.join(self.xml)
            else:
                xml = self.xml

        with open(fname, 'w', encoding="utf-8") as f:
            f.write(xml)
