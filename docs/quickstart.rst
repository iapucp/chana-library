.. _quickstart:

Quickstart
==========

This page gives a quick introduction to Chana.  It assumes you 
already have Chana installed.  If you do not, head over to the
:ref:`installation` section.


Using the Chana NLP Toolkit
---------------------

A minimal code to use the Chana Toolkit looks something like this::

    import chana.lemmatizer as lem
    import chana.ner as ner
    import chana.syllabificator as syl
    import chana.pos_tagger as pos

    lemmatizer = lem.ShipiboLemmatizer()
    lemma = lemmatizer.lemmatize('pikanwe')

    ship_ner = ner.ShipiboNER()
    ner_tags = ship_ner.crf_tag('Enero Limanko atsa enra piawe')

    tagger = pos.ShipiboPosTagger()
    tags = tagger.pos_tag('Atsa enra piai')

    syllables = syl.syllabify('atsabo')



So what did that code do?

1. First we imported the Chana tools (Lemmatizer, NER, Syllabificator and Pos-Tagger). 
2. Next we create an instance of the Shipibo Lemmatizer and then we used it to get
   the lemma of a Shipibo word.
3. We then create an instance of the Shipibo NER and use it to get the NER tags of
   a Shipibo sentence.
3. Next we create an instance of the Shipibo Pos-Tagger and use it to get the pos-tags of
   a Shipibo sentence.
3. Finally we use the syllabify function of the Shipibo Syllabificator in order to get
   the syllables of a Shipibo word.

Just save it as :file:`test.py` or something similar, to start using the chana tools
in a similar way.