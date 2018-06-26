import numpy as np
from Individual import Individual
import LocalSearcher


class GeneticAlgorithm:

    def __init__(self, initializer, selector, recombiner, mutator, replacer, terminator,
                 probDef, popSize, nrOffspring, localSearcher = LocalSearcher.Idle()):
        self.initializer = initializer
        self.selector = selector
        self.recombiner = recombiner
        self.mutator = mutator
        self.replacer = replacer
        self.terminator = terminator
        self.localSearcher = localSearcher

        self.probDef = probDef
        self.pop = self.initializer.initialize(self.probDef, popSize)
        self.nrIt = 0
        self.popSize = popSize
        self.nrOffspring = nrOffspring

    def run(self):
        results = list()
        #main loop
        while not self.terminator.checkTermination(self):
            newInds = self.__generateOffspring(self.nrOffspring)
            self.pop = self.replacer.replace(newInds, self.pop)
            self.nrIt += 1
            # pass the progress to the mutator and selector module to enable simulated annealing
            self.mutator.dynamicAdaptation(self.terminator.estimateProgress())
            self.selector.dynamicAdaptation(self.terminator.estimateProgress())
            results.append([x.fitness for x in self.pop])
        #return best solution and results
        return np.max(self.pop), np.array(results)

    def __generateOffspring(self, nrOff):
        newInds = np.empty(nrOff, dtype=Individual)
        for i in range(nrOff):
            ind0 = self.selector.select(self.pop)
            ind1 = self.selector.select(self.pop)
            indNew = self.recombiner.recombine(self.probDef, ind0, ind1)
            self.mutator.mutate(indNew,self.probDef)
            newInds[i] = self.localSearcher.search(indNew)
        return newInds

