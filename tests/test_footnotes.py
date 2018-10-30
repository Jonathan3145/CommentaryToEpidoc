import os
import sys
from collections import OrderedDict
import pytest
from testfixtures import LogCapture
import logging

from .conftest import Footnote, Footnotes, FootnotesException


file_path = os.path.realpath(__file__)
path = os.path.dirname(file_path)
sys.path.append(path)

path_testdata = os.path.join(path, 'test_files') + os.sep
# examples = os.path.join(path, '..', 'Examples', 'TextFiles') + os.sep
template_file = os.path.join(path, '..', 'exegis', 'template',
                             'xml_template.txt')


# ################# _omission ###################

def test_omission():
    """
    Runs the function _omission(...) on the text in
    test_process_omission.in, and compare the output against the text in
    test_process_omission.ref
    """

    ft = Footnote()
    # Load text from input file
    with open(path_testdata + 'test_process_omission.in', 'r',
              encoding="utf-8") as f:
        text_in = f.read()

    # Load text from reference file
    with open(path_testdata + 'test_process_omission.ref', 'r',
              encoding="utf-8") as f:
        text_ref = f.read()

    # Run the function with the input
    ft.footnote = text_in
    ft.xml = []
    ft.omission()

    # Convert the output list to a string with each element on a new line
    # This is not good in a test you should not modify the results
    # before the test.
    text_out = '\n'.join(ft.xml)

    assert text_out == text_ref


def test_omission_bad_first_split():
    """Test coverage
    """
    ft = Footnote()
    ft.footnote = 'addd]'
    ft.omission()


def test_omission_and_correxi():
    """
    Runs the function _omission(...) on the text in
    test_process_omission.in, and compare the output against the text in
    test_process_omission.ref
    """

    ft = Footnote()
    # Load text from input file
    with open(path_testdata + 'test_omission_and_correxi.in', 'r',
              encoding="utf-8") as f:
        text_in = f.read()

    # Load text from reference file
    with open(path_testdata + 'test_omission_and_correxi.ref', 'r',
              encoding="utf-8") as f:
        text_ref = f.read()

    # Run the function with the input
    ft.footnote = text_in
    ft.xml = []
    ft.omission()

    # Convert the output list to a string with each element on a new line
    # This is not good in a test you should not modify the results
    # before the test.
    text_out = '\n'.join(ft.xml)

    assert text_out == text_ref


def test_omission_and_conieci():
    """
    Runs the function _omission(...) on the text in
    test_process_omission.in, and compare the output against the text in
    test_process_omission.ref
    """
    ft = Footnote()
    # Load text from input file
    with open(path_testdata + 'test_omission_and_conieci.in', 'r',
              encoding="utf-8") as f:
        text_in = f.read()

    # Load text from reference file
    with open(path_testdata + 'test_omission_and_conieci.ref', 'r',
              encoding="utf-8") as f:
        text_ref = f.read()

    # Run the function with the input
    ft.footnote = text_in
    ft.xml = []
    ft.omission()

    # Convert the output list to a string with each element on a new line
    # This is not good in a test you should not modify the results
    # before the test.
    text_out = '\n'.join(ft.xml)

    assert text_out == text_ref


def test_omission_and_conieci_no_tttt_w1():
    """
    Runs the function _omission(...) on the text in
    test_process_omission.in, and compare the output against the text in
    test_process_omission.ref
    """
    ft = Footnote()
    # Load text from input file
    with open(path_testdata + 'test_omission_and_conieci_no_tttt_w1.in',
              'r', encoding="utf-8") as f:
        text_in = f.read()

    # # Load text from reference file
    with open(path_testdata + 'test_omission_and_conieci_no_tttt_w1.ref',
              'r', encoding="utf-8") as f:
        text_ref = f.read()

    # Run the function with the input
    ft.footnote = text_in
    ft.xml = []
    ft.omission()

    # Convert the output list to a string with each element on a new line
    # This is not good in a test you should not modify the results
    # before the test.
    text_out = '\n'.join(ft.xml)

    assert text_out == text_ref


