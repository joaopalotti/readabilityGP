from pylab import *
from myStatistics import *
from collections import Counter
import math


## The idea of this program is to get two different files and compare its values

inFile1 = "all.en"
inFile2 = "all.simple"

with open(inFile1, "r") as f:
    data1 = f.readlines()

with open(inFile2, "r") as f:
    data2 = f.readlines()


fleish1 = getOneColumn(data1, 1)
fleish2 = getOneColumn(data2, 1)

fleishInt1 = [ floor(v) for v in fleish1 ] 
fleishInt2 = [ floor(v) for v in fleish2 ] 

c1 = Counter(fleishInt1)
c2 = Counter(fleishInt2)

c1[0] = 0
c2[0] = 0

plot ( c1.keys(), c1.values() )
plot ( c2.keys(), c2.values() )

show()


