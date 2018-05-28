from abc import ABC, abstractmethod
from Problem import *
from Individual import *

class Initializer(ABC):
    def __init__(self, NP: int, xMin: np.array, xMax: np.array, problem: Problem):
        """
        :param NP:
        :param xMin:
        :param xMax:
        """

        self.NP = NP
        self.xMin = xMin
        self.xMax = xMax
        self.problem = problem

    @abstractmethod
    def initialize(self) -> np.array:
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
        """

        pop = list()
        for i in range(self.NP):
            pop.append(Individual(np.random.rand(self.xMin.size) * (self.xMax - self.xMin) + self.xMin, self.problem))
        if not all([Problem.validate(individual) for individual in pop]):
            raise ValueError("No valid initialization of population!")
        return pop
