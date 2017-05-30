.. _howto:

######
How-To
######

Usage
=====

The expected way of using the module is to run the software ``AphorismsToXML`` in a terminal where you want to save the XML files
which should be produce at the end of the process.

The software is expecting at least one argument which can be:

1. a folder name which contain the text files
2. a file name

The text file has to follow a specific structure (XXXXX)

An optional argument can be given to use a specic template which
will be used to create the XML files.

::

    > AphorismsToXML file_to_analyse
    > AphorismsToXML file_to_analyse --xml-main-template=xml_main_template.xml
    > AphorismsToXML directory
    > AphorismsToXML directory --xml-main-template=xml_main_template.xml

where:

- ``file_to_analyse`` contains the text to transform in XML (TEI compliant)
- ``directory`` is the name of a directory with file(s) to transform in XML
  (TEI compliant).
  All the files will be treated.
- ``--xml-main-template=`` is an option to precise the xml template used for
  the treatment (here ``xml_main_template.xml``)

The software provided the information on how to use it if it is called
wihtout arguments or with the option ``-h`` or ``--help``::

    > AphorismsToXML

will give::

    Usage:
            AphorismsToXML <files> [--xml-main-template=<tmpl>]
            AphorismsToXML -h | --help
            AphorismsToXML --version


Example
=======

The user have a file called ``aphorisms.txt`` in the internal format and he want
to convert it in the XML TEI format. The file is locate in a sub-directory
called ``texts``.

::

    .
    └── texts
        └── aphorisms.txt

to achieve the transformation in a terminal::

    > AphorismsToXML texts/aphorisms.txt

or just use the name of the directory (All the files inside it will be treated)::

    > AphorismsToXML texts


If everything is running well the user will not get any message but will come
back to the normal terminal prompt ``>``::

    > AphorismsToXML texts/
    >

if there are a problem an error message will appeared in the terminal::

    >AphorismsToXML texts/
    2017-04-25 11:57:05,389 - hippocratic - ERROR - N aphorism expected 4, got: 3
    2017-04-25 11:57:05,389 - hippocratic - ERROR - Missing or problematic aphorism: [2]
    2017-04-25 11:57:05,389 - hippocratic - ERROR - Error: unable to process "aphorisms.txt", see log file.
    >

In this example, the error message said that the problem is at the aphorism 2.
It can be missing or having other problem to find it. The user interaction is
needed at this stage and he should verify the ``aphorisms.txt`` file.

For both results a logging file will be created in the working directory::

    .
    ├── hippocratic.log
    ├── texts
       └── aphorisms.txt

If the process is running until the end without any problems, a new directory
will be created in the working directory with the name ``XML``::

    .
    ├── hippocratic.log
    ├── texts
    │   └── aphorisms.txt
    └── XML
        ├── aphorisms_app.xml
        └── aphorisms_main.xml

Two files are presents inside an app file, which contains the footnotes
information and the main file which contains the texts and the references
to the footnotes.
