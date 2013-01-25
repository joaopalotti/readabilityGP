from __future__ import division
import os
import re
import sys
from bs4 import BeautifulSoup
from myRegularText import MyRegularText
from myWikiText import MyWikiText

def removeLink(matchobj):
    return matchobj.group(0).strip("}] ").split("|")[1]

def saveItemize(matchobj):
    soup = BeautifulSoup(matchobj.group(0))
    if soup.ol:
        return soup.ol.get_text()
    elif soup.ul:
        return soup.ul.get_text()


def makeSection(matchobj):
    soup = BeautifulSoup(matchobj.group(0))
    stringToChange = soup.span.string
    
    #Sometimes, there are more than one aligned 'span' tag
    #This is the best solution found so far.
    if not stringToChange:
        if 'id' in soup.span:
            stringToChange = ' '.join(soup.span['id'].split('_'))
        else: # lets just return
           return 
    
    # I make up this symbol as a section separator because I think it is an option that is not going to appear in the document
    soup.span.string = "\n=&=" + stringToChange + "=&="
    return str(soup.span)

def removeHTMLWikipediaStuff(lines):
    
    # Delete some classes
    lines = re.sub('(?i)<div class="dablink"[\s\S]*?div>', '', lines)
    lines = re.sub('(?i)<div class="magnify"[\s\S]*?div>', '', lines)
    lines = re.sub('(?i)<div class="thumb[\s\S]*?div>', '', lines)
    lines = re.sub('(?i)<div class="rellink[\s\S]*?div>', '', lines)
    lines = re.sub('(?i)<div id="toctitle"[\s\S]*?div>', '', lines)
    
    # Delete (external/internal) refrences
    lines = re.sub('(?i)<div class="reflist[\s\S]*?div>', '', lines)
    lines = re.sub('(?i)<span[^>]*id="references">[\s\S]*?span>','', lines)

    lines = re.sub('(?i)<span[^>]*id="further_reading">[\s\S]*?span>','', lines)
    lines = re.sub('(?i)<span[^>]*id="external_links">[\s\S]*?span>','', lines)
    lines = re.sub('(?i)<span[^>]*id="see_also">[\s\S]*?span>','', lines)
    lines = re.sub('(?i)<span[^>]*id="notes">[\s\S]*?span>','', lines)
    lines = re.sub('(?i)<span[^>]*id="sources_and_notes">[\s\S]*?span>','', lines)
    lines = re.sub('(?i)<span[^>]*id="bibliography">[\s\S]*?span>','', lines)
    
    #Save itemizeses
    #lines = re.sub("<ol>[\s\S]*?ol>", saveItemize , lines)
    #lines = re.sub("<ul>[\s\S]*?ul>", saveItemize , lines)

    # Delete Tables    
    lines = re.sub('(?i)<table class="infobox[\s\S]*?table>', '', lines)
    lines = re.sub('(?i)<ul[\s\S]*?ul>', '', lines)
    lines = re.sub('(?i)<li[\s\S]*?li>', '', lines)
    lines = re.sub('(?i)<th[\s\S]*?th>', '', lines)
    lines = re.sub('(?i)<td[\s\S]*?td>', '', lines)
    lines = re.sub('(?i)<tr[\s\S]*?tr>', '', lines)
    lines = re.sub('(?i)<dt[\s\S]*?dt>', '', lines)
    lines = re.sub('(?i)<span class="editsection"[\s\S]*?span>', '', lines)
    lines = re.sub('(?i)<caption*?caption>', '', lines)
    
    # Remove comments like <!-- comment -->
    lines = re.sub("<!--[\s\S]*?-->", "", lines) 
    
    lines = re.sub('<span class="mw-headline"[\s\S]*?span>', makeSection , lines)

    return lines


def getTextOnly(lines, removeWikiGarbage):
    
    soup = BeautifulSoup(lines)
    text = soup.get_text()
   
    if removeWikiGarbage:
        # Remove references [ number ]   
        text = re.sub("\[[0-9]*\]", "", text)

    return text

