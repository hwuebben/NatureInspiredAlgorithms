from __future__ import division
from abc import abstractmethod
import numpy as np
import time
from Module import Module

class Terminator(Module):

    @abstractmethod
    def checkTermination(self, aco):
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

    def checkTermination(self, aco):
        if aco.nrIt >= self.maxIt:
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

    def checkTermination(self, aco):
        if self.startTime is None:
            self.startTime = time.time()
            return False
        else:
            return ((self.startTime+self.maxRuntime) <= time.time())

    def estimateProgress(self):
        return (time.time()-self.startTime) / self.maxRuntime

    def reset(self):
        self.startTime = None


class convergenceTerminator(Terminator):

    def __init__(self, maxIter, rtol=1e-05):
        """
        if performance of best solution doesn't change more than
        rtol (relative change) for maxIter iteration, then terminate
        :param maxIter:
        :param rtol:
        """
        self.lastPerf = np.finfo(np.float64).min
        self.counter = 0
        self.maxIter = maxIter
        self.rtol = rtol

    def checkTermination(self, aco):
        perf = aco.best_score
        if np.isclose(perf, self.lastPerf, rtol=self.rtol, atol=0):
            self.counter += 1
        self.lastPerf = perf
        if self.counter >= self.maxIter:
            return True
        return False

    def reset(self):
        self.lastPerf = np.finfo(np.float64).min
        self.counter = 0