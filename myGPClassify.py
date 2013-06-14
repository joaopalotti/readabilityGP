#!/usr/bin/env python
# encoding: utf-8

from __future__ import division
import sys, random, operator, math, csv
from deap import algorithms, base, creator, tools, gp
from optparse import OptionParser

usingScoop = True

'''
The goal of this version is to separate the Simple English from the English Wikipedia as much as possible.
'''

def kernelCalc(func, t):          
    
    return func(t[0],t[1],t[2],t[3],t[4],t[5],t[6],t[7],t[8],t[9],t[10],t[11],t[12],t[13],t[14],t[15])
    #return func(\
    #          t["numWords"],\
    #          t["numSentences"],\
    #          t["numSyllables"],\
    #          t["numberOfPolysyllableWord"],\
    #          t["numberOfChars"],\
    #          t["avgWordLengthSyl"],\
    #          t["avgWordLengthInChars"],\
    #          t["avgSenLengthInChars"],\
    #          t["avgWordsPerSentece"],\
    #          t["avgSyllablesPerSentence"],\
    #          # Optionals
    #          t["fleschReadingEase"],\
    #          t["fleschKincaidGradeLevel"],\
    #          t["colemanLiauIndex"],\
    #          t["lixIndex"],\
    #          t["gunningFogIndex"],\
    #          t["SMOG"],\
    #          t["ARI"],\
    #          t["newDaleChall"],\
    #      )

def staticLimitCrossover(ind1, ind2, heightLimit, toolbox): 
    # Store a backup of the original individuals 
    keepInd1, keepInd2 = toolbox.clone(ind1), toolbox.clone(ind2) 

    # Mate the two individuals 
    # The crossover is done in place (see the documentation) 
    gp.cxOnePoint(ind1, ind2)

    # If a child is higher than the maximum allowed, then 
    # it is replaced by one of its parent 
    if ind1.height > heightLimit: 
        ind1[:] = keepInd1 
    if ind2.height > heightLimit: 
        ind2[:] = keepInd2

    return ind1, ind2

def staticLimitMutation(individual, expr, heightLimit, toolbox): 
    # Store a backup of the original individual 
    keepInd = toolbox.clone(individual) 

    # Mutate the individual 
    # The mutation is done in place (see the documentation) 
    gp.mutUniform(individual, expr) 

    # If the mutation sets the individual higher than the maximum allowed, 
    # replaced it by the original individual 
    if individual.height > heightLimit: 
        individual[:] = keepInd  

    return individual,

def safeDiv(left, right):
    try:
        return left / right
    except ZeroDivisionError:
        return 0.0


def getInputFile(fileName):
    
    file = open(fileName,"rb")
    reader = csv.reader(file, delimiter=',', quotechar ='"', escapechar='\\', doublequote=False)
    
    featureList = [ [ float(element.strip()) for element in line ] for line in reader ]
    
    print "len list = ", len(featureList)
    return featureList

## Create the fitness and individual classes
# The second argument is the number of arguments used in the function
pset = gp.PrimitiveSet("MAIN", 16)
'''
    Arg-1 => filename
    Arg0  => numWords
    Arg1  => numSentences
    Arg2  => numSyllables
    Arg3  => numberOfPolysyllableWord
    Arg4  => numberOfChars
    Arg5  => avgWordLengthSyl
    Arg6  => avgWordLengthInChars
    Arg7  => avgSenLengthInChars
    Arg8  => avgWordsPerSentece
    Arg9  => avgSyllablesPerSentence
   
    Optionals
    Arg10  => fleschReadingEase
    Arg11  => fleschKincaidGradeLevel
    Arg12  => colemanLiauIndex
    Arg13  => lixIndex
    Arg14  => gunningFogIndex
    Arg15  => SMOG
    Arg16  => ARI
    Arg17  => newDaleChall
'''
pset.addPrimitive(safeDiv, 2)
pset.addPrimitive(operator.add, 2)
pset.addPrimitive(operator.mul, 2)
pset.addPrimitive(operator.sub, 2)

def myEphemeral():
    return random.random()

