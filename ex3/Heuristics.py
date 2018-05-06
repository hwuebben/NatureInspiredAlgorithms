import numpy as np
from Problem import Problem, TSPProblem
from abc import ABC, abstractmethod


class Heuristic(ABC):

    @classmethod
    @abstractmethod
    def calculate_etas(cls, problem: Problem):
        pass


class TSPHeuristic(Heuristic):

    @classmethod
    def calculate_etas(cls, problem: TSPProblem):
        return 1 / (problem.get_distance_matrix() + np.eye(problem.get_size())) - np.eye(problem.get_size())
