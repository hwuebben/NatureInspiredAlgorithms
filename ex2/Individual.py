from __future__ import division
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
        return (1/np.max(counts))

    def getFitness(self):
        return self.fitness

    """definitions of neighborhoods"""
    def swapNH(self):
        """the swap neighborhood"""
        nh = []
        for i,s in enumerate(self.jobAssignments):
            solCop = np.copy(self.jobAssignments)
            #swap with right neighbor
            solCop[i] = solCop[(i+1)%solCop.size]
            solCop[(i + 1) % solCop.size] = s
            nh.append(solCop)
        return nh

    def transpNH(self):
        """the transposition neighborhood"""
        nh = []
        for i,s in enumerate(self.jobAssignments):
            for j in range(i,self.jobAssignments.size):
                solCop = np.copy(self.jobAssignments)
                solCop[i] = solCop[j]
                solCop[j] = s
                nh.append(solCop)
        return nh
    """
    overwrite compare methods for sorting purposes
    """
    def __eq__(self, other):
        return self.getFitness() == other.getFitness()
    def __lt__(self, other):
        return self.getFitness() < other.getFitness()
    def __le__(self, other):
        return self.getFitness() <= other.getFitness()
    def __gt__(self, other):
        return self.getFitness() > other.getFitness()
    def __ge__(self, other):
        return self.getFitness() >= other.getFitness()








