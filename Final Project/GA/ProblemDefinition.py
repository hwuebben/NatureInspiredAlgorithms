import numpy as np
class ProblemDefinition:

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

        #enumCapacity contains entries for each vehicle (in the number of their capacities)
        # self.enumCapacity = []
        # for vehicle,cap in enumerate(capacity):
        #     self.enumCapacity.extend([vehicle]*cap)
        # self.enumCapacity = np.array(self.enumCapacity)


