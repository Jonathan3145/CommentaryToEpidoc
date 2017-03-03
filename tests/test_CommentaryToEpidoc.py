import os
import sys
from collections import OrderedDict
import unittest
import pytest

from context import Process, CommentaryToEpidocException

file_path = os.path.realpath(__file__)
path = os.path.dirname(file_path)
sys.path.append(path)

path_testdata = os.path.join(path, 'test_files') + os.sep
# examples = os.path.join(path, '..', 'Examples', 'TextFiles') + os.sep
template_file = os.path.join(path, '..', 'hyppocratic', 'xml_template.txt')


class TestProcess(unittest.TestCase):

    def setUp(self):
        self.comtoepi = Process()

    # ################# divide_document ###################

    def test_divide_document(self):

        # Read test introduction
        with open(path_testdata + 'introduction.txt', 'r',
                  encoding="utf-8") as f:
            introduction = f.read().strip()

        # Read test title
        with open(path_testdata + 'title.txt', 'r',
                  encoding="utf-8") as f:
            title = f.read().strip()

        # Read test text
        with open(path_testdata + 'text.txt', 'r',
                  encoding="utf-8") as f:
            text = f.read().strip()

        # Read test footnotes
        with open(path_testdata + 'footnotes.txt', 'r',
                  encoding="utf-8") as f:
            footnotes = f.read().strip()

        # Read full text file
        with open(path_testdata +
                  'aphorysm_with_intro_title_text_footnotes.txt', 'r',
                  encoding="utf-8") as f:
            self.comtoepi.text = f.read().strip()

        self.comtoepi.divide_document()
        self.assertEqual(self.comtoepi.introduction, introduction)
        self.assertEqual(self.comtoepi.title, title)
        self.assertEqual(self.comtoepi.text, text)
        self.assertEqual(self.comtoepi.footnotes, footnotes)

    def test_divide_document_no_intro(self):

        # Read test title
        with open(path_testdata + 'title.txt', 'r',
                  encoding="utf-8") as f:
            title = f.read().strip()

        # Read test text
        with open(path_testdata + 'text.txt', 'r',
                  encoding="utf-8") as f:
            text = f.read().strip()

        # Read test footnotes
        with open(path_testdata + 'footnotes.txt', 'r',
                  encoding="utf-8") as f:
            footnotes = f.read().strip()

        # Read full text file
        with open(path_testdata +
                  'aphorysm_no_intro_title_text_footnotes.txt', 'r',
                  encoding="utf-8") as f:
            self.comtoepi.text = f.read().strip()

        self.comtoepi.divide_document()
        self.assertEqual(self.comtoepi.title, title)
        self.assertEqual(self.comtoepi.text, text)
        self.assertEqual(self.comtoepi.footnotes, footnotes)

    def test_divide_document_no_footnotes(self):

        # Read test title
        with open(path_testdata + 'title.txt', 'r',
                  encoding="utf-8") as f:
            title = f.read().strip()

        # Read test text
        with open(path_testdata + 'text.txt', 'r',
                  encoding="utf-8") as f:
            text = f.read().strip()

        # Read full text file
        with open(path_testdata +
                  'aphorysm_no_intro_title_text_no_footnotes.txt', 'r',
                  encoding="utf-8") as f:
            self.comtoepi.text = f.read().strip()

        self.assertRaises(CommentaryToEpidocException,
                          self.comtoepi.divide_document)

    # ################# read_template ###################

    def test_read_template_missing_template(self):
        self.comtoepi.template_folder = 'ttttt'

        with self.assertRaises(SystemExit) as cm:
            self.comtoepi.read_template()
        self.assertEqual(cm.exception.code, 1)

    def test_read_template(self):
        # Read the template comparison manually
        with open(path_testdata + 'xml_template.txt', 'r') as f:
            template = f.read()
        # split it as in the method
        part1, sep, part2 = template.partition(self.comtoepi.template_marker)

        self.comtoepi.template_folder = path_testdata
        self.comtoepi.read_template()
        self.assertEqual(part1, self.comtoepi.template_part1)
        self.assertEqual(part2, self.comtoepi.template_part2)

    # ################# process_folder ###################

    def test_process_folder(self):
        self.comtoepi.template_folder = path_testdata
        self.assertTrue(self.comtoepi.process_folder(path_testdata))

    def test_process_folder_raise_error_folder_not_present(self):
        folder = os.path.join('path_failed')
        self.assertRaises(CommentaryToEpidocException,
                          self.comtoepi.process_folder,
                          folder)

if __name__ == '__main__':
    pytest.main()
