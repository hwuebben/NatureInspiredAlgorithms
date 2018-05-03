import numpy as np


class Intensifier:
    def __init__(self, delta=0.1):
        """

        :param evaporation: quickness of the evaporation in percent
        :return:
        """
        self.delta = delta

    def intensify(self, pheromone_matrix: np.array, best_solution: np.array) -> np.array:
        """
        use the best solution to intensify the its path
        :param pheromone_matrix: NxN matrix
        :param best_solution: NxN binary matrix
        :return:
        """
        update = self.delta * best_solution
        return pheromone_matrix * update
