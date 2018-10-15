from abc import ABC, abstractmethod
import numpy as np


class Replacer(ABC):
    @abstractmethod
    def replace(self, newInds, pop):
        pass
    def dynamicAdaptation(self, progress):
        pass

class KeepBestReplacer(Replacer):
    def __init__(self,dynAdapt = True):
        self.dynAdapt = dynAdapt
        self.firstPopSize = 0
        self.targetPopSize = 0
    def replace(self, newInds, pop):
        if self.firstPopSize == 0:
            self.firstPopSize = pop.size
            self.targetPopSize = pop.size
        #Todo: unique ist eig schlecht hier, da fitness Werte und nicht assignments verglichen werden
        unified = np.unique(np.concatenate((newInds, pop)))
        #unified = np.sort(unified)
        size = min(self.targetPopSize, unified.size)
        assert(size == self.targetPopSize)
        unified = np.partition(unified,-size)
        pop = unified[-size::]
        return pop
    def dynamicAdaptation(self, progress):
        if not self.dynAdapt:
            return
        self.targetPopSize = max(5,int(self.firstPopSize * min(1,(1.1 - progress))))

class BottomReplacer(Replacer):
    def __init__(self, includeBest=True, dynAdapt = True):
        self.includeBest = includeBest
        self.dynAdapt = dynAdapt

    def replace(self, newInds, pop):
        """
        replace the worst individuums in pop with newInds
        :param newInds:
        :param pop:
        :return: updated pop
        """

        pop = np.sort(pop)
        pop[0:newInds.size] = newInds
        return pop

    def dynamicAdaptation(self, progress):
        if not self.dynAdapt:
            return
        self.targetPopSize = max(5,int(self.firstPopSize * min(1,(1.1 - progress))))
class PlainReplacer(Replacer):
    def __init__(self,includeBest = False,dynAdapt = True):
        self.includeBest = includeBest
        self.dynAdapt = dynAdapt
        self.firstPopSize = 0
        self.targetPopSize = 0
    def replace(self, newInds, pop):
        if self.firstPopSize == 0:
            self.firstPopSize = pop.size
            self.targetPopSize = pop.size

        if self.includeBest:
            newInds[0] = np.max(pop)
        return newInds[0:min(newInds.size,self.targetPopSize)]

    def dynamicAdaptation(self, progress):
        if not self.dynAdapt:
            return
        self.targetPopSize = max(5, int(self.firstPopSize * min(1, (1.1 - progress))))

class RouletteReplacer(Replacer):
    def __init__(self, includeBest=True, dynAdapt = True):
        self.includeBest = includeBest
        self.dynAdapt = dynAdapt
        self.firstPopSize = 0
        self.targetPopSize = 0

    def replace(self, newInds, pop):
        if self.firstPopSize == 0:
            self.firstPopSize = pop.size
            self.targetPopSize = pop.size

        unified = np.concatenate((newInds,pop))
        #unified = set(unified)
        bestInd = np.max(unified)
        minFitDec = np.min(unified).fitness+bestInd.fitness
        if self.includeBest:

            probs = np.array([0 if x is bestInd else (x.fitness-minFitDec) for x in unified])
        else:
            probs = np.array([(x.fitness-minFitDec) for x in unified])
        probs /= sum(probs)
        pop = np.random.choice(unified,size=self.targetPopSize,replace=False, p=probs)
        if self.includeBest:
            pop[-1] = bestInd
        return pop

    def dynamicAdaptation(self, progress):
        if not self.dynAdapt:
            return
        self.targetPopSize = max(5,int(self.firstPopSize * min(1,(1.1 - progress))))


class deleteAllReplacer(Replacer):

    def replace(self, newInds, pop):
        """
        replace the all individuums in pop with newInds
        :param newInds:
        :param pop:
        :return: updated pop
        """

        return newInds