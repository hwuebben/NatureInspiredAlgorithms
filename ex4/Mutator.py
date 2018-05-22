from abc import ABC, abstractmethod
import numpy as np
from .Individual import Individual
from copy import deepcopy, copy


class Mutator(ABC):
    def __init__(self,F: float):
        """
        :param F: scale Factor
        """
        self.F = F


    @abstractmethod
    def mutate(self,toMutate: Individual, population: list) -> Individual:
        pass

    def mutate_population(self, population: list) -> list:
        """
        generates a list of donors individuals for a given population
        :param population:
        :return:
        """
        result = []
        for individuum in population:
            result.append(self.mutate(toMutate=individuum,population=population))
        return result



class DEmutator(Mutator):

    def mutate(self,toMutate: Individual, population: list) -> Individual:
        """
        mutate a single inidivual and return a donor vector
        :param toMutate: a Individual to mutate
        :param population: A list Individuals, forming the current population (including the Individual to mutate)
        :return:
        """
        # exclude the original sample by setting its choice probability to 0
        probabilities = np.ones(len(population)) / (len(population)-1)
        probabilities[population.index(toMutate)] = 0

        # choose two other vectors from the population
        samples = np.random.choice(population, size=2, replace=False, p=probabilities)

        # create a result-object by deepcopy the target
        result = deepcopy(toMutate)
        result.targFuncVal = Individual.targetFunc(result.x)

        # modify
        result.x += self.F*(samples[0].x - samples[1].x)

        return result



