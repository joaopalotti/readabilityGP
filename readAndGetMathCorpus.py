#!/usr/bin/env python
# encoding: utf-8

from __future__ import division
from bs4 import BeautifulSoup
import re
import string
from xml.dom import minidom
from processFile import *
import urllib2

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def getElement(item, name):
    element = item.getElementsByTagName(name)[0] 
    return getText(element.childNodes)

if __name__ == "__main__":
    
    dataDir = "MathWebpageCorpus"
    outFileName = "MathWebpage"
    fo = open( outFileName + ".out", "w")
#    fo.write("%s,,,%s,,,%s,,,%s,,,%s,,,%s,,,%s,,,%s,,,%s,,,%s,,,%s,,,%s,,,%s,,,%s\n" % ("filename",\
    fo.write("%s,,,%s,,,%s\n" % ("filename",\
          #  "numWords",\
          #  "numSentences",\
          #  "numSyllables",\
          #  "avgWordLengthSyl",\
          #  "avgWordLengthInChars",\
          #  "avgSenLengthInChars",\
          #  "avgWordsPerSentece",\
          #  "avgSyllablesPerSentence",\
            "fleschReadingEase",\
          #  "fleschKincaidGradeLevel",\
           # "colemanLiauIndex",\
           # "lixIndex",\
            "goal"))

    xmldoc = minidom.parse('MathWebpageCorpus.xml')
    itemlist = xmldoc.getElementsByTagName('item') 
    
    for item in itemlist:
        if getElement(item, 'status') == "Annotated":
            url = getElement(item, 'url')
            title = getElement(item, 'filename')
            readability = getElement(item, 'readability')
            print item.attributes['ID'].value, title, readability, url
            
            res = urllib2.urlopen("http://www.read-able.com/check.php?uri="+url)
            html = res.read()
            soup  = BeautifulSoup(html)
            
            #print soup
            if "Sorry! We can't get to that page" in soup.h2.text:
                print "Failed ---> ", title
                continue
            
            fkre = soup.table.td.text
            fo.write("%s,,,%f,,,%f\n" % (title, float(fkre), float(readability)))
            
            #processFile(title, dataDir, fo, float(readability), removeWikiGarbage=False)
            
