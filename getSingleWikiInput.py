from __future__ import division
import os
import re
import sys
from myWikiText import MyWikiText
from processFile import *

if __name__ == "__main__":

    dataDir = "data/en"
    title = "Zoonosis.en" 
    fo = sys.stdout
    
    fo.write("%s,,,%s,,,%s,,,%s,,,%s,,,%s,,,%s,,,%s,,,%s,,,%s,,,%s,,,%s,,,%s\n" % ("filename",\
            "numWords",\
            "numSentences",\
            "numSyllables",\
            "avgWordLengthSyl",\
            "avgWordLengthInChars",\
            "avgSenLengthInChars",\
            "avgWordsPerSentece",\
            "avgSyllablesPerSentence",\
            "fleschReadingEase",\
            "fleschKincaidGradeLevel",\
            "colemanLiauIndex",\
            "lixIndex"))
    
    myWikiText = processFile(title, dataDir, fo)
    print myWikiText.sentences()


    fo.close()
