import os
import sys
import unittest

from .context import analysis

file_path = os.path.realpath(__file__)
path = os.path.dirname(file_path)
sys.path.append(path)

path_testdata = os.path.join(path, 'test_files') + os.sep
# examples = os.path.join(path, '..', 'Examples', 'TextFiles') + os.sep
template_file = os.path.join(path, '..', 'hyppocratic', 'template',
                             'xml_template.txt')


class TestAnalysis(unittest.TestCase):

    def test_references(self):
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

        self.assertEqual(text_out, text_ref)

    def test_reference_empty_line(self):
        self.assertIsNone(analysis.references(''))
        self.assertIsNone(analysis.references(None))

    def test_reference_sep_empty(self):
        self.assertRaises(analysis.AnalysisException,
                          analysis.references, ' [W1 W2 ')

    def test_reference_missing_space(self):
        self.assertRaises(analysis.AnalysisException,
                          analysis.references, ' [W1W2] ')

    # BUG (workaround)
    def test_footnotes_failed_known_bug(self):
        self.assertRaises(analysis.AnalysisException,
                          analysis.footnotes, 'tttt*1*ssss', 1)
