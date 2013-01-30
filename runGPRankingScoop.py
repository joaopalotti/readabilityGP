
from __future__ import division
from myGPRanking import *

'''
HOW TO USE:
    python runGPs.py mathData/CV5/input 10 40
'''
## TODO:
# run X times and get the mean fitness of this X times -- > use the last parameter to send a different seed to my GP

baseFileName = sys.argv[1]
CV = int(sys.argv[2])
maxExps = int(sys.argv[3])
means = []

startExps = 28
if len(sys.argv) > 4:
    startExps = int(sys.argv[4])

for seed in range(startExps, startExps + maxExps):
    
    fitness = 0.0
    for i in range(0, CV):
        print "base =", baseFileName + str(i)
        with open("fileToLoad", "w") as f:
            f.write(baseFileName + str(i))

        fitness += main( [0, 0, seed ] )
        print "fitnessAcc %d = %f" % (i, fitness)

    means.append(fitness/CV)
    print "Mean Fitness = ", fitness/CV


print "Means ---", means
print "Sum - ", sum(means)
print "Size - ", len(means)
print "Final Mean = ", sum(means)/len(means)