pset.addEphemeralConstant(myEphemeral)
#    pset.addTerminal(1)
#    pset.addTerminal(0)


tournSize = 2 #int(npop / 100)
heightMaxCreation = 5
heightMaxNew = 1
heightLimit = 30

creator.create("Fitness", base.Fitness, weights=(-1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.Fitness, pset=pset)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genRamped, pset=pset, min_=0, max_=heightMaxNew)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("lambdify", gp.lambdify, pset=pset)

if usingScoop:
    from scoop import futures
    toolbox.register("map", futures.map)

def evaluate(individual):
    func = toolbox.lambdify(expr=individual)
    funcResult = 0
    alpha = 0.001
    regularization = 0.0
    correct, total = 0.0, 0

    for t in simpleFeatures:
        funcResult = kernelCalc(func, t)
        if funcResult < 0:
            correct += 1
        total += 1

    for t in enFeatures:
        funcResult = kernelCalc(func, t) - 1
        if funcResult > 0:
            correct += 1
        total += 1
  
    fitness = (total - correct) / total
    return fitness,


toolbox.register("evaluate", evaluate)
#toolbox.register("evaluateTest", evaluateTest)
toolbox.register("select", tools.selTournament, tournsize=tournSize)
#toolbox.register("select", cTools.selNSGA2)

#Crossover
#toolbox.register("mate", gp.cxOnePoint)
toolbox.register("mate", staticLimitCrossover, heightLimit=heightLimit, toolbox=toolbox)
#Mutation
toolbox.register("expr_mut", gp.genGrow, min_=0, max_=heightMaxNew)
toolbox.register("mutate", staticLimitMutation, expr=toolbox.expr_mut, heightLimit=heightLimit, toolbox=toolbox)


def main(ngen, npop, mutpb, cxpb, seedValue):

    #here starts the algorithm
    random.seed(seedValue)
    pop = toolbox.population(n=npop)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", tools.mean)
    stats.register("std", tools.std)
    stats.register("min", min)
    stats.register("max", max)

    algorithms.eaSimple(pop, toolbox, cxpb, mutpb, ngen, stats, halloffame=hof)
    #algorithms.eaMuPlusLambda(pop, toolbox, npop, npop + 50, cxpb, mutpb, ngen, stats, halloffame=hof)

    #print pop, stats, hof
    print stats, hof
    print "Fitness in training = ", map(toolbox.evaluate, hof)
    #fitnessInTest  = map(toolbox.evaluate, hof)
    #print "Fitness in test = %.4f" % ( fitnessInTest[0][0] * 100.0 )
    #return fitnessInTest[0][0]
    
simpleFeatures = getInputFile("../readability/simpleMediaWiki.csv")
enFeatures = getInputFile("../readability/enMediaWiki.csv")
if __name__ == "__main__":

    op = OptionParser(version="%prog 0.001")
    #op.add_option("--simple", "-s", action="store", type="string", dest="simpleFileName", help="File Name for the Simple English Wikipedia Dataset.", metavar="FILE")
    #op.add_option("--en", "-e", action="store", type="string", dest="enFileName", help="File Name for the English Wikipedia Dataset.", metavar="FILE")
    op.add_option("--gen", "-g", action="store", type="int", dest="ngen", help="Number of generations.", metavar="GEN", default=50)
    op.add_option("--pop", "-p", action="store", type="int", dest="npop", help="Number of individuals.", metavar="POP", default=100)
    op.add_option("--mutb", "-m", action="store", type="float", dest="mutpb", help="Probability of multation.", metavar="PROB", default=0.10)
    op.add_option("--cxpb", "-c", action="store", type="float", dest="cxpb", help="Probability of crossover.", metavar="PROB", default=0.90)
    op.add_option("--seed", "-s", action="store", type="int", dest="seed", help="Random Seed.", metavar="SEED", default=29)
    (opts, args) = op.parse_args()
    
    if len(args) > 0:
        op.error("this script takes no arguments.")
        sys.exit(1)

    main(opts.ngen, opts.npop, opts.mutpb, opts.cxpb, opts.seed)

