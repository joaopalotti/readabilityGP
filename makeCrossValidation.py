from __future__ import division
import sys
import math
import random


'''
    HOW TO USE:
        python makeCrossValidation.py input 10
'''

inFile = sys.argv[1]
lines = (open(inFile, "r")).readlines()

newInputFormat = []
allData = []

nCV = int(sys.argv[2])

titles = lines[0]

shuffledLines = lines[1:]
#shuffle the data
#random.shuffle(shuffledLines)

eachCV = int(len(shuffledLines)/nCV)

trainingFiles = []
testFiles = []
for i in range(nCV):
    trainingFile = open(inFile + str(i) + ".training", "w")
    testFile = open(inFile + str(i) + ".test", "w")

    trainingFiles.append(trainingFile)
    testFiles.append(testFile)
    
    testFile.write("%s" % titles) 
    trainingFile.write("%s" % titles) 

for i in range(len(shuffledLines)):
   
    if (i % eachCV) == 0:

        #We avoid the last elements, putting them in the last file
        if int(i / eachCV) < nCV:
            print "Writing file " + str( int(i/ eachCV) )
            testFile = testFiles[ int(i / eachCV )]
    
    line = shuffledLines[i]
#    print line
    testFile.write("%s" % line) 

    for j in range(len(trainingFiles)):
        
        if int(i/eachCV) == j:
            continue

        #adjust the last training file
        if int(i / eachCV) >= nCV and j == len(trainingFiles) - 1:
            continue

        trainingFile = trainingFiles[j]
        trainingFile.write("%s" % line) 

