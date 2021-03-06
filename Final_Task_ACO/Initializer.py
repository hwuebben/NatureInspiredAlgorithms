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
        num_of_vehicles = problem.selected_capacity.shape[0]
        num_of_nodes = problem.get_size()
        shape = [num_of_vehicles, num_of_nodes, num_of_nodes]
        return np.ones(shape)
