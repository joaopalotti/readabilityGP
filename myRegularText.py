#!/usr/bin/env python
# encoding: utf-8

from __future__ import division
import nltk
import re, string, math
from myHyphernator import myHyphernator
from nltk import word_tokenize, wordpunct_tokenize
from collections import Counter
import nltk.data # to import "punkt"
from nltk.tokenize.punkt import PunktWordTokenizer

from myText import MyText

'''
'''

class MyRegularText(MyText):
    
    #self.sentences = []
    #self.__data = []

    def __init__(self, rawData):
        super(MyRegularText, self).__init__(rawData)

        self.__makeSentences()
        self.__makeWords()
        self.__myHyp = myHyphernator()
    
    def __makeWords(self):
        self.words = []
        for sen in range(len(self.sentences)):
                
            allTokens = PunktWordTokenizer().tokenize(self.sentences[sen])
            #allTokens = nltk.wordpunct_tokenize(self.sentences[sen]) 
                    
            #eliminate empty words and eliminate . from the final of words:
            # Ex.:  This is the final. -> ['This', 'is', 'the', 'final.'] -> [...,'final']
            tokens = [re.sub('\.', '', tok) for tok in allTokens if tok]
                    
            #TODO: improve this quick and dirt solution
            tokens2 = [tok for tok in allTokens if tok not in '.']
                    
            if not tokens or not tokens2:
                continue

            self.words += tokens[:]
            self.sentences[sen] = tokens[:]

    def __makeSentences(self):
        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        self.sentences = tokenizer.tokenize(self.raw.strip())
 
