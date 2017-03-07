"""
This module has been written to convert transcribed commentaries from text
files to EpiDoc compatible XML, see http://www.stoa.org/epidoc/gl/latest/
and http://sourceforge.net/p/epidoc/wiki/Home/ for more information on EpiDoc.

Funding is provided by an ERC funded project studying Arabic commentaries on
the Hippocratic Aphorisms. The Principal Investigator is Peter E. Pormann,
The University of Manchester.


It is anticipated the module will be used via the function process_text_files()
which attempts to to process any file with a .txt extension within a specified
directory. Each text file base name should end in an underscore followed by a
numerical value, e.g. file_1.txt, file_2.txt, etc. The numerical value is
subsequently used when creating the title section <div> element, e.g.
<div n="1" type="Title_section"> for file_1.txt.

If processing succeeds two XML files will be created in a folder called XML.
The XML file names start with the text file base name and end in _main.xml (for
the XML files will be file_1_main.xml and file_1_app.xml.

If processing fails error messages will be saved in the hyppocratic.log file.

The commentaries should be utf-8 text files with the format as documented
in the associated documentation (doc/_build/index.html).

Authors: Jonathan Boyle, Nicolas Gruel
Copyright: IT Services, The University of Manchester
"""

# Import the string and os modules
import os
import sys
import re
import logging.config

try:
    from hyppocratic.analysis import references, footnotes, AnalysisException
    from hyppocratic.introduction import Introduction
    from hyppocratic.title import Title
    from hyppocratic.footnotes import Footnotes, FootnotesException
    from hyppocratic.conf import LOGGING
    from hyppocratic.baseclass import Hyppocratic
except ImportError:
    from analysis import references, footnotes, AnalysisException
    from introduction import Introduction
    from title import Title
    from footnotes import Footnotes, FootnotesException
    from conf import LOGGING
    from baseclass import Hyppocratic

# Read logging configuration and create logger
logging.config.dictConfig(LOGGING)
# pylint: disable=locally-disabled, invalid-name
logger = logging.getLogger('hyppocratic.CommentaryToEpidoc')


# Define an Exception
class CommentaryToEpidocException(Exception):
    """Class for exception
    """
    pass


