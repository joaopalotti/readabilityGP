from __future__ import division
from ranking import *
from myStatistics import *

'''
    HOW TO USE:
        python compareWikipedia.py all colNumber


        Compare two wikipedia articles with the same name
'''

def main(argv):
    baseFileName = argv[1]
    colNumber = int(argv[2])

    with open( baseFileName + ".en") as f:
        enData = f.readlines()

    with open( baseFileName + ".simple") as f:
        simpleData = f.readlines()

    labels = enData[0]

    enData = [labels] + sorted(enData[1:])
    simpleData = [labels] + sorted(simpleData[1:])

    enCol = getOneColumn(enData, colNumber)
    simpleCol = getOneColumn(simpleData, colNumber)
    colName = getColumnName(enData, colNumber)

    print  "%s -> %.4f" % (colName , compare(enCol, simpleCol) * 100)


def compare(enCol, simpleCol):

    ok = 0
    for i in range(len(enCol)):
        if float(enCol[i]) >= float(simpleCol[i]):
            ok += 1

    return ok / len(enCol)


if __name__ == "__main__":
    main(sys.argv)
