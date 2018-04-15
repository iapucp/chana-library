#coding=UTF-8
"""
Lemmatizer for shipibo-konibo
Source model is from the Chana project and a use KNeighborsClassifier from scikit-learn
"""
import codecs
import os
import numpy as np
from sklearn.externals import joblib
from sklearn import neighbors
import warnings

warnings.filterwarnings("ignore")

def replace_last(source_string, replace_what, replace_with):
    """ Function that replaces the last ocurrence of a string in a word

        :param source_string: the source string
        :type source_string: str
        :param replace_what: the substring to be replaced
        :type replace_what: str
        :param replace_with: the string to be inserted
        :type replace_with: str
        :returns: string with the replacement
        :rtype: str

        :Example:

        >>> import chana.lemmatizer
        >>> chana.lemmatizer.replace_last('piati','ti','ra')
        'piara'
        
    """
    head, _sep, tail = source_string.rpartition(replace_what)
    return head + replace_with + tail

def longest_common_substring(string1, string2):
    """  Function to find the longest common substring of two strings

        :param string1: string1
        :type string1: str
        :param string2: string2
        :type string2: str
        :returns: longest common substring
        :rtype: str

        :Example:

        >>> import chana.lemmatizer
        >>> chana.lemmatizer.longest_common_substring('limanko','limanra')
        'liman'
        
    """
    m = [[0] * (1 + len(string2)) for i in range(1 + len(string1))]
    longest, x_longest = 0, 0
    for x in range(1, 1 + len(string1)):
        for y in range(1, 1 + len(string2)):
            if string1[x - 1] == string2[y - 1]:
                m[x][y] = m[x - 1][y - 1] + 1
                if m[x][y] > longest:
                    longest = m[x][y]
                    x_longest = x
            else:
                m[x][y] = 0
    return string1[x_longest - longest: x_longest]

def has_shipibo_suffix(str):
    """  Function that returns the possible existence of a shipo suffix in a a word

        :param str: word to evaluate
        :type str: str
        :returns: True or False
        :rtype: bool

        :Example:

        >>> import chana.lemmatizer
        >>> chana.lemmatizer.has_shipibo_suffix('pianra')
        True
        
    """
    my_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(my_path, "files/lemmatizer/shipibo_suffixes.dat")
    suffixes = codecs.open(path, "r", "utf-8")
    lines = suffixes.read().splitlines()
    lines = tuple(lines)
    if str.endswith(lines):
        return True
    else:
        return False

def shipibo_suffixes():
    """  Function that returns a list with all the shipibo suffixes

        :returns: list with all the suffixes
        :rtype: list

        :Example:

        >>> import chana.lemmatizer
        >>> chana.lemmatizer.shipibo_suffixes()
        ['naan', 'yama', 'men', 'iosma', ..., 'shoko']
        
    """
    my_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(my_path, "files/lemmatizer/shipibo_suffixes.dat")
    suffixes = codecs.open(path, "r", "utf-8")
    shipibo_suffixes = suffixes.read().splitlines()
    return(shipibo_suffixes)


class ShipiboLemmatizer:
    """
    Instance of the pre-trained shipibo lemmatizer
    """

    def __init__(self):
        """
        Constructor of the class that loads the pretrained model
        """
        my_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(my_path, "files/lemmatizer/shipibo_knn_model.pkl")
        self.lemmatizer = joblib.load(path)
        self.features_length = 18

    def preprocess_word(self, word):
        """ Method that turns a word in an array of features for the classifier

        :param word: a word to be transformed
        :type word: str
        :returns: list with the features
        :rtype: list

        :Example:

        >>> import chana.lemmatizer
        >>> lemmatizer = chana.lemmatizer.ShipiboLemmatizer()
        >>> lemmatizer.preprocess_word('shipibobo')
        [111, 98, 111, 98, 105, 112, 105, 104, 115, 0, 0, 0, 0, 0, 0, 0, 0, 0]        
        
    """
        features = [0 for x in range(self.features_length)]
        i = 0
        pal = reversed(list(word))
        for letter in pal:
            features[i]=ord(letter)
            i+=1
        return features

    def get_lemma(self, rule, word):
        """ Method that returns the lemma of a shipibo word given a possible rule

        :param rule: a rule to transform a word
        :type rule: list
        :param word: a word to be transformed
        :type word: str
        :returns: word transformed
        :rtype: str

        :Example:

        >>> import chana.lemmatizer
        >>> lemmatizer = chana.lemmatizer.ShipiboLemmatizer()
        >>> lemmatizer.get_lemma(['bo>'],'shipibobo')
        'shipibo'       
        
    """
        rule = (rule[0].split('>'))
        substract = rule[0]
        add = rule[1]
        if substract=='':
            return word+add
        elif word.endswith(substract):
            lemma = replace_last(word,substract,add)
            return lemma
        else:
            return word    

    def get_rule(self, word):
        """ Method that returns the transformation rule for a shipibo word

        :param word: a word to get the rule
        :type word: str
        :returns: numpy array with the rule
        :rtype: array

        :Example:

        >>> import chana.lemmatizer
        >>> lemmatizer = chana.lemmatizer.ShipiboLemmatizer()
        >>> lemmatizer.get_rule('pikanwe')
        array(['anwe>i'], dtype='<U16')       
        
    """
        lemma_num = self.preprocess_word(word)
        lemma_num = np.array(lemma_num).reshape(1 ,-1)
        rule = self.lemmatizer.predict(lemma_num)
        return rule

    def lemmatize(self, word):
        """ Method that predicts the lemma of a shipibo word

        :param word: a word to get the lemma
        :type word: str
        :returns: lemma of the word
        :rtype: str

        :Example:

        >>> import chana.lemmatizer
        >>> lemmatizer = chana.lemmatizer.ShipiboLemmatizer()
        >>> lemmatizer.lemmatize('pikanwe')
        'piki'       
        
    """
        if has_shipibo_suffix(word): 
            rule = self.get_rule(word)
            lemma = self.get_lemma(rule, word)
            return lemma
        else:
            return word


