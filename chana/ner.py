#coding=UTF-8
"""
Named-entity recognizer for shipibo-konibo
Source model is from the Chana project and use predefined rules for the language as well as a crf from pycrfsuite
"""
import codecs
import collections
import re
import os
import string
import numpy as np
import pycrfsuite


def load_array(file,array):
    """
    Inner function that loads the information of a file into a list

    :param file: a file to be loaded
    :type file: File
    :param array: a list to be populated with the information from the file
    :type array: list
    :returns: none
    :rtype: None
    """
    my_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(my_path, file)
    f = codecs.open(path, "r", encoding= "utf-8")
    f_read = f.read()
    lines = f_read.splitlines()
    for word in lines:
        first_letter = word[0]
        array[first_letter].append(word)
    f.close()
    for key, elem in array.items():
        array[key]='|'.join(elem)

def is_number(word):
    """ Function that returns 'NUM' if a shipo word is a number or False if not

        :param word: a word to be evaluated
        :type word: str
        :returns: 'NUM' if a shipo word is a number or False if not
        :rtype: str

        :Example:

        >>> import chana.ner
        >>> chana.ner.is_number('kimisha')
        'NUM'
        
    """
    numbers=['westiora','rabé','kimisha','chosko','pichika','sokota','kanchis','posaka','iskon','chonka','pacha','waranka']
    if word.lower() in numbers:
        return 'NUM'
    else:
        return False

def is_location(word):
    """ Function that returns 'LOC' if a shipo word is a location or False if not

        :param word: a word to be evaluated
        :type word: str
        :returns: 'LOC' if a shipo word is a location or False if not
        :rtype: str

        :Example:

        >>> import chana.ner
        >>> chana.is_location.is_name('Limanko')
        'LOC'
        
    """
    pattern = re.compile('ain|nko|ainko|mea|meax|nkonia|nkoniax|kea|keax|ainoa|ainoax|oa|oax')
    
    letters = string.ascii_uppercase + 'Ñ'
    locations = dict.fromkeys(letters, [])
    
    load_array('files/ner/loc_esp_s.dat', locations)

    if word.istitle():
        first_letter = word[0]
        if pattern.search(word):
            return 'LOC'
        elif re.search('[ÑA-Z]', first_letter)!=None and re.compile(locations[first_letter]).search(word):
            return 'LOC'
    else:
        return False

def is_name(word):
    """ Function that returns 'PER' if a shipo word is a proper name/person or False if not

        :param word: a word to be evaluated
        :type word: str
        :returns: 'PER' if a shipo word is a proper name/person or False if not
        :rtype: str

        :Example:

        >>> import chana.ner
        >>> chana.ner.is_name('Adriano')
        'PER'
        
    """
    letters = string.ascii_uppercase + 'Ñ'
    names = dict.fromkeys(letters, [])
    
    load_array('files/ner/per_esp_s.dat', names)

    if word.title():
        first_letter=word[0]
        if re.search('[ÑA-Z]', first_letter)!=None and re.compile(names[first_letter]).search(word):
            return 'PER'
    else:
        return False

def is_organization(word):
    """ Function that returns 'ORG' if a shipo word is an organization or False if not

        :param word: a word to be evaluated
        :type word: str
        :returns: 'ORG' if a shipo word is an organization or False if not
        :rtype: str

        :Example:

        >>> import chana.ner
        >>> chana.ner.is_organization('AUT')
        'ORG'
        
    """
    letters = string.ascii_uppercase + 'Ñ'
    organizations = dict.fromkeys(letters, [])
    
    load_array('files/ner/org_esp_s.dat', organizations)

    if word.title():
        first_letter=word[0]
        if re.search('[ÑA-Z]', first_letter)!=None and re.compile(organizations[first_letter]).search(word):
            return 'ORG'
    else:
        return False

def is_date(word):
    """ Function that returns 'FEC' if a shipo word is a date or False if not

        :param word: a word to be evaluated
        :type word: str
        :returns: 'FEC' if a shipo word is a date or False if not
        :rtype: str

        :Example:

        >>> import chana.ner
        >>> chana.ner.is_date('Agosto')
        'FEC'
        
    """
    months=['enero','febrero','marzo','abril','mayo','junio','julio','agosto','setiembre','octubre','noviembre','diciembre']
    if word.lower() in months:
        return 'FEC'


