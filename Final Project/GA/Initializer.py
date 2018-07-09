from abc import ABC, abstractmethod
import numpy as np
from Individual import Individual
from ProblemDefinition import ProblemDefinition as PD


class Initializer(ABC):

    @abstractmethod
    def initialize(self, probDef, popSize):
        """
        generate individuals of first generation
        :param popSize:
        :return: pop
        """
        pass


class RandomInitializer(Initializer):

    def initialize(self, probDef, popSize):
        """
        randomly generate individuals
        :param popSize:
        :param probDef:
        :return: pop
        """
        population = np.empty(popSize, dtype=Individual)
        for i in range(popSize):
            population[i] = Individual.initIndividual(probDef, "random")
        return population

class HeuristicInitializer(Initializer):

    def initialize(self, probDef, popSize):
        population = np.empty(popSize, dtype=Individual)
        for i in range(popSize):
            population[i] = Individual.initIndividual(probDef, "heuristic")
            # population[i].checkConsistency(probDef)
        return population
