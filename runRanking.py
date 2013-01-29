from __future__ import division
from ranking import *

'''
    HOW TO USE:
        python runRanking.py input2 5 -4
        python runRanking.py fileFamily CV colNumber
'''


baseFileName = sys.argv[1]
CV = int(sys.argv[2])
col = int(sys.argv[3])
fitness = 0

for i in range(0, CV):
    print "base =", baseFileName + str(i)
    fitness += calculateRanking ([baseFileName + str(i) + ".test" , col] )
    print "fitness %d = %f" % (i, fitness)

print "Mean Fitness = ", fitness/CV



