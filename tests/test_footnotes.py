import os
import sys
from collections import OrderedDict
import unittest
import pytest

from context import Footnote, Footnotes, FootnotesException

file_path = os.path.realpath(__file__)
path = os.path.dirname(file_path)
sys.path.append(path)

path_testdata = os.path.join(path, 'test_files') + os.sep
# examples = os.path.join(path, '..', 'Examples', 'TextFiles') + os.sep
template_file = os.path.join(path, '..', 'hyppocratic', 'xml_template.txt')


class TestFootnote(unittest.TestCase):

    def setUp(self):
        self.ft = Footnote()

# ################# _omission ###################

    def test_omission(self):
        """
        Runs the function _omission(...) on the text in
        test_process_omission.in, and compare the output against the text in
        test_process_omission.ref
        """

        # Load text from input file
        with open(path_testdata + 'test_process_omission.in', 'r',
                  encoding="utf-8") as f:
            text_in = f.read()

        # Load text from reference file
        with open(path_testdata + 'test_process_omission.ref', 'r',
                  encoding="utf-8") as f:
            text_ref = f.read()

        # Run the function with the input
        list_out = []
        self.ft.footnote = text_in
        self.ft.omission(list_out)

        # Convert the output list to a string with each element on a new line
        # This is not good in a test you should not modify the results
        # before the test.
        text_out = '\n'.join(list_out)

        self.assertEqual(text_out, text_ref)

    def test_omission_and_correxi(self):
        """
        Runs the function _omission(...) on the text in
        test_process_omission.in, and compare the output against the text in
        test_process_omission.ref
        """

        # Load text from input file
        with open(path_testdata + 'test_omission_and_correxi.in', 'r',
                  encoding="utf-8") as f:
            text_in = f.read()

        # Load text from reference file
        with open(path_testdata + 'test_omission_and_correxi.ref', 'r',
                  encoding="utf-8") as f:
            text_ref = f.read()

        # Run the function with the input
        list_out = []
        self.ft.footnote = text_in
        self.ft.omission(list_out)

        # Convert the output list to a string with each element on a new line
        # This is not good in a test you should not modify the results
        # before the test.
        text_out = '\n'.join(list_out)

        self.assertEqual(text_out, text_ref)

    def test_omission_and_conieci(self):
        """
        Runs the function _omission(...) on the text in
        test_process_omission.in, and compare the output against the text in
        test_process_omission.ref
        """

        # Load text from input file
        with open(path_testdata + 'test_omission_and_conieci.in', 'r',
                  encoding="utf-8") as f:
            text_in = f.read()

        # Load text from reference file
        with open(path_testdata + 'test_omission_and_conieci.ref', 'r',
                  encoding="utf-8") as f:
            text_ref = f.read()

        # Run the function with the input
        list_out = []
        self.ft.footnote = text_in
        self.ft.omission(list_out)

        # Convert the output list to a string with each element on a new line
        # This is not good in a test you should not modify the results
        # before the test.
        text_out = '\n'.join(list_out)

        self.assertEqual(text_out, text_ref)

    def test_correction_add_form1(self):
        """
        Runs the function _correxi(...) on the text in
        test_process_correxi1.in and test_process_correxi2.in,
        and compares the output against the text in test_process_correxi1.ref
        and test_process_correxi2.ref
        """
        basename = path_testdata + 'test_process_addition1'

        # Load text from input file
        with open(basename + '.in', 'r',
                  encoding="utf-8") as f:
            text_in = f.read()

        # Load text from reference file
        with open(basename + '.ref', 'r', encoding="utf-8") \
                as f:
            text_ref = f.read()

        # Run the function with the input
        list_out = []
        self.ft.footnote = text_in
        self.ft.correction('add', list_out)

        # Convert the output list to a string with each element
        # on a new line
        text_out = '\n'.join(list_out)

        self.assertEqual(text_out, text_ref)

    def test_correction_add_form2(self):
        """
        Runs the function _correxi(...) on the text in
        test_process_correxi1.in and test_process_correxi2.in,
        and compares the output against the text in test_process_correxi1.ref
        and test_process_correxi2.ref
        """
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
        list_out = []
        self.ft.footnote = text_in
        self.ft.correction('add', list_out)

        # Convert the output list to a string with each element
        # on a new line
        text_out = '\n'.join(list_out)

        self.assertEqual(text_out, text_ref)

    def test_correction_add_form3(self):
        """
        Runs the function _correxi(...) on the text in
        test_process_correxi1.in and test_process_correxi2.in,
        and compares the output against the text in test_process_correxi1.ref
        and test_process_correxi2.ref
        """

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
        list_out = []
        self.ft.footnote = text_in
        self.ft.correction('add', list_out)

        # Convert the output list to a string with each element
        # on a new line
        text_out = '\n'.join(list_out)

        self.assertEqual(text_out, text_ref)

    # ################# _correxi ###################

    def test_correction_correxi_form1(self):
        """
        Runs the function _correxi(...) on the text in
        test_process_correxi1.in and test_process_correxi2.in,
        and compares the output against the text in test_process_correxi1.ref
        and test_process_correxi2.ref
        """

        n_test = 2
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
        list_out = []
        self.ft.footnote = text_in
        self.ft.correction('correxi', list_out)

        # Convert the output list to a string with each element
        # on a new line
        text_out = '\n'.join(list_out)

        self.assertEqual(text_out, text_ref)

    def test_correction_correxi_form2(self):
        """
        Runs the function _correxi(...) on the text in
        test_process_correxi1.in and test_process_correxi2.in,
        and compares the output against the text in test_process_correxi1.ref
        and test_process_correxi2.ref
        """

        n_test = 2
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
        list_out = []
        self.ft.footnote = text_in
        self.ft.correction('correxi', list_out)

        # Convert the output list to a string with each element
        # on a new line
        text_out = '\n'.join(list_out)

        self.assertEqual(text_out, text_ref)

    def test_correction_conieci_form1(self):
        """
        Runs the function _correxi(...) on the text in
        test_process_correxi1.in and test_process_correxi2.in,
        and compares the output against the text in test_process_correxi1.ref
        and test_process_correxi2.ref
        """

        n_test = 2
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
        list_out = []
        self.ft.footnote = text_in
        self.ft.correction('conieci', list_out)

        # Convert the output list to a string with each element
        # on a new line
        text_out = '\n'.join(list_out)

        self.assertEqual(text_out, text_ref)

    def test_correction_conieci_form2(self):
        """
        Runs the function _correxi(...) on the text in
        test_process_correxi1.in and test_process_correxi2.in,
        and compares the output against the text in test_process_correxi1.ref
        and test_process_correxi2.ref
        """

        n_test = 2
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
        list_out = []
        self.ft.footnote = text_in
        self.ft.correction('conieci', list_out)

        # Convert the output list to a string with each element
        # on a new line
        text_out = '\n'.join(list_out)

        self.assertEqual(text_out, text_ref)

    def test_correction_standard_variant(self):
        """
        Runs the function _standard_variant(...) on the text in
        test_process_standard_variant.in, and compare the output against
        the text in test_process_standard_variant.ref
        """

        # Load text from input file
        with open(path_testdata + 'test_process_standard_variant.in', 'r',
                  encoding="utf-8") as f:
            text_in = f.read()

        # Load text from reference file
        with open(path_testdata + 'test_process_standard_variant.ref', 'r',
                  encoding="utf-8") as f:
            text_ref = f.read()

        # Run the function with the input
        list_out = []
        self.ft.footnote = text_in
        self.ft.correction('standard', list_out)

        # Convert the output list to a string with each element on a new line
        text_out = '\n'.join(list_out)

        f = open('ssssss', 'w', encoding='utf-8')
        f.write(text_out)
        f.close()

        # Test the return value matches the expected output
        self.assertEqual(text_out, text_ref)


class TestFootnotes(unittest.TestCase):

    def setUp(self):
        self.ft = Footnotes()

    def test_footnotes_dictionary_wrong_istance(self):
        self.ft.footnotes = 1
        self.assertRaises(FootnotesException, self.ft._dictionary)

    def test_footnotes_dictionary_istance(self):
        self.ft.footnotes = '*1*'

        print(self.ft._dictionary())
        # self.assertRaises(FootnotesException, self.ft._dictionary)


    def test_footnotes_xml_app(self):
        pass

    def test_verification_footnotes(self):
        pass

    def test_save_xml(self):
        pass