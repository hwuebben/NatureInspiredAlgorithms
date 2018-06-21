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
        for i, nodeAssign in enumerate(assign):
            capLeft = probDef.capacity - assign[i]
            capLeftInd = np.argwhere(capLeft > 0).flatten()
            for _ in range(probDef.demand[i]):

                randInd = np.random.choice(capLeftInd)
                assign[i,randInd] += 1
                capLeft[randInd] -= 1
                if capLeft[randInd] == 0:
                    capLeftInd = np.delete(capLeftInd,np.argwhere(capLeftInd == randInd))
        return Individual(assign)



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








