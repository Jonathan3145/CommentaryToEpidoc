import os
import sys
import unittest

from .context import Process, AphorismsToXMLException

file_path = os.path.realpath(__file__)
path = os.path.dirname(file_path)
sys.path.append(path)

path_testdata = os.path.join(path, 'test_files') + os.sep
# examples = os.path.join(path, '..', 'Examples', 'TextFiles') + os.sep
template_file = os.path.join(path, '..', 'hippocratic', 'template',
                             'xml_template.txt')


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
            text = f.readlines()

        # Read test footnotes
        with open(path_testdata + 'footnotes.txt', 'r',
                  encoding="utf-8") as f:
            footnotes = f.readlines()

        # Read full text file
        with open(path_testdata +
                  'aphorism_with_intro_title_text_footnotes.txt', 'r',
                  encoding="utf-8") as f:
            self.comtoepi._text = f.read().strip()

        self.comtoepi.divide_document()

        self.assertEqual(self.comtoepi._introduction, introduction)
        self.assertEqual(self.comtoepi._title, title)
        for i, line in enumerate(self.comtoepi._text.splitlines()):
            self.assertEqual(line.strip(), text[i].strip())
        for i, line in enumerate(self.comtoepi.footnotes.splitlines()):
            self.assertEqual(line.strip(), footnotes[i].strip())

    def test_divide_document_no_intro(self):

        # Read test title
        with open(path_testdata + 'title.txt', 'r',
                  encoding="utf-8") as f:
            title = f.read().strip()

        # Read test text
        with open(path_testdata + 'text.txt', 'r',
                  encoding="utf-8") as f:
            text = f.readlines()

        # Read test footnotes
        with open(path_testdata + 'footnotes.txt', 'r',
                  encoding="utf-8") as f:
            footnotes = f.readlines()

        # Read full text file
        with open(path_testdata +
                  'aphorism_no_intro_title_text_footnotes.txt', 'r',
                  encoding="utf-8") as f:
            self.comtoepi._text = f.read().strip()

        self.comtoepi.divide_document()

        self.assertEqual(self.comtoepi._title, title)
        for i, line in enumerate(self.comtoepi._text.splitlines()):
            self.assertEqual(line.strip(), text[i].strip())
        for i, line in enumerate(self.comtoepi.footnotes.splitlines()):
            self.assertEqual(line.strip(), footnotes[i].strip())

    def test_divide_document_no_footnotes(self):
        # Read full text file
        with open(path_testdata +
                  'aphorism_no_intro_title_text_no_footnotes.txt', 'r',
                  encoding="utf-8") as f:
            self.comtoepi._text = f.read().strip()

        self.assertRaises(AphorismsToXMLException,
                          self.comtoepi.divide_document)

    # ################# read_template ###################

    def test_read_template_missing_template(self):
        self.comtoepi.template_fname = 'ttttt'

        self.assertRaises(AphorismsToXMLException,
                          self.comtoepi.read_template)
        # with self.assertRaises(SystemExit) as cm:
        #     self.comtoepi.read_template()
        # self.assertEqual(cm.exception.code, 1)

    # #################### save_xml #########################
    def test_treat_footnote(self):
        self.comtoepi.footnotes = ['*1*ssss tttt ] conieci: '
                                    'aaaa bbbb L5: om. Y']
        self.comtoepi.treat_footnotes()
        self.assertIsNotNone(self.comtoepi.footnotes_app.footnotes)
        self.assertIsNotNone(self.comtoepi.footnotes_app.xml)

    def test_main_open_document(self):
        self.comtoepi.fname = path_testdata + 'aphorisms.txt'
        self.comtoepi.main()
        self.assertIsNotNone(self.comtoepi._text)

    def test_main_open_document_failed(self):
        self.comtoepi.fname = path_testdata + 'do not exit'
        self.assertRaises(AphorismsToXMLException, self.comtoepi.main)

    def test_main_division_failed(self):
        self.comtoepi.fname = path_testdata + 'aphorisms_failed_division.txt'
        self.assertRaises(AphorismsToXMLException, self.comtoepi.main)

    def test_main_no_point_commentaries(self):
        """test for coverage"""
        self.comtoepi.fname = (path_testdata +
                               'aphorisms_no_point_commentaries.txt')
        self.comtoepi.main()
        # self.assertRaises(AphorismsToXMLException, self.comtoepi.main)

    def test_main_references(self):
        self.comtoepi.fname = (path_testdata +
                               'aphorisms_references_failed.txt')
        self.comtoepi.main()

    # # ################# process_folder ###################
    # Moved to driver:
    # TODO: implement unittest for driver
    # def test_process_folder(self):
    #     self.comtoepi.template_folder = path_testdata
    #     self.assertTrue(self.comtoepi.process_folder(path_testdata))
    #
    # def test_process_folder_raise_error_folder_not_present(self):
    #     folder = os.path.join('path_failed')
    #     self.assertRaises(AphorismsToXMLException,
    #                       self.comtoepi.process_folder,
    #                       folder)

# if __name__ == '__main__':
#     pytest.main()
