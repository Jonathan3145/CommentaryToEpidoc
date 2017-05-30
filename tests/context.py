"""
Module to
"""


import os
import sys
# sys.path.insert(0, os.path.abspath('..'))
file_path = os.path.realpath(__file__)
path = os.path.dirname(file_path) + os.sep + '..'
sys.path.append(path)

import hippocratic
from hippocratic.aphorisms_to_xml import Process, \
    AphorismsToXMLException

# Module
from hippocratic.footnotes import Footnote, Footnotes, FootnotesException
import hippocratic.analysis as analysis
import hippocratic.title as title