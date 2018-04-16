from abc import ABC, abstractmethod
import numpy as np
import time

class Terminator(ABC):
    @abstractmethod
    def checkTermination(self,GA):
        pass


class maxItTerminator(Terminator):
    def __init__(self, maxIt):
        """
        create terminator that terminates after maxIt iterations
        :param maxIt:
        """
        self.maxIt = maxIt
    def checkTermination(self,GA):
        if GA.nrIt >= self.maxIt:
            return True
        return False
class maxRuntimeTerminator(Terminator):
    def __init__(self,maxRuntime):
        """
        create terminator that terminates after maxRuntime seconds
        :param maxRuntime:
        """
        self.maxRuntime = maxRuntime
        self.startTime = None
    def checkTermination(self,GA):
        if self.startTime is None:
            self.startTime = time.time()
            return False
        else:
            return ((self.startTime+self.maxRuntime) <= time.time())


