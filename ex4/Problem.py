from Individual import *
import numpy as np

# prohibitively large value
LARGE = 1e99

class Problem:
    def __init__(self, problem_nr):
        # plant types
        # k:kWh per plant
        # c:cost per plant
        # m:maximum number of plants that can be used
        self.k = [50e3, 600e3, 4e6]
        self.c = [10e3, 80e3, 400e3]
        self.m = [100, 50, 3]

        if (problem_nr == 1):
            # market types
            self.mp = [0.45, 0.25, 0.2]
            self.md = [2e6, 30e6, 20e6]
            # purchase cost price
            self.costPrice = 0.6

        elif (problem_nr == 2):
            # market types
            self.mp = [0.45, 0.25, 0.2]
            self.md = [2e6, 30e6, 20e6]
            # purchase cost price
            self.costPrice = 0.1

        elif (problem_nr == 3):
            # market types
            self.mp = [0.5, 0.3, 0.1]
            self.md = [1e6, 5e6, 5e6]
            # purchase cost price
            self.costPrice = 0.6
        else:
            raise ValueError("Problem number not valid.")

    def targetFunc(self, x) -> float:
        """
        :param x: genome vector
        :return: profit
        """
        e, s, p = x[0:3], x[3:6], x[6:]
        return self.__revenue(s, p) - (self.__prodCost(e) + self.__purchCost(e, s))

    def __prodCost(self, e) -> float:
        """
        :param e: energy produced
        :return: production cost
        """
        plantsNeeded = np.ceil(e / self.k)
        plantsNeeded = np.where(e < 0, np.zeros_like(e), plantsNeeded)
        plantsNeeded = np.where(e > np.dot(self.k, self.m), np.full_like(e, LARGE), plantsNeeded)

        return np.dot(plantsNeeded, self.c)

    def __purchCost(self, e, s) -> float:
        """
        :param e: energy produced
        :param s: energy sold
        :return: purchase cost
        """
        return max(np.sum(s) - np.sum(e), 0) * self.costPrice

    def __demand(self, price, maxPrice, maxDemand) -> float:
        """
        :param price: actual sales prices
        :param maxPrice: maximum price of market type accepted by customers
        :param maxDemand: maximum demand of market type
        :return: resulting demand
        """
        if price > maxPrice:
            return 0
        if price <= 0:
            return maxDemand
        demand = maxDemand - price**2 * maxDemand / maxPrice**2
        return demand

    def __revenue(self, s, p) -> float:
        """
        :param s: energy sold
        :param p: actual prices
        :return: purchase cost
        """
        revenue = 0
        for i in range(len(self.mp)):
            demand = self.__demand(p[i], self.mp[i], self.md[i])
            revenue += np.minimum(demand, s[i]) * p[i]
        return revenue

    @staticmethod
    def validate(individual: Individual) -> bool:
        """
        :param individual: individual solution
        :return: validation result
        """
        e =  individual.x[0:3]
        return (np.min(individual.x) >= 0)