import os
import numpy as np
from abc import ABC, abstractmethod


class Problem(ABC):

    @abstractmethod
    def get_score(self, solution: np.array) -> float:
        """
        Calculate the score based on the problem definition
        :param solution: matrix describing a solution wrt the problem structure
        :return: the score for the solution
        """
        pass

class PermutationProblem(Problem):

    @abstractmethod
    def get_size(self):
        """
        Get the size of the sequence to be permuted
        :return:
        """

class TSPProblem(PermutationProblem):

    def __init__(self, problem: int = 1):
        """

        :param problem: integer, specifying the problem, valid inputs are 1,2 and 3
        :return:
        """
        if problem == 1:
            self.filename = '01.tsp'
        elif problem == 2:
            self.filename = '02.tsp'
        elif problem == 3:
            self.filename = '03.tsp'
        else:
            raise ValueError('Unknown benchmark problem, valid inputs are 1,2 or 3')
        self.distance_matrix = self.__load_data()
        if self.distance_matrix.shape[0] != self.distance_matrix.shape[1]:
            raise AssertionError('Distance matrix is not quadratic.')

    def __load_data(self) -> np.array:
        """
        parse .tsp file into the distance matrix.
        :return:
        """
        with open('.'+os.sep+'ressources'+os.sep+self.filename,'r') as fp:
            distance_matrix = []
            for line in fp:
                row = self.__parse_line(line)
                distance_matrix.append(row)
            return np.asarray(distance_matrix)

    def __parse_line(self, line: str) -> list:
        """
        parse a single line of the .tsp-file into a list of integers.
        :param line:
        :return:
        """
        row = line.split(' ')
        for i in range(len(row)-1):
            row[i] = int(row[i])
        row = row[0:-1]
        return row

    def get_score(self, solution: np.array) -> float:
        """
        calculate the score based on the distance between cities
        :param solution: NxN binary matrix
        :return:
        """
        return np.sum(self.get_distance_matrix()[solution[0:-1], solution[1:]])

    def get_size(self):
        return self.distance_matrix.shape[0]

    def get_distance_matrix(self) -> np.array:
        return self.distance_matrix
