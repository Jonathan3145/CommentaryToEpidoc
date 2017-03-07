"""Module which contains the function to analyse aphorism and commentaries line

There are two functions which are treating the references [W1 W2]
and the footnotes *XXX*.

The `references` function has to be used before the `footnotes`.

note: pylint analysis: 10

Authors: Jonathan Boyle, Nicolas Gruel
Copyright: IT Services, The University of Manchester
"""

import logging.config

try:
    from hyppocratic.conf import LOGGING, XML_OSS, XML_N_OFFSET
except ImportError:
    from conf import LOGGING, XML_OSS, XML_N_OFFSET

# Read logging configuration and create logger
logging.config.dictConfig(LOGGING)
# pylint: disable=locally-disabled, invalid-name
logger = logging.getLogger('hyppocratic.CommentaryToEpidoc')


# Define an Exception
class AnalysisException(Exception):
    """Class for exception
    """
    pass


def references(line):
    """
    This helper function searches a line of text for witness references
    with the form ``[WW LL]`` and returns a string containing the original
    text with each witness reference replaced with XML with the form
    ``<locus target="WW">LL</locus>``.

    ``\n`` characters are added at the start and end of each XML insertion
    so each instance of XML is on its own line.

    It is intended this function is called by function process_file()
    for each line of text from the main body of the text document before
    processing footnote references using the _footnotes() function.
    """

    # Create a string to contain the return value
    result = ''

    if not line:
        return

    while True:
        # Try to partition this line at the first '[' character
        text_before, sep, text_after = line.partition('[')

        # Note: if sep is zero there are no more witnesses to add

        # Add text_before to the result string
        if text_before != '':
            result += text_before
            # If there is a witness to add start a new line
            if sep != '':
                result += '\n'

        # If sep has zero length we can stop because there are no more
        # witness _references
        if sep == '':
            break

        # Try to split text_after at the first ']' character
        reference, sep, line = text_after.partition(']')

        # If this partition failed then something went wrong,
        # so throw an error
        if sep == '':
            error = 'Unable to partition string {} at "]" ' \
                    'when looking for a reference'.format(line)
            logger.error(error)
            raise AnalysisException

        # Partition the reference into witness and location (these are
        # separated by the ' ' character)
        witness, sep, page = reference.partition(' ')

        # If this partition failed there is an error
        if sep == '':
            error = ('Unable to partition reference {} '
                     'because missing " " '
                     'character'.format(reference))
            logger.error(error)

        # Add the witness and location XML to the result string
        result += '<locus target="' + witness.strip() + \
                  '">' + page.strip() + '</locus>'

        # If text has zero length we can stop
        if line == '':
            break
        else:
            # There is more text to process so start a new line
            result += '\n'

    return result


def footnotes(string_to_process, next_footnote):
    """
    This helper function takes a single string containing text and
    processes any embedded footnote symbols (describing additions,
    omissions, correxi, conieci and standard textual variations)
    to generate XML. It also deals with any XML generated using
    function _references().

    The output is two lists of XML, one for the main text, the other
    for the apparatus.

    Parameters
    ----------

    string_to_process: str

        This string contains the text to be processed. This should contain
        a single line from the text file being processed, e.g. a title,
        aphorism or commentary. This string may already contain XML
        generated using the _references() function i.e. XML
        identifying witnesses with each <locus> XML on a new line.

    Returns
    -------

    1. A Python list containing XML for the main text.
    2. A Python list containing XML for the critical apparatus.
    3. The number of the next footnote to be processed when this function
       complete.

    It is intended this function is called by process_file() on each line
    of text from the main document body.
    """
    # Create lists to contain the XML
    xml_main = []

    try:
        while True:
            # Use string partition to try to split this text at
            # the next footnote symbol
            footnote_symbol = '*' + str(next_footnote) + '*'
            text_before_symbol, sep, string_to_process = \
                string_to_process.partition(footnote_symbol)

            # If the partition failed sep will have zero length and the next
            # footnote is not in this line, hence we can stop
            # processing and return
            if sep == '':
                # Add text_before_symbol to the XML and stop processing
                for next_line in text_before_symbol.splitlines():
                    xml_main.append(XML_OSS * XML_N_OFFSET +
                                    next_line.strip())
                break

            # We know sep has non-zero length and we are dealing with
            # a footnote.
            # Now use string partition to try to split text_before_symbol
            # at a '#' character.
            next_text_for_xml, sep, base_text = \
                text_before_symbol.partition('#')

            # If the above partition failed the footnote refers
            # to a single word
            if sep == '':
                # Use rpartition to partition at the LAST space in the
                # string before the footnote symbol
                next_text_for_xml, sep, base_text = \
                    text_before_symbol.rpartition(' ')

            # Check we succeeded in partitioning the text before the footnote
            # at '#' or ' '. If we didn't there's an error.
            if sep == '':
                error = 'Unable to partition text before footnote symbol ' \
                        '{}'.format(footnote_symbol)
                logger.error(error)
                raise AnalysisException

            # Add the next_text_for_xml to xml_main
            for next_line in next_text_for_xml.splitlines():
                xml_main.append(XML_OSS * XML_N_OFFSET + next_line.strip())

            # Create XML for this textural variation for xml_main
            next_string = ('<app n="' +
                           str(next_footnote) +
                           '" type="footnote" xml:id="begin_fn' +
                           str(next_footnote) +
                           '"><rdg>' +
                           base_text +
                           '</rdg><anchor xml:id="end_fn' +
                           str(next_footnote) + '"/>')

            # Add next_string to the xml_main, remember this may contain '\n'
            # characters and XML from a witness reference
            for next_line in next_string.splitlines():
                xml_main.append(XML_OSS * XML_N_OFFSET + next_line)

            # Close the XML for the main text
            xml_main.append(XML_OSS * XML_N_OFFSET + '</app>')

            # Increment the footnote number
            next_footnote += 1

            # Test to see if there is any more text to process
            if string_to_process == '':
                break
    except AttributeError:
        error = 'Cannot analyse aphorysm or commentary ' \
                '{}'.format(string_to_process)
        logger.error(error)
        raise AnalysisException

    return xml_main, next_footnote
