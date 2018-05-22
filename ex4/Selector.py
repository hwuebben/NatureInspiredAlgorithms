from abc import ABC, abstractmethod
import numpy as np


class Selector(ABC):

    @abstractmethod
    def select(self,population: list, trials: list) -> list:
        """

        :param population: current population
        :param trials: trial-individuals
        :return:
        """
        pass



class DEselector(Selector):

    def select(self, population: list, trials: list) -> list:
        """
        The vanilla version of the selector, using simple comparisons of the objective function.
        The function assumes that population Individuals and trial Individuals are ordered the same way
        :param population: current population
        :param trials: trial-individuals
        :return:
        """
        next_gen = []
        for i in range(len(population)):
            if population[i] >= trials[i]:
                next_gen.append(population[i])
            else:
                next_gen.append(trials[i])
        return next_gen