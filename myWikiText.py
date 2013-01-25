#!/usr/bin/env python
# encoding: utf-8

from __future__ import division
import nltk
import re
import string
from myHyphernator import myHyphernator
from nltk import word_tokenize, wordpunct_tokenize

'''
''Class myWikiText:
''  int getNumberOfSentences
''  int getNumberOfWords
'''

class MyWikiText:
    
    #self.__sentences = []
    #self.__data = []

    def __init__(self, rawData):
        self.__raw = rawData
        
        #self.__tokens = self.__tokenize()
        self.__sectionsNames = self.__makeSections()
        self.__makeParagraphs()
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
    
    def paragraphs(self):
        return self.__paragraphs

    def sections(self):
        return self.__sections
    
    def sectionsNames(self):
        return self.__sectionsNames

    def __makeWords(self):
        self.__words = []
        paragraphCounter = -1
        senCounter = -1
        for sec in range(len(self.__sections)):
            for par in range(len(self.__sections[sec])):
                tokensInParagraph = []
                for sen in range(len(self.__sections[sec][par])):
                    #allTokens = re.findall("\w+(?:[-']\w+)*|'|[-.(]+|\S\w*", self.__sections[sec][par][sen])
                    allTokens = nltk.wordpunct_tokenize(self.__sections[sec][par][sen]) 
                    
                    #eliminate empty words 
                    tokens = [tok for tok in allTokens if tok]
                    
                    #TODO: improve this quick and dirt solution
                    tokens2 = [tok for tok in allTokens if tok not in '.']
                    
                    if not tokens or not tokens2:
                        continue

                    
                    senCounter += 1
                    self.__words += tokens[:]
                    tokensInParagraph += tokens[:]
                    self.__sentences[senCounter] = tokens[:]
                    self.__sections[sec][par][sen] = tokens 
                
                if tokensInParagraph:
                    paragraphCounter += 1
                    self.__paragraphs[paragraphCounter] = tokensInParagraph

    def __makeSentences(self):
        self.__sentences = []
        paragraphCounter = -1
        
        # Change section object
        for sec in range(len(self.__sections)):
            for par in range(len(self.__sections[sec])):
                #sentences = [sen.strip() for sen in self.__sections[sec][par].split("\n") if len(sen.strip()) > 0]
                sentences = [sen.strip() for sen in re.split("\n|\.", self.__sections[sec][par]) if len(sen.strip()) > 0] #TODO: implement a better way to separate sentences
                if sentences:
                    paragraphCounter += 1
                    self.__sentences += sentences[:]
                    self.__paragraphs[paragraphCounter] = sentences[:]
                    self.__sections[sec][par] = sentences[:]
 
    def __makeParagraphs(self):
        self.__paragraphs = []
        for s in range( len(self.__sections) ):
            innerParagraphs = [ par for par in self.__sections[s].split("\n") if len(par.strip()) > 0]
            if innerParagraphs:
                self.__paragraphs += innerParagraphs[:]
                self.__sections[s] = innerParagraphs[:]

    def __makeSections(self):
        sectionDivision = self.__raw.split("\n=&=")
       
        #Add first nameless section
        self.__sections = [ sectionDivision[0] ] 
        sectionsNames = [""]

        for sec in range(1, len(sectionDivision)):
            sectionName, sectionContent = sectionDivision[sec].split("=&=")
            self.__sections.append(sectionContent) 
            sectionsNames.append(sectionName)
        
        return sectionsNames

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
