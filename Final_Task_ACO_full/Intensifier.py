import numpy as np


class Intensifier:
    def __init__(self, delta=0.1):
        """
        :param evaporation: quickness of the evaporation in percent
        :return:
        """
        self.delta = delta

    def intensify(self, pheromone_matrix: np.array, solution: np.array, ratio: float) -> np.array:
        """
        use the best solution to intensify the its path

        :param pheromone_matrix: NxN matrix
        :param solution: NxN binary matrix
        :param ratio: degree by which influences the pheromones
        :return: updated pheromone matrix
        """
        update = np.zeros(pheromone_matrix.shape)
        for vehicle_solution in solution:
            update[vehicle_solution[0:-1], vehicle_solution[1:]] = self.delta * ratio
        return pheromone_matrix + update
