from abc import ABC, abstractmethod
import numpy as np


class Selector(ABC):

    @abstractmethod
    def select(self,pop):
        pass



class DEselector(Selector):

    def select(self, pop):
        pass



