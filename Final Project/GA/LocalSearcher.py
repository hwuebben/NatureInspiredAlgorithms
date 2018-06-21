from abc import ABC, abstractmethod
import numpy as np


class LocalSearcher(ABC):
    @abstractmethod
    def search(self, ind):
        pass


class HillClimber(LocalSearcher):

    def search(self, ind, firstChoice=False, nh="swap"):
        done = False
        sol = ind
        while not done:
            sol0 = self.__climb(sol, firstChoice, nh)
            if sol0 == sol:
                done = True
            sol = sol0
        return sol

    def __climb(self, ind, firstChoice, nh):
        # currently best solution
        bq = ind.fitness
        bSol = ind
        for n in self.__getNeighborhood(ind, nh):
            cq = n.fitness
            if cq > bq:
                bq = cq
                bSol = n
                if firstChoice:
                    return bSol
        return bSol

    @staticmethod
    def __getNeighborhood(ind, nh):
        if nh == "swap":
            return ind.swapNH()
        elif nh == "transpose":
            return ind.transposeNH()

class Idle(LocalSearcher):

    def search(self, ind):
        return ind
