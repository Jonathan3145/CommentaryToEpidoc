.. _commentaries:

#######################
Format for commentaries
#######################

It is assumed the commentaries are utf-8 text files consisting of a
main body of text, followed by a list of numbered and ordered
footnotes describing:

1. :ref:`Omissions <omissions>`

2. :ref:`Additions <additions>`

3. :ref:`Correxi <correxi>`

4. :ref:`Conieci <conieci>`

5. :ref:`Other textual variations from two source documents. <variations>`

The main body of text should have a block of text containing an
optional introduction and the document title followed by a series of
numbered aphorisms and commentaries. If an introduction is included it
should be separated from the title by a line containing the two plus
symbols, i.e. ``++``, the title can be more than one line of text.

The aphorisms and commentaries should have the following format.

1. A single line contains the aphorism number followed by a period ``.``
   character, e.g. ``1.`` for aphorism 1.

.. note:

    If using an editor which does support properly the right-to-left writing,
    it will show ``.1``.

2. The next line contains the aphorism text

3. The next line (or lines) contain one or more commentaries
   associated with that aphorism, with each commentary on a single
   line

4. This is repeated for any additional aphorisms

This main text (title, aphorisms and commentaries) contains symbols
referring to witnesses (``WW``) and footnotes.

1. Witness symbols have the form ``[WW LL]`` where ``WW`` is a code to
   identify the document and ``LL`` is a location in the
   document. Witness codes should be listed in the ``<listWit>``
   element in the XML template file described below.

2. Footnote symbols have one of two forms depending on whether
   they refer to single word or multiple word variations. If ``tttt``
   represent a word of text without a variant, ``vvvv`` represent a
   word of text with a variant, and ``n`` is the footnote number then
   single word variants use form (a) and multiple word variations
   use form (b) where the ``#`` marks the end of the variation.

   a. ``ttt tttt *n*vvvv tttt tttt``

   b. ``ttt tttt *n*vvvv vvvv vvvv# tttt tttt``

After the main body of text is a list of numbered and ordered
footnotes, each footnote has a corresponding reference in the main
text. A footnote is a single line with the following format.

1. At the start is the footnote number enclosed within a pair of
   asterisks, e.g. for footnote 1 the line starts with ``*1*``

2. Following the footnote number is a mix of witness text
   (i.e. title, aphorism or commentary) and symbols defining
   omissions, additions, correxi, conieci and other variations

3. The footnote line ends with a period ``.`` character

The formats for the five footnote types are now described where ``n`` is
the footnote number, ``W1`` and ``W2`` are witness codes, and ``ssss``,
``tttt`` and ``uuuu`` represent segments of witness text (segments can be
one or more words in length).

.. _omissions:

Omissions
---------

Omissions can have the following forms, i.e.

a. ``*n*ssss ] W1: om. W2.``

   This means the segment of text ``ssss`` is found in witness ``W1`` but
   not ``W2``.

b. ``*n*ssss ] correxi: tttt W1: om. W2.``

   This means the segment of text ``ssss`` is found in witness ``W1`` but
   not ``W2`` however the editor has corrected ``ssss`` to ``tttt``.

c. ``*n*ssss ] conieci: tttt W1: om. W2.``

   This means the segment of text ``ssss`` is found in witness ``W1`` but
   not ``W2`` however the editor has conjonctured that it should be ``ssss``
   instead of ``tttt``.

d. ``*n*ssss ] correxi: om. W1.`` or ``*n*ssss ] correxi: om. W1, W2.``

   This means add the text ``ssss`` which is missing in witness ``W1`` or
   missing in witness ``W1`` and ``w2``.

e. ``*n*ssss ] conieci: om. W1.`` or ``*n*ssss ] correxi: om. W1, W2.``

   This means add a conjonctured text ``ssss`` which is missing in witness
   ``W1`` or missing in witness ``W1`` and ``w2``.

f. More generally an omission can have the form:

   ``*n*ssss ] conieci: tttt W1, W2, W3: om. W4, W5, W6.`` or
   ``*n*ssss ] correxi: tttt W1, W2, W3: om. W4, W5, W6.`` or
   ``*n*ssss ] W1, W2, W3: om. W4, W5, W6.``


.. _additions:

Additions
---------

Additions have three forms depending on whether the addition
applies to one or both witnesses, and for the latter case
whether the addition is the same or not for both witnesses.

a. Form 1: ``*n*ssss ] add. tttt W1.``

  This means both witnesses have ``ssss`` and W1 adds ``tttt``.

b. Form 2: ``*n*ssss ] add. tttt W1, W2.``

  This means both witnesses have ``ssss`` and both add ``tttt``,
  however the editor felt the need to omit ``tttt``.

c. Form 3: ``*n*ssss ] add. tttt W1: uuuu W2.``

  This means both witnesses have ``ssss``, ``W1`` adds ``tttt`` whereas
  ``W2`` adds ``uuuu``.

.. _correxi:

Correxi
-------
Correxi can have two forms, depending on whether witness texts
are the same or not.

a. Form 1: ``*n*ssss ] correxi: tttt W1, W2.``

  This means the text ``tttt`` is found in witnesses ``W1`` and ``W2``
  and the editor has corrected this to ``ssss``.

b. Form 2: ``*n*ssss ] correxi: tttt W1: uuuu W2.``

  This means the text ``tttt`` is found in witness ``W1``, whereas ``W2``
  has ``uuuu``. The editor has corrected these to ``ssss``.

.. _conieci:

Conieci
-------

Conieci can have two forms, depending on whether the witness texts are
the same or not.

a. Form 1: ``*n*ssss ] conieci: tttt W1, W2.``

  This means the text 'tttt' is found in witnesses ``W1`` and ``W2``,
  the editor conjectures that this should be ``ssss``.

b. Form 2: ``*n*ssss ] conieci: tttt W1: uuuu W2.``

  This means the text ``tttt`` is found in witness ``W1``, whereas
  ``W2`` has ``uuuu``. The editor conjectures that these should be
  ``ssss``.

.. _variations:

Textual variations
------------------

Standard variations have only two forms:

a. ``*n*ssss ] W1: tttt W2.``

   This means witness ``W1`` has text ``ssss`` whereas ``W2`` has ``tttt``.

b. ``*n*ssss ] W1, W2, W3: tttt W4, W5, W6.``

   This means witnesses ``W1``, ``W2`` and ``W3`` have text ``ssss``
   whereas ``W4``, ``W5``, ``W6`` have ``tttt``.
