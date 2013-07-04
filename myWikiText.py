#!/usr/bin/env python
# encoding: utf-8

from __future__ import division
import nltk
import re, string, math
from myHyphernator import myHyphernator
from nltk import word_tokenize, wordpunct_tokenize

from myText import MyText

'''
''Class myWikiText:
'''

class MyWikiText(MyText):
    
    #self.sentences = []
    #self.__data = []

    def __init__(self, rawData):
        super(MyWikiText, self).__init__(rawData)
        
        #self.__tokens = self.__tokenize()
        self.__sectionsNames = self.__makeSections()
        self.__makeParagraphs()
        self.__makeSentences()
        self.__makeWords()
        
    def __tokenize(self):
        self.__tokens = nltk.word_tokenize(self.raw)
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

    def paragraphs(self):
        return self.__paragraphs

    def sections(self):
        return self.__sections
    
    def sectionsNames(self):
        return self.__sectionsNames

    def __makeWords(self):
        self.words = []
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
                    self.words += tokens[:]
                    tokensInParagraph += tokens[:]
                    self.sentences[senCounter] = tokens[:]
                    self.__sections[sec][par][sen] = tokens 
                
                if tokensInParagraph:
                    paragraphCounter += 1
                    self.__paragraphs[paragraphCounter] = tokensInParagraph

    def __makeSentences(self):
        self.sentences = []
        paragraphCounter = -1
        
        # Change section object
        for sec in range(len(self.__sections)):
            for par in range(len(self.__sections[sec])):
                #sentences = [sen.strip() for sen in self.__sections[sec][par].split("\n") if len(sen.strip()) > 0]
                sentences = [sen.strip() for sen in re.split("\n|\.", self.__sections[sec][par]) if len(sen.strip()) > 0] #TODO: implement a better way to separate sentences
                if sentences:
                    paragraphCounter += 1
                    self.sentences += sentences[:]
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
        sectionDivision = self.raw.split("\n=&=")
       
        #Add first nameless section
        self.__sections = [ sectionDivision[0] ] 
        sectionsNames = [""]

        for sec in range(1, len(sectionDivision)):
            sectionName, sectionContent = sectionDivision[sec].split("=&=")
            self.__sections.append(sectionContent) 
            sectionsNames.append(sectionName)
        
        return sectionsNames

