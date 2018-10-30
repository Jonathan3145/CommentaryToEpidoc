import os
import sys
import pytest

from .conftest import Process, AphorismsToXMLException

file_path = os.path.realpath(__file__)
path = os.path.dirname(file_path)
sys.path.append(path)

path_testdata = os.path.join(path, 'test_files') + os.sep
# examples = os.path.join(path, '..', 'Examples', 'TextFiles') + os.sep
template_file = os.path.join(path, '..', 'exegis', 'template',
                             'xml_template.txt')


def test_divide_document():

    comtoepi = Process()
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
        comtoepi._text = f.read().strip()

    comtoepi.divide_document()

    assert comtoepi._introduction == introduction
    assert comtoepi._title == title

    for i, line in enumerate(comtoepi._text.splitlines()):
        assert line.strip() == text[i].strip()
    for i, line in enumerate(comtoepi.footnotes.splitlines()):
        assert line.strip() == footnotes[i].strip()


def test_divide_document_no_intro():

    comtoepi = Process()
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
        comtoepi._text = f.read().strip()

    comtoepi.divide_document()

    assert comtoepi._title == title
    for i, line in enumerate(comtoepi._text.splitlines()):
        assert line.strip() == text[i].strip()
    for i, line in enumerate(comtoepi.footnotes.splitlines()):
        assert line.strip() == footnotes[i].strip()


def test_divide_document_no_footnotes():

    comtoepi = Process()
    # Read full text file
    with open(path_testdata +
              'aphorism_no_intro_title_text_no_footnotes.txt', 'r',
              encoding="utf-8") as f:
        comtoepi._text = f.read().strip()

    with pytest.raises(AphorismsToXMLException):
        comtoepi.divide_document()


################# read_template ###################

def test_read_template_missing_template():

    comtoepi = Process()
    comtoepi.template_fname = 'ttttt'

    with pytest.raises(AphorismsToXMLException):
        comtoepi.read_template()
    # with assertRaises(SystemExit) as cm:
    #     comtoepi.read_template()
    # assertEqual(cm.exception.code, 1)


# #################### save_xml #########################
def test_treat_footnote():
    comtoepi = Process()
    comtoepi.footnotes = ['*1*ssss tttt ] conieci: '
                                'aaaa bbbb L5: om. Y']
    comtoepi.treat_footnotes()
    assert comtoepi.footnotes_app.footnotes is not None
    assert comtoepi.footnotes_app.xml is not None


def test_main_open_document():
    comtoepi = Process()
    comtoepi.fname = path_testdata + 'aphorisms.txt'
    comtoepi.main()
    assert comtoepi._text is not None


def test_main_open_document_failed():
    comtoepi = Process()
    comtoepi.fname = path_testdata + 'do not exit'
    with pytest.raises(AphorismsToXMLException):
        comtoepi.main()


def test_main_division_failed():
    comtoepi = Process()
    comtoepi.fname = path_testdata + 'aphorisms_failed_division.txt'
    with pytest.raises(AphorismsToXMLException):
        comtoepi.main()


def test_main_no_point_commentaries():
    """test for coverage"""
    comtoepi = Process()
    comtoepi.fname = (path_testdata + 'aphorisms_no_point_commentaries.txt')
    comtoepi.main()
    #with pytest.raises(AphorismsToXMLException):
    #    comtoepi.main()


def test_main_references():
    comtoepi = Process()
    comtoepi.fname = (path_testdata + 'aphorisms_references_failed.txt')
    comtoepi.main()
    #with pytest.raises(AphorismsToXMLException):
    #    comtoepi.main()


def test_main_aphorism_point_number():
    '''Function to test that the program return an error if the aphorism
    is wrongly number (1. or 1 is ok but .1 is not)
    '''
    comtoepi = Process()
    comtoepi.fname = (path_testdata + 'aphorisms_wrong_numeration.txt')
    with pytest.raises(AphorismsToXMLException):
        comtoepi.main()


    # # ################# process_folder ###################
    # Moved to driver:
    # TODO: implement unittest for driver
    # def test_process_folder(self):
    #     comtoepi.template_folder = path_testdata
    #     assertTrue(comtoepi.process_folder(path_testdata))
    #
    # def test_process_folder_raise_error_folder_not_present(self):
    #     folder = os.path.join('path_failed')
    #     assertRaises(AphorismsToXMLException,
    #                       comtoepi.process_folder,
    #                       folder)

# if __name__ == '__main__':
#     pytest.main()
