import numpy as np
from ex3.Evaporator import *
from ex3.Initializer import *
from ex3.Intensifier import *
from ex3.ReadProblem import TSP_Problem
from ex3.SolutionGenerator import *
from ex3.Terminator import *

class Ant_Colony_Optimizer:

    def __init__(self,
                 problem: TSP_Problem,
                 initializer: AbstractInitializer,
                 evaporator: Evaporator,
                 intensifier: Intensifier,
                 solution_gen: AbstractSolutionGenerator,
                 terminator: Terminator):

        self.problem = problem
        self.initializer = initializer
        self.evaporator = evaporator
        self.intensifier = intensifier
        self.solution_generator = solution_gen
        self.terminator = terminator

        self.pheromone_matrix = self.initializer.initialize()


    def run(self):
        while not self.terminator.checkTermination(self):
            best_solution, best_score = self.solution_generator.get_solution(self.pheromone_matrix, self.problem.get_distance_matrix())
            self.pheromone_matrix = Evaporator.evaporate(self.pheromone_matrix)
            self.pheromone_matrix = self.intensifier.intensify(self.pheromone_matrix, best_solution)
        return best_score