def test_omission_and_conieci_no_tttt_w1_w2():
    ft = Footnote()
    # Load text from input file
    with open(path_testdata + 'test_omission_and_conieci_no_tttt_w1_w2.in',
              'r', encoding="utf-8") as f:
        text_in = f.read()

    # # Load text from reference file
    with open(path_testdata + 'test_omission_and_conieci_no_tttt_w1_w2.ref',
              'r', encoding="utf-8") as f:
        text_ref = f.read()

    # Run the function with the input
    ft.footnote = text_in
    ft.xml = []
    ft.omission()

    # Convert the output list to a string with each element on a new line
    # This is not good in a test you should not modify the results
    # before the test.
    text_out = '\n'.join(ft.xml)

    assert text_out == text_ref


def test_omission_and_correxi_multiple_witnesses():
    ft = Footnote()
    # Load text from input file
    with open(path_testdata +
              'test_omission_and_correxi_multiple_witnesses.in',
              'r', encoding="utf-8") as f:
        text_in = f.read()

    # Load text from reference file
    with open(path_testdata +
              'test_omission_and_correxi_multiple_witnesses.ref',
              'r', encoding="utf-8") as f:
        text_ref = f.read()

    # Run the function with the input
    ft.footnote = text_in
    ft.xml = []
    ft.omission()

    # Convert the output list to a string with each element on a new line
    # This is not good in a test you should not modify the results
    # before the test.
    text_out = '\n'.join(ft.xml)

    assert text_out == text_ref


def test_omission_and_correxi_no_tttt_w1():
    ft = Footnote()
    # Load text from input file
    with open(path_testdata + 'test_omission_and_correxi_no_tttt_w1.in',
              'r', encoding="utf-8") as f:
        text_in = f.read()

    # # Load text from reference file
    with open(path_testdata + 'test_omission_and_correxi_no_tttt_w1.ref',
              'r', encoding="utf-8") as f:
        text_ref = f.read()

    # Run the function with the input
    ft.footnote = text_in
    ft.xml = []
    ft.omission()

    # Convert the output list to a string with each element on a new line
    # This is not good in a test you should not modify the results
    # before the test.
    text_out = '\n'.join(ft.xml)

    assert text_out == text_ref


def test_omission_and_correxi_no_tttt_w1_w2():
    ft = Footnote()
    # Load text from input file
    with open(path_testdata + 'test_omission_and_correxi_no_tttt_w1_w2.in',
              'r', encoding="utf-8") as f:
        text_in = f.read()

    # # Load text from reference file
    with open(path_testdata + 'test_omission_and_correxi_no_tttt_w1_w2.ref',
              'r', encoding="utf-8") as f:
        text_ref = f.read()

    # Run the function with the input
    ft.xml = []
    ft.footnote = text_in
    ft.omission()

    # Convert the output list to a string with each element on a new line
    # This is not good in a test you should not modify the results
    # before the test.
    text_out = '\n'.join(ft.xml)

    assert text_out == text_ref


def test_correction_add_form1():
    """
    Runs the function _correxi(...) on the text in
    test_process_correxi1.in and test_process_correxi2.in,
    and compares the output against the text in test_process_correxi1.ref
    and test_process_correxi2.ref
    """
    ft = Footnote()
    basename = path_testdata + 'test_process_addition1'

    # Load text from input file
    with open(basename + '.in', 'r',
              encoding="utf-8") as f:
        text_in = f.read()

    # Load text from reference file
    with open(basename + '.ref', 'r', encoding="utf-8") as f:
        text_ref = f.read()

    # Run the function with the input
    ft.xml = []
    ft.footnote = text_in
    ft.correction('add')

    # Convert the output list to a string with each element
    # on a new line
    text_out = '\n'.join(ft.xml)

    assert text_out == text_ref


