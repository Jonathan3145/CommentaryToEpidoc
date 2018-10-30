import os
import sys
import pytest

from .conftest import analysis

file_path = os.path.realpath(__file__)
path = os.path.dirname(file_path)
sys.path.append(path)

path_testdata = os.path.join(path, 'test_files') + os.sep
# examples = os.path.join(path, '..', 'Examples', 'TextFiles') + os.sep
template_file = os.path.join(path, '..', 'exegis', 'template',
                             'xml_template.txt')


def test_references():
    """
    Runs the function _references(...) on the text in
    test_process_references.in, and compares the output against the text in
    test_process_references.ref
    """
    # Load text from input file
    with open(path_testdata + 'test_process_references.in', 'r',
              encoding="utf-8") as f:
        text_in = f.read()

    # Load text from reference file
    with open(path_testdata + 'test_process_references.ref', 'r',
              encoding="utf-8") as f:
        text_ref = f.read()

    # Run the function with the input
    text_out = analysis.references(text_in)

    assert text_out == text_ref


def test_reference_empty_line():
    assert analysis.references('') is None
    assert analysis.references(None) is None


def test_reference_sep_empty():
    with pytest.raises(analysis.AnalysisException):
        analysis.references(' [W1 W2 ')


def test_reference_missing_space():
    with pytest.raises(analysis.AnalysisException):
        analysis.references(' [W1W2] ')


# BUG (workaround)
def test_footnotes_failed_known_bug():
    with pytest.raises(analysis.AnalysisException):
        analysis.footnotes('tttt*1*ssss', 1)
