from abc import ABC, abstractmethod
import numpy as np
from Individual import Individual
from ProblemDefinition import ProblemDefinition


class Mutator(ABC):

    @abstractmethod
    def mutate(self,toMutate:Individual,probDef:ProblemDefinition)->Individual:
        pass

    @abstractmethod
    def dynamicAdaptation(self, progress):
        pass

class SwapMutator(Mutator):

    def mutate(self, toMutate:Individual,probDef:ProblemDefinition):
        """
        randomly swaps
        :param toMutate:
        :return: mutated individual
        """
        #TODO: how many mutation should be performed per function call?
        for i,NodeAssign in enumerate(toMutate.assign):
            #calculate redInd, the indice that should be reduced
            redInd = np.random.choice(np.argwhere(NodeAssign > 0))
            #and incInd the one that should be increased
            incInds = np.argwhere(NodeAssign < probDef.capacity)
            incInds = np.delete(incInds,np.argwhere(incInds == redInd))
            incInd = np.random.choice(incInds)

            toMutate.assign[i,redInd] -= 1
            toMutate.assign[i,incInd] += 1
        return toMutate

    def dynamicAdaptation(self, progress):
        pass