class GeneralLemmatizer:
    """
    Instance of a new lemmatizer to be trained and used
    """

    def __init__(self, features_length = 10, n_neighbors = 5):
        """
        Constructor of the class with the number of features to be used by the lemmatizer

        :param features_length: number of features to be used
        :type features_length: int
        :param n_neighbors: number of neighbors to be used
        :type n_neighbors: int

        """
        self.features_length = features_length
        self.n_neighbors = n_neighbors
        self.lemmatizer = None

    def train(self, words, lemmas):
        """ Method that trains a new lemmatizer with a list of words and a list of lemmas of the same size

        :param words: list of words
        :type words: list
        :param lemmas: list of lemmas
        :type lemmas: list
        :returns: none
        :rtype: None

        :Example:

        >>> import chana.lemmatizer
        >>> lemmatizer = chana.lemmatizer.GeneralLemmatizer()
        >>> lemmas = ['perro','gato','mono']
        >>> words = ['perritos','gatitos','monotes']
        >>> lemmatizer.train(words,lemmas)       
        
    """
        if len(words) != len(lemmas):
            return 'Both arrays must be of the same size'

        if len(words) < self.n_neighbors:
            return 'The number of words to train must be greater than the number of neighbors to predict'

        array_clases=[]
        array_features = [[0 for x in range(self.features_length)] for y in range(len(words))]
        iterator = 0

        for word, lemma in zip(words, lemmas):
            sub_string = longest_common_substring(word,lemma)
            left = word.replace(sub_string, "")
            right = lemma.replace(sub_string, "")
            array_clases.append(left+">"+right)
            word = reversed(word)
            let = 0
            for letter in word:
                if(let<self.features_length):
                    array_features[iterator][let] = ord(letter)
                let += 1
            iterator += 1

        model = neighbors.KNeighborsClassifier(n_neighbors=self.n_neighbors, metric='hamming')
        model.fit(array_features, array_clases)
        self.lemmatizer = model


    def preprocess_word(self,word):
        """ Method that turns a word in an array of features for the classifier according to its features_length

        :param word: a word to be transformed
        :type word: str
        :returns: list with the features
        :rtype: list

        :Example:

        >>> import chana.lemmatizer
        >>> lemmatizer = chana.lemmatizer.GeneralLemmatizer()
        >>> lemmatizer.preprocess_word('perritos')
        [115, 111, 116, 105, 114, 114, 101, 112, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]        
        
    """
        features = [0 for x in range(self.features_length)]
        i = 0
        pal = reversed(list(word))
        for letter in pal:
            features[i]=ord(letter)
            i+=1
        return features

    def get_lemma(self, rule, word):
        """ Method that returns the lemma of a word given a possible rule

        :param rule: a rule to transform a word
        :type rule: list
        :param word: a word to be transformed
        :type word: str
        :returns: word transformed
        :rtype: str

        :Example:

        >>> import chana.lemmatizer
        >>> lemmatizer = chana.lemmatizer.GeneralLemmatizer()
        >>> lemmatizer.get_lemma(['bo>'],'shipibobo')
        'shipibo'       
        
    """
        rule = (rule[0].split('>'))
        substract = rule[0]
        add = rule[1]
        if substract=='':
            return word+add
        elif word.endswith(substract):
            lemma = replace_last(word,substract,add)
            return lemma
        else:
            return word    

    def get_rule(self, word):
        """ Method that returns the transformation rule for a word

        :param word: a word to get the rule
        :type word: str
        :returns: numpy array with the rule
        :rtype: array

        :Example:

        >>> import chana.lemmatizer
        >>> lemmatizer = chana.lemmatizer.GeneralLemmatizer()
        >>> lemmatizer.get_rule('perrito')
        array(['ito>0'], dtype='<U16')       
        
    """
        lemma_num = self.preprocess_word(word)
        lemma_num = np.array(lemma_num).reshape(1 ,-1)
        rule = self.lemmatizer.predict(lemma_num)
        return rule

    def lemmatize(self, word):
        """ Method that predicts the lemma of a word with the trained model

        :param word: a word to get the lemma
        :type word: str
        :returns: lemma of the word
        :rtype: str

        :Example:

        >>> import chana.lemmatizer
        >>> lemmatizer = chana.lemmatizer.GeneralLemmatizer()
        >>> lemmatizer.lemmatize('perrito')
        'perro'       
        
    """
        if self.lemmatizer == None:
        	return 'The lemmatizer must be trained first'
        rule = self.get_rule(word)
        lemma = self.get_lemma(rule, word)
        return lemma

