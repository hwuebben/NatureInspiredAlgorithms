from __future__ import division
import numpy as np
from ProblemDefinition import ProblemDefinition
from abc import ABC, abstractmethod

class IndividualProto(ABC):

    @staticmethod
    @abstractmethod
    def initIndividual(probDef: ProblemDefinition, initType: str):
        """
        this function is called by the initializer with a respective initType
        :param probDef:
        :param initType:
        :return:
        Individual created by respective initType choice
        """
        pass

class Individual(IndividualProto):

    def __init__(self, assign : np.array):
        """

        :param assign:
        """
        self.assign = assign
        self.fitness = self.__calcFitness()

    def __calcFitness(self):
        return 0

    def __calcGraphs(self):
        pass

    def repairInd(self):
        pass

    @staticmethod
    def initIndividual(probDef: ProblemDefinition, initType: str):
        if initType == "random":
            return Individual.calcRandomIndividual(probDef)

    @staticmethod
    def calcRandomIndividual(probDef:ProblemDefinition):
        assign = np.zeros((probDef.nrNodes, probDef.nrVehicles))
        for i in range(assign.shape[0]):
            loads = np.sum(assign, 0)
            capLeft = probDef.capacity - loads
            capLeftInds = np.argwhere(capLeft > 0).flatten()
            for _ in range(probDef.demand[i]):

                randInd = np.random.choice(capLeftInds)
                assign[i,randInd] += 1
                capLeft[randInd] -= 1
                if capLeft[randInd] == 0:
                    capLeftInds = np.delete(capLeftInds,np.argwhere(capLeftInds == randInd))
        return Individual(assign)

    def checkConsistency(self,probDef:ProblemDefinition):
        """
        function for debug purposes, checks whether the individual is a valid solution
        :return:
        """
        assert( ((np.sum(self.assign, 0) - probDef.capacity) <= 0).all() )
        assert( ((np.sum(self.assign, 1) - probDef.demand) >= 0).all() )

    #@staticmethod
    #deprecated, old representation
    # def calcRandomIndividual(probDef:ProblemDefinition):
    #
    #     assign = []
    #     for demand in probDef.demand:
    #         assign.append(np.random.choice(probDef.enumCapacity,demand,False))
    #     randInd = Individual(assign)
    #     return randInd



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








