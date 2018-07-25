import numpy as np
from Individual import Individual
import LocalSearcher
import copy
import pickle


class GeneticAlgorithm:

    def __init__(self, initializer, selector, recombiner, mutator, replacer, terminators,
                 probDef, popSize, offspringProp, localSearcher = LocalSearcher.Idle(), includeUnmutated = True):
        self.initializer = initializer
        self.selector = selector
        self.recombiner = recombiner
        self.mutator = mutator
        self.replacer = replacer
        self.terminators = terminators
        self.localSearcher = localSearcher

        self.probDef = probDef
        self.pop = self.initializer.initialize(self.probDef, popSize)
        self.nrIt = 0
        self.popSize = popSize
        self.nrOffspring = int(offspringProp*popSize)
        self.includeUnmutated = includeUnmutated

    def run(self):
        results = list()
        #main loop

        while not any([t.checkTermination(self) for t in self.terminators]):
            newInds = self.__generateOffspring(self.nrOffspring)
            self.pop = self.replacer.replace(newInds, self.pop)
            self.nrIt += 1
            # pass the progress to the mutator and selector module to enable simulated annealing
            self.mutator.dynamicAdaptation(self.terminators[-1].estimateProgress())
            self.selector.dynamicAdaptation(self.terminators[-1].estimateProgress())
            #results.append([x.fitness for x in self.pop])
        #return best solution and results
        return np.max(self.pop), np.array(results)

    def __generateOffspring(self, nrOff):
        newInds = np.empty(nrOff*(self.includeUnmutated+1), dtype=Individual)
        for i in range(nrOff):
            ind0,ind1 = self.selector.select(self.pop)
            indNew = self.recombiner.recombine(self.probDef, ind0, ind1)
            if self.includeUnmutated:
                newInds[-(i+1)] = copy.deepcopy(indNew)
            #indNewCopy = copy.deepcopy(indNew)
            self.mutator.mutate(indNew,self.probDef)
            newInds[i] = self.localSearcher.search(indNew)
        return newInds

    def pickleStore(self, name):
        pickle.dump(self,open(name+".p","wb"))
