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

    def __init__(self, problem: int = 1, selection = 'all', criterion: str = 'none', objective: str = 'none'):
        """

        :param problem: integer, specifying the problem, valid inputs are 1,2 and 3
        :return:
        """
        if problem == 1:
            self.path = 'problem_1'
        elif problem == 2:
            self.path = 'problem_2'
        else:
            raise ValueError('Unknown benchmark problem, valid inputs are 1,2')
        self.capacity, self.demand, self.distance_matrix, self.transportation_cost = self.__load_data()
        if self.distance_matrix.shape[0] != self.distance_matrix.shape[1]:
            raise AssertionError('Distance matrix is not quadratic.')
        if self.distance_matrix.shape[0] != self.demand.shape[0]+1:
            raise AssertionError('Number of customers is not consistent.')
        if self.capacity.shape[0] != self.transportation_cost.shape[0]:
            raise AssertionError('Number of vehicles is not consistent.')
        if np.sum(self.capacity) < np.sum(self.demand):
            raise AssertionError('Insufficient capacity')

        if selection == 'all':
            self.selected_vehicles = self.__get_vehicles(criterion, objective)
        elif selection == 'sufficient':
            self.selected_vehicles = self.__get_sufficient_vehicles(criterion, objective)
        else:
            raise ValueError('Unknown selection method.')
        self.selected_capacity = self.capacity[self.selected_vehicles]
        self.selected_transportation_cost = self.transportation_cost[self.selected_vehicles]

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
        for vehicle_count, vehicle_solution in enumerate(solution):
            distances = self.distance_matrix[vehicle_solution[0:-1], vehicle_solution[1:]]
            costs = distances * self.selected_transportation_cost[vehicle_count]
            score += np.sum(costs)
        return score

    def get_size(self):
        return self.distance_matrix.shape[0]

    def __get_sufficient_vehicles(self, criterion: str, objective: str) -> np.array:
        vehicle_index = self.__get_vehicles(criterion, objective)
        cum_capacity = np.cumsum(self.capacity[vehicle_index])
        sufficient_vehicle_index = cum_capacity < np.sum(self.demand)
        count = np.sum(sufficient_vehicle_index)
        sufficient_vehicle_index[count] = True
        return vehicle_index[sufficient_vehicle_index]

    def __get_vehicles(self, criterion: str, objective: str) -> np.array:
        return self.__sort_vehicles(np.arange(self.capacity.shape[0]), criterion, objective)

    def __sort_vehicles(self, vehicles, criterion: str, objective: str) -> np.array:
        if criterion == 'cost':
            vehicle_index = np.argsort(self.transportation_cost[vehicles])
        elif criterion == 'cost_per_item':
            vehicle_index = np.argsort(self.transportation_cost[vehicles] / self.capacity[vehicles])
        elif criterion == 'capacity':
            vehicle_index = np.argsort(self.capacity[vehicles])
        elif criterion == 'cost_per_item_and_capacity':
            vehicle_index = np.argsort(self.transportation_cost[vehicles] / (self.capacity[vehicles]**2))
        elif criterion == 'random':
            vehicle_index = np.random.permutation(np.arange(0, vehicles.shape[0]))
        elif criterion == 'none':
            vehicle_index = np.arange(vehicles.shape[0])
        else:
            raise ValueError('Unknown optimization!')

        if objective == 'max':
            vehicle_index = np.flip(vehicle_index,axis=0)
        elif criterion != 'none' and criterion != 'random' and objective != 'min':
            raise ValueError('Unknown objective!')
        return vehicle_index
