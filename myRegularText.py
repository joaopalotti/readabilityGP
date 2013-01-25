#!/usr/bin/env python
# encoding: utf-8

from __future__ import division
import nltk
import re
import string
from myHyphernator import myHyphernator
from nltk import word_tokenize, wordpunct_tokenize

'''
'''

class MyRegularText:
    
    #self.__sentences = []
    #self.__data = []

    def __init__(self, rawData):
        self.__raw = rawData
        
        #self.__tokens = self.__tokenize()
        self.__makeSentences()
        self.__makeWords()
        self.__myHyp = myHyphernator()
    
    def validDocument(self):
        return self.getNumberOfWords() > 0

    def __tokenize(self):
        self.__tokens = nltk.word_tokenize(self.__raw)
        openSection = False
        strSaved = ""
        initialT = -1
        markedToDelete = []

        for t in range(len(self.__tokens)):
            str = self.__tokens[t]
            
            # There is only one == in this term
            if "==" in str and not re.match("==[\w\s]*==", str) and not openSection:
                openSection = True
                strSaved = str
                initialT = t
            
            elif "==" in str and openSection:
                strSaved = strSaved + " " + str
                self.__tokens[initialT] = strSaved
                markedToDelete.append(t)
                openSection = False

            elif openSection:
                strSaved = strSaved + " " + str
                markedToDelete.append(t)

        for t in reversed(markedToDelete):
            del self.__tokens[t]
        print self.__tokens

    def words(self):
        return self.__words

    def getNumberOfWords(self):
        return len( [w for w in self.__words if w not in string.punctuation] )

    def getNumberOfSyllables(self):
        return sum ( [self.__myHyp.numberOfSyllables(w) for w in self.__words if w not in string.punctuation] )

    def sentences(self):
        return self.__sentences
    
    def __makeWords(self):
        self.__words = []
        for sen in range(len(self.__sentences)):
                
            allTokens = nltk.wordpunct_tokenize(self.__sentences[sen]) 
                    
            #eliminate empty words 
            tokens = [tok for tok in allTokens if tok]
                    
            #TODO: improve this quick and dirt solution
            tokens2 = [tok for tok in allTokens if tok not in '.']
                    
            if not tokens or not tokens2:
                continue

            self.__words += tokens[:]
            self.__sentences[sen] = tokens[:]

    def __makeSentences(self):
        self.__sentences = self.__raw.split(".")
 
    def getNumberOfSentences(self):
        return len(self.__sentences)

    def getAvgSentenceLengthInChars(self):
        #all words
        #return sum( [ len(sen) for sen in self.__sentences for w in sen if w not in string.punctuation ] ) / len(self.__sentences)
        # excluding punctuation
        
        if self.getNumberOfSentences() == 0:
            return 0.0
        return sum( [len(w) for sen in self.__sentences for w in sen if w not in string.punctuation ] ) / len(self.__sentences)
    
#    def getAvgSentenceLengthInSyllables(self):
#        return sum( [self.__myHyp.numberOfSyllables(w) for sen in self.__sentences for w in sen if w not in string.punctuation ] ) / len(self.__sentences)
### equal to - > avgSyllablesPerSentence = numSyllables / numSentences

    def getAvgWordLengthInChars(self):
        if self.getNumberOfWords() == 0:
            return 0.0
        nonPunctationWords =  [len(w) for w in self.__words if w not in string.punctuation]
        return sum(nonPunctationWords) / len(nonPunctationWords)

    def getAvgWordLengthInSyllables(self):
        if self.getNumberOfWords() == 0:
            return 0.0
        nonPunctationWords =  [self.__myHyp.numberOfSyllables(w) for w in self.__words if w not in string.punctuation]
        return sum(nonPunctationWords) / len(nonPunctationWords)

    def getFleschReadingEase(self):
        if self.getNumberOfSentences() == 0:
            return 0.0
        return 206.835 - 1.015 * ( self.getNumberOfWords() / self.getNumberOfSentences() ) - 85.6 * ( self.getNumberOfSyllables()/  self.getNumberOfWords() )

    def getFleschKincaidGradeLevel(self):
        if self.getNumberOfSentences() == 0:
            return 0.0
        return 0.39 * ( self.getNumberOfWords() / self.getNumberOfSentences() ) + 11.8 * ( self.getNumberOfSyllables() / self.getNumberOfWords() ) - 15.59

    def getColemanLiauIndex(self):
        if self.getNumberOfSentences() == 0:
            return 0.0
        return ( 5.89 * self.getAvgWordLengthInChars() ) - ( 30.0 * ( self.getNumberOfSentences() / self.getNumberOfWords() ) ) -15.8

    def getLIX(self):
        if self.getNumberOfSentences() == 0:
            return 0.0
        longWords = len ( [ w for w in self.__words if len(w) >= 7 ] )
        return self.getNumberOfWords() / self.getNumberOfSentences() + ( (100.0 * longWords) / self.getNumberOfWords() )
