from abc import ABC, abstractmethod
import numpy as np
class LocalSearcher(ABC):
    @abstractmethod
    def search(self,ind):
        pass

class HillClimber(LocalSearcher):
    def search(self,ind, firstChoice):
        # currently best solution
        bq = ind.getFitness()
        bSol = ind
        for n in ind.swapNH():
            cq = n.getFitness()
            if cq > bq:
                bq = cq
                bSol = n
                if firstChoice:
                    return bSol
        return bSol
