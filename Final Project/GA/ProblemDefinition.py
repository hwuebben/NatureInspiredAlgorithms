import numpy as np
class ProblemDefinition:
    #static reference to self so not ever individual need ProblemDefinition instance
    #maybe a Singleton would be better
    probDef = None
    def __init__(self, capacity,demand,distance,transCost):
        """

        :param capacity:
        :param demand:
        :param distance:
        :param transCost:
        """

        self.capacity = capacity
        self.demand = demand
        self.distance = distance
        self.transCost = transCost

        self.nrNodes = self.demand.size
        self.nrVehicles = self.capacity.size
        self.problemSize = self.nrNodes*self.nrVehicles

        #enumCapacity contains entries for each vehicle (in the number of their capacities)
        # self.enumCapacity = []
        # for vehicle,cap in enumerate(capacity):
        #     self.enumCapacity.extend([vehicle]*cap)
        # self.enumCapacity = np.array(self.enumCapacity)

        ProblemDefinition.probDef = self


