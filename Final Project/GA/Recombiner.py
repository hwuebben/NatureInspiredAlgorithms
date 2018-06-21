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
    def recombine(self, probDef: ProblemDefinition, ind0: Individual, ind1: Individual):
        newAssign = (ind0.assign + ind1.assign) / 2
        # change all fraction assignments to even ones
        fracInds = np.argwhere(newAssign % 1 != 0)
        decFracInds = fracInds[np.random.choice(np.arange(fracInds.shape[0]), fracInds.shape[0] / 2, False)]
        newAssign[decFracInds] -= 0.5
        newAssign = np.ceil(newAssign)

        return Individual(newAssign)
