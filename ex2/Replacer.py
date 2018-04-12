from abc import ABC, abstractmethod
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
        pass