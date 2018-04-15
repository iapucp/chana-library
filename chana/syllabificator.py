#coding=UTF-8
"""
Syllabificator for shipibo-konibo.
General functions and rules to syllabify a shipibo-konibo word
"""
def syllabify(word):
    """ Function that returns all the syllables of a word

        :param word: a word to get its syllables
        :type word: str
        :returns: list of syllables
        :rtype: list

        :Example:

        >>> import chana.syllabificator
        >>> chana.syllabificator.syllabify('atsabo')
        ['a', 'tsa', 'bo']

    """
    word_vc = get_vc(word)
    sibilantes = ['m','n', 's', 'sh', 'x']
    syllables = []
    syllable = ""
    actual_pos = len(word_vc) - 1
    if len(word_vc) == 1:
        syllables.append(word_vc[0][0])
        return syllables
    while actual_pos >= 0 and word_vc:
        #vowl check
        if word_vc[actual_pos][1] == 'V':
            syllable = word_vc[actual_pos][0]
            del word_vc[-1]
            actual_pos = actual_pos - 1
            #long vowel
            if word_vc and (word_vc[actual_pos][0] == syllable or
                              word_vc[actual_pos][0] == accentuate(syllable)):
                if (len(word_vc) > 1):
                    syllables.insert(0, syllable)
                    syllable = ""
                else:
                    syllables.insert(0, syllable)
                    syllable = ""
            elif word_vc and word_vc[actual_pos][1] == 'C':          
                if (word_vc[actual_pos][0] == 'u' or
                        word_vc[actual_pos][0] == accentuate('u') or word_vc[actual_pos][0] == 'h'):                    
                    syllables.insert(0, syllable)
                    syllable = ""
                else:                   
                    #Se agrega a la syllable CV
                    syllable = word_vc[actual_pos][0] + syllable  #C
                    actual_pos = actual_pos - 1
                    del word_vc[-1]
                    syllables.insert(0, syllable)
                    syllable = ""
            else:
                if (len(word_vc) < 2 and actual_pos != 0):  #lone syllable
                    syllables.insert(0, syllable)
                    syllable = ""
                    actual_pos = actual_pos - 1
                    if (word_vc):
                        del word_vc[-1]
                else:
                    syllables.insert(0, syllable)
                    syllable = ""
        else: #consonant check           
            if word_vc[actual_pos][0] in sibilantes:
                syllable = word_vc[actual_pos][0] + syllable
                actual_pos = actual_pos - 1
                if (word_vc):
                    del word_vc[-1]
                #first CVC 
                if word_vc and word_vc[actual_pos][1] == 'V':
                    syllable = word_vc[actual_pos][0] + syllable  #V
                    actual_pos = actual_pos - 1
                    del word_vc[-1]
                    #syllable = VC
                    if len(word_vc) and word_vc[actual_pos][1] == 'C':
                        if word_vc[actual_pos][0] == 'u' or word_vc[
                                actual_pos][0] == accentuate('u') or word_vc[actual_pos][0] == 'h':
                            syllables.insert(0, syllable)
                            syllable = ""
                        else:
                            #is CVC
                            syllable = word_vc[actual_pos][0] + syllable  #V
                            syllables.insert(0, syllable)
                            syllable = ""
                            actual_pos = actual_pos - 1
                            del word_vc[-1]
                    else:  #is VC
                        syllables.insert(0, syllable)
                        syllable = ""
                else:
                    if word_vc and (word_vc[actual_pos][0] == 'u' or
                                      word_vc[actual_pos][0] == accentuate('u')):
                        syllables.insert(0, syllable)
                        syllable = ""
                        actual_pos = actual_pos - 1
                        del word_vc[-1]
            else:
                if (word_vc[actual_pos][0] == 'h'):
                    syllable = word_vc[actual_pos][0]
                    actual_pos = actual_pos - 1
                    del word_vc[-1]
                elif (word_vc[actual_pos][0] == 'u' or
                        word_vc[actual_pos][0] == accentuate('u')):                   
                    syllable = word_vc[actual_pos][0]
                    syllables.insert(0, syllable)
                    syllable = ""
                    actual_pos = actual_pos - 1
                    if (word_vc):
                        del word_vc[-1]
                else:
                    if len(syllables):
                        if word_vc[actual_pos][0] == 't' and syllables[0][0] == 's':
                            syllables[0] = word_vc[actual_pos][0] + syllables[0]
                        if word_vc[actual_pos][0] == 'c' and syllables[0][0] == 'h':
                            syllables[0] = word_vc[actual_pos][0] + syllables[0]
                        if word_vc[actual_pos][0] == 's' and syllables[0][0] == 'h':                        
                            syllables[0] = word_vc[actual_pos][0] + syllables[0]
                    actual_pos = actual_pos - 1
                    if (word_vc):
                        del word_vc[-1]
    return syllables

