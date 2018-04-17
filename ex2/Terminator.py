from __future__ import division
from abc import ABC, abstractmethod
import numpy as np
import time

class Terminator(ABC):
    @abstractmethod
    def checkTermination(self,GA):
        pass
    def estimateProgress(self):
        """
        return the progress (from 0-1) of the GA
        this method CAN be overwritten to enable modules to change
        behavior based on GAs progress
        :return:
        """
        return 0


class maxItTerminator(Terminator):
    def __init__(self, maxIt):
        """
        create terminator that terminates after maxIt iterations
        :param maxIt:
        """
        self.maxIt = maxIt
        self.nrIt = 0
    def checkTermination(self,GA):
        self.nrIt = GA.nrIt
        if self.nrIt >= self.maxIt:
            return True
        return False
    def estimateProgress(self):
        return self.nrIt/self.maxIt

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
    def estimateProgress(self):
        return (time.time()-self.startTime) / self.maxRuntime


