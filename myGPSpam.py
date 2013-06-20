#!/usr/bin/env python
# encoding: utf-8

from __future__ import division
import sys, random, operator, math, csv, itertools
from deap import algorithms, base, creator, tools, gp
from optparse import OptionParser

from sklearn.cross_validation import train_test_split
from sklearn import metrics

usingScoop = True
#usingScoop = False

usingBasic = True
#usingBasic = False

'''
The goal of this version is to separate the Simple English from the English Wikipedia as much as possible.
'''

def myF1(pred, labels):
    N = len(pred)
    TP, FP, FN, TN = 0, 0, 0, 0
    for a, b in zip(pred, labels):
        if a == b:
            TP += 1
    
    precision = TP / (TP + FP)
    recall = TP / (TP + FN)
    acc = (TP + TN) / N
    return 2.0 * precision * recall / (precision + recall)


def kernelCalc(func, t):          
    
    if usingBasic:
        return func(t[0],t[1],t[2],t[3],t[4],t[5],t[6],t[7])
    else:
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
        #print "Left = ", left, "---"
        #print "Right = ", right, "---"
        return left / right
    except ZeroDivisionError, RuntimeWarning:
        return 0.0

def getInputFile(fileName):
    
    file = open(fileName,"rb")
    reader = csv.reader(file, delimiter=',', quotechar ='"', escapechar='\\', doublequote=False)
    
    featureList = [ [ float(element.strip()) for element in line ] for line in reader ]
    
    print "len list = ", len(featureList)
    return featureList

## Create the fitness and individual classes
# The second argument is the number of arguments used in the function

if usingBasic:
    pset = gp.PrimitiveSetTyped("MAIN", itertools.repeat("float", 8), "bool")
else:
    pset = gp.PrimitiveSetTyped("MAIN", itertools.repeat("float", 16), "bool")

#pset = gp.PrimitiveSet("MAIN", 16)

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

pset.addPrimitive(operator.and_, ["bool", "bool"], "bool")
pset.addPrimitive(operator.or_, ["bool", "bool"], "bool")
pset.addPrimitive(operator.not_, ["bool"], "bool")
pset.addPrimitive(operator.add, ["float","float"], "float")
pset.addPrimitive(operator.sub, ["float","float"], "float")
pset.addPrimitive(operator.mul, ["float","float"], "float")
#pset.addPrimitive(safeDiv, ["float","float"], "float")
def if_then_else(input, output1, output2):
    if input: 
        return output1
    else: 
        return output2
pset.addPrimitive(operator.lt, ["float", "float"], "bool")
pset.addPrimitive(operator.eq, ["float", "float"], "bool")
pset.addPrimitive(if_then_else, ["bool", "float", "float"], "float")

#pset.addPrimitive(safeDiv, 2)
#pset.addPrimitive(operator.add, 2)
#pset.addPrimitive(operator.mul, 2)
#pset.addPrimitive(operator.sub, 2)

def myEphemeral():
    return random.random()

pset.addEphemeralConstant(myEphemeral, "float")
pset.addTerminal(0, "bool")
pset.addTerminal(1, "bool")

#pset.addEphemeralConstant(myEphemeral)
#pset.addTerminal(1)
#pset.addTerminal(0)

creator.create("Fitness", base.Fitness, weights=(1.0,-1.0))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.Fitness, pset=pset)

toolbox = base.Toolbox()
toolbox.register("lambdify", gp.lambdify, pset=pset)

if usingScoop:
    from scoop import futures
    toolbox.register("map", futures.map)

def evaluate(individual, metric_):
    func = toolbox.lambdify(expr=individual)

    result = [ kernelCalc(func,t) for t in instancesTraining ]
    correct = sum( not (a ^ b) for (a, b) in zip(result, labelsTraining) )
    total = len(instancesTraining)

    if metric_ == "f1":
        fitness = metrics.f1_score(labelsTraining, result)

    elif metric_ == "acc":
        fitness = correct / total

    return fitness, len(individual)

def finalTest(individual):
    func = toolbox.lambdify(expr=individual)
    correct = 0.0

    result = [ kernelCalc(func,t) for t in instancesTest ]
    #print result[2], labelsTraining[2], result[2] == labelsTraining[2]
    correct = sum( not (a ^ b) for (a, b) in zip(result, labelsTest) )
    total = len(instancesTest)

    fitness = (correct) / total # + alpha * (pow( len(individual), 2))

    print "Accuracy = ", correct / total
    print "Accuracy (scikit) = ", metrics.accuracy_score(labelsTest, result)
    print "F1-score (micro)    = ", metrics.f1_score(labelsTest, result, average='micro')
    print "F1-score (macro)    = ", metrics.f1_score(labelsTest, result, average='macro')
    print "F1-score (weighted) = ", metrics.f1_score(labelsTest, result, average='weighted')
    print metrics.classification_report(labelsTest, result)

    return fitness, len(individual)

