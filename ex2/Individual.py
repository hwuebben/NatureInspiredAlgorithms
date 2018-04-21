from __future__ import division
import numpy as np
from ProblemDefinition import ProblemDefinition


class Individual:

    def __init__(self, probDef, jobAssignments):
        self.probDef = probDef
        self.jobAssignments = jobAssignments
        self.fitness = self.__calcFitness()

    def __calcFitness(self):
        total_time = np.zeros(self.probDef.nrMachines)
        for ja in self.jobAssignments:
            total_time[ja] += self.probDef.jobRuntimes[ja]
        return (1/np.max(total_time))

    """definitions of neighborhoods"""
    def swapNH(self):
        """the swap neighborhood"""
        nh = []
        for i,s in enumerate(self.jobAssignments):
            solCop = np.copy(self.jobAssignments)
            #swap with right neighbor
            solCop[i] = solCop[(i+1)%solCop.size]
            solCop[(i + 1) % solCop.size] = s
            nh.append(Individual(self.probDef, solCop))
        return nh

    def transpNH(self):
        """the transposition neighborhood"""
        nh = []
        for i,s in enumerate(self.jobAssignments):
            for j in range(i,self.jobAssignments.size):
                solCop = np.copy(self.jobAssignments)
                solCop[i] = solCop[j]
                solCop[j] = s
                nh.append(Individual(solCop))
        return nh

    """
    overwrite compare methods for sorting purposes
    """
    def __eq__(self, other):
        return self.fitness == other.fitness

    def __lt__(self, other):
        return self.fitness < other.fitness

    def __le__(self, other):
        return self.fitness <= other.fitness

    def __gt__(self, other):
        return self.fitness > other.fitness

    def __ge__(self, other):
        return self.fitness >= other.fitness








