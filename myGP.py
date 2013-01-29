#!/usr/bin/env python
# encoding: utf-8

from __future__ import division
import sys
import random
import operator
from deap import algorithms, base, creator, tools, gp
from scoop import futures

inputData = []
labels = []

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

def getInputFile(filename):
    with open(filename,"r") as f:
        lines = f.readlines()
     
    labels = [ l.strip() for l in lines[0].split(",,,") ]
        
    for line in lines[1:]:
        valuesTmp = [ value.strip() for value in line.split(",,,")]
        values = [ float(v) for v in valuesTmp[1:]  ]
        values = [ valuesTmp[0] ] + values
        inputData.append(dict(zip(labels, values))) 
            
    return inputData

def main(argv=None):
    
    getInputFile("input")
    
    ## Create the fitness and individual classes
    # The second argument is the number of arguments used in the function
    pset = gp.PrimitiveSet("MAIN", 8)
    '''
        Arg-1 => fileName
        Arg0  => numWords
        Arg1  => numSentences
        Arg2  => numSyllables
        Arg3  => avgWordLengthSyl
        Arg4  => avgWordLengthInChars
        Arg5  => avgSenLengthInChars
        Arg6  => avgWordsPerSentece
        Arg7  => avgSyllablesPerSentence
    '''

    pset.addPrimitive(safeDiv, 2)
    pset.addPrimitive(operator.add, 2)
#    pset.addPrimitive(operator.mul, 2)
    
#    pset.addEphemeralConstant(lambda: random.random() * 100)
#    pset.addTerminal(1)
#    pset.addTerminal(0)
#    pset.addTerminal(numSentences)

    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin, pset=pset)

    toolbox = base.Toolbox()
    toolbox.register("expr", gp.genRamped, pset=pset, min_=0, max_=5)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("lambdify", gp.lambdify, pset=pset)
    
    toolbox.register("map", futures.map)

    def evaluate(individual):
        func = toolbox.lambdify(expr=individual)
        
        error = 0

        for test in inputData:
            
            #goal = test["fleschReadingEase"]
            goal = test["goal"]

            funcResult = func(test["numWords"],\
                           test["numSentences"],\
                           test["numSyllables"],\
                           test["avgWordLengthSyl"],\
                           test["avgWordLengthInChars"],\
                           test["avgSenLengthInChars"],\
                           test["avgWordsPerSentece"],\
                           test["avgSyllablesPerSentence"],\
                           )
            error += abs( goal - funcResult )
        
        fitness = error/len(inputData)

        return fitness,

    toolbox.register("evaluate", evaluate)
    toolbox.register("select", tools.selTournament, tournsize=2)
    
    toolbox.register("mate", gp.cxOnePoint)
    toolbox.register("expr_mut", gp.genGrow, min_=0, max_=10)
    toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut)
    
    #toolbox.register("mate", staticLimitCrossover, heightLimit=20, toolbox=toolbox)
    #Mutation
    #toolbox.register("expr_mut", gp.genGrow, min_=0, max_=5)
    #toolbox.register("mutate", staticLimitMutation, expr=toolbox.expr_mut, heightLimit=20, toolbox=toolbox)


    #here starts the algorithm
    random.seed(10)
    pop = toolbox.population(n=100)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", tools.mean)
    stats.register("std", tools.std)
    stats.register("min", min)
    stats.register("max", max)

    algorithms.eaSimple(pop, toolbox, 0.8, 0.1, 100, stats, halloffame=hof)

    #print pop, stats, hof
    print stats, hof

    
if __name__ == "__main__":
    sys.exit(main())

