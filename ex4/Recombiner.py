from abc import ABC, abstractmethod
import numpy as np
from Individual import Individual


class Recombiner(ABC):
    def __init__(self, Cr: float, problem):
        """
        :param Cr: Crossover rate
        :param problem:
        """
        self.Cr = Cr
        self.problem = problem

    @abstractmethod
    def recombine(self,targetVector: Individual, donorVector: Individual) -> Individual:
        pass

    def get_trials(self, population: list, donors: list) -> list:
        """
        recombine a population given the population and the donors, assumes in donor and target population
        :param population:
        :param donors:
        :return:
        """
        result = []
        for i in range(len(population)):
            result.append(self.recombine(population[i], donors[i]))
        return result


class ExponentialCrossover(Recombiner):

    def __get_L(self, max_length):
        L = 1
        while L <= max_length and np.random.uniform(0,1.0) <= self.Cr:
            L += 1
        return L

    def recombine(self, targetVector: Individual, donorVector: Individual) -> Individual:
        """
        Exponential recombination
        :param targetVector:
        :param donorVector:
        :return:
        """

        trial = np.copy(targetVector.x)
        donor = donorVector.x

        D = len(trial) # dimensionality of individual genome
        n = np.random.randint(0, D, 1)[0] # random starting point
        L = self.__get_L(D) # number of contributing donor components

        # if crossoveer exceeds bounds
        if n+L > D:
            trial[n-D:n+L-D] = donor[n-D:n+L-D]
        else:
            trial[n:L] = donor[n:L]

        return Individual(trial, self.problem)

class BinomialCrossover(Recombiner):

    def recombine(self,targetVector: Individual, donorVector: Individual) -> Individual:
        """
        performs a binominal recombination.
        :param targetVector:
        :param donorVector:
        :return:
        """
        trial = np.copy(targetVector.x)
        donor = donorVector.x

        D = len(trial)

        j_rand = np.random.randint(0,D,1)

        bin_vals = np.random.uniform(size=D)

        trial[bin_vals <= self.Cr] = donor[bin_vals <= self.Cr]
        trial[j_rand] = donor[j_rand]

        return Individual(trial, self.problem)

