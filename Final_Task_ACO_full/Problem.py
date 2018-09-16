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


class VehicleRoutingProblem(PermutationProblem):

    def __init__(self, problem: int = 1):
        """

        :param problem: integer, specifying the problem, valid inputs are 1,2 and 3
        :return:
        """
        self.path = 'problem_' + str(problem)
        try:
            self.capacity, self.demand, self.distance_matrix, self.transportation_cost = self.__load_data()
        except FileNotFoundError:
            raise ValueError('Unknown benchmark problem ' + str(problem))
        if self.distance_matrix.shape[0] != self.distance_matrix.shape[1]:
            raise AssertionError('Distance matrix is not quadratic.')
        if self.distance_matrix.shape[0] != self.demand.shape[0]+1:
            raise AssertionError('Number of customers is not consistent.')
        if self.capacity.shape[0] != self.transportation_cost.shape[0]:
            raise AssertionError('Number of vehicles is not consistent.')
        if np.sum(self.capacity) < np.sum(self.demand):
            raise AssertionError('Insufficient capacity')
        self.vehicles = self.capacity.shape[0]

    def __load_data(self) -> np.array:
        """
        parse .tsp file into the distance matrix.
        :return:
        """
        with open('.'+os.sep+'ressources'+os.sep+self.path+os.sep+'capacity.txt','r') as fp:
            capacity = self.__parse_line(fp.readline())
        with open('.' + os.sep + 'ressources' + os.sep + self.path + os.sep + 'demand.txt', 'r') as fp:
            demand = self.__parse_line(fp.readline())
        with open('.' + os.sep + 'ressources' + os.sep + self.path + os.sep + 'distance.txt', 'r') as fp:
            distance_matrix = []
            for line in fp:
                row = self.__parse_line(line)
                distance_matrix.append(row)
        with open('.' + os.sep + 'ressources' + os.sep + self.path + os.sep + 'transportation_cost.txt', 'r') as fp:
            transportation_cost = self.__parse_line(fp.readline())
        return np.asarray(capacity), np.asarray(demand), np.asarray(distance_matrix), np.asarray(transportation_cost)

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
        score = 0
        for vehicle, vehicle_solution in enumerate(solution):
            vehicle_solution = (vehicle_solution[1:] - 1) % self.get_size()
            distances = self.distance_matrix[vehicle_solution[0:-1], vehicle_solution[1:]]
            costs = distances * self.transportation_cost[vehicle]
            score += np.sum(costs)
        return score

    def get_size(self):
        return self.distance_matrix.shape[0]
