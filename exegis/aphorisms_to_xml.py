"""
This module has been written to convert transcribed commentaries from text
files to TEI compatible XML.

Funding is provided by an ERC funded project studying Arabic commentaries on
the Hippocratic Aphorisms. The Principal Investigator is Peter E. Pormann,
The University of Manchester.

It is anticipated the module will be used via the main.py module
which attempts to to process any input file or directory containing files with
a .txt extension.

Each text file base name should end in an underscore followed by a
numerical value, e.g. file_1.txt, file_2.txt, etc. The numerical value is
subsequently used when creating the title section ``<div>`` element, e.g.
``<div n="1" type="Title_section">`` for file_1.txt.

.. note::
    This is optional, by default the version is set at 1.

If processing succeeds two XML files will be created in a folder called XML.
The XML file names start with the text file base name and end in _main.xml (for
the XML files will be file_1_main.xml and file_1_app.xml.

If processing fails error messages will be saved in the exegis.log file.

The commentaries should be utf-8 text files with the format as documented
in the associated documentation (docs/_build/index.html).

:Authors: Jonathan Boyle, Nicolas Gruel <nicolas.gruel@manchester.ac.uk>

:Copyright: IT Services, The University of Manchester
"""
# pylint: disable=locally-disabled, invalid-name
import os
import re
from lxml import etree

try:
    from .analysis import references, footnotes, AnalysisException
    from .introduction import Introduction
    from .title import Title, TitleException
    from .footnotes import Footnotes, FootnotesException
    from .baseclass import Exegis, logger, TEMPLATE_FNAME, RELAXNG_FNAME
except ImportError:
    from analysis import references, footnotes, AnalysisException
    from introduction import Introduction, IntroductionException
    from title import Title, TitleException
    from footnotes import Footnotes, FootnotesException
    from baseclass import Exegis, logger, TEMPLATE_FNAME, RELAXNG_FNAME


# Define an Exception
class AphorismsToXMLException(Exception):
    """Class for exception
    """
    pass


