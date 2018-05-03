import numpy as np
from abc import ABC, abstractmethod

class AbstractSolutionGenerator(ABC):

    def __init__(self, number_of_ants: int):
        self.number_of_ants = number_of_ants

    @abstractmethod
    def create_single_solution(self, pheromone_matrix: np.array, distance_matrix: np.array) -> np.array:
        pass

    def get_score(self, solution: np.array, distance_matrix: np.array) -> float:
        """
        calculate the score based on the distance between cities
        :param solution: NxN binary matrix
        :param distance_matrix: NxN distance matrix
        :return:
        """
        return np.sum(solution*distance_matrix)

    def get_solution(self, pheromone_matrix: np.array, distance_matrix: np.array) -> np.array:
        """
        Create solutions corresponding to the number of ants and return the best solution
        :param pheromone_matrix: the pheromon values for each decision
        :param distance_matrix: NxN distance matrix
        :return: NxN binary matrix, representing the best solution according to the objective function
        """
        best_solution = None
        best_score = None

        for i in range(self.number_of_ants):
            solution = self.create_single_solution(pheromone_matrix, distance_matrix)
            score = self.get_score(solution, distance_matrix)
            if best_score is None or score < best_score:
                best_score = score
                best_solution = solution
        return best_solution, best_score


class SolutionGenerator(AbstractSolutionGenerator):

    def __init__(self, number_of_ants : int, alpha : int, beta : int):
        """
        Implements the simple distance heuristic solution generation
        :param number_of_ants:
        :param alpha:
        :param beta:
        :return:
        """
        super().__init__(number_of_ants)
        self.alpha = alpha
        self.beta = beta
