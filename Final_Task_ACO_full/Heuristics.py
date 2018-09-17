import numpy as np
from Problem import Problem, VehicleRoutingProblem
from abc import ABC, abstractmethod


class Heuristic(ABC):
    """
    Abstract Heuristic class, representing a heuristic used by the ACO
    """

    @classmethod
    @abstractmethod
    def calculate_etas(cls, problem: Problem) -> np.array:
        """
        Calculate the heuristic given a arbitrary problem
        :param problem:  the Problem in question
        :return: result of the heuristic estimation
        """
        pass


class TSPHeuristic(Heuristic):

    @classmethod
    def calculate_etas(cls, problem: VehicleRoutingProblem) -> np.array:
        """
        Calculate the estimated time of arrival of vehicles for a vehicle routingproblem
        :param problem: a vehicle routing problem as vehicle routing problem object
        :return: estimated times of arrival for all vehicles provided by the problem
        """
        vehicle_etas = 1 / (problem.distance_matrix + np.eye(problem.get_size())) - np.eye(problem.get_size())
        num_of_vehicles = problem.vehicles
        num_of_nodes = problem.get_size()
        shape = [1 + num_of_vehicles * num_of_nodes, 1 + num_of_vehicles * num_of_nodes]
        etas = np.ones(shape=shape)
        for vehicle in range(num_of_vehicles):
            start_pos = 1 + vehicle * num_of_nodes
            end_pos = start_pos + num_of_nodes
            etas[start_pos:end_pos, start_pos:end_pos] = vehicle_etas

        return etas
