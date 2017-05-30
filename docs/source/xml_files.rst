.. _xmlfiles:

#########
XML files
#########

The Python module generates TEI XML for insertion within the ``<body>``
element. Therefore the Python module requires a suitable XML template
file as input which contains all XML other than the contents of the
``<body>`` section.  The template file should contain the string
``#INSERT#`` at the location where the new XML should be inserted
i.e. the template should contain::

  <body>
  #INSERT#
  </body>

in the XML.

After successful processing each text file two XML files are created
in a folder called XML. The new files contain the main body of XML and
the apparatus XML linked using the double-end-point-attached method as
described `here
<http://www.tei-c.org/release/doc/tei-p5-doc/en/html/TC.html#TCAPLK>`_.

A text file base name should end in an underscore followed by a
numerical value representing the document number, e.g. file_1.txt,
file_2.txt, etc. The numerical value after the underscore is
subsequently used to create the title section ``<div>`` element,
e.g. ``<div n="1" type="Title_section">`` for file_1.txt.

The names for the new files is the text file base name plus
'_main.xml' (for the main XML) and '_apps.xml' (for the apparatus
XML). For example for text file file_1.txt the XML will be
file_1_main.xml and file_1_app.xml.