class Process(Hyppocratic):
    """Class to process hypocratic aphorysm text to produce a TEI XML file.

    Attributes
    ----------

    folder: str, optional
        Name of the folder where are the files to convert

    fname: str
        Name of the file to convert.
        The text file base name is expected to end with an underscore followed
        by a numerical value, e.g. file_1.txt, file_2.txt, etc. This numerical
        value is used when creating the title section <div> element, e.g.
        <div n="1" type="Title_section"> for file_1.txt.

    template_folder: str, optional
        Name of the folder where are the XML template is located

    template_marker: str, optional
            string which will be replace in the template file.
            Default=``#INSERT#``

    template_fname: str, optional
        The name of the XML template file containing the string
        ``#INSERT#`` at the location in which to insert XML for the
        ``<body>`` element.

    next_footnote: int

    introduction: str

    title: str
    text: str
    footnotes: str
    n_footnote: int
    template_part1: str
    template_part2: str
    doc_num: int

    # Initialisation of the xml_main and xml_app list
    # They are created here and not in the __init__ to have
    # the reinitialisation where it is needed.
    xml_main = []
    xml_app = []

    """

    def __init__(self,
                 fname=None,
                 folder=None,
                 doc_num=None,
                 template_folder='.',
                 template_fname='xml_template.txt',
                 template_marker='#INSERT#'):
        Hyppocratic.__init__(self)
        self.folder = folder
        self.fname = fname
        self.doc_num = doc_num
        self.template_folder = template_folder
        self.template_fname = template_fname
        self.template_marker = template_marker
        self.footnotes_app = None

        # Create basename file.
        if self.fname is not None:
            self.setbasename()
        else:
            self.base_name = None

        # Initialise footnote number
        self.next_footnote = 1

        # other attributes used
        self.introduction = ''
        self.title = ''
        self.aph_com = {}  # aphorism and commentaries
        self.text = ''
        self.footnotes = ''
        self.n_footnote = 1
        self.template_part1 = ''
        self.template_part2 = ''

        # Initialisation of the xml_main and xml_app list
        # They are created here and not in the __init__ to have
        # the reinitialisation where it is needed.

    def setbasename(self):
        """Method to set the basename attribute if fname is not None
        """
        self.base_name = os.path.splitext(os.path.basename(self.fname))[0]

    def open_document(self, fname=None):
        """Method to open and read the hyppocratic document.

        Parameters
        ----------
        fname: str, optional
            name of the file to analyse.

        Attributes
        ----------
        self.folder: str, optional
            Name of the folder where are the files to convert

        self.fname: str
            Name of the file to convert.
            The text file base name is expected to end with an underscore
            followed by a numerical value, e.g. file_1.txt, file_2.txt, etc.
            This numerical value is used when creating the title section
            <div> element, e.g. <div n="1" type="Title_section"> for file_1.txt.

        self.text: str
            string which contains the whole file in utf-8 format.
        """
        if fname is not None:
            self.folder, self.fname = os.path.split(fname)
            self.setbasename()

        if self.base_name is None and self.fname is not None:
            self.setbasename()

        if self.folder is None:
            self.folder = '.'

        if self.base_name is None:
            logger.error("There are no file to convert.")
            raise CommentaryToEpidocException

        # Extract the document number, it is expected this is at the end of the
        # base name following an '_'
        if self.doc_num is None:
            try:
                sep, doc_num = self.base_name.rpartition('_')[1:]
                self.doc_num = int(doc_num)
                if sep == '':
                    raise CommentaryToEpidocException
            except ValueError:
                self.doc_num = 1
                info = ('File name {} does not provide version information. '
                        'Use version 1 by default'.format(self.fname))
                logger.info(info)

        # Open the file to process
        # pylint: disable=locally-disabled, invalid-name
        with open(os.path.join(self.folder, self.fname), 'r',
                  encoding="utf-8") as f:
            # Read in file
            self.text = f.read().strip()

    def divide_document(self):
        """Method to divide the document in the three main parts.

        An hyppocratic document si composed in three or four main parts:

        - The introduction (optional)
        - The title
        - The aphorisms
        - The footnotes

        This method will divide the document in the three or four parts.

        Attributes
        ----------
        self.introduction: str
            A string which contains the introduction of the document if present
        self.title: str
            A string which contains the title of the document
        self.text: str
            A string which contains the aphorisms and commentaries
            of the document
        self.footnotes: str
            A string which contains the footnotes of the document
        """

        # Not sure that is the best way to do but this is just a trial

        # cut the portion of the test, starting from the end, until the
        # characters footnotes_sep
        footnotes_sep = '*1*'
        loc_footnotes = self.text.rfind(footnotes_sep)

        if loc_footnotes == self.text.find(footnotes_sep):
            logger.error('Footnote referenced in the text but '
                         'no footnote section present.')
            self.footnotes = ''
            raise CommentaryToEpidocException

        if loc_footnotes != -1:
            self.footnotes = self.text[loc_footnotes:].strip()
            self.text = self.text[:loc_footnotes]
        else:
            logger.info('There are no footnotes present.')

        # Cut the intro (if present)
        intro_sep = '++\n'
        loc_intro = self.text.find(intro_sep, 3)
        # Cut the intro (remove the '++\n' at the beginning and the end.
        if loc_intro != -1:
            self.introduction = self.text[3:loc_intro].strip()
            self.text = self.text[loc_intro+3:]
        else:
            logger.info('There are no introduction present.')

        try:
            p = re.compile(r'\s+1\.?\n')
            self.title, self.text = p.split(self.text)
            self.text = '1.\n' + self.text
        except ValueError as e:
            raise CommentaryToEpidocException(e)

    #     def analysis_aphorism_dict(self, com):
