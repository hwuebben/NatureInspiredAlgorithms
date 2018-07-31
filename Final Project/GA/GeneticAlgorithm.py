import numpy as np
from Individual import Individual
import LocalSearcher
import copy
import pickle


class GeneticAlgorithm:

    def __init__(self, initializer, selector, recombiner, mutators, replacer, terminators,
                 probDef, popSize, offspringProp, localSearcher = LocalSearcher.Idle(), includeUnmutated = True,verbose = True):
        self.initializer = initializer
        self.selector = selector
        self.recombiner = recombiner
        self.mutators = mutators
        self.replacer = replacer
        self.terminators = terminators
        self.localSearcher = localSearcher

        self.probDef = probDef
        self.pop = self.initializer.initialize(self.probDef, popSize)
        self.nrIt = 0
        self.popSize = popSize
        self.nrOffspring = int(offspringProp*popSize)
        self.includeUnmutated = includeUnmutated
        self.verbose = verbose


    def run(self):
        results = list()
        #main loop

        while not any([t.checkTermination(self) for t in self.terminators]):
            if self.verbose:
                print("best fitness: ",np.max(self.pop).fitness)
                print("terminator progress: ",self.terminators[-1].estimateProgress())
            newInds = self.__generateOffspring(self.nrOffspring)
            self.pop = self.replacer.replace(newInds, self.pop)
            self.nrIt += 1
            # pass the progress to the mutator and selector module to enable simulated annealing
            for mutator in self.mutators:
                mutator.dynamicAdaptation(self.terminators[-1].estimateProgress())
            self.selector.dynamicAdaptation(self.terminators[-1].estimateProgress())
            self.replacer.dynamicAdaptation(self.terminators[-1].estimateProgress())
            self.recombiner.dynamicAdaptation(self.terminators[-1].estimateProgress())
            #results.append([x.fitness for x in self.pop])
        #return best solution and results
        return np.max(self.pop), np.array(results)

    def __generateOffspring(self, nrOff):
        newInds = []
        for i in range(nrOff):
            ind0,ind1 = self.selector.select(self.pop)
            indNew = self.recombiner.recombine(self.probDef, ind0, ind1)

            if self.includeUnmutated:
                #TODO: not generic, idea is to not add redundant individuals to pop
                if (indNew.assign != ind0.assign).any() and (indNew.assign != ind1.assign).any():
                    newInds.append(copy.deepcopy(indNew))
                    # if self.isInPop(indNew):
                    #     print("redundant Ind after Recombination")
            #indNewCopy = copy.deepcopy(indNew)
            #np.random.choice(self.mutators).mutate(indNew,self.probDef)
            for mutator in self.mutators:
                mutator.mutate(indNew,self.probDef)

            # if self.isInPop(indNew):
            #     print("redundant Ind after Mutation")
            #assert ((indNew.assign != indNewCopy.assign).any())
            newInds.append(self.localSearcher.search(indNew))
        return np.array(newInds)

    def printNrEqualIndis(self,preText):
        print(preText)
        nrEqual = 0
        for i, ind in enumerate(self.pop):
            for ind1 in self.pop[0:i]:
                if (ind.assign == ind1.assign).all():
                    assert (ind.fitness == ind1.fitness)
                    nrEqual += 1
                    break
        print("nrEqual: ", nrEqual)

    def isInPop(self,ind):
        for ind0 in self.pop:
            if (ind0.assign == ind.assign).all():
                return True
        return False
    def pickleStore(self, name):
        pickle.dump(self,open(name+".p","wb"))

    def getNthbestInd(self,n):
        if n == 0:
            return np.max(self.pop)
        else:
            return np.partition(self.pop, -n)[-n]

