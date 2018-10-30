# -*- coding: utf-8 -*-
"""Main module to treat aphorisms and convert them in XML files.

:Authors: Jonathan Boyle, Nicolas Gruel <nicolas.gruel@manchester.ac.uk>

:Copyright: IT Services, The University of Manchester
"""
import sys
import os

try:
    from docopt import docopt
except ImportError:
    print("Install docopt package: pip install docopt --user")
    sys.exit()

try:
    from .__init__ import __version__
    from .aphorisms_to_xml import logger, Process, AphorismsToXMLException
except ImportError:
    from __init__ import __version__
    from aphorisms_to_xml import logger, Process, AphorismsToXMLException


def main(args=None):
    """Run eXegis scripts to produce the TEI XML

    Command line::

        Usage:
            exegis <files>  [--relaxng=<relax>]
            exegis -h | --help
            exegis --version

        Options:
            -h --help                   Show this screen.
            --version                   Show version.
            --xml-template=<name>       Name of the XML template
            --relaxng=<name>            Name of the Relaxng file use to validate the resulting XML

        Examples:
            exegis TextFiles
            exegis Textfiles --xml-template=template.xml
            exegis Textfiles --relaxng=tei.rng
            exegis Textfiles --xml-template=template.xml --relaxng=tei.rng


    Raises
    ------
    SystemExit
        if the file or the folder to treat is not available.
    """

    arguments = docopt(main.__doc__, argv=args,
                       version=__version__)

    # Convert docopt results in the proper variable (change type when needed)

    fname = arguments['<files>']
    template_file = arguments['--xml-template']
    relaxng_file = arguments['--relaxng']

    try:
        if os.path.isdir(fname):
            directory = fname.strip(os.pathsep)
            files = os.listdir(directory)
        else:
            files, directory = [fname], ''
    except FileNotFoundError:
        error = 'Error: path {} for text files ' \
                'not found'.format(directory)
        logger.error(error)
        sys.exit()

    for fname in files:
        try:
            comtoepi = Process(fname=fname, folder=directory)
            if template_file:
                comtoepi.template_fname = template_file
            if relaxng_file:
                comtoepi.relaxng_fname = relaxng_file
            comtoepi.main()
        except AphorismsToXMLException:
            error = 'Error: unable to process "{}", ' \
                    'see log file.'.format(fname)
            logger.error(error)

    logger.info("Finished " + logger.name)


if __name__ == '__main__':
    main()
