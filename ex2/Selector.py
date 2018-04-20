from abc import ABC, abstractmethod
import numpy as np
class Selector(ABC):
    @abstractmethod
    def select(self,pop):
        pass
    def dynamicAdaptation(self,progress):
        pass


class RouletteSelector(Selector):

    def select(self,pop):
        """
        perform roulette wheel selection on pop
        :param pop:
        :return: selected individual
        """
        probs = [x.getFitness() for x in pop]
        probs /= sum(probs)
        result =  np.random.choice(pop,p=probs)
        return result


class TournamentSelector(Selector):
    def __init__(self,s=2,dynAdapt=False,maxS=12):
        self.s = s
        self.originalS = s
        self.dynAdapt=dynAdapt
        self.maxS=maxS

    def select(self,pop):
        """
        perform tournament selection on pop with s individuals
        :param pop:
        :return: selected individual
        """
        self.s = min(self.s, pop.size)
        candidates =  np.random.choice(pop,self.s,replace=False)
        if candidates[0] > candidates[1]:
            return candidates[0]
        else:
            return candidates[1]

    def dynamicAdaptation(self,progress):
        self.s = int(self.originalS + progress*self.maxS)


