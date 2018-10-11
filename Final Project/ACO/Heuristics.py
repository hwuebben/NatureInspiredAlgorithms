import numpy as np
from ACO.Problem import Problem, TSPProblem
from abc import abstractmethod
from ACO.Module import Module


class Heuristic(Module):

    @classmethod
    @abstractmethod
    def calculate_etas(cls, problem: Problem):
        pass


class TSPHeuristic(Heuristic):

    @classmethod
    def calculate_etas(cls, problem: TSPProblem):
        return 1 / (problem.get_distance_matrix() + np.eye(problem.get_size())) - np.eye(problem.get_size())
