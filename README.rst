Hyppocratic Aphorisms
=====================

AphorismToXML
-------------

A Python module which provide a conversion from aphorisms annotated text
files to TEI compatible XML (for the version 2).

The ``docs`` folder contains more information for usage and development.

-  Example input files can be found in the Example folder
-  the convenience script: main.py was used to run the module on these
   files to produce the corresponding output in the XML folder,
   xml\_template.txt is optional.

-  The input and reference output for the unittests tests are in folder
   test\_files

Installation
------------

Required
~~~~~~~~

-  Python ( v3.5 or higher)

Installation from Source
~~~~~~~~~~~~~~~~~~~~~~~~

Clone the code from the github repository:

.. code:: commandline

    git clone https://github.com/UoMResearchIT/CommentaryToEpidoc.git

go into the project directory:

.. code:: commandline

    cd CommentaryToEpidoc

Install the package:

.. code:: commandline

    python setup.py install --user

The ``--user`` is optional but will install the package without the need
to be administrator. It will install the package in a user accessible
directory (plateforme dependant).

For development other python modules are needed and can be installed
with:

.. code:: commandline

    pip install -U -r requirements.txt --user 

Usage
-----

When the package is installed, it should be available in your ``PATH``
under the name ``AphorismToXML``.

To use it start a terminal and execute the command:

.. code:: commandline

    AphorismToXML <path or file> 

where:

-  ``path`` is the name of the directory which contains the files to
   analyse and convert to XML..
-  ``file`` is the name of the individual file to analyse and convert to
   XML.

At the end of the treatment a log file called *hippocratic.log* will be
found in the directory of the execution. It will contains information,
errors and warning related to the process.

If everything is going well, an XML directory will be also created in
the execution file. This directory will contains the two XML files.
The main one which contains the aphorisms, the commentaries and the
annotations. An additional one will also be present (called app) which
will contains the footnotes present in the texts.
