import numpy as np
from ProblemDefinition import ProblemDefinition
class Individual:


    def __init__(self,jobAssignments):
        self.jobAssignments = jobAssignments
        self.fitness = self.calcFitness()

    def calcFitness(self):
        counts = np.zeros(ProblemDefinition.jobRuntimes.size)
        for ja in self.jobAssignments:
            counts[ja] += ProblemDefinition.jobRuntimes[ja]
        return np.max(counts)

    def getFitness(self):
        return self.fitness






