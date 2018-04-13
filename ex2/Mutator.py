from abc import ABC, abstractmethod
import numpy as np
from ProblemDefinition import ProblemDefinition as PD
class Mutator(ABC):
    @abstractmethod
    def mutate(self,toMutate):
        pass

class RandomMutator(Mutator):

    def mutate(self, toMutate):
        """
        :param toMutate:
        :return: mutated individual
        """
        toMutate.jobAssignments[np.random.randint(0,PD.nrJobs)] = np.random.randint(0,PD.nrMachines)
        return toMutate

