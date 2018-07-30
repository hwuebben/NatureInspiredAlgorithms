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
        minFitDec = np.min(unified).fitness-1
        if self.includeBest:
            bestInd = np.max(unified)
            probs = [0 if x is bestInd else (x.fitness-minFitDec) for x in unified]
        else:
            probs = [(x.fitness-minFitDec) for x in unified]
        probs /= sum(probs)
        pop = np.random.choice(unified,size=self.targetPopSize,replace=False, p=probs)
        if self.includeBest:
            pop[-1] = bestInd
        return np.array(pop)

    def dynamicAdaptation(self, progress):
        if not self.dynAdapt:
            return
        self.targetPopSize = max(10, int(self.firstPopSize * min(1,(1.1 - progress))))


class deleteAllReplacer(Replacer):

    def replace(self, newInds, pop):
        """
        replace the all individuums in pop with newInds
        :param newInds:
        :param pop:
        :return: updated pop
        """

        return newInds