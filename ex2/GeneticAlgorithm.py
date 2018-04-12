from ProblemDefinition import ProblemDefinition as PD
import numpy as np
from Individual import Individual
class GeneticAlgorithm:
    def __init__(self,initializer,mutator,recombiner,selector, replacer, problemDef, popSize):
        self.mutator = mutator
        self.recombiner = recombiner
        self.selector = selector
        self.replacer = replacer
        PD.setPD(problemDef[0],problemDef[1],problemDef[2])
        self.pop = initializer.initialize(popSize)

    def run(self):
        #some more Parameters:
        #max number of Iterations
        maxIt = 100
        #nr offspring per generation
        nrOff = 10

        done = False
        itCnt = 0
        #main loop
        while not done:
            self.generateOffspring(nrOff)

            itCnt += 1
            #check termination condition
            if itCnt == maxIt:
                done = True
        return self.getBestSol()


    def generateOffspring(self, nrOff):
        newInds = np.empty(nrOff,dtype=Individual)
        for i in range(nrOff):
            ind0 = self.selector.select()
            ind1 = self.selector.select()
            indNew = self.recombiner.recombine(ind0,ind1)
            newInds[i] = self.mutator.mutate(indNew)

        self.pop = self.replacer.replace(newInds,self.pop)

    def getBestSol(self):
        pass