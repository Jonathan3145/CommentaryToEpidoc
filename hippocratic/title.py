"""Module which contains the class which create the XML part related to
the title in the hippocratic aphorism document.

:Authors: Jonathan Boyle, Nicolas Gruel <nicolas.gruel@manchester.ac.uk>

:Copyright: IT Services, The University of Manchester
"""
try:
    from .analysis import references, footnotes
    from .baseclass import Hippocratic, logger
except ImportError:
    from analysis import references, footnotes
    from baseclass import Hippocratic, logger


# Define an Exception
class TitleException(Exception):
    """Class for exception
    """
    pass


class Title(Hippocratic):
    """Class Title which will create the title XML part

    Attributes
    ----------
    title : str
        string which contain the title of the hippocratic aphorisms
        document.

    doc_num : int
        integer which contain the version of the document.

    next_footnote : int
        integer which contains the footnote reference number which
        can be present.
    """
    def __init__(self, title, next_footnote=1, doc_num=1):
        Hippocratic.__init__(self)
        self.title = title
        self.doc_num = doc_num
        self.next_footnote = next_footnote

    def xml_main(self):
        """Method to treat the title.

        Modify the attribute ``xml`` to add the title section in the main XML
        """
        self.title = self.title.strip(' \n').splitlines()
        # remove empty line in title if present.
        self.title = [line for line in self.title if line]

        # Now process the title
        # ---------------------

        # Generate the opening XML for the title
        self.xml.append(self.xml_oss * self.xml_n_offset +
                        '<div n="{}" '
                        'type="Title_section">'.format(self.doc_num))
        self.xml.append(self.xml_oss * (self.xml_n_offset + 1) + '<ab>')

        for line in self.title:

            # Process any witnesses in this line.
            # If this raises an exception then print an error message
            # and return
            try:
                line_ref = references(line)
            except TitleException:
                error = ('Unable to process title references '
                         'in line {} '.format(line))
                logger.error(error)
                raise TitleException

            # Process any footnotes in line_ref,
            # if this fails print to the error file and return
            try:
                self.xml_n_offset += 2
                xml_main_to_add, self.next_footnote = \
                    footnotes(line_ref, self.next_footnote)
                self.xml_n_offset -= 2
            except(TitleException, TypeError):
                error = ('Unable to process title footnote '
                         'in line {} '.format(line))
                logger.error(error)
                return

            # Add the return values to the XML lists
            self.xml.extend(xml_main_to_add)

        # Close the XML for the title
        self.xml.append(self.xml_oss * (self.xml_n_offset + 1) + '</ab>')
        self.xml.append(self.xml_oss * self.xml_n_offset + '</div>')
