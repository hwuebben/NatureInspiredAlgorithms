from abc import ABC, abstractmethod
class Recombiner(ABC):
    @abstractmethod
    def recombine(self,ind0,ind1):
        pass

class CrossoverRecombiner(Recombiner):
    def recombine(self,ind0,ind1):
        """
        perform recombination operation
        :param ind0:
        :param ind1:
        :return: recombiated child
        """
        pass