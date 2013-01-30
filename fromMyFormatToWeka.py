
import sys
import math


def convertToWeka(inFile, fo=None):

    if fo is None:
        fo = sys.stdout
    
    lines = (open(inFile, "r")).readlines()

    allData = []
    labels = []
    labels = [ l.strip() for l in lines[0].split(",,,") ]

    for line in lines[1:]:
        fields = line.split(",,,")
        newInputFormat = []
        
        for f in range(len(fields) - 1):
            newInputFormat.append(float(fields[f+1]))

        allData.append(newInputFormat)
    
    fo.write("@RELATION %s\n" % inFile)
    for att in labels[1:-1]:
        fo.write("@ATTRIBUTE %s NUMERIC\n" % att)
    
    #Maybe you want to edit this line!
    fo.write("@ATTRIBUTE goal {1,0}\n")
    fo.write("@DATA\n")
    
    for line in allData:
        fo.write("%f" % line[0])
        for f in line[1:-1]:
            fo.write(",%f" % f)
        
        #And also this one
        fo.write(",%d" % line[-1])
        fo.write("\n")
    

if __name__ == "__main__":
    convertToWeka(sys.argv[1])
