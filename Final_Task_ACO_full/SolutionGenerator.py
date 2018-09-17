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

    def get_solutions(self, pheromone_matrix: np.array) -> np.array:
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


class VRPSolutionGenerator(AbstractSolutionGenerator):

    def __init__(self, number_of_ants: int, alpha: int, beta: int, heuristic: Heuristic, problem: VehicleRoutingProblem):
        """
        Implements the simple distance heuristic solution generation
        :param number_of_ants:
        :param alpha:
        :param beta:
        """
        super().__init__(number_of_ants, problem)
        self.alpha = alpha
        self.beta = beta

        # Provide initial selectable start = deposit / vehicle and items = customers and empty vehicle solutions
        vehicles = self.problem.vehicles
        items = problem.get_size()
        pheromone_matrix_size = 1 + vehicles * items
        self.initial_selectable_start_items = np.arange(1, pheromone_matrix_size, items)
        self.initial_selectable_vehicle_items = list()
        self.initial_vehicle_solutions = np.zeros(shape=(vehicles, 1 + items), dtype=np.int)
        for vehicle in range(self.problem.vehicles):
            start_index = vehicle * self.problem.get_size() + 2
            end_index = start_index + self.problem.get_size() - 1
            self.initial_selectable_vehicle_items.append(np.arange(start_index, end_index, 1))
            self.initial_vehicle_solutions[vehicle, :] += start_index - 1

        # Helper function for probability determination
        if (heuristic is not None) and (beta != 0):
            etas = heuristic.calculate_etas(problem)
            self.nominator = lambda x, y, z: np.power(x[y, z], self.alpha) * np.power(etas[y, z], self.beta)
        else:
            self.nominator = lambda x, y, z: np.power(x[y, z], self.alpha)

    def construct_single_solution(self, pheromone_matrix: np.array) -> list:
        """
        Creates a single solution for a permutation based on the pheromone matrix.

        :param pheromone_matrix: the current pheromone matrix
        :return: solution: list with ordered items representing a solution for a permutation problem
        """
        remaining_demand = np.array(self.problem.demand)
        remaining_capacity = np.array(self.problem.capacity)

        vehicle_solutions = np.array(self.initial_vehicle_solutions)
        selectable_start_items = np.array(self.initial_selectable_start_items)
        selectable_vehicle_items = np.array(self.initial_selectable_vehicle_items)

        solution = list()

        next_item = 0
        while np.sum(remaining_capacity) > 0 and np.sum(remaining_demand) > 0:
            last_item = next_item
            # Determine probabilities for next start item = deposit / vehicle
            p_nominator = self.nominator(pheromone_matrix, last_item, selectable_start_items)
            p_items = p_nominator / np.sum(p_nominator)
            # Choose next start item based on probabilities
            next_item = int(np.random.choice(selectable_start_items, 1, False, p_items))
            selectable_start_items = selectable_start_items[selectable_start_items != next_item]

            vehicle = (next_item - 1) // self.problem.get_size()
            vehicle_solutions[vehicle, 0:2] = [last_item, next_item]
            step = 2
            while remaining_capacity[vehicle] > 0 and np.sum(remaining_demand > 0):
                last_item = next_item
                selectable_items = selectable_vehicle_items[vehicle]
                customers = (selectable_items - 1) % self.problem.get_size() - 1
                selectable_items = selectable_items[remaining_demand[customers] > 0]
                # Determine probabilities for next item = customer
                p_nominator = self.nominator(pheromone_matrix, last_item, selectable_items)
                p_items = p_nominator / np.sum(p_nominator)
                # Choose next item based on probabilities
                next_item = int(np.random.choice(selectable_items, 1, False, p_items)[0])
                customer = (next_item - 1) % self.problem.get_size() - 1
                vehicle_solutions[vehicle, step] = next_item
                # Heuristic: always serve full demand if there is remaining load
                delivery_quantity = min(remaining_capacity[vehicle], remaining_demand[customer])
                remaining_capacity[vehicle] -= delivery_quantity
                remaining_demand[customer] -= delivery_quantity
                step += 1

        for vehicle in range(self.problem.vehicles):
            solution.append(vehicle_solutions[vehicle])

        return solution
