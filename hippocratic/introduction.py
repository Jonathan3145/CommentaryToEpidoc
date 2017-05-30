"""Module which contains the class which create the XML part related to
the introduction (if present) in the hippocratic aphorism document.

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
class IntroductionException(Exception):
    """Class for exception
    """
    pass


class Introduction(Hippocratic):
    """Class Introduction which will create the introduction XML part

    Attributes
    ----------

    introduction : str
        string which contain the introduction of the hippocratic aphorisms
        document.

    next_footnote : int
        integer which contains the footnote reference number which
        can be present.

    Raises
    ------
    IntroductionException
        if cannot create the xml code for the introduction.
    """

    def __init__(self, introduction, next_footnote):
        Hippocratic.__init__(self)
        self.introduction = introduction
        self.next_footnote = next_footnote

    def xml_main(self):
        """Method to treat the optional part of the introduction.

        Modify the attribute ``xml`` to add the title section in the main XML
        """
        introduction = self.introduction.splitlines()

        # Generate the opening XML for the intro
        self.xml.append(self.xml_oss * self.xml_n_offset +
                        '<div type="intro">')
        self.xml.append(self.xml_oss * (self.xml_n_offset + 1) + '<p>')

        for line in introduction:
            if line == '':
                continue

            # Process any witnesses in this line. If this fails with a
            # IntroductionException print an error and return
            try:
                line_ref = references(line)
            except IntroductionException:
                error = ('Unable to process references in the introduction'
                         ' (line: {})'.format(line))
                logger.error(error)
                raise IntroductionException

            # Process any footnotes in line_ref. If this fails with a
            # IntroductionException print an error and return
            try:
                self.xml_n_offset += 2
                xml_main_to_add, self.next_footnote = \
                    footnotes(line_ref, self.next_footnote)
                self.xml_n_offset -= 2
            except IntroductionException:
                error = ('Unable to process footnote in the introduction'
                         ' (line: {})'.format(line))
                logger.error(error)
                raise IntroductionException

            # Add to the XML
            self.xml.extend(xml_main_to_add)

        # Add XML to close the intro section
        self.xml.append(self.xml_oss * (self.xml_n_offset + 1) + '</p>')
        self.xml.append(self.xml_oss * self.xml_n_offset + '</div>')
