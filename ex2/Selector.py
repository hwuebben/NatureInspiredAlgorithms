from abc import ABC, abstractmethod
import numpy as np
class Selector(ABC):
    @abstractmethod
    def select(self,pop):
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
        return np.random.choice(pop,p=probs)


