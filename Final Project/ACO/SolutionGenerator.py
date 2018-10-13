import numpy as np
from abc import abstractmethod
from ACO.Problem import Problem, PermutationProblem
from ACO.Heuristics import Heuristic
from ACO.Module import Module


class AbstractSolutionGenerator(Module):

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
        #solutions = list()
        #scores = list()
        solutions = np.empty((self.number_of_ants,self.problem.get_size()+1),dtype=int)
        scores = np.empty(self.number_of_ants)
        for i in range(self.number_of_ants):
            solutions[i] = self.construct_single_solution(pheromone_matrix)
            scores[i] = self.problem.get_score(solutions[i])

        sort_index = np.argsort(scores)
        solutions = solutions[sort_index]
        scores = scores[sort_index]

        return solutions, scores

class PermutationSolutionGenerator(AbstractSolutionGenerator):

    def __init__(self, number_of_ants: int, alpha: int, beta: int, heuristic: Heuristic, problem: PermutationProblem):
        """
        Implements the simple distance heuristic solution generation
        :param number_of_ants:
        :param alpha:
        :param beta:
        """
        super().__init__(number_of_ants, problem)
        self.alpha = alpha
        self.beta = beta
        self.heuristic = heuristic
        if (self.heuristic is not None) and (beta != 0):
            etas = self.heuristic.calculate_etas(problem)
            self.nominator = lambda x, y, z: np.power(x[y, z], self.alpha) * np.power(etas[y, z], self.beta)
            self.denominator = lambda x, y, z: np.sum(np.power(x[y, z], self.alpha) * np.power(etas[y, z], self.beta))
        else:
            self.nominator = lambda x, y, z: np.power(x[y, z], self.alpha)
            self.denominator = lambda x, y, z: np.sum(np.power(x[y, z], self.alpha))

    def construct_single_solution(self, pheromone_matrix: np.array):
        """
        Creates a single solution for a permutation based on the pheromone matrix.

        :param pheromone_matrix: the current pheromone matrix
        :return: solution: 1D array with ordered items representing a solution for a permutation problem
        """
        steps = self.problem.get_size()
        selectable_items = np.arange(1, steps, 1)
        #solution = np.array([0])
        #solution = [0]
        solution = np.zeros(steps+1,dtype=int)
        for i,step in enumerate(range(steps-1)):
            # Determine probabilities for next item
            last_item = solution[i]
            p_items = self.nominator(pheromone_matrix, last_item, selectable_items) \
                      / self.denominator(pheromone_matrix, last_item, selectable_items)
            # Choose next item based on probabilities
            next_item = np.random.choice(np.arange(0, selectable_items.shape[0], 1), 1, False, p_items)
            # Add next chosen item to solution and remove it from selectable solutions
            #solution = np.append(solution, selectable_items[next_item])
            #solution.append(selectable_items[next_item])
            solution[i+1] = selectable_items[next_item]
            selectable_items = np.delete(selectable_items, next_item)
        return solution
