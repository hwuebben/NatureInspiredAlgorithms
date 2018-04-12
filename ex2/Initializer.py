from abc import ABC, abstractmethod
import numpy as np
from Individual import Individual
from ProblemDefinition import ProblemDefinition as PD
class Initializer(ABC):
    @abstractmethod
    def initialize(self,popSize):
        pass


class RandomInitializer(Initializer):
    def initialize(self,popSize):
        """
        randomly generate individuals
        :param popSize:
        :return: pop
        """
        population = []
        for i in range(popSize):
            population.append(Individual(np.random.randint(0,PD.nrMachines-1,PD.nrJobs)))
        population.sort(key=lambda x: x.getFitness())
        return population

#example for another module
class SomeOtherInitializer(Initializer):
    #parameters can be passed in the constructor
    def __init__(self, someParameters):
        self.someParameters = someParameters

    def initialize(self,popSize):
        pass