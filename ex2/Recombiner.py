from abc import ABC, abstractmethod
import numpy as np
from ProblemDefinition import ProblemDefinition as PD
from Individual import Individual

class Recombiner(ABC):
    @abstractmethod
    def recombine(self,ind0,ind1):
        pass

class CrossoverRecombiner(Recombiner):
    def recombine(self,ind0,ind1):
        """
        perform recombination operation
        :param ind0:
        :param ind1:
        :return: recombiated child
        """
        breakPoint = np.random.randint(0,PD.nrJobs+1)
        if(np.random.rand() >= 0.5):
            newJobAssignment = np.hstack((ind0.jobAssignments[0:breakPoint],ind1.jobAssignments[breakPoint::]))
        else:
            newJobAssignment = np.hstack((ind1.jobAssignments[0:breakPoint],ind0.jobAssignments[breakPoint::]))
        return Individual(newJobAssignment)