#         """Create an ordered dictionary with the different witness and
#          footnotes present in a commentary
#
#         Returns
#         -------
#
#         """
#         # Find all the witnesses in the line
#         # Note on the regex:
#         #     \w = [a-AA-Z0-9_]
#         #     \s = any king of space
#         #     + = one or more
#         # It match all the witness with form like [WWWWW XXXXX]
#
#         # find all the footnote in the line
#         # It match all the footnote marker like *XXX*
#         p_foot = re.compile(r'\*\d+\*')
#         footnotes = p_foot.finditer(com)
#         footnotes = {int(i.group().strip('*')): i.span() for i in footnotes}
#
#         p_wits = re.compile(r'\[\w+\s+\w+\]')
#         # wits = p.findall(com)
#         wits = p_wits.finditer(com)
#         wits = {i.group().strip('*'): i.span() for i in wits}
#
#         return footnotes, wits, com
# #        return footnotes, wits, span_f

    def aphorisms_dict(self):
        """Create an order dictionary (OrderedDict object) with the aphorisms
        and commentaries.
        """

        # \n\d+.\n == \n[0-9]+.\n (\d == [0-9])
        aphorism = re.split(r'\s+[0-9]+\.?\n', '\n' + self.text)[1:]

        # n_aphorism = [int(i.strip('\n').strip('.')) for i in
        #               re.findall('\n[0-9]+.\n', '\n' + self.text)]

        # n_aphorism = [int(i.group().strip('\n').strip('.')) for i in
        #               re.finditer('\n[0-9]+.\n', '\n' + self.text)]

        # Split the text in function of the numbers (i.e. the separation
        # of the aphorism.
        # '\s[0-9]+.\n' means 'find string :
        #    which start with end of line or any space characer
        #    with at least on number ending
        #    with a point and a end of line.
        p = re.compile(r'\s+[0-9]+.?\n')
        try:
            n_aphorism = [
                int(i.group().strip('.\t\n '))
                for i in p.finditer('\n' + self.text)]
            if not n_aphorism:
                raise CommentaryToEpidocException
        except (ValueError, CommentaryToEpidocException):
            error = ("aphorism format does not respect the convention. "
                     "It should be a number following by a point")
            logger.error(error)
            debug = "we got:\n{}".format(self.text.splitlines()[:2])
            logger.debug(debug)
            raise CommentaryToEpidocException

        # create the dictionary with the aphorism (not sure that we need
        # the ordered one)
        # use n_aphorism to be sure that there are no error

        try:
            self.aph_com = {}
            for i, aph in enumerate(aphorism):
                self.aph_com[n_aphorism[i]] = [s.strip()
                                               for s in aph.split('\n')
                                               if len(s) != 0]
        except (IndexError, CommentaryToEpidocException):
            error = ('Problem in the creation of the dictionary which'
                     'which contains the aphorisms')
            logger.error(error)
            raise CommentaryToEpidocException

    def read_template(self):
        """Method to read the XML template used for the transformation

        Attribute
        ---------

        template: str

            Contain the text of the XML template provided.

        Exception
        ---------
        SystemExit if template cannot be read.
        """
        _template = os.path.join(self.template_folder, self.template_fname)
        # Open the template file. Kill the process if not there.
        # Template is not optional.

        try:
            with open(_template, 'r', encoding="utf-8") as f:
                template = f.read()
                info = 'Template file {} found in the folder {}.'.format(
                    self.template_fname, self.folder)
                logger.info(info)
        except FileNotFoundError:
            error = 'Template file {} not found in folder {}'.format(
                self.template_fname, self.template_folder)
            logger.error(error)
            sys.exit(1)

        # Split the template at template_marker
        self.template_part1, sep, self.template_part2 = template.partition(
            self.template_marker)

        # Test the split worked
        if sep == '':
            error = ('Unable to find template marker text ({}) '
                     'in the template file {} '
                     'located in the folder {}.'.format(self.template_marker,
                                                        self.template_fname,
                                                        self.template_folder))
            logger.error(error)
            sys.exit(1)

        logger.debug('Template file splitted.')

    def save_xml(self):
        """Method to save the XML files expected

        Two XML files are created as result to the transformation in the EPIDOC
        format

        Exceptions
        ==========

        """
        # Create folder for XML
        if not os.path.exists('XML'):
            os.mkdir('XML')

        # Embed xml_main into the XML in the template
        if self.template_part1 == '':
            self.read_template()

        # Set XML file name
        xml_main_file = os.path.join('XML', self.base_name + '_main.xml')
        xml_app_file = os.path.join('XML', self.base_name + '_app.xml')

        # Save main XML to file
        with open(xml_main_file, 'w', encoding="utf-8") as f:
            f.write(self.template_part1)
            for s in self.xml:
                f.write(s + '\n')
            f.write(self.template_part2)

        # Save app XML to file
        if self.footnotes_app is not None:
            self.footnotes_app.save_xml(xml_app_file)

    def treat_footnotes(self):
        """Method to treat Footnote.

        Work even if division of the document didn't work properly but
        for the footnotes part.
        """
        if not self.footnotes == '':
            # In most of the file the footnote will be present and can be
            # treated independently from the aphorism.

            # Treat the footnote part and create the XML app
            self.footnotes_app = Footnotes(self.footnotes)
            logger.info('Footnotes treated')

            # Create XML app
            self.footnotes_app.xml_app()
            logger.info('Footnotes app file created')

    def process_file(self):
        """
        A function to process a text file containing symbols representing
        references to witnesses and symbols and footnotes defining textual
        variations, omissions, additions, correxi or conieci. This function
        uses these symbols to produce files containing EpiDoc compatible XML.

        If processing succeeds two XML files will be created in folder ./XML
        with file names that start with the text file base name and ending in
        _main.xml (for the main XML) and _apps.xml (for the apparatus XML).
        For example for file_1.txt the XML files will be file_1_main.xml and
        file_1_app.xml.

        Error messages are saved in a file in the ./errors folder.

        After successful processing the function returns True, if an error
        is detected this function returns False.

        It is intended this function is called by process_folder().
        """

        # Open and read the hyppocratic document
        self.open_document()

        debug = 'Open document {}'.format(self.fname)
        logger.debug(debug)

        # Divide the document in the different part (intro, title,
        # text, footnotes)

        try:
            self.divide_document()
            logger.info('Division of the document ok.')
            self.treat_footnotes()
            self.footnotes_app.save_xml()
        except CommentaryToEpidocException:
            logger.error('Division of the document failed.')
            self.treat_footnotes()
            raise CommentaryToEpidocException

        self.aphorisms_dict()
        logger.info('Created aphorisms dictionary')

        if self.introduction != '':
            intro = Introduction(self.introduction, self.next_footnote)
            intro.xml_main()
            self.next_footnote = intro.next_footnote
            self.xml += intro.xml
            logger.debug('Introduction treated')

        # Deal with the first block of text which should contain
        # an optional intro
        # and the title
        # =======================================================

        title = Title(self.title, self.next_footnote, self.doc_num)
        logger.debug('Title treated')

        title.xml_main()
        logger.debug('Title xml created')

        self.next_footnote = title.next_footnote

        # Add title to the xml main
        self.xml += title.xml

        # Now process the rest of the main text
        # =====================================
        logger.debug('Start aphorisms and commentaries treatment')
        for k in self.aph_com:

            aphorism = self.aph_com[k][0]
            commentaries = self.aph_com[k][1:]

            # Add initial XML for the aphorism + commentary unit
            self.xml.append(self.xml_oss * self.xml_n_offset + '<div n="' +
                            str(k) + '" type="aphorism_commentary_unit">')

            # Add initial XML for this aphorism
            self.xml.append(self.xml_oss * (self.xml_n_offset + 1) +
                            '<div type="aphorism">')
            self.xml.append(self.xml_oss * (self.xml_n_offset + 2) + '<p>')

            # Now process any witnesses in it. If this fails with a
            # CommentaryToEpidocException print an error and return
            try:
                line_ref = references(aphorism)
            except AnalysisException:
                error = ('Unable to process _references in '
                         'aphorism {}'.format(k))
                logger.error(error)
                raise CommentaryToEpidocException from None

            # Process any footnotes in line_ref, if there are errors write
            # to the log file and return
            try:
                self.xml_n_offset += 3
                xml_main_to_add, self.next_footnote = \
                    footnotes(line_ref, self.next_footnote)
                self.xml_n_offset -= 3
            except (TypeError, AnalysisException):
                error = ('Unable to process footnotes in '
                         'aphorism {}'.format(k))
                logger.error(error)
                raise CommentaryToEpidocException from None

            # Add the XML
            self.xml.extend(xml_main_to_add)

            # Close the XML for the aphorism
            self.xml.append(self.xml_oss * (self.xml_n_offset + 2) + '</p>')
            self.xml.append(self.xml_oss * (self.xml_n_offset + 1) + '</div>')

            # Get the next line of text
            for n_com, line in enumerate(commentaries):

                # Workaround footnote on first word
                line = ' ' + line

                if line[-1] != '.':

                    warning = ('Commentaries should ended with a `.`\n'
                               'Warning in aphorism {}\n'
                               'commentary {}'.format(k, line))
                    logger.warning(warning)

                # Add initial XML for this aphorism's commentary
                self.xml.append(self.xml_oss * (self.xml_n_offset + 1) +
                                '<div type="commentary">')
                self.xml.append(self.xml_oss * (self.xml_n_offset + 2) + '<p>')

                # Now process any witnesses in this line. If this fails with a
                # CommentaryToEpidocException and log an error
                try:
                    line_ref = references(line)
                except AnalysisException:
                    error = ('Unable to process _references,'
                             'commentary {} for aphorism '
                             '{}'.format(n_com, k))
                    logger.error(error)
                    raise CommentaryToEpidocException from None

                # Process any _footnotes in line_ref. If this fails with a
                # CommentaryToEpidocException and log an error
                try:
                    self.xml_n_offset += 3
                    xml_main_to_add, self.next_footnote = \
                        footnotes(line_ref, self.next_footnote)
                    self.xml_n_offset -= 3

                except (TypeError, AnalysisException):
                    error = "Unable to proceed Aphorism {}".format(k)
                    logger.error(error)
                    raise CommentaryToEpidocException from None

                # Add the XML
                self.xml.extend(xml_main_to_add)

                # Close the XML for this commentary
                self.xml.append(self.xml_oss * (self.xml_n_offset + 2) + '</p>')
                self.xml.append(self.xml_oss * (self.xml_n_offset + 1) +
                                '</div>')

            # Close the XML for the aphorism + commentary unit
            self.xml.append(self.xml_oss * self.xml_n_offset + '</div>')

        logger.debug('Finish aphorisms and commentaries treatment')
        # Save the xmls created
        self.save_xml()
        logger.debug('Save main xml')

    def reset(self):
        """Reset some of the attributes to be use with process_folder
        """
        self.doc_num = None
        self.introduction = ''
        self.n_footnote = 1
        self.next_footnote = 1
        self.xml = []

    def process_folder(self, folder=None):
        """
        A function to process all files with the .txt extension in a directory.
        These files are expected to be utf-8 text files containing symbols
        representing references to witnesses and symbols and footnotes defining
        textual variations, omissions, additions, correxi or conieci.
        For each text file this function will attempt to use the symbols
        to produce files containing EpiDoc compatible XML.

        The text file base name is expected to end with an underscore followed
        by a numerical value, e.g. file_1.txt, file_2.txt, etc.
        This numerical value is used when creating the title section
        <div> element, e.g. <div n="1" type="Title_section"> for file_1.txt.

        If processing succeeds two XML files will be created in folder ./XML
        with file names starting with the text file base name and ending
        in _main.xml (for the main XML) and _apps.xml (for the apparatus XML).
        For example for file_1.txt the XML files will be file_1_main.xml and
        file_1_app.xml.

        Parameters
        ----------

        folder: str, optional
            The folder containing the text file
        """

        if folder is not None:
            self.folder = folder

        # Test that the working folder exists
        if not os.path.exists(self.folder):
            error = 'Error: path {} for text files ' \
                    'not found'.format(self.folder)
            logger.error(error)
            raise CommentaryToEpidocException

        files = os.listdir(self.folder)

        for fname in files:
            if fname.endswith('.txt'):
                info = 'Processing: "{}"'.format(fname)
                logger.info(info)
                try:
                    self.reset()
                    self.fname = fname
                    self.setbasename()
                    self.process_file()
                except (CommentaryToEpidocException, FootnotesException,
                        AnalysisException):
                    error = 'Error: unable to process "{}", ' \
                            'see log file.'.format(self.fname)
                    logger.error(error)
        return True