def get_vc(word):
    """ Function that returns all the vowels and consonants of a word

        :param word: word to get its vowels and consonants
        :type word: str
        :returns: list of 'V' and 'C' for each letter of the word
        :rtype: list

        :Example:

        >>> import chana.syllabificator
        >>> chana.syllabificator.get_vc('piti')
        [['p', 'C'], ['i', 'V'], ['t', 'C'], ['i', 'V']]

    """
    structure = []
    vowels = ['a', 'e', 'i', 'o']
    acentuado = ['á', 'é', 'í', 'ó']
    specials = ['ch', 'hu', 'sh', 'ts', 'qu'] 
    pos_special_cons = -1
    transformation = {
        "ch": "1",
        "hu": "2",
        "sh": "3",
        "ts": "4",
        "qu": "5"
    } 
    for special in specials:
        if special in word:
            word = word.replace(special, transformation[special])
    for pos in range(0, len(word)):
        if (pos_special_cons != -1):
            if pos != pos_special_cons + 1:
                if word[pos] in vowels or word[pos] in acentuado:
                    structure.append([word[pos], "V"])
                else:
                    if word[pos] == " ":
                        structure.append([word[pos], " "])
                    else:
                        if word[pos] == "-":
                            structure.append([word[pos], "-"])
                        else:
                            structure.append([word[pos], "C"])
            else:  
                structure[pos - 1] = [word[pos - 1] + word[pos], "C"]
        else:
            if word[pos] in vowels or word[pos] in acentuado:
                structure.append([word[pos], "V"])
            else:
                if word[pos] == " ":
                    structure.append([word[pos], " "])
                else:
                    if word[pos] == "-":
                        structure.append([word[pos], "-"])
                    else:
                        structure.append([word[pos], "C"])
    for syllable in structure:
        syllable[0] = change(syllable[0])
    return structure

def change(syllable):

    """ Function that returns the original form of a syllable

        :param syllable: a syllable to be transformed
        :type syllable: str
        :returns: syllable with its original form
        :rtype: str

        :Example:

        >>> import chana.syllabificator
        >>> chana.syllabificator.change('1a')
        cha

    """
    if "1" in syllable:
        syllable = syllable.replace("1", "ch")
    elif "2" in syllable:
        syllable = syllable.replace("2", "hu")
    elif "3" in syllable:
        syllable = syllable.replace("3", "sh")
    elif "4" in syllable:
        syllable = syllable.replace("4", "ts")
    elif "5" in syllable:
        syllable = syllable.replace("5", "qu")
    else:
        syllable = syllable.replace("6", "bu")
    return syllable

def accentuate(letter):
    """ Function that adds the accentuation mark of a letter:

        :param letter: a letter to be accentuated
        :type letter: str
        :returns: letter accentuated
        :rtype: str

        :Example:

        >>> import chana.syllabificator
        >>> chana.syllabificator.accentuate('a')
        á

    """
    if letter == "a":
        letter = "á"
    elif letter == "e":
        letter = "é"
    elif letter == "i":
        letter = "í"
    elif letter == "o":
        letter = "ó"
    elif letter == "u":
        letter = "ú"
    return letter
