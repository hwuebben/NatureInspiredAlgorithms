from Problem import *
from Evaporator import *
from Initializer import *
from Intensifier import *
from SolutionGenerator import *
from Terminator import *


class AntColonyOptimizer:
    """
    Main class of the ant colony optimizer
    """

    def __init__(self,
                 problem: VehicleRoutingProblem,
                 initializer: AbstractInitializer,
                 evaporator: Evaporator,
                 intensifier: Intensifier,
                 solution_gen: AbstractSolutionGenerator,
                 terminator: Terminator,
                 num_solutions: int=1,
                 quality_dependence: bool=False,
                 verbose: bool=False):
        """

        :param problem:     the vehicle routing problem to solve
        :param initializer: Initializer object for initializing the pheromon matrix
        :param evaporator:  Evaporation strategy for the pheromone matrix
        :param intensifier: Intensifier strategy for the peromone matrix
        :param solution_gen: Solution Generator strategy
        :param terminator:  One or multiple terminators that act as stop condicitons for the optimization process
        :param num_solutions: the number of solutions to generate
        :param quality_dependence: switching on and off if the intensifier update should be score dependant
        :param verbose:     if true, get updates about the training process each iteration
        """

        self.problem = problem
        self.initializer = initializer
        self.evaporator = evaporator
        self.intensifier = intensifier
        self.solution_generator = solution_gen
        self.terminator = terminator
        self.num_solutions = num_solutions
        self.quality_dependence = quality_dependence
        self.verbose = verbose

        self.pheromone_matrix = self.initializer.initialize(self.problem)

        self.nrIt = 0
        self.scores = list()
        self.solutions = list()
        self.best_solution = None
        self.best_score = -1
        self.iteration_best_score = -1

    def run(self) -> tuple:
        """
        The run function executes the optimization process, utilizing the modules provided in the constructor.
        :return: two numpy arrays: the solutions and their respective scores.
        """
        while not any([t.checkTermination(self) for t in self.terminator]):
            # Construct solutions and evaluate solutions
            iteration_solutions, iteration_scores = self.solution_generator.get_solutions(self.pheromone_matrix)

            self.solutions.append(iteration_solutions)
            self.scores.append(iteration_scores)
            self.iteration_best_score = iteration_scores[0]
            if self.best_score < 0 or self.iteration_best_score < self.best_score:
                self.best_solution = iteration_solutions[0]\
                    .reshape((1, iteration_solutions.shape[1], iteration_solutions.shape[2]))
                self.best_score = self.iteration_best_score
            elif self.best_solution is not None:
                iteration_solutions = np.append(self.best_solution, iteration_solutions, axis=0)
                iteration_scores = np.append([self.best_score], iteration_scores, axis=0)

            if self.verbose:
                print('Iteration %d - best score: %d / all iterations best score %d'
                      % (self.nrIt, self.iteration_best_score, self.best_score))

            # Update pheromone matrix
            self.pheromone_matrix = self.evaporator.evaporate(self.pheromone_matrix)
            for i in range(self.num_solutions):
                if self.quality_dependence:
                    ratio = np.min(iteration_scores) / iteration_scores[i] # Quality-dependent update ratio
                else:
                    ratio = 1
                self.pheromone_matrix\
                    = self.intensifier.intensify(self.pheromone_matrix, iteration_solutions[i, :], ratio)

            self.nrIt += 1

        self.best_solution = self.best_solution.reshape((self.best_solution.shape[1], self.best_solution.shape[2]))

        return np.array(self.solutions), np.array(self.scores)