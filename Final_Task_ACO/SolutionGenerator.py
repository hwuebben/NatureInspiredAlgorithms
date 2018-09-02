import numpy as np
from abc import ABC, abstractmethod
from Problem import *
from Heuristics import Heuristic


class AbstractSolutionGenerator(ABC):

    def __init__(self, number_of_ants: int, problem: Problem):
        self.number_of_ants = number_of_ants
        self.problem = problem

    @abstractmethod
    def construct_single_solution(self, pheromone_matrix: np.array) -> np.array:
        """
        Creates a single solution based on the pheromone matrix.

        :param pheromone_matrix: the current pheromone matrix
        :return: solution: 1D array with ordered items representing a solution
        """
        pass

    def get_solutions(self, pheromone_matrix: np.array):
        """
        Create solutions corresponding to the number of ants and returns them in descent order by their score
        :param pheromone_matrix: the pheromon values for each decision
        :return: solutions: number of ants x size of solution array containing all ants' solutions ordered by score
        """
        solutions = list()
        scores = list()

        for ant in range(self.number_of_ants):
            solution = self.construct_single_solution(pheromone_matrix)
            solutions.append(solution)
            scores.append(self.problem.get_score(solution))
        sort_index = np.argsort(scores)
        solutions = np.array(solutions)[sort_index]
        scores = np.array(scores)[sort_index]

        return solutions, scores


class PermutationSolutionGenerator(AbstractSolutionGenerator):

    def __init__(self, number_of_ants: int, alpha: int, beta: int, heuristic: Heuristic,
                 problem: VehicleRoutingProblem, parallel: bool):
        """
        Implements the simple distance heuristic solution generation
        :param number_of_ants:
        :param alpha:
        :param beta:
        """
        super().__init__(number_of_ants, problem)
        self.alpha = alpha
        self.beta = beta
        self.parallel = parallel
        if (heuristic is not None) and (beta != 0):
            etas = heuristic.calculate_etas(problem)
            self.nominator = lambda x, y, z: np.power(x[y, z], self.alpha) * np.power(etas[y, z], self.beta)
            self.denominator = lambda x, y, z: np.sum(np.power(x[y, z], self.alpha) * np.power(etas[y, z], self.beta))
        else:
            self.nominator = lambda x, y, z: np.power(x[y, z], self.alpha)
            self.denominator = lambda x, y, z: np.sum(np.power(x[y, z], self.alpha))

    def construct_single_solution(self, pheromone_matrix: np.array):
        """
        Creates a single solution for a permutation based on the pheromone matrix.

        :param pheromone_matrix: the current pheromone matrix
        :return: solution: list with ordered items representing a solution for a permutation problem
        """
        vehicles = self.problem.selected_vehicles.shape[0]
        vehicle_solutions = np.zeros(shape=(vehicles, self.problem.get_size()), dtype=np.int)
        remaining_demand = np.array(self.problem.demand)
        solution = list()

        if self.parallel:
            remaining_capacity = np.array(self.problem.selected_capacity)
            selectable_items = np.arange(1, self.problem.get_size(), 1)
            step = 1
            while selectable_items.shape[0] > 0:
                for vehicle in range(vehicles):
                    if remaining_capacity[vehicle] > 0 and selectable_items.shape[0] > 0:
                        # Determine probabilities for next item
                        last_item = vehicle_solutions[vehicle, step - 1]
                        p_items = self.nominator(pheromone_matrix[vehicle], last_item, selectable_items) \
                                  / self.denominator(pheromone_matrix[vehicle], last_item, selectable_items)
                        # Choose next customer based on probabilities
                        customer = np.random.choice(selectable_items, 1, False, p_items) - 1
                        # Add next chosen item to solution and remove it from selectable solutions
                        vehicle_solutions[vehicle, step] = customer + 1
                        delivery_quantity = min(remaining_capacity[vehicle], remaining_demand[customer])
                        remaining_capacity[vehicle] -= delivery_quantity
                        remaining_demand[customer] -= delivery_quantity
                    selectable_items = np.arange(1, self.problem.get_size(), 1)[remaining_demand > 0] #TODO: avoid redundancy
                step += 1

        else:
            for vehicle in range(vehicles):
                remaining_capacity = self.problem.selected_capacity[vehicle]
                selectable_items = np.arange(1, self.problem.get_size(), 1)[remaining_demand > 0]
                steps = selectable_items.shape[0]
                for step in range(1, steps):
                    # Determine probabilities for next item
                    last_item = vehicle_solutions[vehicle, step - 1]
                    p_items = self.nominator(pheromone_matrix[vehicle], last_item, selectable_items) \
                              / self.denominator(pheromone_matrix[vehicle], last_item, selectable_items)
                    # Choose next customer based on probabilities
                    customer = np.random.choice(selectable_items, 1, False, p_items) - 1
                    # Add next chosen item to solution and remove it from selectable solutions
                    vehicle_solutions[vehicle, step] = customer + 1
                    delivery_quantity = min(remaining_capacity, remaining_demand[customer])
                    remaining_capacity -= delivery_quantity
                    remaining_demand[customer] -= delivery_quantity
                    if remaining_capacity == 0:
                        break
                    selectable_items = np.arange(1, self.problem.get_size(), 1)[remaining_demand > 0] #TODO: avoid redundancy

        for vehicle in range(vehicle_solutions.shape[0]):
            solution.append(vehicle_solutions[vehicle])

        return solution