def removeWikipediaWikiTextStuff(lines):

    # Remove external multiline references
    lines = re.sub("(?i)<ref[^<]*<[^r]*ref>","", lines)
    # Remove comments like <!-- comment -->
    lines = re.sub("<!--[\s\S]*?-->", "", lines) 

    # Remove "See also" section
    lines = re.sub("(?i)==see also==[^=]*(?===)","", lines)
    lines = re.sub("(?i)==see also==[^$]*$","", lines)

    # Remove "References" section
    lines = re.sub("(?i)==references==[^=]*(?===)","", lines, re.IGNORECASE)
    lines = re.sub("(?i)==references==[^$]*$","", lines, re.IGNORECASE)
    
    # Remove "External Links" section
    lines = re.sub("(?i)==external links==[^=]*(?===)","", lines, re.IGNORECASE)
    lines = re.sub("(?i)==external links==[^$]*$","", lines, re.IGNORECASE)

    # Remove internal links such as {{link|link name}} or [[link|link name]]
    lines = re.sub("{{[\w\s()]*\|([\w\s()]*)}}", removeLink, lines)
    lines = re.sub("\[\[[\w\s()]*\|([\w\s()]*)\]\]", removeLink, lines)
    lines = re.sub("[{}\[\]]", "", lines)

    # Remove italic
    lines = re.sub("'''", "", lines)
    
    # Remove HTML like tokens
    lines = re.sub("<[^>]*>(?: *\n)", "", lines)

    return lines


def processFile(title, dataDir="MathWebpageCorpus", outputFile=sys.stdout, goal=0.0, removeWikiGarbage=True, wiki=True):

    with open(dataDir + "/" + title) as f:
        lines = f.read()
        
    if removeWikiGarbage:
        lines = removeHTMLWikipediaStuff(lines)
    
    textOnly = getTextOnly(lines, removeWikiGarbage)
    
    #print textOnly
    if wiki:
        myTextObj = MyWikiText(textOnly)
    else:
        myTextObj = MyRegularText(textOnly)

    if not myTextObj.validDocument():
        print title , " IS NOT VALID!!!!!!"
        return
        
    fleishReadingEase       = myTextObj.getFleschReadingEase()
    fleschKincaidGradeLevel = myTextObj.getFleschKincaidGradeLevel()
    colemanLiauIndex        = myTextObj.getColemanLiauIndex()
    lixIndex                = myTextObj.getLIX()

    # Syllables
    numSyllables            = myTextObj.getNumberOfSyllables()
    
    # Words
    numWords                = myTextObj.getNumberOfWords()
    avgWordLengthInChars    = myTextObj.getAvgWordLengthInChars()
    avgWordLengthSyl        = myTextObj.getAvgWordLengthInSyllables()
    
    # Sentences
    numSentences            = myTextObj.getNumberOfSentences()
    avgSenLengthInChars     = myTextObj.getAvgSentenceLengthInChars()

    # Combined
    avgWordsPerSentece      = numWords / numSentences
    avgSyllablesPerSentence = numSyllables / numSentences

    #outputFile.write("%s,,,%.3f,,,%.3f,,,%.3f\n" % (title,\
    outputFile.write("%s,,,%d,,,%d,,,%d,,,%.3f,,,%.3f,,,%.3f,,,%.3f,,,%.3f,,,%.3f,,,%.3f,,,%.3f,,,%.3f,,,%.3f\n" % (title,\
                                                            numWords,\
                                                            numSentences,\
                                                            numSyllables,\
                                                            avgWordLengthSyl,\
                                                            avgWordLengthInChars,\
                                                            avgSenLengthInChars, \
                                                            avgWordsPerSentece,\
                                                            avgSyllablesPerSentence,\
                                                            fleishReadingEase,\
                                                            fleschKincaidGradeLevel,\
                                                            colemanLiauIndex,\
                                                            lixIndex,\
                                                            goal))

    return myTextObj        

