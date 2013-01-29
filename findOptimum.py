from __future__ import division
from myStatistics import *
from collections import Counter
import math
import sys


def checkCorrect(data1, data2, value):
    correct = 0
    for i in range(len(data1)):
        if data1[i] < value:
            correct += 1

    for i in range(len(data2)):
        if data2[i] > value:
            correct += 1
    return correct
 

def getNewRepresentation(data1, data2):

    data1 = sorted(data1)
    data2 = sorted(data2)

    # data1 -> 1
    # data2 -> 2
    newRepresentation = [] 
    if not data1:
        while data2:
            newRepresentation.append(2)
            data2.pop()
        return newRepresentation
    
    if not data2:
        while data1:
            newRepresentation.append(1)
            data1.pop()
        return newRepresentation

    v1 = data1[0]
    v2 = data2[0]

    while len(data1) > 0 or len(data2) > 0:
        if not data1:
            while data2:
                newRepresentation.append(2)
                data2.pop()
            return newRepresentation
        
        if not data2:
            while data1:
                newRepresentation.append(1)
                data1.pop()
            return newRepresentation
       
        if v1 < v2:
            newRepresentation.append(1)
            data1.pop(0)
            if not data1:
                while data2:
                    newRepresentation.append(2)
                    data2.pop()
                return newRepresentation
            v1 = data1[0]

        elif v1 > v2:
            newRepresentation.append(2)
            data2.pop(0)
            if not data2:
                while data1:
                    newRepresentation.append(1)
                    data1.pop()
                return newRepresentation
            v2 = data2[0]
        else:
            newRepresentation.append(3)
            data1.pop(0)
            data2.pop(0)

    return newRepresentation

def linearSearch(data1, data2):
    newRepresentation = getNewRepresentation(data1, data2)
    
    #print newRepresentation
    ones = newRepresentation.count(1)
    twos = newRepresentation.count(2)
    threes = newRepresentation.count(3)
    NOnes = 0
    NTwos = 0
    correct = max(ones + NTwos, NOnes + twos)
    
    #print "ones ", ones, " nones", NOnes, " twos", twos, " NTwos", NTwos

    for n in newRepresentation:
        #print "ones ", ones, " nones", NOnes, " twos", twos, " NTwos", NTwos
        if n == 1:
            ones -= 1
            NOnes += 1
        else:
            twos -= 1
            NTwos += 1

        temp = max(ones + NTwos, NOnes + twos)
        correct = max(temp, correct)

    return (correct - (threes)) / len(newRepresentation)

def bruteForce(data1, data2):
    bigest = -1
    value = -1
    for i in range(len(data1)):
        v = checkCorrect(data1, data2, data1[i])
        if v > bigest:
            value = data1[i]
            bigest = v
    
    for i in range(len(data2)):
        v = checkCorrect(data1, data2, data2[i])
        if v > bigest:
            value = data2[i]
            bigest = v
    
    return value 


def binary_search(data1, data2, lo=None, hi=None):

    if hi is None:
        hi = max(data1 + data2)
    if lo is None:
        lo = min(data1 + data2)

    while lo < hi:
        
        mid = (lo+hi)//2
        midval = checkCorrect(data1, data2, mid)
        
        if midval < x:
            lo = mid+1
        elif midval > x: 
            hi = mid
        else:
            return mid
    return -1

def binarySearch(data1, data2, limitInf, limitSup):
    
    print limitInf, limitSup
    
    correctInf = checkCorrect(data1, data2, limitInf)
    correctSup = checkCorrect(data1, data2, limitSup)
    mean = (limitInf + limitSup) / 2.0

    if correctInf > correctSup:
        return binarySearch(data1, data2, limitInf, mean)
    if correctInf < correctSup:
        return binarySearch(data1, data2, mean, limitSup)
    else:
        meanResult = checkCorrect(data1, data2, mean)
        print "Mean result = ", meanResult , " maxResult = ", correctSup, " minresult = ", correctInf, " meanValue = ", mean
        if meanResult > correctInf:
            return mean
        
        return limitInf 

def main():

    #inFile1 = "all.en.gpout"
    #inFile2 = "all.simple.gpout"
    inFile1 = "all.en"
    inFile2 = "all.simple"

    columnToAnalyse = int(sys.argv[1])

    with open(inFile1, "r") as f:
        data1 = f.readlines()

    with open(inFile2, "r") as f:
        data2 = f.readlines()

    data1 = getOneColumn(data1, columnToAnalyse)
    data2 = getOneColumn(data2, columnToAnalyse)

    data1 = sorted(data1)
    data2 = sorted(data2)

    valueFound = bruteForce(data1, data2)
    
    minData2 = data2[0]
    maxData1 = data1[-1]

#if they have intercection
    if maxData1 > minData2:
        for i in range(len(data1)):
            if data1[i] >= minData2:
                if i > 0:
                    limitInf = data1[i-1]
                    limitInfIndex = i-1
                else :
                    limitInf = data1[0]
                    limitInfIndex = 0
                break
        limitSup = data1[-1]
        limitSupIndex = len(data2)

        for i in range(len(data2)):
            if data2[i] > limitSup:
                limitSupIndex = i
            
        #valueFound = binarySearch(data1[limitInfIndex:], data2[:limitSupIndex], limitInf, limitSup)
        #valueFound = binarySearch(data1, data2, limitInf, limitSup)

    correct = 0
    for i in range(len(data1)):
        if data1[i] < valueFound:
            correct += 1

    for i in range(len(data2)):
        if data2[i] > valueFound:
            correct += 1

    print "Len(data1) = ", len(data1), " len(data2) = ", len(data2), " total len ", len(data1) + len(data2) , " correct = ", correct, " --> ", correct / (len(data1) + len(data2))



if __name__ == "__main__":
    main()

