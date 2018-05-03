import numpy as np

class Ant_Colony_Optimizer:

    def __init__(self, initializer, evaporator, intensifier, solution_generator, terminator):

        self.initializer = initializer
        self.evaporator = evaporator
        self.intensifier = intensifier
        self.solution_generator = solution_generator
        self.terminator = terminator

        self.pheromone_matrix = self.initializer.initialize()


    def run(self):
        pass