from abc import ABC, abstractmethod
import numpy as np
from Individual import Individual


class Recombiner(ABC):
    def __init__(self, Cr):
        """
        :param Cr: Crossover rate
        """
        self.Cr = Cr

    @abstractmethod
    def recombine(self):
        pass


class BinomialCrossover(Recombiner):

    def recombine(self):
        pass

