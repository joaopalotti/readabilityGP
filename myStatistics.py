#!/usr/bin/env python
# encoding: utf-8

from __future__ import division
import sys

def main(argv):

    inFile="test"
    if len(argv) > 1:
        inFile = argv[1]

    with open(inFile, "r") as f:
        data = f.readlines()

    means = calculateMeans(data)
    divideByVector(data, means, 1, 4)


def divideByVector(data, vectorValues, *cols):
    
    newData = []
    
    firstCol, lastCol = defineFirstAndlastCol(vectorValues, *cols)

    for row in data[1:]:
        
        name = row.split(",,,")[0:1]
        numbers = ( [ float(n) for n in row.split(",,,")[1:] ] )
        
        before = [ numbers[i] for i in range(0, firstCol) ]
        v = [ numbers[i]/vectorValues[i] for i in range(firstCol, lastCol) ]
        after = [ numbers[i] for i in range(lastCol, len(numbers)) ]
        
        newData.append( name + before + v + after)
    
    for row in newData:
        sys.stdout.write("%s" % row[0:1][0])
        for v in row[1:]:
            sys.stdout.write(",,,%f" % v)
        sys.stdout.write("\n")


def calculateMeans(data):

    numbers = []
    for row in data[1:]:
        numbers.append( [ float(n) for n in row.split(",,,")[1:] ] )
        
    finalMean = [ sum(a)/len(numbers) for a in zip(*numbers) ]

    print finalMean[0], finalMean[1], finalMean[2], finalMean[3]
    return finalMean

def calculateMinAndMax(data, *cols):

    mins = []
    maxs = []
    
    firstCol, lastCol = defineFirstAndlastCol(data, *cols)
    for col in range(firstCol, lastCol):
        values = getOneColumn(data, col)
        mins.append( min(values) )
        maxs.append( max(values) )

    return [ mins, maxs ]

def defineFirstAndlastCol(data, *cols):
    firstCol = 0
    lastCol = len(data)
    
    if len(cols) == 1:
        firstCol = cols[0]

    if len(cols) > 1:
        firstCol = cols[0]
        lastCol = cols[1]
    return firstCol, lastCol

def minMaxNormalization(data, *cols):
    
    mins, maxs = calculateMinAndMax(data, *cols)
    firstCol, lastCol = defineFirstAndlastCol(data, *cols)
    
    newData = []
    print firstCol, lastCol
    print mins, maxs

    for row in data[1:]:
             
        name = row.split(",,,")[0:1]
        numbers = ( [ float(n) for n in row.split(",,,")[1:] ] )
        
        before = [ numbers[i] for i in range(0, firstCol - 1) ]
        v = [ ( numbers[i] - mins[i] )/ (maxs[i] - mins[i]) for i in range(firstCol - 1, lastCol - 1) ]
        after = [ numbers[i] for i in range(lastCol - 1, len(numbers)) ]
        
        newData.append( name + before + v + after)
    
    titles = data[0:1][0].split(",,,")
    sys.stdout.write("%s" % titles[0])
    for t in titles[1:]:
        sys.stdout.write(",,,%s" % t)
    for row in newData:
        sys.stdout.write("%s" % row[0:1][0])
        for v in row[1:]:
            sys.stdout.write(",,,%.2f" % v)
        sys.stdout.write("\n")

   

def getColumnName(data, col):
    return data[0].split(",,,")[col:col+1][0]

def getOneColumn(data, col):
    #print "Getting Column ", col
    values = []
    for row in data[1:]:
        values.append( float(row.split(",,,")[col:col+1][0]) )
    return values

if __name__ == "__main__":
    main(sys.argv)