class Process(Exegis):
    """Class to main hypocratic aphorism text to produce a TEI XML file.

    Attributes
    ----------
    fname : str
        Name of the file to convert.
        The text file base name is expected to end with an underscore followed
        by a numerical value, e.g. file_1.txt, file_2.txt, etc. This numerical
        value is used when creating the title section <div> element, e.g.
        <div n="1" type="Title_section"> for file_1.txt.

    folder : str, optional
        Name of the folder where are the files to convert

    doc_num : int, optional
        version of the document treated.
        Default value: 1
    """
    def __init__(self,
                 fname=None,
                 folder=None,
                 doc_num=1):

        Exegis.__init__(self)
        self.folder = folder
        self.fname = fname
        self.doc_num = doc_num
        self.template_fname = TEMPLATE_FNAME
        self.relaxng_fname = None

        # Create basename file.
        if self.fname is not None:
            self.set_basename()
        else:
            self.base_name = None

        self.footnotes_app = None

        # Initialise footnote number
        self._next_footnote = 1

        # other attributes used
        self._introduction = ''
        self._title = ''
        self._aph_com = {}  # aphorism and commentaries
        self._text = ''
        self.footnotes = ''
        self._n_footnote = 1
        self.template = ''

        # Initialisation of the xml_main and xml_app list
        # They are created here and not in the __init__ to have
        # the reinitialisation where it is needed.

    def set_basename(self):
        """Method to set the basename attribute if fname is not None
        """
        self.base_name = os.path.splitext(os.path.basename(self.fname))[0]

        # Create folder for XML
        if not os.path.exists('XML'):
            os.mkdir('XML')

        # Set XML file name
        self.xml_file = os.path.join('XML', self.base_name + '.xml')

    def open_document(self, fname=None):
        """Method to open and read the exegis document.

        Parameters
        ----------
        fname : str, optional
            name of the file to analyse.

        Attributes
        ----------
        folder : str, optional
            Name of the folder where are the files to convert

        fname : str
            Name of the file to convert.
            The text file base name is expected to end with an underscore
            followed by a numerical value, e.g. file_1.txt, file_2.txt, etc.
            This numerical value is used when creating the title section
            <div> element, e.g. <div n="1" type="Title_section">
            for file_1.txt.

        text : str
            string which contains the whole file in utf-8 format.

        Raises
        ------
        AphorismsToXMLException
            if document can not be:
                - open
                - there subfolder present in the folder
                - file not treatable by the software (e.g. .DS_Store)
                - file does not exist
        """
        if fname is not None:
            self.folder, self.fname = os.path.split(fname)
            self.set_basename()

        if self.base_name is None and self.fname is not None:
            self.set_basename()

        if self.folder is None:
            self.folder = '.'

        if self.base_name is None:
            logger.error("There are no file to convert.")
            raise AphorismsToXMLException

        full_path = os.path.join(self.folder, self.fname)
        if os.path.isdir(full_path):
            logger.info('The software does not treat subfolder.')
            raise AphorismsToXMLException

        # Extract the document number, it is expected this is at the end of the
        # base name following an '_'
        try:
            sep, doc_num = self.base_name.rpartition('_')[1:]
            self.doc_num = int(doc_num)
            if sep == '':
                raise AphorismsToXMLException
        except ValueError:
            info = ('File name {} does not provide version information. '
                    'Use version 1 by default'.format(self.fname))
            logger.info(info)

        # Open the file to process
        # pylint: disable=locally-disabled, invalid-name
        try:
            with open(full_path, 'r', encoding="utf-8") as f:
                # Read in file
                self._text = f.read().strip()
        except UnicodeDecodeError:
            info = ('File {} is not treatable by the software'.format(
                self.fname))
            logger.info(info)
            raise AphorismsToXMLException
        except FileNotFoundError:
            info = ('File {} does not exist'.format(self.fname))
            logger.info(info)
            raise AphorismsToXMLException

    def divide_document(self):
        """Method to divide the document in the three main parts.

        An exegis document si composed in three or four main parts:

        - The introduction (optional)
        - The title
        - The aphorisms
        - The footnotes

        This method will divide the document in the three or four parts.

        Attributes
        ----------
        _introduction : str
            A string which contains the introduction of the document if present

        _title : str
            A string which contains the title of the document

        _text : str
            A string which contains the aphorisms and commentaries
            of the document

        _footnotes : str
            A string which contains the footnotes of the document

        Raises
        ------
        AphorismsToXMLException
            if it is not possible to divide the document.
        """

        # Not sure that is the best way to do but this is just a trial

        # cut the portion of the test, starting from the end, until the
        # characters footnotes_sep
        footnotes_sep = '*1*'
        loc_footnotes = self._text.rfind(footnotes_sep)

        if loc_footnotes == self._text.find(footnotes_sep):
            logger.error('Footnote referenced in the text but '
                         'no footnote section present.')
            self.footnotes = ''
            raise AphorismsToXMLException

        if loc_footnotes != -1:
            self.footnotes = self._text[loc_footnotes:].strip()
            self._text = self._text[:loc_footnotes]
        else:
            logger.info('There are no footnotes present.')

        # Cut the intro (if present)
        try:
            p = re.compile(r'\+\+\n')
            _tmp = p.split(self._text)
            if len(_tmp) == 3:
                self._title = _tmp[0].strip()
                self._introduction = _tmp[1].strip()
                self._text = _tmp[2].strip()
            elif len(_tmp) == 2:
                self._introduction = _tmp[0].strip()
                self._text = _tmp[1].strip()
        except ValueError as e:
            raise AphorismsToXMLException(e)

        try:
            p = re.compile(r'\n\s{0,}1\.?\n')
            if self._title == '':
                _tmp = p.split(self._text)
                self._title = _tmp[0]
                self._text = '1.\n' + '1.\n'.join(_tmp[1:])
        except ValueError as e:
            logger.error('Aphorism should have numeration as 1. or 1')
            raise AphorismsToXMLException(e)

        return

    def aphorisms_dict(self):
        """Create an order dictionary (OrderedDict object) with the aphorisms
        and commentaries.

        Attributes
        ----------
        _aph_com : dict
            dictionary which contains the aphorisms and the commentaries
            associated.

        Raises
        ------
        AphorismsToXMLException
            if it is not possible to create the dictionary.
        """
        aphorism = re.split(r'\n\s{0,}[0-9]+\.?\n', '\n' + self._text)[1:]

        # Split the text in function of the numbers (i.e. the separation
        # of the aphorism.
        # '\s[0-9]+.\n' means 'find string :
        #    which start with end of line or any space character
        #    with at least on number ending
        #    with a point and a end of line.
        p = re.compile(r'\n\s{0,}?[0-9]+\.?\n')
        error = ''
        try:
            n_aphorism = [int(i.group().strip('.\t\n '))
                          for i in p.finditer('\n' + self._text)]
            # Find missing aphorism or badly written (e.g.: 14-)
            missing = [i for i in list(range(1, max(n_aphorism)))
                       if i not in n_aphorism]
            # Find if multiple aphorism with the same number.
            doublon = list({i for i in n_aphorism if n_aphorism.count(i) > 1})
            if not n_aphorism:
                error = 'There are no aphorisms detected'
                logger.error(error)
            if max(n_aphorism) != len(n_aphorism):
                error = 'N aphorism expected {}, got: {}'.format(
                    n_aphorism[-1],
                    len(n_aphorism)
                )
                logger.error(error)
            if missing:
                error = 'Missing or problematic aphorism: {}'.format(missing)
                logger.error(error)
                warning = ('Last aphorism can be problematic but '
                           'not detected by the software.')
                logger.warning(warning)
            if doublon:
                error = 'Aphorism with same number: {}'.format(doublon)
                logger.error(error)
            if error:
                raise AphorismsToXMLException(error)
        except ValueError:
            error = ('Aphorism numeration format probably does not respect '
                     'the convention. '
                     'It should be a number following by a point')
            logger.error(error)
            raise AphorismsToXMLException
        except AphorismsToXMLException as e:
            raise AphorismsToXMLException(e)

        # create the dictionary with the aphorism (not sure that we need
        # the ordered one)
        # use n_aphorism to be sure that there are no error

        try:
            self._aph_com = {}
            for i, aph in enumerate(aphorism):
                self._aph_com[n_aphorism[i]] = [s.strip()
                                                for s in aph.split('\n')
                                                if len(s) != 0]
        except (IndexError, AphorismsToXMLException):
            error = ('Problem in the creation of the dictionary which'
                     'which contains the aphorisms')
            logger.error(error)
            raise AphorismsToXMLException

    def read_template(self):
        """Method to read the XML template used for the transformation

        Attributes
        ----------
        template : str
            Contain the text of the XML template provided.

        Raises
        ------
        AphorismsToXMLException
            if template cannot be found or read.
        """
        # Open the template file. Kill the process if not there.
        # Template is not optional.

        try:
            with open(self.template_fname, 'r', encoding="utf-8") as f:
                self.template = f.read()
                info = 'Template file {} found.'.format(self.template_fname)
                logger.info(info)
        except FileNotFoundError:
            error = 'Template file {} not found.'.format(self.template_fname)
            logger.error(error)
            raise AphorismsToXMLException

        if self.relaxng_fname is None:
            tree = etree.parse(self.template_fname)
            root = tree.getroot()
            model = root.xpath("/processing-instruction('xml-model')")[0]

            self.relaxng_fname = model.text.split('"')[1]

        logger.info('Relaxng file '
                    'use for validation: {} '.format(self.relaxng_fname))

    def _create_xml(self):

        if self.template == '':
            self.read_template()

        xml = self.template

        if self.wits:
            wits = set(self.wits)
            wits = list(wits)
            wits.sort()
            info = 'Witnesses found in the aphorisms and ' \
                   'commentaries {}'.format(wits)
            logger.info(info)
            _wits = []
            for w in wits:
                _wits.append(self.xml_oss * self.xml_n_offset +
                             '<witness> {} </witness>'.format(w))
            xml = re.sub('#INSERTWITNESSES#', '\n'.join(_wits), xml)

        if self.xml:
            xml = re.sub('#INSERTBODY#', '\n'.join(self.xml), xml)
        if self.app:
            xml = re.sub('#INSERTAPP#', '\n'.join(self.app), xml)

        self.xml = xml

    def _validate_xml(self):

        try:
            relaxng_doc = etree.parse(self.relaxng_fname)
        except OSError:
            relaxng_doc = etree.parse(RELAXNG_FNAME)
            self.relaxng_fname = RELAXNG_FNAME

        relaxng = etree.RelaxNG(relaxng_doc)
        xml = etree.parse(self.xml_file)
        # relaxng.validate(xml)
        # if not relaxng(xml):
        #     logger.error("INVALID")
        # else:
        #     logger.error(self.xml_file)
        #     logger.error("VALID")

        try:
            relaxng.assertValid(xml)
            logger.info('The document {} created is '
                        'valid corresponding '
                        'to the Relaxng declared '
                        'or used'.format(self.xml_file))

        except etree.DocumentInvalid:
            logger.error('The document {} created is '
                         'not valid corresponding '
                         'to the Relaxng declared '
                         'or used'.format(self.xml_file))
            raise AphorismsToXMLException

    def treat_footnotes(self):
        """Method to treat Footnote.

        Work even if division of the document didn't work properly but
        for the footnotes part.
        """
        if not self.footnotes == '':
            # In most of the file the footnote will be present and can be
            # treated independently from the aphorism.

            # Treat the footnote part and create the XML app
            try:
                self.footnotes_app = Footnotes(self.footnotes)
            except FootnotesException:
                raise AphorismsToXMLException from None
            logger.info('Footnotes treated')

            # Create XML app
            self.footnotes_app.xml_app()
            self.app = self.footnotes_app.xml
            self.wits = self.footnotes_app.wits
            logger.info('Footnotes app file created')

    def main(self):
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

        Modify the attribute ``xml`` to add the title section in the main XML

        Raises
        ------
        AphorismsToXMLException
            if the processing of the file does not work as expected.

        """

        # Open and read the exegis document
        self.open_document()

        debug = 'Open document {}'.format(self.fname)
        logger.debug(debug)

        # Divide the document in the different part (intro, title,
        # text, footnotes)

        try:
            self.divide_document()
            logger.info('Division of the document ok.')
        except AphorismsToXMLException:
            logger.error('Division of the document failed.')
            raise AphorismsToXMLException

        self.treat_footnotes()

        self.aphorisms_dict()
        logger.info('Created aphorisms dictionary')

        if self._introduction != '':
            try:
                intro = Introduction(self._introduction, self._next_footnote)
                intro.xml_main()
                self._next_footnote = intro.next_footnote
                self.xml += intro.xml
                logger.debug('Introduction treated')
            except IntroductionException:
                raise AphorismsToXMLException from None

        # Deal with the first block of text which should contain
        # an optional intro
        # and the title
        # =======================================================

        try:
            title = Title(self._title, self._next_footnote, self.doc_num)
        except TitleException:
            raise AphorismsToXMLException from None
        logger.debug('Title treated')

        title.xml_main()
        logger.debug('Title xml created')

        self._next_footnote = title.next_footnote

        # Add title to the xml main
        self.xml += title.xml

        # Now process the rest of the main text
        # =====================================
        logger.debug('Start aphorisms and commentaries treatment')
        for k in self._aph_com:
            if not len(self._aph_com[k]):
                error = ('There are no aphorisms  in the file. '
                         'It can be because of the numeration. '
                         'Verify that the it is starting at 1 or 1. not .1 '
                         '(the point can be after the number but not before.')
                logger.error(error)
                raise AphorismsToXMLException

            aphorism = self._aph_com[k][0]
            commentaries = self._aph_com[k][1:]

            # Add initial XML for the aphorism + commentary unit
            self.xml.append(self.xml_oss * self.xml_n_offset + '<div n="' +
                            str(k) + '" type="aphorism_commentary_unit">')

            # Add initial XML for this aphorism
            self.xml.append(self.xml_oss * (self.xml_n_offset + 1) +
                            '<div type="aphorism">')
            self.xml.append(self.xml_oss * (self.xml_n_offset + 2) + '<p>')

            # Now process any witnesses in it. If this fails with an
            # Exception print an error and return
            try:
                line_ref = references(aphorism)
            except AnalysisException:
                error = ('Unable to process references in '
                         'aphorism {}'.format(k))
                logger.error(error)
                raise AphorismsToXMLException from None

            if line_ref is None or line_ref == '':
                continue

            # Process any footnotes in line_ref, if there are errors write
            # to the log file and return
            try:
                self.xml_n_offset += 3
                xml_main_to_add, self._next_footnote = \
                    footnotes(line_ref, self._next_footnote)
                self.xml_n_offset -= 3
            except (TypeError, AnalysisException):
                error = ('Unable to process footnotes in '
                         'aphorism {}'.format(k))
                logger.error(error)
                raise AphorismsToXMLException from None

            # Add the XML
            self.xml.extend(xml_main_to_add)

            # Close the XML for the aphorism
            self.xml.append(self.xml_oss * (self.xml_n_offset + 1) + '</p>')
            self.xml.append(self.xml_oss * self.xml_n_offset + '</div>')

            # Get the next line of text
            for n_com, line in enumerate(commentaries):

                # Workaround footnote on first word
                line = ' ' + line

                if line[-1] != '.':

                    debug = ('Commentaries should ended with a `.`\n'
                             'Warning in aphorism {}\n'
                             'commentary {}'.format(k, line))
                    logger.debug(debug)

                # Add initial XML for this aphorism's commentary
                self.xml.append(self.xml_oss * self.xml_n_offset +
                                '<div type="commentary">')
                self.xml.append(self.xml_oss * (self.xml_n_offset + 1) + '<p>')

                # Now process any witnesses in this line. If this fails with a
                # CommentaryToEpidocException and log an error
                try:
                    line_ref = references(line)
                except AnalysisException:
                    error = ('Unable to process references, '
                             'commentary {} for aphorism '
                             '{}'.format(n_com+1, k))
                    logger.error(error)
                    raise AphorismsToXMLException from None

                # Process any _footnotes in line_ref. If this fails with a
                # CommentaryToEpidocException and log an error
                try:
                    self.xml_n_offset += 3
                    xml_main_to_add, self._next_footnote = \
                        footnotes(line_ref, self._next_footnote)
                    self.xml_n_offset -= 3
                except (TypeError, AnalysisException):
                    error = ('Unable to process footnote, '
                             'commentary {} for aphorism '
                             '{}'.format(n_com+1, k))
                    logger.error(error)
                    raise AphorismsToXMLException from None

                # Add the XML
                self.xml.extend(xml_main_to_add)

                # Close the XML for this commentary
                self.xml.append(self.xml_oss * (self.xml_n_offset + 1) +
                                '</p>')
                self.xml.append(self.xml_oss * self.xml_n_offset +
                                '</div>')

            # Close the XML for the aphorism + commentary unit
            self.xml.append(self.xml_oss * self.xml_n_offset + '</div>')

        logger.debug('Finish aphorisms and commentaries treatment')
        # Save the xmls created

        self._create_xml()
        self.save_xml(self.xml_file)
        self._validate_xml()
        logger.debug('Save main xml')
