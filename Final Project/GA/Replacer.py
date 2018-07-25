from abc import ABC, abstractmethod
import numpy as np


class Replacer(ABC):
    @abstractmethod
    def replace(self, newInds, pop):
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
    def replace(self, newInds, pop):
        unified = np.concatenate((newInds,pop))
        # unified = np.empty(newInds.size + pop.size)
        # unified[0:newInds.size] = newInds
        # unified[newInds.size::] = pop
        probs = [x.fitness for x in unified]
        #if fitness values are negative, make positive
        minProb = min(probs)
        if minProb < 0:
            probs -= minProb
        probs /= sum(probs)
        pop = np.random.choice(unified,size=pop.size,replace=False, p=probs)
        pop[-1] = np.max(unified)
        return np.array(pop)


class deleteAllReplacer(Replacer):

    def replace(self, newInds, pop):
        """
        replace the all individuums in pop with newInds
        :param newInds:
        :param pop:
        :return: updated pop
        """

        return newInds