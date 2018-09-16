from Problem import Problem
from ACO.Evaporator import Evaporator
from ACO.Initializer import AbstractInitializer
from ACO.Intensifier import Intensifier
from ACO.SolutionGenerator import AbstractSolutionGenerator
from ACO.Terminator import Terminator
import numpy as np
import matplotlib.pyplot as plt
import pickle

class Ant_Colony_Optimizer:

    def __init__(self,
                 problem: Problem,
                 initializer: AbstractInitializer,
                 evaporator: Evaporator,
                 intensifier: Intensifier,
                 solution_gen: AbstractSolutionGenerator,
                 terminator: Terminator,
                 num_solutions: int=1,
                 quality_dependence: bool=False,
                 verbose: bool=False):

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
        self.sorted_scores = list()
        self.sorted_solutions = list()
        self.best_score = 0

    def run(self):
        while not any([t.checkTermination(self) for t in self.terminator]):
            # Construct solutions and evaluate solutions
            iteration_solutions, iteration_scores = self.solution_generator.get_solutions(self.pheromone_matrix)
            #TODO: having the result for each iteration is nice, but inefficient (should be optional)
            self.sorted_solutions.append(iteration_solutions)
            self.sorted_scores.append(iteration_scores)
            self.best_score = iteration_scores[0]
            if self.best_score == 0:
                print("score is 0")
            if self.verbose:
                print('Iteration %d - best score: %d' % (self.nrIt, self.best_score))

            # Update pheromone matrix
            self.pheromone_matrix = self.evaporator.evaporate(self.pheromone_matrix)
            for i in range(self.num_solutions):
                if self.quality_dependence:
                    ratio = iteration_scores[0] / iteration_scores[i] # Quality-dependent update ratio
                else:
                    ratio = 1
                self.pheromone_matrix\
                    = self.intensifier.intensify(self.pheromone_matrix, iteration_solutions[i, :], ratio)

            self.nrIt += 1

        return np.array(self.sorted_solutions), np.array(self.sorted_scores)

    def getBestSolScore(self):
        return self.sorted_solutions[-1][0], self.sorted_scores[-1][0]
    def hasSolScore(self):
        return (len(self.sorted_scores) > 0)
    def reset(self):
        for t in self.terminator: t.reset()
        self.solution_generator.reset()
        self.problem.reset()
        self.initializer.reset()

    def pickleStoreBestSol(self,name):

        bestSol, bestScore = self.getBestSolScore()
        toPickle = (self.problem,bestSol, bestScore)
        name = name+".p"
        #print(name)
        #path = folderPath / name
        with open('finalResults\\'+name, 'wb') as f:
            pickle.dump(toPickle, f)
