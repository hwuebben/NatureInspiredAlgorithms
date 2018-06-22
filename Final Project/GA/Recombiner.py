from __future__ import division
from abc import ABC, abstractmethod
import numpy as np
from ProblemDefinition import ProblemDefinition
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


class MeanRecombiner(Recombiner):
    def __init__(self):
        #epsilon is used to check whether number is a fraction
        self.epsilon = 1e-5

    def recombine(self, probDef: ProblemDefinition, ind0: Individual, ind1: Individual):


        # change all fraction assignments to even ones (is this necessary?)
        # create a mask that is added on newAssign
        # mask needs the same amount of +0.5 and -0.5 values in each column and row
        # or:
        # round up all fractions, where capacity constraint is violated reduce prior fractions if demand is overfullfilled:
        newAssign = ind0.assign + ind1.assign
        np.divide(newAssign,2.,newAssign)
        np.ceil(newAssign,newAssign)
        #this procedure could potentially break the cap limits of vehicles, therefore repair
        #identify broken Caps
        brokenCaps = np.sum(newAssign, 0) - probDef.capacity
        brokenCapInds = np.argwhere(brokenCaps > 0)
        #iterate over broken caps
        for brokenCapInd in brokenCapInds:
            #iterate over all nodes
            for j in range(newAssign[:,brokenCapInd].size):
                #check whether node has a surplus
                assigned = np.sum(newAssign[j,:])
                hasSurplus = (assigned - probDef.demand[j]) > 0
                #if so relieve brokenCap
                if hasSurplus:
                    newAssign[j,brokenCapInd] -= 1
                    brokenCaps[brokenCapInd] -= 1
                    if brokenCaps[brokenCapInd] == 0:
                        break




        # or do integer division, then fix demands:
        # newAssign = np.ceil((ind0.assign + ind1.assign) // 2)
        # deficits = probDef.demand - np.sum(newAssign,0)
        # defInds = np.argwhere(deficits > 0)
        # openCaps = probDef.capacity - np.sum(newAssign, 1)
        # openCapInds = np.argwhere(openCaps > 0)
        #iterate over nodes that have deficits
        # for i,defInd in enumerate(defInds):
        #     #indices of the vehicles that visit that node
        #     visInds = np.argwhere(newAssign[defInd] > 0)
        #     #increase supply as calculated in deficits, always choose the vehicle with the highest openCap
        #     for _ in deficits[i]:
        #
        #         assign = newAssign[defInd]

        newInd = Individual(newAssign)
        #DEBUG:
        newInd.checkConsistency(probDef)
        return newInd
