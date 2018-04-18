from abc import ABC, abstractmethod
import numpy as np
class Selector(ABC):
    @abstractmethod
    def select(self,pop):
        pass
    def simAnnealing(self,progress):
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

    def select(self,pop):
        """
        perform tournament selection on pop with s = 2
        :param pop:
        :return: selected individual
        """

        candidates =  np.random.choice(pop,2,replace=False)
        if candidates[0] > candidates[1]:
            return candidates[0]
        else:
            return candidates[1]


