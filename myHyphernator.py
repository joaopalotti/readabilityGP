#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function
from hyphenator import Hyphenator
from wordnik import *
import time, urllib2, re, csv

class myHyphernator:

    def __init__(self):

        with open("wordnik.conf", "r") as wf:
            api_key = wf.read()
        
        client = swagger.ApiClient(api_key, 'http://api.wordnik.com/v4')
        self.__wordApi = WordApi.WordApi(client)

        self.__hyp = Hyphenator("hyph_en_GB.dic")
        
        self.__cache = {}
        try:       
            with open("__hypernationCache") as fread:
                reader = csv.reader(fread, delimiter='\t')
                for row in reader:
                    #print (row,)
                    (word, syls) = row
                    self.__cache[word] = int(syls.strip()) 
            

            #self.__cacheFile = file("__hypernationCache", "a+")

        except IOError:
            print("CACHE FILE NOT FOUND!")
            #self.__cacheFile = file("__hypernationCache", "w")
            #self.__csvw = csv.writer(self.__filePointer, delimiter="\t")

    def numberOfSyllables(self, word):
        
        word = word.lower().encode('unicode_escape').strip()
        if len(word) == 0:
            return 0

        if re.match(r"^[\d\W]*$",word):
            return 1

        num = 0
        OK = False
        tries = 3
        if word in self.__cache:
            return self.__cache[word]
        
        syls = None
        while not OK and tries > 0:        
            try:
                syls = self.__wordApi.getHyphenation( word, useCanonical=True)
                OK = True
            
            except urllib2.HTTPError, e:
                    print ("HTTPERROR ===> ", e.code)
                    print ("Word ... ===> ", word)
                    tries -= 1
        
            except urllib2.URLError, e:
                    print ("URLERROR ===> ", e.args)
                    print ("Sleeping to try again latter.... -> Word ", word )
                    time.sleep(0.5)


        if syls:
            #print word, " ---> " , len(syls), " ---------- --- --- - -- " , num
            num = len(syls)
        else:
            #print "Not found ", word, " ==--------------->>>> " , num
            num = len(self.__hyp.positions(word)) + 1

        #print("ADDING TO CACHE AND WRITING FILE  -----  %s=====%d" % (word, num))
        #print("%s\t%d" % (word, num), file=self.__cacheFile)
        
        with open("__hypernationCache", "a+") as fwrite:
            csvw = csv.writer(fwrite, delimiter="\t")
            csvw.writerow([word,num])
        
        self.__cache[word] = num
        
        return num