def main(ngen, npop, mutpb, cxpb, seedValue, tournSize, heightMaxCreation, heightMexNew, heightLimit, metric):

    toolbox.register("expr", gp.genRamped, pset=pset, type_=pset.ret, min_=1, max_=2)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("evaluate", evaluate, metric_=metric)
    toolbox.register("finalTest", finalTest)
    toolbox.register("select", tools.selTournament, tournsize=tournSize)
    toolbox.register("mate", staticLimitCrossover, heightLimit=heightLimit, toolbox=toolbox)
    toolbox.register("expr_mut", gp.genGrow, min_=0, max_=heightMaxNew)
    toolbox.register("mutate", staticLimitMutation, expr=toolbox.expr_mut, heightLimit=heightLimit, toolbox=toolbox)
    #toolbox.register("expr", gp.genRamped, pset=pset, min_=0, max_=heightMaxNew)
    #toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
    #toolbox.register("population", tools.initRepeat, list, toolbox.individual)
 
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
    fitnessInTest  = map(toolbox.finalTest, hof)
    print "Fitness in test = %.4f" % ( fitnessInTest[0][0] * 100.0 )
    #return fitnessInTest[0][0]
    
if usingBasic:
    simpleFeatures = getInputFile("../readability/simpleMediaWiki.basic.csv")
    enFeatures = getInputFile("../readability/enMediaWiki.basic.csv")
else:
    simpleFeatures = getInputFile("../readability/simpleMediaWiki.csv")
    enFeatures = getInputFile("../readability/enMediaWiki.csv")

labels = len(simpleFeatures) * [0] + len(enFeatures) * [1] 
features = simpleFeatures + enFeatures
#print labels
#print features
instancesTraining, instancesTest, labelsTraining, labelsTest = train_test_split(features, labels, test_size=0.33, random_state=42)
#print labelsTraining
#print "Labels Test --> ", labelsTest , len(labelsTest), sum(labelsTest)

if __name__ == "__main__":

    op = OptionParser(version="%prog 0.001")
    #op.add_option("--simple", "-s", action="store", type="string", dest="simpleFileName", help="File Name for the Simple English Wikipedia Dataset.", metavar="FILE")
    #op.add_option("--en", "-e", action="store", type="string", dest="enFileName", help="File Name for the English Wikipedia Dataset.", metavar="FILE")
    op.add_option("--gen", "-g", action="store", type="int", dest="ngen", help="Number of generations.", metavar="GEN", default=50)
    op.add_option("--pop", "-p", action="store", type="int", dest="npop", help="Number of individuals.", metavar="POP", default=100)
    op.add_option("--mutb", "-m", action="store", type="float", dest="mutpb", help="Probability of multation.", metavar="PROB", default=0.10)
    op.add_option("--cxpb", "-c", action="store", type="float", dest="cxpb", help="Probability of crossover.", metavar="PROB", default=0.90)
    op.add_option("--seed", "-s", action="store", type="int", dest="seed", help="Random Seed.", metavar="SEED", default=29)
    op.add_option("--tsize", "-t", action="store", type="int", dest="tsize", help="Tournament Size.", metavar="TSIZE", default=2)
    
    op.add_option("--hmc", action="store", type="int", dest="hcreation", help="Height for creation.", metavar="HEIGHT", default=5)
    op.add_option("--hnew", "-n", action="store", type="int", dest="hnew", help="Height max for creation.", metavar="HEIGHT", default=1)
    op.add_option("--hlim", "-l", action="store", type="int", dest="hlim", help="Height limit.", metavar="HEIGHT", default=30)
    
    op.add_option("--fitnessMetric", "-f", action="store", type="string", dest="fitnessMetric", help="Fitness Metric [f1, acc].", metavar="METRIC", default="acc")
    (opts, args) = op.parse_args()
    
    heightMaxCreation = 5
    heightMaxNew = 1
    heightLimit = 30
    
    if len(args) > 0:
        op.error("this script takes no arguments.")
        sys.exit(1)

    main(opts.ngen, opts.npop, opts.mutpb, opts.cxpb, opts.seed, opts.tsize, opts.hcreation, opts.hnew, opts.hlim, opts.fitnessMetric)

