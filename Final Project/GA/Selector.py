from abc import ABC, abstractmethod
import numpy as np
import numba

class Selector(ABC):

    @abstractmethod
    def select(self,pop):
        """
        perform roulette wheel selection on pop
        :param pop:
        :return: selected individual
        """
        pass

    def dynamicAdaptation(self, progress):
        """
        increase number of tournament candidates due to progress
        :param pop:
        :return: selected individual
        """
        pass



class RouletteSelector(Selector):
    def setProbs(self,pop):
        #since fitness values are negative, make positive
        minProb = np.min(pop).fitness
        maxProb = np.max(pop).fitness
        probs = np.array([x.fitness - (minProb+maxProb) for x in pop])

        probs /= np.sum(probs)
        self.probs = probs
    def select(self, pop):
        """
        perform roulette wheel selection on pop
        :param pop:
        :return: selected individual
        """
        result = np.random.choice(pop,size=2,replace=False, p=self.probs)
        return result[0],result[1]
    def singleSelect(self,pop,nrSelect):
        probs = [x.fitness for x in pop]
        #if fitness values are negative, make positive
        minProb = min(probs)
        if minProb < 0:
            probs -= (minProb+max(probs))
        probs /= sum(probs)
        result = np.random.choice(pop,size=nrSelect,replace=False, p=probs)
        return result
class RouletteSelectorJit(Selector):
    def setProbs(self,pop):
        def f(minProb,maxProb):
            #since fitness values are negative, make positive
            minProb = np.min(pop).fitness
            maxProb = np.max(pop).fitness
            probs = np.array([x.fitness - (minProb+maxProb) for x in pop])

            probs /= np.sum(probs)
            self.probs = probs
    def select(self, pop):
        """
        perform roulette wheel selection on pop
        :param pop:
        :return: selected individual
        """
        result = np.random.choice(pop,size=2,replace=False, p=self.probs)
        return result[0],result[1]
    def singleSelect(self,pop,nrSelect):
        probs = [x.fitness for x in pop]
        #if fitness values are negative, make positive
        minProb = min(probs)
        if minProb < 0:
            probs -= (minProb+max(probs))
        probs /= sum(probs)
        result = np.random.choice(pop,size=nrSelect,replace=False, p=probs)
        return result

class SmartRouletteSelector(Selector):

    def select(self, pop):
        """
        perform roulette wheel selection on pop
        :param pop:
        :return: selected individual
        """
        probs = [x.fitness for x in pop]
        #scale fitness values from positive 1 onwards (negative ones become positive)
        probs -= (min(probs)-1)
        probs /= sum(probs)
        first = np.random.choice(pop,replace=False, p=probs)

        firstAss = first.assign > 0

        invHammings = np.array([self.invHamming(firstAss,x) if not(x is first) else 0 for x in pop])
        #maxInds = np.argmax(invHammings).flatten()
        maxInds = np.nonzero(invHammings >= (np.max(invHammings)*0.99))[0]
        popSlice = pop[maxInds]
        probs = [x.fitness for x in popSlice]
        #scale fitness values from positive 1 onwards (negative ones become positive)
        probs -= (min(probs)-1)
        probs /= sum(probs)
        #probs = invHammings[maxInds]/np.sum(invHammings[maxInds])
        second = np.random.choice(popSlice,p = probs)

        #second = max(pop, key=lambda x: self.invHamming(firstAss,x))
        return first,second


    def invHamming(self,firstAss, ind0):
        return np.sum(np.equal(firstAss, ind0.assign > 0).flat)


class TournamentSelector(Selector):

    def __init__(self, s=4, maxS=12, dynAdapt=False):
        self.s = s
        self.originalS = s
        self.maxS = maxS
        self.dynAdapt = dynAdapt

    def select(self, pop):
        """
        perform tournament selection on pop with s individuals
        :param pop:
        :return: selected individual
        """
        candidates =  np.random.choice(pop, min(self.s, pop.size), replace=False)
        result =  candidates[np.argsort(candidates)[-2:]]
        return result[0],result[1]

    def dynamicAdaptation(self, progress):
        """
        increase number of tournament candidates due to progress
        :param pop:
        :return: selected individual
        """
        if self.dynAdapt:
            self.s = int(self.originalS + progress*self.maxS)


