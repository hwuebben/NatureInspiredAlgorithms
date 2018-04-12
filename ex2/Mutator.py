from abc import ABC, abstractmethod
class Mutator(ABC):
    @abstractmethod
    def mutate(self,toMutate):
        pass

class RandomMutator(Mutator):

    def mutate(self, toMutate):
        """
        :param toMutate:
        :return: mutated individual
        """
        pass

