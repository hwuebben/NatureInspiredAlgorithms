import numpy as np

class Evaporator:

    def __init__(self, evaporation = 0.1):
        """

        :param evaporation: quickness of the evaporation in percent.
        :return:
        """
        self.evaporation = evaporation

    def evaporate(self, pheromone_matrix : np.array) -> np.array:
        """
        evaporate the the values of the pheromone matrix.
        :param pheromone_matrix:
        :return:
        """
        return (1-self.evaporation) * pheromone_matrix