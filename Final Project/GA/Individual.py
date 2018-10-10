from __future__ import division
import numpy as np
from GA.ProblemDefinition import ProblemDefinition as PD
from abc import ABC, abstractmethod
import Heuristic

class IndividualProto(ABC):

    # @classmethod
    # @abstractmethod
    # def copyConstructor(cls,individual):
    #     pass


    @classmethod
    @abstractmethod
    def initIndividual(probDef: PD, initType: str):
        """
        this function is called by the initializer with a respective initType
        :param probDef:
        :param initType:
        :return:
        Individual created by respective initType choice
        """
        pass

class Individual(IndividualProto):
    def __init__(self, assign : np.array, probDef):
        """

        :param assign:
        """
        self.assign = assign
        self.probDef = probDef
        self.fitness = self.__calcFitness()
        # self.checkConsistency(PD.probDef)

    def __calcFitness(self):
        heuristic =  Heuristic.BeardwoodHeuristic()
        #heuristic = Heuristic.AcoHeuristic()
        return heuristic.calcHeuVal(self,self.probDef)
    def recalcFitness(self):
        self.fitness = self.__calcFitness()

    def extractDistMatrix(self,vehicleInd):
        graphInds = np.nonzero(self.assign[:,vehicleInd] > 0)[0]
        #all node indices in graph need to be incremented because the 0 node is not in the representation
        np.add(graphInds,1,graphInds)
        #the 0 node must then be added, creates copy :(
        graphInds = np.insert(graphInds,0,0)
        #get respective slice of distance matrix
        return self.probDef.distance[graphInds][:,graphInds]

    def extractDistMatrices(self):
        distMatrices = []
        for vehicleInd in range(self.probDef.nrVehicles):
            distMatrices.append(self.extractDistMatrix(vehicleInd))
        return distMatrices


    @classmethod
    def initIndividual(cls,probDef: PD, initType: str):
        if initType == "random":
            return cls.calcRandomIndividual(probDef)
        elif initType == "heuristic":
            return cls.calcHeuristicIndividual(probDef)

    @classmethod
    def calcRandomIndividual(cls,probDef:PD):
        assign = np.zeros((probDef.nrNodes, probDef.nrVehicles))
        for i in range(assign.shape[0]):
            loads = np.sum(assign, 0)
            capLeft = probDef.capacity - loads
            #capLeftInds = np.argwhere(capLeft > 0).flatten()
            capLeftInds = np.nonzero(capLeft > 0)[0]

            for _ in range(probDef.demand[i]):

                randInd = np.random.choice(capLeftInds)
                assign[i,randInd] += 1
                capLeft[randInd] -= 1
                if capLeft[randInd] == 0:
                    capLeftInds = np.delete(capLeftInds,np.argwhere(capLeftInds == randInd))
        return cls(assign,probDef)

    @classmethod
    def calcHeuristicIndividual(cls,probDef:PD):
        assign = np.zeros((probDef.nrNodes, probDef.nrVehicles))
        distsOverall = np.copy(probDef.distance)
        demands = np.copy(probDef.demand)
        capacities = np.copy(probDef.capacity)
        # vehicleInds = np.argsort(probDef.transCost)
        vehicleInds = np.arange(probDef.nrVehicles)
        pickProbs = 1 - (probDef.transCost / np.sum(probDef.transCost))
        if probDef.nrVehicles == 1:
            pickProbs[0] = 1
        pickProbs /= np.sum(pickProbs)
        # i = 0
        while np.sum(demands) > 0:
            "copy distsOverall matrix to keep track of which nodes are visited by this vehicle"
            dists = np.copy(distsOverall)
            "choose vehicle (always choose from the cheapest ones)"
            vehicleInd = np.random.choice(vehicleInds,None,True,pickProbs)
            pickProbs[vehicleInd] = 0
            pickProbs /= np.sum(pickProbs)
            # i+=1
            "assign nodes to vehicle until capacity is full"
            currentNode = 0
            while capacities[vehicleInd] > 0 and np.sum(demands) > 0:
                "set distances of self to inf to not visit again"
                dists[:,currentNode] = np.inf
                "use simple heuristic to choose nodes (probabilistic choice anti proportional to distance)"
                # currentNode = np.argmin(dists[currentNode])
                pickProbsNode = 1 - dists[currentNode] / np.sum(dists[currentNode][np.isfinite(dists[currentNode])])
                #if dists[currentNode] has only one finite value it needs to be set from zero to 1
                if pickProbsNode[pickProbsNode == 0].size == 1:
                    pickProbsNode[pickProbsNode == 0] = 1
                pickProbsNode[np.isinf(pickProbsNode)] = 0
                pickProbsNode /= np.sum(pickProbsNode)

                currentNode = np.random.choice(np.arange(dists[currentNode].size),None,True,pickProbsNode)
                delivery = min(demands[currentNode-1], capacities[vehicleInd])
                demands[currentNode-1] -= delivery
                capacities[vehicleInd] -= delivery
                assign[currentNode-1,vehicleInd] = delivery
                if demands[currentNode-1] == 0:
                    distsOverall[:,currentNode] = np.inf
        return cls(assign,probDef)


    def checkConsistency(self,probDef:PD, strict=True):
        """
        function for debug purposes, checks whether the individual is a valid solution
        :return:
        """
        assert( ((np.sum(self.assign, 0) - probDef.capacity) <= 0).all() )
        if strict:
            assert (((np.sum(self.assign, 1) - probDef.demand) == 0).all())
        else:
            assert( ((np.sum(self.assign, 1) - probDef.demand) >= 0).all() )

    # @classmethod
    # def copyConstructor(cls,individual):
    #     return cls(individual.assign)


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








