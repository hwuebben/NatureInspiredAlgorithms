from __future__ import division
from abc import ABC, abstractmethod
import numpy as np
import time


class Terminator(ABC):

    @abstractmethod
    def checkTermination(self, DE):
        pass

    def estimateProgress(self):
        """
        return the progress (from 0-1) of the DE
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

    def checkTermination(self, DE):
        self.nrIt = DE.nrIt
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

    def checkTermination(self, DE):
        if self.startTime is None:
            self.startTime = time.time()
            return False
        else:
            return ((self.startTime+self.maxRuntime) <= time.time())

    def estimateProgress(self):
        return (time.time()-self.startTime) / self.maxRuntime


class minFitness(Terminator):

    def __init__(self, minFitness):
        """
        create terminator that terminates after achieving a minimum fitness
        :param minFitness:
        """
        self.minFitness = minFitness

    def checkTermination(self, DE):
        self.fitness = np.max(DE.pop).targFuncVal
        return self.fitness > self.minFitness

    def estimateProgress(self):
        return self.fitness / self.minFitness


class convergenceTerminator(Terminator):

    def __init__(self, maxIter, rtol=1e-05):
        """
        if performance of best solution doesn't change more than
        rtol (relative change) for maxIter iteration, then terminate
        :param maxIter:
        :param rtol:
        """
        self.lastPerf = 0
        self.counter = 0
        self.maxIter = maxIter
        self.rtol = rtol

    def checkTermination(self, DE):
        perf = DE.best_score
        if np.isclose(perf, self.lastPerf, rtol=self.rtol, atol=0):
            self.counter += 1
        else:
            self.counter = 0
        self.lastPerf = perf
        if self.counter >= self.maxIter:
            return True
        return False

