from abc import ABC, abstractmethod
import numpy as np
from ProblemDefinition import ProblemDefinition as PD
from Individual import Individual


class Recombiner(ABC):

    @abstractmethod
    def recombine(self, probDef, ind0, ind1):
        """
        perform recombination operation on two individuals constrained by problem definition
        :param probDef:
        :param ind0:
        :param ind1:
        :return: recombinated child
        """
        pass


class CrossoverRecombiner(Recombiner):

    def recombine(self, probDef, ind0, ind1):
        """
        perform Crossover recombination operation on two individuals constrained by problem definition
        :param probDef:
        :param ind0:
        :param ind1:
        :return: recombinated child
        """
        breakPoint = np.random.randint(0, probDef.nrJobs+1)
        if(np.random.rand() >= 0.5):
            newJobAssignment = np.hstack((ind0.jobAssignments[0:breakPoint], ind1.jobAssignments[breakPoint::]))
        else:
            newJobAssignment = np.hstack((ind1.jobAssignments[0:breakPoint], ind0.jobAssignments[breakPoint::]))
        return Individual(probDef, newJobAssignment)


class UniformCrossoverRecombiner(Recombiner):

    def recombine(self, probDef, ind0, ind1):
        """
        perform UniformCrossover recombination operation on two individuals constrained by problem definition
        :param probDef:
        :param ind0:
        :param ind1:
        :return: recombinated child
        """
        mask = np.random.randint(0, 2, probDef.nrJobs)
        newJobAssignment = np.zeros(probDef.nrJobs)
        newJobAssignment[mask == 0] = ind0.jobAssignments[mask == 0]
        newJobAssignment[mask == 1] = ind1.jobAssignments[mask == 1]

        return Individual(probDef, newJobAssignment.astype(np.int32))