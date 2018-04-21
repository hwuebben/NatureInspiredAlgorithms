from abc import ABC, abstractmethod
import numpy as np


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
        probs = [x.getFitness() for x in pop]
        probs /= sum(probs)
        result = np.random.choice(pop, p=probs)
        return result


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
        return max(candidates)

    def dynamicAdaptation(self, progress):
        """
        increase number of tournament candidates due to progress
        :param pop:
        :return: selected individual
        """
        if self.dynAdapt:
            self.s = int(self.originalS + progress*self.maxS)


