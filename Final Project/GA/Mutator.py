from abc import ABC, abstractmethod
import numpy as np
from Individual import Individual
from ProblemDefinition import ProblemDefinition


class Mutator(ABC):

    @abstractmethod
    def mutate(self,toMutate:Individual,probDef:ProblemDefinition)->Individual:
        pass

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
        #calculate currently delivered goods (loads) per vehicle
        loads = np.sum(toMutate.assign, 0)
        for i,NodeAssign in enumerate(toMutate.assign):
            #calculate redInd, the indice that should be reduced
            redInd = np.random.choice(np.argwhere(NodeAssign > 0).flatten())
            #and incInd the one that should be increased
            incInds = np.argwhere(loads < probDef.capacity).flatten()
            #make sure not to choose the same index as redInd (would do nothing then)
            #leaving this line out allows strength of mutation to vary randomly, might not be bad
            #incInds = np.delete(incInds,np.argwhere(incInds == redInd))
            incInd = np.random.choice(incInds)

            toMutate.assign[i,redInd] -= 1
            toMutate.assign[i,incInd] += 1
            loads[redInd] -= 1
            loads[incInd] += 1
        #toMutate.checkConsistency(probDef)
        return toMutate


class assignMutator(Mutator):
    def __init__(self,remProb:float = 0.5):
        """
        set remProb
        :param remProb:
        """
        self.remProb = remProb
    def mutate(self,toMutate:Individual,probDef:ProblemDefinition):
        """
        remove vehicle from node with prob remProb
        add vehicle to node with prob 1-remProb
        :param toMutate:
        :param probDef:
        :return:
        """
        shallRem = np.random.rand() <= self.remProb
        #TODO: implement