def test_correction_add_form2():
    """
    Runs the function _correxi(...) on the text in
    test_process_correxi1.in and test_process_correxi2.in,
    and compares the output against the text in test_process_correxi1.ref
    and test_process_correxi2.ref
    """
    ft = Footnote()
    basename = path_testdata + 'test_process_addition2'

    # Load text from input file
    with open(basename + '.in', 'r',
              encoding="utf-8") as f:
        text_in = f.read()

    # Load text from reference file
    with open(basename + '.ref', 'r', encoding="utf-8") \
            as f:
        text_ref = f.read()

    # Run the function with the input
    ft.xml = []
    ft.footnote = text_in
    ft.correction('add')

    # Convert the output list to a string with each element
    # on a new line
    text_out = '\n'.join(ft.xml)

    assert text_out == text_ref


def test_correction_add_form3():
    """
    Runs the function _correxi(...) on the text in
    test_process_correxi1.in and test_process_correxi2.in,
    and compares the output against the text in test_process_correxi1.ref
    and test_process_correxi2.ref
    """
    ft = Footnote()
    basename = path_testdata + 'test_process_addition3'

    # Load text from input file
    with open(basename + '.in', 'r',
              encoding="utf-8") as f:
        text_in = f.read()

    # Load text from reference file
    with open(basename + '.ref', 'r', encoding="utf-8") \
            as f:
        text_ref = f.read()

    # Run the function with the input
    ft.xml = []
    ft.footnote = text_in
    ft.correction('add')

    # Convert the output list to a string with each element
    # on a new line
    text_out = '\n'.join(ft.xml)

    assert text_out == text_ref


# ################# _correxi ###################

def test_correction_correxi_form1():
    """
    Runs the function _correxi(...) on the text in
    test_process_correxi1.in and test_process_correxi2.in,
    and compares the output against the text in test_process_correxi1.ref
    and test_process_correxi2.ref
    """
    ft = Footnote()
    basename = path_testdata + 'test_process_correxi1'

    # Load text from input file
    with open(basename + '.in', 'r',
              encoding="utf-8") as f:
        text_in = f.read()

    # Load text from reference file
    with open(basename + '.ref', 'r', encoding="utf-8") \
            as f:
        text_ref = f.read()

    # Run the function with the input
    ft.xml = []
    ft.footnote = text_in
    ft.correction('correxi')

    # Convert the output list to a string with each element
    # on a new line
    text_out = '\n'.join(ft.xml)

    assert text_out == text_ref


def test_correction_correxi_form2():
    """
    Runs the function _correxi(...) on the text in
    test_process_correxi1.in and test_process_correxi2.in,
    and compares the output against the text in test_process_correxi1.ref
    and test_process_correxi2.ref
    """
    ft = Footnote()
    basename = path_testdata + 'test_process_correxi2'

    # Load text from input file
    with open(basename+'.in', 'r',
              encoding="utf-8") as f:
        text_in = f.read()

    # Load text from reference file
    with open(basename + '.ref', 'r', encoding="utf-8") \
            as f:
        text_ref = f.read()

    # Run the function with the input
    ft.xml = []
    ft.footnote = text_in
    ft.correction('correxi')

    # Convert the output list to a string with each element
    # on a new line
    text_out = '\n'.join(ft.xml)

    assert text_out == text_ref


def test_correction_conieci_form1():
    """
    Runs the function _correxi(...) on the text in
    test_process_correxi1.in and test_process_correxi2.in,
    and compares the output against the text in test_process_correxi1.ref
    and test_process_correxi2.ref
    """
    ft = Footnote()
    basename = path_testdata + 'test_process_conieci1'

    # Load text from input file
    with open(basename + '.in', 'r',
              encoding="utf-8") as f:
        text_in = f.read()

    # Load text from reference file
    with open(basename + '.ref', 'r', encoding="utf-8") \
            as f:
        text_ref = f.read()

    # Run the function with the input
    ft.xml = []
    ft.footnote = text_in
    ft.correction('conieci')

    # Convert the output list to a string with each element
    # on a new line
    text_out = '\n'.join(ft.xml)

    assert text_out == text_ref


