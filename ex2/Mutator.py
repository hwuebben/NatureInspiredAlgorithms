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
        rnadomly shuffles the elements

        :param toMutate:
        :return: mutated individual
        """
        toMutate.jobAssignments[np.random.randint(0,PD.nrJobs)] = np.random.randint(0,PD.nrMachines)
        return toMutate

class BoundaryMutator(Mutator):

    def mutate(self, toMutate):
        """
        Randomly sets indivuals to the upper and lower boundary values of the array

        :param toMutate:
        :return: mutated individual
        """
        mask = np.random.randint(0,3,toMutate.jobAssignments.shape,np.int32)
        max = toMutate.jobAssignments.max()
        min = toMutate.jobAssignments.min()
        toMutate.jobAssignments[mask == 0] = min
        toMutate.jobAssignments[mask == 2] = max
        return toMutate


