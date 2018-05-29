from abc import ABC, abstractmethod
import numpy as np
from Individual import Individual


class Mutator(ABC):
    def __init__(self, F: float, problem):
        """
        :param F: scale Factor
        """
        self.F = F
        self.problem = problem

    @abstractmethod
    def mutate(self,toMutate: Individual, population: list) -> Individual:
        pass

    def mutate_population(self, population: list) -> list:
        """
        generates a list of donor individuals for a given population
        :param population:
        :return: list of donor individuals
        """
        result = list()
        for individual in population:
            result.append(self.mutate(toMutate=individual, population=population))
        return result



class randMutator(Mutator):

    def mutate(self, toMutate: Individual, population: list) -> Individual:
        """
        create and return a mutated donor vector related to the individual to be mutated
        :param toMutate: an individual to mutate
        :param population: a list of individuals, forming the current population (including the Individual to mutate)
        :return: donor individual
        """
        # exclude the target vector by setting its choice probability to 0
        probabilities = np.ones(len(population)) / (len(population)-1)
        probabilities[population.index(toMutate)] = 0
        # choose three other vectors from the population
        samples = np.random.choice(population, size=3, replace=False, p=probabilities)
        # create and return donor vector
        return Individual(samples[0].x + self.F * (samples[1].x - samples[2].x), self.problem)


class bestMutator(Mutator):

    def mutate(self, toMutate: Individual, population: list) -> Individual:
        """
        create and return a mutated donor vector based on the best individual related to the individual to be mutated
        :param toMutate: an individual to mutate
        :param population: a list of individuals, forming the current population (including the Individual to mutate)
        :return: donor individual
        """
        # determine the best individual
        best = population[np.argmax(population)]
        # exclude the target and the best vector by setting its choice probability to 0
        if (toMutate == best):
            probabilities = np.ones(len(population)) / (len(population)-1)
        else:
            probabilities = np.ones(len(population)) / (len(population)-2)
        probabilities[population.index(toMutate)] = 0
        probabilities[population.index(best)] = 0
        # choose two other vectors from the population
        samples = np.random.choice(population, size=2, replace=False, p=probabilities)
        # create and return donor vector
        return Individual(best.x + self.F * (samples[0].x - samples[1].x), self.problem)



