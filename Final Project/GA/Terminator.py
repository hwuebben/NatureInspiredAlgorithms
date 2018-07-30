from __future__ import division
from abc import ABC, abstractmethod
import numpy as np
import time


class Terminator(ABC):

    @abstractmethod
    def checkTermination(self, GA):
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

    def checkTermination(self, GA):
        self.nrIt = GA.nrIt
        if self.nrIt >= self.maxIt:
            return True
        return False

    def estimateProgress(self):
        return self.nrIt/self.maxIt

class maxRuntimeTerminator(Terminator):

    def __init__(self, maxRuntime):
        """
        create terminator that terminates after maxRuntime seconds
        :param maxRuntime:
        """
        self.maxRuntime = maxRuntime
        self.startTime = None

    def checkTermination(self, GA):
        perf = np.max(GA.pop).fitness
        #print("best fitness value: ",perf)
        if self.startTime is None:
            self.startTime = time.time()
            return False
        else:
            return ((self.startTime+self.maxRuntime) <= time.time())

    def estimateProgress(self):
        return (time.time()-self.startTime) / self.maxRuntime


class convergenceTerminator(Terminator):

    def __init__(self, maxIter, rtol=1e-05):
        """
        if performance of best individual doesn't change more than
        rtol (relative change) for maxIter iteration, then terminate
        :param maxIter:
        :param rtol:
        """
        self.lastPerf = np.finfo(np.float64).min
        self.counter = 0
        self.maxIter = maxIter
        self.rtol = rtol

    def checkTermination(self,GA):
        perf = np.max(GA.pop).fitness
        print("best fitness value: ",perf)
        if np.isclose(perf, self.lastPerf, rtol=self.rtol, atol=0):
            self.counter += 1
        else:
            print("convergenceTerminator reset")
            self.counter = 0
        self.lastPerf = perf
        if self.counter >= self.maxIter:
            return True
        return False



