from abc import ABC, abstractmethod
import numpy as np


class Replacer(ABC):
    @abstractmethod
    def replace(self, newInds, pop):
        pass
    def dynamicAdaptation(self, progress):
        pass

class KeepBestReplacer(Replacer):
    def replace(self, newInds, pop):
        unified = np.concatenate((newInds, pop))
        unified = np.sort(unified)
        pop = unified[-pop.size::]
        return pop


class BottomReplacer(Replacer):

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
class PlainReplacer(Replacer):
    def __init__(self,keepMax = False):
        self.keepMax = keepMax
    def replace(self, newInds, pop):
        if self.keepMax:
            newInds[np.argmin(newInds)] = np.max(pop)
        return newInds

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