import numpy as np
from abc import abstractmethod
from ACO.Module import Module


class AbstractInitializer(Module):

    @abstractmethod
    def initialize(self, num_cities : int) -> np.array:
        """
        generate pheromone matrix
        :param popSize:
        :return: pop
        """
        pass

class TSP_Initializer(AbstractInitializer):

    def initialize(self, problem) -> np.array:
        """
        generate pheromone matrix for TSP
        :param popSize:
        :return: pop
        """
        size = problem.get_size()
        return np.ones((size, size))