from abc import ABC, abstractmethod
import numpy as np
from Individual import Individual
from copy import deepcopy


class Recombiner(ABC):
    def __init__(self, Cr):
        """
        :param Cr: Crossover rate
        """
        self.Cr = Cr

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
            result.append(self.recombine(population[i],donors[i]))
        return result



class ExponentialCrossover(Recombiner):

    def get_L(self, max_length):
        L = 1
        while L <= max_length and np.random.uniform(0,1.0) <= self.Cr:
            L += 1
        return L

    def recombine(self,targetVector: Individual, donorVector: Individual) -> Individual:
        """
        Exponential recombination
        :param targetVector:
        :param donorVector:
        :return:
        """

        # deepcopy the target Vector
        trial = targetVector.x[:]
        donor = donorVector.x

        n = np.random.randint(0, len(trial), 1)
        D = len(trial)
        L = self.get_L(D)

        # if crossoveer exceeds bounds
        if n+L > D:
            trial[n:D] = donor[n:D]
            trial[0:(n+L) % D] = trial[0:(n+L) % D]
        else:
            trial[n:L] = donor[n:L]

        trialVector = deepcopy(targetVector)
        trialVector.x = trial
        trialVector.targFuncVal = Individual.targetFunc(trial)

        return trial

class BinomialCrossover(Recombiner):

    def recombine(self,targetVector: Individual, donorVector: Individual) -> Individual:
        """
        performs a binominal recombination.
        :param targetVector:
        :param donorVector:
        :return:
        """
        trial = targetVector.x[:]
        donor = donorVector.x

        D = len(trial)

        j_rand = np.random.randint(0,D,1)

        bin_vals = np.random.uniform(size=D)

        trial[bin_vals <= self.Cr] = donor[bin_vals <= self.Cr]
        trial[j_rand] = donor[j_rand]

        return trial