def test_correction_conieci_form2():
    """
    Runs the function _correxi(...) on the text in
    test_process_correxi1.in and test_process_correxi2.in,
    and compares the output against the text in test_process_correxi1.ref
    and test_process_correxi2.ref
    """
    ft = Footnote()
    basename = path_testdata + 'test_process_conieci2'

    # Load text from input file
    with open(basename+'.in', 'r',
              encoding="utf-8") as f:
        text_in = f.read()

    # Load text from reference file
    with open(basename + '.ref', 'r', encoding="utf-8") \
            as f:
        text_ref = f.read()

    # Run the function with the input
    ft.xml = []
    ft.footnote = text_in
    ft.correction('conieci')

    # Convert the output list to a string with each element
    # on a new line
    text_out = '\n'.join(ft.xml)

    assert text_out == text_ref


def test_correction_standard_variant():
    """
    Runs the function _standard_variant(...) on the text in
    test_process_standard_variant.in, and compare the output against
    the text in test_process_standard_variant.ref
    """
    ft = Footnote()
    # Load text from input file
    with open(path_testdata + 'test_process_standard_variant.in', 'r',
              encoding="utf-8") as f:
        text_in = f.read()

    # Load text from reference file
    with open(path_testdata + 'test_process_standard_variant.ref', 'r',
              encoding="utf-8") as f:
        text_ref = f.read()

    # Run the function with the input
    ft.xml = []
    ft.footnote = text_in
    ft.correction('standard')

    # Convert the output list to a string with each element on a new line
    text_out = '\n'.join(ft.xml)

    # Test the return value matches the expected output
    assert text_out == text_ref


def test_correction_standard_variant2():
    """
    Runs the function _standard_variant(...) on the text in
    test_process_standard_variant.in, and compare the output against
    the text in test_process_standard_variant.ref
    """
    ft = Footnote()
    # Load text from input file
    with open(path_testdata + 'test_process_standard_variant2.in', 'r',
              encoding="utf-8") as f:
        text_in = f.read()

    # Load text from reference file
    with open(path_testdata + 'test_process_standard_variant2.ref', 'r',
              encoding="utf-8") as f:
        text_ref = f.read()

    # Run the function with the input
    ft.xml = []
    ft.footnote = text_in
    ft.correction('standard')

    # Convert the output list to a string with each element on a new line
    text_out = '\n'.join(ft.xml)

    # Test the return value matches the expected output
    assert text_out == text_ref


def test_footnotes_dictionary_wrong_istance():
    ft = Footnotes()
    ft.footnotes = 1
    with pytest.raises(FootnotesException):
        ft._dictionary()


def test_footnotes_dictionary_is_orderdict():
    ft = Footnotes()
    ft.footnotes = '*1*'
    ft._dictionary()
    assert isinstance(ft.footnotes, OrderedDict)


def test_footnotes_is_empty_string():
    ft = Footnotes()
    ft.footnotes = ''
    with pytest.raises(FootnotesException):
        ft._dictionary()


def test_footnotes_numeration_agree_with_number():
    ft = Footnotes()
    ft.footnotes = ['*1*aaa', '*4*bbbb']
    with pytest.raises(FootnotesException):
        ft._dictionary()


def test_footnote_inside_footnote():
    logger_root = logging.getLogger()
    logcapture = LogCapture()
    ft = Footnotes()
    ft.footnotes = ['*1*aaa vvvvv*3*cccc ']
    ft._dictionary()

    logcapture.check(('exegis', 'WARNING',
              'Problem in footnote: *1*aaa vvvvv*3*cccc '),
            ('exegis', 'WARNING',
             'There are a footnote reference inside the footnote. '
             'This case is not treatable by the actual version of '
             'the software'))


def test_footnotes_xml_app():
    pass


def test_save_xml():
    pass
