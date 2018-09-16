from Problem import *
import numpy as np
from abc import ABC, abstractmethod


class AbstractInitializer(ABC):

    @abstractmethod
    def initialize(self, problem: Problem) -> np.array:
        """
        generate pheromone matrix
        :param problem:
        :return: pheromone matrix
        """
        pass


class VRP_Initializer(ABC):

    def initialize(self, problem: VehicleRoutingProblem) -> np.array:
        """
        generate pheromone matrix for TSP
        :param problem:
        :return: pheromone matrix
        """
        vehicles = problem.vehicles
        items = problem.get_size()
        shape = [1 + vehicles * items, 1 + vehicles * items]
        return np.ones(shape)
