from abc import ABC, abstractmethod
import numpy as np


class Mutator(ABC):
    def __init__(self,F):
        """
        :param F: scale Factor
        """
        self.F = F


    @abstractmethod
    def mutate(self,toMutate):
        pass


class DEmutator(Mutator):
    pass