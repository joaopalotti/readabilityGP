from __future__ import division
import os
import re
import sys
from myWikiText import MyWikiText
from processFile import *

if __name__ == "__main__":

    if len(sys.argv) < 2:
        paths = [ "data/en", "data/simple" ]
    else:
        paths = sys.argv[1:]

    print paths
    for path in paths:
        dataDir = path
        outFileName = re.sub("/","",path)
        fo = open(outFileName + ".out", "w")
        print "Writing %s.out" % (outFileName)
        
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
        
        for title in os.listdir(dataDir):
        
        #   print title
            processFile(title, dataDir, fo)
    
        fo.close()
