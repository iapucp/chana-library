#coding=UTF-8
"""
Part-of-Speech (POS) Tagger for shipibo-konibo.
Source model is from the Chana project
"""
import os
from sklearn.externals import joblib
import warnings

warnings.filterwarnings("ignore")


class ShipiboPosTagger:
    """
    Instance of the pre-trained shipibo part-of-speech tagger
    """

    def __init__(self):
        """ Constructor of the ShipiboPosTagger class that loads the pretrained model    
    """
        my_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(my_path, "files/pos_tagger/shipibo_svm_model.pkl")
        self.postagger = joblib.load(path)


    def features(self, sentence, tags, index):
        """ Method that returns the features of a word in a sentence to be used by the model

        :param sentence: a sentence in shipibo-konibo
        :type sentence: str
        :param tags: tags to be returned for the word
        :type tags: list
        :param index: position of the word in the sentence
        :type index: int
        :returns: dict of features for the indexed word
        :rtype: dict

        :Example:

        >>> import chana.pos_tagger
        >>> tagger = chana.pos_tagger.ShipiboPosTagger()
        >>> tagger.features('Atsa ea piai',['','',''],2)
        {'word': 's', 'prevWord': 't', 'nextWord': 'a', 'isFirst': False, 'isLast': False, 'isCapitalized': False, 'isAllCaps': False, 'isAllLowers': True, 'prefix-1': 's', 'prefix-2': 's', 'prefix-3': 's', 'prefix-4': 's', 'suffix-1': 's', 'suffix-2': 's', 'suffix-3': 's', 'suffix-4': 's', 'tag-1': '', 'tag-2': ''}
        
    """
        return{
        'word': sentence[ index ],
        'prevWord': '' if index == 0 else sentence[ index - 1 ],
        'nextWord': '' if index == len( sentence ) -1  else sentence[ index + 1 ],
        'isFirst': index == 0,
        'isLast': index == len( sentence ) - 1,
        'isCapitalized': sentence[index][0].upper() == sentence[ index ][ 0],
        'isAllCaps': sentence[ index ].upper() == sentence[ index ],
        'isAllLowers': sentence[ index ].lower() == sentence[ index ],
        'prefix-1': sentence[ index ][ 0 ],
        'prefix-2': '' if ( len(sentence) < 2 ) else sentence[ index ][:2],
        'prefix-3': '' if ( len(sentence) < 3 ) else sentence[ index ][:3],
        'prefix-4': '' if ( len(sentence) < 4 ) else sentence[ index ][:4],
        'suffix-1': sentence[ index ][ -1 ],
        'suffix-2': '' if ( len(sentence) < 2 ) else sentence[ index ][-2:],
        'suffix-3': '' if ( len(sentence) < 3 ) else sentence[ index ][-3:],
        'suffix-4': '' if ( len(sentence) < 4 ) else sentence[ index ][-4:],
        'tag-1': '' if index == 0 else tags[ index - 1 ],
        'tag-2': '' if index < 2 else tags[ index - 2 ]
        }


    def pos_tag(self, sentence):
        """ Method that predict the pos-tags of a shipibo sentence in the UD format

        :param sentence: a sentence in shipibo-konibo
        :type sentence: str
        :returns: list of the tags in UD format
        :rtype: list

        :Example:

        >>> import chana.pos_tagger
        >>> tagger = chana.pos_tagger.ShipiboPosTagger()
        >>> tagger.pos_tag('Atsa ea piai')
        ['NOUN', 'PRON', 'VERB']
        
    """
        tags = []
        tokens = sentence.split(" ")
        for i in range(len(tokens)):
            tags.append('')
        for i in range (len(tokens)):
            feat = []
            feat.append(self.features(tokens,tags,i))
            tag_predicted =  self.postagger.predict(feat)[0]
            tags[i] = tag_predicted
        return tags

    def full_pos_tag(self, sentence):
        """ Method that predict the pos-tags of a shipibo sentence and returns the full tag in spanish

        :param sentence: a sentence in shipibo-konibo
        :type sentence: str
        :returns: list of the tags in spanish
        :rtype: list

        :Example:

        >>> import chana.pos_tagger
        >>> tagger = chana.pos_tagger.ShipiboPosTagger()
        >>> tagger.full_pos_tag('Atsa ea piai')
        ['Nombre', 'Pronombre', 'Verbo']
        
    """
        tags = self.pos_tag(sentence)
        for i in range(len( tags)):
            tags[i] = self.get_complete_tag(tags[i])
        return tags

    def get_complete_tag(self,pos):
        """ Method that returns the full tag in spanish of a tag

        :param pos: a pos tag in the UD format
        :type pos: str
        :returns: str with the tag in spanish
        :rtype: str

        :Example:

        >>> import chana.pos_tagger
        >>> tagger = chana.pos_tagger.ShipiboPosTagger()
        >>> tagger.get_complete_tag('ADJ')
        'Adjetivo'
        
    """
        if pos == "ADJ": return "Adjetivo"
        elif pos == "ADV" : return "Adverbio"
        elif pos == "CONJ" : return "Conjunción"
        elif pos == "DET" : return "Determinante"
        elif pos == "INTJ" : return "Interjección"
        elif pos == "NOUN" : return "Nombre"
        elif pos == "PROPN" : return "Nombre Propio"
        elif pos == "NUM" : return "Numeral"
        elif pos == "ONM" : return "Onomatopeya"
        elif pos == "INTW" : return  "Palabra Interrogativa"
        elif pos == "ADP" : return "Postposición"
        elif pos == "PRON" : return  "Pronombre"
        elif pos == "PUNCT" : return  "Puntuación"
        elif pos == "SYM" : return  "Símbolo"
        elif pos == "VERB": return  "Verbo"
        elif pos == "AUX" : return  "Verbo Auxiliar"
        return "Desconocido"
   
