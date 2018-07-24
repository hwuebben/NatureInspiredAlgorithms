from abc import ABC, abstractmethod
import numpy as np
from Individual import Individual


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

    def select(self, pop):
        """
        perform roulette wheel selection on pop
        :param pop:
        :return: selected individual
        """
        probs = [x.fitness for x in pop]
        #if fitness values are negative, make positive
        minProb = min(probs)
        if minProb < 0:
            probs -= minProb
        probs /= sum(probs)
        result = np.random.choice(pop,size=2,replace=False, p=probs)
        return result[0],result[1]

class SmartRouletteSelector(Selector):

    def select(self, pop):
        """
        perform roulette wheel selection on pop
        :param pop:
        :return: selected individual
        """
        probs = [x.fitness for x in pop]
        #if fitness values are negative, make positive
        minProb = min(probs)
        if minProb < 0:
            probs -= minProb
        probs /= sum(probs)
        first = np.random.choice(pop,replace=False, p=probs)

        firstAss = first.assign > 0

        #find appropriate mate
        # probs = [self.invHamming(firstAss, x) if x != first else 0 for x in pop]
        # probs /= np.sum(probs)
        # second = np.random.choice(pop,replace=False, p=probs)

        invHammings = [self.invHamming(firstAss,x) for x in pop]
        maxInds = np.argmax(invHammings).flatten()
        probs = invHammings[maxInds]/np.sum(invHammings[maxInds])
        popSlice = pop[maxInds]
        if popSlice.size > 1:
            second = np.random.choice(popSlice,p = probs)
        else:
            second = popSlice[0]
        #second = max(pop, key=lambda x: self.invHamming(firstAss,x))
        return first,second


    def invHamming(self,firstAss, ind0):
        return np.sum(np.equal(firstAss, ind0.assign > 0).flat)


class TournamentSelector(Selector):

    def __init__(self, s=2, maxS=12, dynAdapt=False):
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
        result =  max(candidates)
        candidates =  np.random.choice(pop, min(self.s, pop.size), replace=False)
        result =  max(candidates)
        return result

    def dynamicAdaptation(self, progress):
        """
        increase number of tournament candidates due to progress
        :param pop:
        :return: selected individual
        """
        if self.dynAdapt:
            self.s = int(self.originalS + progress*self.maxS)


