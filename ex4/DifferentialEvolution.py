import numpy as np

from Individual import Individual
import LocalSearcher


class DifferentialEvolution:

    def __init__(self,initializer, selector, recombiner, mutator, terminator):
        self.initializer = initializer
        self.selector = selector
        self.recombiner = recombiner
        self.mutator = mutator
        self.terminator = terminator

        self.pop = self.initializer.initialize()
        self.nrIt = 0

    def run(self):
        results = list()
        #main loop
        while not self.terminator.checkTermination(self):
            newInds = self.__generateOffspring(self.nrOffspring)
            self.pop = self.replacer.replace(newInds, self.pop)
            self.nrIt += 1
            results.append([x.fitness for x in self.pop])
        #return best solution and results
        return np.max(self.pop), np.array(results)

    def __generateOffspring(self, nrOff):
        newInds = np.empty(nrOff, dtype=Individual)
        for i in range(nrOff):
            ind0 = self.selector.select(self.pop)
            ind1 = self.selector.select(self.pop)
            indNew = self.recombiner.recombine(self.probDef, ind0, ind1)
            indNew = self.mutator.mutate(indNew)
            newInds[i] = self.localSearcher.search(indNew)
        return newInds

