#!/usr/bin/env python
# encoding: utf-8

from __future__ import division
from bs4 import BeautifulSoup
import re
import string
from xml.dom import minidom
from processFile import *
import urllib2
import random
import collections

from NB import NB

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def getElement(item, name):
    element = item.getElementsByTagName(name)[0] 
    return getText(element.childNodes)


def getStatisticsFromInternet(url):

    res = urllib2.urlopen("http://www.read-able.com/check.php?uri="+url)
    html = res.read()
    soup  = BeautifulSoup(html)

    #print soup
    if "Sorry! We can't get to that page" in soup.h2.text:
        print "Failed ---> ", title
        return -0.0

    fkre = soup.table.td.text
    return fkre


class doc:
    def __init__(self, name, readability, tokens):
        self.name = name
        self.readability = readability
        self.tokens = tokens

def buildNBInput(documents, allTokens):
    nbInput = []
    
    for doc in documents:
        input = {}
        input[0] = int( float(doc.readability) + 0.5)
        input[1] = doc.name
        
        for i in range(len(allTokens)):
            word = allTokens[i]

            if word in doc.tokens:
                input[i+2] = int(doc.tokens[word])
        nbInput.append(input)
    
    nbTest = []
    nbTraining = []
    random.shuffle(nbInput)
    for t in nbInput:
        if random.random() >= 0.8:
            nbTest.append(t)
        else:
            nbTraining.append(t)
    
    print "Using %d intances: %d for training and %d for test" %(len(nbInput), len(nbTraining), len(nbTest))
    #nbInput is read!
    nb = NB()
    nb.trainClassifier(nbTraining)

    nb.testInBatch(nbTest)
    
def buildSVMInput(documents, allTokens):
    
    for doc in documents:
        print "%d" % ( int( float(doc.readability) + 0.5) ),

#        for (key,value) in doc.tokens.iteritems():
#            print "%d:%d" % ( int(allTokens[key]), int(value)),
#        print

        for i in range(len(allTokens)):
            word = allTokens[i]

            if word in doc.tokens:
                print "%d:%d" % (i+1, int(doc.tokens[word])),
            else:
                print "%d:0" % (i+1) ,
        print


if __name__ == "__main__":
    
    dataDir = "MathWebpageCorpus"
    outFileName = "MathWebpage"
    fo = open( outFileName + ".out", "w")
    printLabels(fo)
    
       xmldoc = minidom.parse('MathWebpageCorpus.xml')
    itemlist = xmldoc.getElementsByTagName('item') 
    
    allTokensSet = set()
    documents = list()

    classes = collections.defaultdict(lambda: 0)

    for item in itemlist:
        if getElement(item, 'status') == "Annotated":
            url = getElement(item, 'url')
            title = getElement(item, 'filename')
            readability = getElement(item, 'readability')
            
            classes[int( float(readability) + 0.5)] += 1

            #getStatisticsFromInternet(url)
            #print item.attributes['ID'].value, title, readability, url
            #fo.write("%s,,,%f,,,%f\n" % (title, float(fkre), float(readability)))
            
            myTextObj = processFile(title, dataDir, fo, float(readability), removeWikiGarbage=False, wiki=False)
            tokens = myTextObj.tokens()
            
            documents.append(doc(title, readability, tokens))

            allTokensSet.update(tokens.keys())
            
#    print "NUMBER OF VALID = ", len(allTokensSet)
    #allTokens = dict( zip(allTokensSet, range(1, len(allTokensSet) + 1 )))
    allTokens = list(allTokensSet)

    #buildSVMInput(documents, allTokens)
    buildNBInput(documents, allTokens)

    for c,v in classes.iteritems():
        print "CLASS %s - %d items" % (c,v) 

