#!/usr/bin/env python
# encoding: utf-8

from __future__ import division
import sys
import random
import operator
from deap import algorithms, base, creator, tools, gp
import math

#from deap import cTools


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
    
    training = []
    test = []

    with open(filename + ".training","r") as f:
        trainingLines = f.readlines()
     
    with open(filename + ".test","r") as f:
        testLines = f.readlines()
    
    labels = [ l.strip() for l in trainingLines[0].split(",,,") ]
        
    for line in trainingLines[1:]:
        valuesTmp = [ value.strip() for value in line.split(",,,")]
        values = [ float(v) for v in valuesTmp[1:]  ]
        values = [ valuesTmp[0] ] + values
        training.append(dict(zip(labels, values))) 
         
    for line in testLines[1:]:
        valuesTmp = [ value.strip() for value in line.split(",,,")]
        values = [ float(v) for v in valuesTmp[1:]  ]
        values = [ valuesTmp[0] ] + values
        test.append(dict(zip(labels, values))) 
    
    return labels, training, test

def main(argv=None):
    
    training = []
    test = []
    labels = []
    
    cxpb = 0.8
    mutpb = 0.1 
    ngen = 5
    npop = 10
    tournSize = 5 #int(npop / 100)
    heightMaxCreation = 5
    heightMaxNew = 1
    heightLimit = 30

    labels, training, test = getInputFile(argv[1])
    
    seedValue = 29
    if len(argv) > 2:
        seedValue = argv[2] 

    ## Create the fitness and individual classes
    # The second argument is the number of arguments used in the function
    pset = gp.PrimitiveSet("MAIN", 10 ) #+ 8)
    '''
        Arg-1 => fileName
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
    pset.addEphemeralConstant(lambda: random.random() * 10)
#    pset.addTerminal(1)
#    pset.addTerminal(0)

    creator.create("Fitness", base.Fitness, weights=(1.0,))
    creator.create("Individual", gp.PrimitiveTree, fitness=creator.Fitness, pset=pset)

    toolbox = base.Toolbox()
    toolbox.register("expr", gp.genRamped, pset=pset, min_=0, max_=heightMaxCreation)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("lambdify", gp.lambdify, pset=pset)
     
    def evaluate(individual):
        func = toolbox.lambdify(expr=individual)
        correct = 0.0
        possible = 0
       
        for i in range(len(training)):
            t = training[i]
            for j in range(i + 1, len(training)):
                other = training[j]
                
                if abs(t["goal"] - other["goal"]) < 0.5:
                    continue
                
                possible += 1
                funcResult = func(t["numWords"],\
                        t["numSentences"],\
                        t["numSyllables"],\
                        t["numberOfPolysyllableWord"],\
                        t["numberOfChars"],\
                        t["avgWordLengthSyl"],\
                        t["avgWordLengthInChars"],\
                        t["avgSenLengthInChars"],\
                        t["avgWordsPerSentece"],\
                        t["avgSyllablesPerSentence"],\
                        # Optionals
                        #t["fleschReadingEase"],\
                        #t["fleschKincaidGradeLevel"],\
                        #t["colemanLiauIndex"],\
                        #t["lixIndex"],\
                        #t["gunningFogIndex"],\
                        #t["SMOG"],\
                        #t["ARI"],\
                        #t["newDaleChall"],\
                    )
                otherResult = func(other["numWords"],\
                        other["numSentences"],\
                        other["numSyllables"],\
                        other["numberOfPolysyllableWord"],\
                        other["numberOfChars"],\
                        other["avgWordLengthSyl"],\
                        other["avgWordLengthInChars"],\
                        other["avgSenLengthInChars"],\
                        other["avgWordsPerSentece"],\
                        other["avgSyllablesPerSentence"],\
                        # Optionals
                        #other["fleschReadingEase"],\
                        #other["fleschKincaidGradeLevel"],\
                        #other["colemanLiauIndex"],\
                        #other["lixIndex"],\
                        #other["gunningFogIndex"],\
                        #other["SMOG"],\
                        #other["ARI"],\
                        #other["newDaleChall"],\
                    )
                if funcResult >= otherResult and t["goal"] >= other["goal"]:
                    correct += 1
                 
                elif funcResult < otherResult and t["goal"] < other["goal"]:
                    correct += 1
            
        #fitness = math.sqrt(error2) / len(training)
        fitness = correct / possible
        return fitness,
    
    def evaluateTest(individual):
        func = toolbox.lambdify(expr=individual)
        correct = 0.0
        possible = 0
       
        for i in range(len(test)):
            t = test[i]
            for j in range(i + 1, len(test)):
                other = test[j]
                
                if abs(t["goal"] - other["goal"]) < 0.5:
                    continue
                
                possible += 1
                funcResult = func(t["numWords"],\
                        t["numSentences"],\
                        t["numSyllables"],\
                        t["numberOfPolysyllableWord"],\
                        t["numberOfChars"],\
                        t["avgWordLengthSyl"],\
                        t["avgWordLengthInChars"],\
                        t["avgSenLengthInChars"],\
                        t["avgWordsPerSentece"],\
                        t["avgSyllablesPerSentence"],\
                        # Optionals
                        #t["fleschReadingEase"],\
                        #t["fleschKincaidGradeLevel"],\
                        #t["colemanLiauIndex"],\
                        #t["lixIndex"],\
                        #t["gunningFogIndex"],\
                        #t["SMOG"],\
                        #t["ARI"],\
                        #t["newDaleChall"],\
                    )
                otherResult = func(other["numWords"],\
                        other["numSentences"],\
                        other["numSyllables"],\
                        other["numberOfPolysyllableWord"],\
                        other["numberOfChars"],\
                        other["avgWordLengthSyl"],\
                        other["avgWordLengthInChars"],\
                        other["avgSenLengthInChars"],\
                        other["avgWordsPerSentece"],\
                        other["avgSyllablesPerSentence"],\
                        # Optionals
                        #other["fleschReadingEase"],\
                        #other["fleschKincaidGradeLevel"],\
                        #other["colemanLiauIndex"],\
                        #other["lixIndex"],\
                        #other["gunningFogIndex"],\
                        #other["SMOG"],\
                        #other["ARI"],\
                        #other["newDaleChall"],\
                    )

                if funcResult >= otherResult and t["goal"] >= other["goal"]:
                    correct += 1
                 
                elif funcResult < otherResult and t["goal"] < other["goal"]:
                    correct += 1
            
        #fitness = math.sqrt(error2) / len(training)
        fitness = correct / possible
        
        print "Final test..."
        print "Tested: ", len(test), " correct: ", correct, "possible ", possible, " final ===", correct/possible
        return fitness,

    toolbox.register("evaluate", evaluate)
    toolbox.register("evaluateTest", evaluateTest)
    toolbox.register("select", tools.selTournament, tournsize=tournSize)
    #toolbox.register("select", tools.selNSGA2)

    #Crossover
    #toolbox.register("mate", gp.cxOnePoint)
    toolbox.register("mate", staticLimitCrossover, heightLimit=heightLimit, toolbox=toolbox)
    #Mutation
    toolbox.register("expr_mut", gp.genGrow, min_=0, max_=heightMaxNew)
    toolbox.register("mutate", staticLimitMutation, expr=toolbox.expr_mut, heightLimit=heightLimit, toolbox=toolbox)

    #toolbox.register("expr_mut", gp.genGrow, min_=0, max_=heightMaxNew)
    #toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut)
    #Mutation options:
    #toolbox.register("mutate", gp.mutEphemeral, mode="one")              # 0.543709266384
    #toolbox.register("mutate", gp.mutEphemeral, mode="all")             #
    #toolbox.register("mutate", gp.mutNodeReplacement)  # OK
    #toolbox.register("mutate", gp.mutInsert)  #--> terrible                          # 0.543709266384
   
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


    #print pop, stats, hof
    print stats, hof
    print "Fitness in training = ", map(toolbox.evaluate, hof)
    fitnessInTest  = map(toolbox.evaluateTest, hof)
    print "Fitness in test = ", fitnessInTest

    return fitnessInTest[0][0]
    
if __name__ == "__main__":
    sys.exit(main(sys.argv))

