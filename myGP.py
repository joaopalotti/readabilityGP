#!/usr/bin/env python
# encoding: utf-8

import sys
import random
import operator
from deap import algorithms, base, creator, tools, gp

inputData = []
labels = []

def numSentences():
    return 4

def safeDiv(left, right):
    try:
        return left / right
    except ZeroDivisionError:
        return 0.0

def getInputFile(filename):
    with open(filename,"r") as f:
        lines = f.readlines()
     
    labels = [ l.strip() for l in lines[0].split(",") ]
        
    for line in lines[1:]:
        valuesTmp = [ value.strip() for value in line.split(",")]
        values = [ float(v) for v in valuesTmp[1:]  ]
        values = [ valuesTmp[0] ] + values
        inputData.append(dict(zip(labels, values))) 
            

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
    toolbox.register("expr", gp.genRamped, pset=pset, min_=0, max_=2)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("lambdify", gp.lambdify, pset=pset)
    

    def evaluate(individual):
        func = toolbox.lambdify(expr=individual)
        
        error = 0

        for test in inputData:
            
            goal = test["fleschReadingEase"]

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
        
        fitness = error

        return fitness,

    toolbox.register("evaluate", evaluate)
    toolbox.register("select", tools.selTournament, tournsize=2)
    toolbox.register("mate", gp.cxOnePoint)
    toolbox.register("expr_mut", gp.genGrow, min_=0, max_=1)
    toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut)

    #here starts the algorithm
    random.seed(10)
    pop = toolbox.population(n=400)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", tools.mean)
    stats.register("std", tools.std)
    stats.register("min", min)
    stats.register("max", max)

    algorithms.eaSimple(pop, toolbox, 0.8, 0.1, 20, stats, halloffame=hof)

    #print pop, stats, hof
    print stats, hof

    
if __name__ == "__main__":
    sys.exit(main())

