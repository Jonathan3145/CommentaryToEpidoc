"""
Module to
"""


import os
import sys
# sys.path.insert(0, os.path.abspath('..'))
file_path = os.path.realpath(__file__)
path = os.path.dirname(file_path) + os.sep + '..'
sys.path.append(path)

import exegis
from exegis.aphorisms_to_xml import Process, \
    AphorismsToXMLException

# Module
from exegis.footnotes import Footnote, Footnotes, FootnotesException
import exegis.analysis as analysis
import exegis.title as title