from abc import ABC, abstractmethod
import numpy as np
from Individual import Individual

class Initializer(ABC):
    def __init__(self,NP:int, xMin:np.array, xMax:np.array):
        self.NP = NP
        self.xMin = xMin
        self.xMax = xMax

    @abstractmethod
    def initialize(self, ) -> np.array:
        """
        generate individuals of first generation
        :param popSize:
        :return: pop
        """
        pass


class RandomInitializer(Initializer):

    def initialize(self):
        """
        randomly generate NP individuals with value ranges xMin xMax
        :param NP:
        :param xMin:
        :param xMax:
        :return:
        """

        pop = np.empty(self.NP, dtype=Individual)
        for i in range(self.NP):
            pop[i] = Individual(self.xMin,self.xMax)
        return pop
