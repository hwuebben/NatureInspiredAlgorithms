from __future__ import division
import numpy as np

#big ass value
LARGE = 1e99

#TODO: this should be modulized
"""
market types
"""
p = [0.45, 0.25, 0.2]
d = [2e6, 30e6, 20e6]

"""
plant types
"""
k = [50e3, 600e3, 4e6]
c = [10e3, 80e3, 400e3]
m = [100, 50, 3]


class Individual:

    def __init__(self, xMin:np.array, xMax:np.array):
        """

        :param xMin:
        :param xMax:
        x = (e1, e2, e3,s1,s2,s3, p1, p2, p3)
        """
        self.x = np.random.rand(xMin.size) * (xMax-xMin) + xMin
        self.targFuncVal = Individual.targetFunc(self.x)

    @staticmethod
    def targetFunc(x):
        return Individual.revenue(x) - (Individual.prodCost(x) + Individual.purchCost(x))

    @staticmethod
    def cost(e, k, c, m):
        """
        :param e: energy produced
        :param k:kWh per plant
        :param c:cost per plant
        :param m:maximum number of plants that can be used
        :return: cost
        """
        if e <= 0:
            return 0
        if e > k*m:
            return LARGE
        plantsNeeded = np.ceil(e/k)
        return plantsNeeded * c

    @staticmethod
    def prodCost(x):
        prodCost = 0
        for i in range(0,3):
            prodCost += Individual.cost(x[i],k[i],c[i],m[i])
        return prodCost

    @staticmethod
    def purchCost(x):
        return np.max(np.sum(x[3:6]) - np.sum(x[0:4]), 0) * 0.6


    @staticmethod
    def demand(price, maxPrice, maxDemand):
        if price > maxPrice:
            return 0
        if price <= 0:
            return maxDemand
        demand = maxDemand - price**2 * maxDemand / maxPrice**2
        return demand

    @staticmethod
    def revenue(x):
        revenue = 0
        for i in range(1,4):
            demand = Individual.demand(x[-i],p[i-1],d[i-1])
            revenue += np.minimum(demand, x[-(i+3)]) * x[-i]
        return revenue



    """
    overwrite compare methods for sorting purposes
    """
    def __eq__(self, other):
        return self.targFuncVal == other.targFuncVal

    def __lt__(self, other):
        return self.targFuncVal < other.targFuncVal

    def __le__(self, other):
        return self.targFuncVal <= other.targFuncVal

    def __gt__(self, other):
        return self.targFuncVal > other.targFuncVal

    def __ge__(self, other):
        return self.targFuncVal >= other.targFuncVal








