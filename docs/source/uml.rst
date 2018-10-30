############
Architecture
############

Package Diagram
===============

.. .. image:: ../images/packages_exegis.pdf
.. image:: ../images/packages_exegis.*

Class Diagram
=============

.. uml::

    class Exegis {
        xml
        xml_oss
        xml_n_offset
        xml_offset_size

        __init__(self)
        xml_main(self)
        note_xml(self, note)
        save_xml(self)
    }

    class Title {
        title
        doc_num
        next_footnote

        __init__(self, title, next_footnote=1, doc_num=1)
        xml_main(self)
    }

    class Footnote {
        footnote
        n_footnote
        xml
        - _d_footnote

        __init__(footnote=None, n_footnote=None, xml=None)
        check_endnote()
        omission()
        - _omission_xml()
        correction()
        - _correction_xml()
    }

    class Footnotes {
        footnotes
        - _xml_app

        __init__(self, footnotes=None)
        - _dictionary(self)
        xml_app(self)
        save_xml(self, fname='xml_app.xml')
    }

    class Process{

        fname
        folder
        doc_num
        base_name
        template_fname
        template_marker
        xml_main_file
        xml_main_app
        footnotes
        - _footnotes_app
        - _next_footnote
        - _introduction
        - _title
        - _aph_com
        - _text
        - _n_footnote
        - _template_part1
        - _template_part2

        __init__(self, fname=None, folder=None, doc_num=1)
        set_basename(self)
        open_document(self, fname=None)
        divide_document(self)
        aphorisms_dict(self)
        read_template(self)
        save_xml(self)
        treat_footnotes(self)
        main(self)
    }

    class Introduction {
        next_footnote
        introduction

        __init__(self, introduction, next_footnote)
        xml_main()
    }

    Exegis <|-- Title
    Exegis <|-- Footnote
    Exegis <|-- Process
    Exegis <|-- Introduction

    Process *-- Footnotes


