from abc import ABC, abstractmethod
import numpy as np
from ProblemDefinition import ProblemDefinition as PD
class Mutator(ABC):
    @abstractmethod
    def mutate(self,toMutate):
        pass
    def simAnnealing(self,progress):
        pass

class RandomMutator(Mutator):
    def __init__(self,mutationRate=0.5):
        self.mutationRate = mutationRate

    def mutate(self, toMutate):
        """
        randomly mutate alleles
        :param toMutate:
        :return: mutated individual
        """
        mutPos = np.random.choice([True,False],size =toMutate.jobAssignments.size,p=[self.mutationRate,1-self.mutationRate])
        toMutate.jobAssignments[mutPos] = np.random.randint(0,PD.nrMachines,toMutate.jobAssignments[mutPos].size)
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


