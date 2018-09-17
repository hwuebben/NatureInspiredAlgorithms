from Problem import *
import numpy as np
from abc import ABC, abstractmethod


class AbstractInitializer(ABC):
    """
    Abstract Initializer class, used for different initializer strategies
    """

    @abstractmethod
    def initialize(self, problem: Problem) -> np.array:
        """
        generate pheromone matrix for specific problem
        :param problem: a arbitrary problem as Problem-object
        :return: pheromone matrix
        """
        pass


class VRP_Initializer(ABC):

    def initialize(self, problem: VehicleRoutingProblem) -> np.array:
        """
        generate pheromone matrix for a Vehicle Routing Problem
        :param problem: the VRP in question
        :return: pheromone matrix
        """
        vehicles = problem.vehicles
        items = problem.get_size()
        shape = [1 + vehicles * items, 1 + vehicles * items]
        return np.ones(shape)
