import numpy as np
from abc import ABC, abstractmethod

class AbstractSolutionGenerator(ABC):

    def __init__(self, number_of_ants: int, distance_matrix: np.array):
        self.number_of_ants = number_of_ants
        self.distance_matrix = distance_matrix

    @abstractmethod
    def create_single_solution(self, pheromone_matrix: np.array) -> np.array:
        pass

    def get_score(self, solution: np.array):
        """
        calculate the score based on the distance between cities
        :param solution: NxN binary matrix
        :return:
        """
        return np.sum(solution*self.distance_matrix)

    def get_solution(self, pheromone_matrix : np.array) -> np.array:
        """
        Create solutions corresponding to the number of ants and return the best solution
        :param pheromone_matrix: the pheromon values for each decision
        :return: NxN binary matrix, representing the best solution according to the objective function
        """
        best_solution = None
        best_score = None

        for i in range(self.number_of_ants):
            solution = self.create_single_solution(pheromone_matrix)
            score = self.get_score(solution)
            if best_score == None or score < best_score:
                best_score = score
                best_solution = solution
        return best_solution


class SolutionGenerator(AbstractSolutionGenerator):

    def __init__(self, number_of_ants : int,distance_matrix: np.array, alpha : int, beta : int):
        """
        Implements the simple distance heuristic solution generation
        :param number_of_ants:
        :param alpha:
        :param beta:
        :return:
        """
        super().__init__(number_of_ants, distance_matrix)
        self.alpha = alpha
        self.beta = beta

    def create_single_solution(self, pheromone_matrix: np.array) -> np.array:
        pass
