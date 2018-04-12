from abc import ABC, abstractmethod
import numpy as np
class Selector(ABC):
    @abstractmethod
    def select(self,pop):
        pass


class RouletteSelector(Selector):

    def select(self,pop):
        """
        perform roulette wheel selection on sorted pop
        :param pop:
        :return: selected individual
        """
        fitnessSum = 0
        for ind in pop:
            fitnessSum += ind.getFitness()
        randVal = fitnessSum * np.random.rand()
        itSum = 0
        for ind in pop:
            itSum += ind.getFitness()
            if itSum >= randVal:
                return ind


