from abc import ABC, abstractmethod
import numpy as np
class LocalSearcher(ABC):
    @abstractmethod
    def search(self,ind):
        pass

class HillClimber(LocalSearcher):
    def climb(self,ind, firstChoice, nh):
        # currently best solution
        bq = ind.getFitness()
        bSol = ind
        for n in self.getNeighborhood(ind):
            cq = n.getFitness()
            if cq > bq:
                bq = cq
                bSol = n
                if firstChoice:
                    return bSol
        return bSol

    def search(self,ind,firstChoice=false,nh="swap"):
        done = False
        sol = nh
        while not done:
            sol0 = self.climb(sol,firstChoice,nh)
            if sol0 == sol:
                done = True
            sol = sol0
        return sol

    def getNeighborhood(self,ind,nh):
        if nh == "swap":
            return ind.swapNH()
        elif nh == "transpose":
            return ind.transposeNH()
