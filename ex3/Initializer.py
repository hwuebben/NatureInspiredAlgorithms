import numpy as np
from abc import ABC, abstractmethod


class AbstractInitializer(ABC):

    @abstractmethod
    def initialize(self, num_cities : int) -> np.array:
        """
        generate pheromone matrix
        :param popSize:
        :return: pop
        """
        pass

class ZeroInitializer(ABC):

    def initialize(self, num_cities : int) -> np.array:
        """
        generate pheromone matrix
        :param popSize:
        :return: pop
        """
        return np.zeros((num_cities, num_cities))
