
from __future__ import division
from myGPRanking import *

## TODO:
# run X times and get the mean fitness of this X times -- > use the last parameter to send a different seed to my GP

baseFileName = sys.argv[1]
CV = int(sys.argv[2])
fitness = 0

for i in range(0, CV):
    print "base =", baseFileName + str(i)
    fitness += main( [0, baseFileName + str(i) ] )
    print "fitness %d = %f" % (i, fitness)

print "Mean Fitness = ", fitness/CV


