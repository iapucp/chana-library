#coding=UTF-8
"""
Lemmatizer for shipibo-konibo

General functions to use the lemmatizer for shipibo-konibo or to train a new lemmatizer for other similar languages (agglutinative)
Both lemmatizers use a KNeighborsClassifier from scikit-learn

Source model for the shipibo lemmatizer is from the Chana project
"""
import codecs
import os
import numpy as np
from sklearn.externals import joblib
from sklearn import neighbors
import warnings

warnings.filterwarnings("ignore")

def replace_last(source_string, replace_what, replace_with):
    """
    Function that replaces the last ocurrence of a string in a word
    """
    head, _sep, tail = source_string.rpartition(replace_what)
    return head + replace_with + tail

def longest_common_substring(string1, string2):
    """
    Function to find the longest common substring of two strings
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
    """
    Function that returns the possible existence of a shipo suffix in a a word
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
    """
    Function that returns a list with all the shipibo suffixes
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
        my_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(my_path, "files/lemmatizer/shipibo_knn_model.pkl")
        self.lemmatizer = joblib.load(path)
        self.features_length = 18

    def preprocess_word(self, word):
        """
        Method that turns a word in an array of features for the classifier
        """
        features = [0 for x in range(self.features_length)]
        i = 0
        pal = reversed(list(word))
        for letter in pal:
            features[i]=ord(letter)
            i+=1
        return features

    def get_lemma(self, rule, word):
        """
        Method that returns the lemma of a shipibo word given a possible rule
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
        """
        Method that returns the transformation rule for a shipibo word
        """
        lemma_num = self.preprocess_word(word)
        lemma_num = np.array(lemma_num).reshape(1 ,-1)
        rule = self.lemmatizer.predict(lemma_num)
        return rule

    def lemmatize(self, word):
        """
        Method that predicts the lemma of a shipibo word
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
        """
        self.features_length = features_length
        self.n_neighbors = n_neighbors
        self.lemmatizer = None

    def train(self, words, lemmas):
        """
        Method that trains a new lemmatizer with an array of words and an array of lemmas of the same size
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
        """
        Method that turns a word in an array of features for the classifier
        """
        features = [0 for x in range(self.features_length)]
        i = 0
        pal = reversed(list(word))
        for letter in pal:
            features[i]=ord(letter)
            i+=1
        return features

    def get_lemma(self, rule, word):
        """
        Method that returns the lemma of a word given a possible rule
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
        """
        Method that returns the transformation rule for a word
        """
        lemma_num = self.preprocess_word(word)
        lemma_num = np.array(lemma_num).reshape(1 ,-1)
        rule = self.lemmatizer.predict(lemma_num)
        return rule

    def lemmatize(self, word):
        """
        Method that predicts the lemma of a word
        """
        if self.lemmatizer == None:
        	return 'The lemmatizer must be trained first'
        rule = self.get_rule(word)
        lemma = self.get_lemma(rule, word)
        return lemma