class ShipiboNER:
    """
    Instance of the rule based NER for shipibo
    """
    def __init__(self):
        """
        Constructor of the class that loads the crf model and the information files
        """
        self.letters = string.ascii_uppercase + 'Ñ'
        
        self.names = dict.fromkeys(self.letters, [])
        self.locations = dict.fromkeys(self.letters, [])
        self.organizations = dict.fromkeys(self.letters, [])

        self.tagger = pycrfsuite.Tagger()
        my_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(my_path, 'files/ner/crf_ner.crfsuite')
        self.tagger.open(path)


        load_array('files/ner/per_esp_s.dat',self.names)
        load_array('files/ner/loc_esp_s.dat',self.locations)
        load_array('files/ner/org_esp_s.dat',self.organizations)

    def check_locations(self,words,entity_tag):
        """
        Inner method that tags the locations of a sentence with 'LOC'

        :param words: a list of words to be evaluated
        :type words: list
        :param entity_tag: a list of words to be evaluated
        :type entity_tag: list
        :returns: none
        :rtype: None
        """
        pattern = re.compile('ain|nko|ainko|mea|meax|nkonia|nkoniax|kea|keax|ainoa|ainoax|oa|oax')
        idWord=0
        last_Loc=-1
        for word in words:
            if word.istitle():
                first_letter=word[0]
                if pattern.search(word):
                    entity_tag[idWord]='LOC'
                    last_Loc=idWord
                elif re.search('[ÑA-Z]', first_letter)!=None and re.compile(self.locations[first_letter]).search(word):
                        entity_tag[idWord]='LOC'
                        last_Loc=idWord
            idWord+=1

    def check_names(self,words,entity_tag):
        """
        Inner method that tags the names/persons of a sentence with 'PER'

        :param words: a list of words to be evaluated
        :type words: list
        :param entity_tag: a list of words to be evaluated
        :type entity_tag: list
        :returns: none
        :rtype: None
        """
        idWord=0
        last_per=-1
        for word in words:
            if word.title():
                first_letter=word[0]
                if re.search('[ÑA-Z]', first_letter)!=None and re.compile(self.names[first_letter]).search(word):
                    entity_tag[idWord]='PER'
                    last_per=idWord
            idWord+=1

    def check_organizations(self,words,entity_tag):
        """
        Inner method that tags the organizations of a sentence with 'ORG'

        :param words: a list of words to be evaluated
        :type words: list
        :param entity_tag: a list of words to be evaluated
        :type entity_tag: list
        :returns: none
        :rtype: None
        """
        idWord=0
        last_org=-1
        for word in words:
            if word.title():
                first_letter=word[0]
                if re.search('[ÑA-Z]', first_letter)!=None and re.compile(self.organizations[first_letter]).search(word):
                    entity_tag[idWord]='ORG'
                    last_org=idWord
            idWord+=1

    def check_numbers(self,words,entity_tag):
        """
        Inner method that tags the numbers of a sentence with 'NUM'

        :param words: a list of words to be evaluated
        :type words: list
        :param entity_tag: a list of words to be evaluated
        :type entity_tag: list
        :returns: none
        :rtype: None
        """
        numbers=['westiora','rabé','kimisha','chosko','pichika','sokota','kanchis','posaka','iskon','chonka','pacha','waranka']
        idWord=0
        for word in words:
            if word.lower() in numbers:
                entity_tag[idWord]='NUM'
            idWord+=1

    def check_dates(self,words,entity_tag):
        """
        Inner method that tags the dates of a sentence with 'FEC'

        :param words: a list of words to be evaluated
        :type words: list
        :param entity_tag: a list of words to be evaluated
        :type entity_tag: list
        :returns: none
        :rtype: None
        """
        months=['enero','febrero','marzo','abril','mayo','junio','julio','agosto','setiembre','octubre','noviembre','diciembre']
        idWord=0
        last_date=-1
        for word in words:
            if word.lower() in months:
                entity_tag[idWord]='FEC'
                last_date=idWord
                if idWord > 0:
                    pre=words[idWord-1]
                    if pre.isdigit():
                        entity_tag[idWord-1]='FEC'
                if idWord<len(words)-1:
                    pos=words[idWord+1]
                    if pos.isdigit():
                        entity_tag[idWord+1]='FEC'
            idWord+=1

    def rule_tag(self, sentence):
        """ Method that tags a sentence with the rule based system

        :param sentence: a sentence to be evaluated
        :type sentence: str
        :returns: list with the ner tags
        :rtype: list

        :Example:

        >>> import chana.ner
        >>> ner = chana.ner.ShipiboNer()
        >>> ner.rule_tag('Limanko enra atsawe')
        ['LOC', 'O', 'O']
        
    """
        words=sentence.split()
        entity_tag=[]
        for x in range(len(words)):
            entity_tag.append('O')
        self.check_names(words,entity_tag)
        self.check_organizations(words,entity_tag)
        self.check_locations(words,entity_tag)
        self.check_numbers(words,entity_tag)
        self.check_dates(words,entity_tag)
        return entity_tag

    def word2features(self,sent, i):
        """
        Inner method that add features to the words of a sentence to be tagged by the crf model

        :param sent: a sentence in list form to be transformed into features
        :type sent: list
        :param i: index of the word to be evaluated
        :type i: int
        :returns: list with the features for the indexed word
        :rtype: list
        """
        word = sent[i][0]
        tagBR = sent[i][1]
        features = [
            'bias',
            'word.lower=' + word.lower(),
            'word[-3:]=' + word[-3:],
            'word[-2:]=' + word[-2:],
            'word.isupper=%s' % word.isupper(),
            'word.istitle=%s' % word.istitle(),
            'word.isdigit=%s' % word.isdigit(),
            'tagBR=' + tagBR,
            'tagBR[:2]=' + tagBR[:2],
        ]
        if i > 0:
            word1 = sent[i-1][0]
            tagBR1 = sent[i-1][1]
            features.extend([
                '-1:word.lower=' + word1.lower(),
                '-1:word.istitle=%s' % word1.istitle(),
                '-1:word.isupper=%s' % word1.isupper(),
                '-1:tagBR=' + tagBR1,
                '-1:tagBR[:2]=' + tagBR1[:2],
            ])
        else:
            features.append('BOS')


        if i < len(sent)-1:
            word1 = sent[i+1][0]
            tagBR1 = sent[i+1][1]
            features.extend([
                '+1:word.lower=' + word1.lower(),
                '+1:word.istitle=%s' % word1.istitle(),
                '+1:word.isupper=%s' % word1.isupper(),
                '+1:tagBR=' + tagBR1,
                '+1:tagBR[:2]=' + tagBR1[:2],
            ])
        else:
            features.append('EOS')

        return features

    def sent2features(self,sent):
        """
        Inner method that add features to a sentence to be tagged by the crf model
        
        :param sent: a sentence in list form to be transformed into features
        :type sent: list
        :returns: list with features
        :rtype: list

        """
        return [self.word2features(sent, i) for i in range(len(sent))]

    def crf_tag(self,sentence):
        """ Method that tags a sentence with the rule based method and then with the crf model

        :param sentence: a sentence to be evaluated
        :type sentence: str
        :returns: list with the ner tags
        :rtype: list

        :Example:

        >>> import chana.ner
        >>> ner = chana.ner.ShipiboNer()
        >>> ner.crf_tag('Limanko enra atsawe')
        ['LOC', 'O', 'O']
        
    """
        entity_tag_R=self.rule_tag(sentence)
        vectorWord=[]
        words=sentence.split()
        idWord=0
        for word in words:
                tag_r=entity_tag_R[idWord]
                result_tag=(word,tag_r)
                vectorWord.append(result_tag)
                idWord+=1
        entity_tag=self.tagger.tag(self.sent2features(vectorWord))
        return entity_tag