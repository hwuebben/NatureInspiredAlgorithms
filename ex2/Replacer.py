from abc import ABC, abstractmethod
import numpy as np
class Replacer(ABC):
    @abstractmethod
    def replace(self,newInds,pop):
        pass

class bottomReplacer(Replacer):

    def replace(self,newInds,pop):
        """
        replace the worst individuums in pop with newInds
        :param newInds:
        :param pop:
        :return: updated pop
        """
        pop = pop[np.argpartition(pop,newInds.size)]
        pop[0:newInds.size] = newInds
        return pop