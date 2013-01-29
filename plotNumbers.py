from pylab import *
from myStatistics import *
from collections import Counter
import math
import sys

## The idea of this program is to get two different files and compare its values

#inFile1 = "all.en.gpout"
#inFile2 = "all.simple.gpout"
inFile1 = "all.en"
inFile2 = "all.simple"

columnToAnalyse = int(sys.argv[1])

with open(inFile1, "r") as f:
    data1 = f.readlines()

with open(inFile2, "r") as f:
    data2 = f.readlines()

#print "DATA 1 = ", data1
columnName = getColumnName(data1, columnToAnalyse)

data1 = getOneColumn(data1, columnToAnalyse)
data2 = getOneColumn(data2, columnToAnalyse)

dataInt1 = [ floor(v) for v in data1 ] 
dataInt2 = [ floor(v) for v in data2 ] 

c1 = Counter(dataInt1)
c2 = Counter(dataInt2)

c1[0] = 0
c2[0] = 0

ylabel("Frequency")
xlabel(columnName)

plot(c1.keys(), c1.values(), "o", label='En')
plot(c2.keys(), c2.values(), "o", label='Simple')
legend()

show()

savefig("bla.png")
