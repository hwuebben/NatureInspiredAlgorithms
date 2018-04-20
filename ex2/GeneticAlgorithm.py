from ProblemDefinition import ProblemDefinition as PD
import numpy as np
from Individual import Individual
class GeneticAlgorithm:
    def __init__(self,moduleSet, problemDef, popSize, nrOffspring):
        PD.setPD(problemDef[0], problemDef[1])

        self.initializer = moduleSet[0]
        self.mutator = moduleSet[1]
        self.recombiner = moduleSet[2]
        self.selector = moduleSet[3]
        self.replacer = moduleSet[4]
        self.terminator = moduleSet[5]

        self.pop = self.initializer.initialize(popSize)
        self.nrIt = 0
        self.popSize = popSize
        self.nrOffspring = nrOffspring

    def run(self):
        #main loop
        while not self.terminator.checkTermination(self):
            newInds = self.generateOffspring(self.nrOffspring)
            self.pop = self.replacer.replace(newInds, self.pop)
            self.nrIt += 1
            #pass the progress to the mutator and selector module to enable simulated annealing
            self.mutator.dynamicAdaptation(self.terminator.estimateProgress())
            self.selector.dynamicAdaptation(self.terminator.estimateProgress())
        #return best solution
        return np.max(self.pop)


    def generateOffspring(self, nrOff):
        newInds = np.empty(nrOff,dtype=Individual)
        for i in range(nrOff):
            ind0 = self.selector.select(self.pop)
            ind1 = self.selector.select(self.pop)
            indNew = self.recombiner.recombine(ind0,ind1)
            newInds[i] = self.mutator.mutate(indNew)
        return newInds

