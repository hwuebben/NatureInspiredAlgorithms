from abc import ABC, abstractmethod
class Selector(ABC):
    @abstractmethod
    def select(self,pop):
        pass


class RouletteSelector(Selector):

    def select(self,pop):
        """
        perform roulette wheel selection on pop
        :param pop:
        :return: selected individual
        """
        pass

