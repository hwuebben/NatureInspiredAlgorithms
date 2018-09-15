import numpy as np
from Individual import Individual
import LocalSearcher
import copy
import pickle
import time
from pathlib import Path

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
        #self.offspringProp = offspringProp
        self.nrOffspring = max(1,int(offspringProp*popSize))

        self.includeUnmutated = includeUnmutated
        self.verbose = verbose

    def runWithQueue(self,queue,n = 0):
        lastBest = -np.inf
        #main loop
        while not any([t.checkTermination(self) for t in self.terminators]):
            self.iteration()
            bestInd = self.getNthbestInd(n)
            if bestInd.fitness > lastBest:
                queue.put_nowait(bestInd)

    def runWithPipe(self,pipe):
        #main loop
        while not any([t.checkTermination(self) for t in self.terminators]):
            self.iteration()
            if pipe.poll():
                n = pipe.receive()
                pipe.send(self.getNthbestInd(n))
    def runWithPipeFinalGA(self,pipe):
        while not any([t.checkTermination(self) for t in self.terminators]):
            self.iteration()
        pipe.send(self)

    def run(self):
        #main loop
        while not any([t.checkTermination(self) for t in self.terminators]):
            self.iteration()
        #return best solution and results
        return np.max(self.pop)

    def iteration(self):
        if self.verbose:
            print("best fitness: ", np.max(self.pop).fitness)
            print("terminator progress: ", self.terminators[-1].estimateProgress())
        newInds = self.__generateOffspring(self.nrOffspring)
        #newInds = self.__generateOffspringSingleSelect(self.nrOffspring)
        self.pop = self.replacer.replace(newInds, self.pop)
        self.nrIt += 1
        # pass the progress to the mutator and selector module to enable simulated annealing
        for mutator in self.mutators:
            mutator.dynamicAdaptation(self.terminators[-1].estimateProgress())
        self.selector.dynamicAdaptation(self.terminators[-1].estimateProgress())
        self.replacer.dynamicAdaptation(self.terminators[-1].estimateProgress())
        self.recombiner.dynamicAdaptation(self.terminators[-1].estimateProgress())

    def __generateOffspringSingleSelect(self,nrOff):
        """
        this method selects individuals and recombines each with each
        in order to achieve the desired amount of offspring.
        :param nrOff:
        :return:
        """
        newInds = []
        for i in range(nrOff):
            #nrSelect is the necessary amount of individuals to create nrOff (reversed gauss sum formula)
            nrSelect = max(2,int(np.ceil(-0.5 + np.sqrt(0.25 + 2*nrOff))))
            inds = self.selector.singleSelect(self.pop,nrSelect)
            count = 0
            for i,ind0 in enumerate(inds):
                for ind1 in inds[i+1::]:
                    if count > nrOff:
                        break
                    indNew = self.recombiner.recombine(self.probDef, ind0, ind1)

                    if self.includeUnmutated:
                        newInds.append(copy.deepcopy(indNew))

                    for mutator in self.mutators:
                        mutator.mutate(indNew,self.probDef)

                    newInds.append(self.localSearcher.search(indNew,self.probDef))
                    count += 1

        return np.array(newInds)

    def __generateOffspring(self, nrOff):
        newInds = []
        self.selector.setProbs(self.pop)
        for i in range(nrOff):
            ind0,ind1 = self.selector.select(self.pop)
            indNew = self.recombiner.recombine(self.probDef, ind0, ind1)

            if self.includeUnmutated:
                # #TODO: not generic, idea is to not add redundant individuals to pop
                # if (indNew.assign != ind0.assign).any() and (indNew.assign != ind1.assign).any():
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
            newInds.append(self.localSearcher.search(indNew,self.probDef))
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
        #import os
        #folderPath = Path("PickledGAs/")
        name += ".p"
        #path = folderPath / name
        pickle.dump(self,open(name,"wb"))

    def getNthbestInd(self,n):
        if n == 0:
            return np.max(self.pop)
        else:
            return np.partition(self.pop, -n)[-n]
    def putNthbestIndQueue(self,n):
        if n == 0:
            self.queue.put(np.max(self.pop))
        else:
            self.queue.put_nowait(np.partition(self.pop, -n)[-n])

