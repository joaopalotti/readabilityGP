
from __future__ import division
import sys
import math
from scipy.stats.stats import pearsonr
from itertools import imap

def pearsonr2(x, y):
    # Assume len(x) == len(y)
    n = len(x)
    sum_x = float(sum(x))
    sum_y = float(sum(y))
    sum_x_sq = sum(map(lambda x: pow(x, 2), x))
    sum_y_sq = sum(map(lambda x: pow(x, 2), y))
    psum = sum(imap(lambda x, y: x * y, x, y))
    num = psum - (sum_x * sum_y/n)
    den = pow((sum_x_sq - pow(sum_x, 2) / n) * (sum_y_sq - pow(sum_y, 2) / n), 0.5)
    if den == 0: return 0
    return num / den

def calculateRanking(argv=None):

    inFile = argv[0]
    columnNumber = int(argv[1])
    lines = (open(inFile, "r")).readlines()

    columnData = []
    goals = []

    print "Getting data from column: ", lines[0].split(",,,")[columnNumber:columnNumber+1]
    for line in lines[1:]:
        fields = line.split(",,,")
        goal = float( fields[-1] )
        columnD = float(fields[columnNumber])

        goals.append(goal)
        columnData.append(columnD)


    correct = 0
    example = 0

    for i in range(len(goals)):
        goal = goals[i]
        data = columnData[i]
        for j in range(i+1, len(goals)):
            goalOther = goals[j]
            dataOther = columnData[j]

            if abs(goal - goalOther) < 0.5:
                continue
            
            example += 1
            if goal >= goalOther and data >= dataOther:
                correct += 1

            if goal < goalOther and data < dataOther:
                correct += 1

    print correct/ example
    print len(goals) , len(columnData)
    #goals = sorted(goals)
    #columnData  = sorted(columnData)
    #print "GOALS ", goals
    #print "COLUMNDATA ", columnData
    print  pearsonr(goals, columnData)

    print pearsonr2(goals, columnData)
    return correct/example



