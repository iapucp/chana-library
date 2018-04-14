#coding=UTF-8
"""
Part-of-Speech (POS) Tagger for shipibo-konibo

General functions to use the pos tagger for shipibo-konibo.

Source model for the shipibo pos tagger is from the Chana project
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
        my_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(my_path, "files/pos_tagger/shipibo_svm_model.pkl")
        self.postagger = joblib.load(path)


    def features(self, sentence, tags, index):
        """
        Function that returns the features of a sentence to be used in the model
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
        """
        Method that predict the pos-tags of a shipibo sentence
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
        """
        Method that predict the pos-tags of a shipibo sentence and returns the full tag in spanish
        """
        tags = self.pos_tag(sentence)
        for i in range(len( tags)):
            tags[i] = self.get_complete_tag(tags[i])
        return tags

    def get_complete_tag(self,pos):
        """
        Method that predict the pos-tags of a shipibo sentence and returns the full tag in spanish
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
   
