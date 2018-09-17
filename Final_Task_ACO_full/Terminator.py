from __future__ import division
from abc import ABC, abstractmethod
import numpy as np
import time

class Terminator(ABC):
    """
    Astract terminator, the objects defines the termination condition of the learning process
    """

    @abstractmethod
    def checkTermination(self, aco) -> bool:
        """
        Checks if the learning process reached it's goalstate
        :param aco: the optimizer
        :return: False: commence training, True: goalstate reached, end training
        """
        pass

    def estimateProgress(self) -> float:
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

    def checkTermination(self, aco) -> float:
        """
        checks if the maximum number if iterations are done, if so: True else False
        :param aco:
        :return:
        """
        if aco.nrIt >= self.maxIt:
            return True
        return False

    def estimateProgress(self) -> bool:
        """
        percentage of iterations performed
        :return:
        """
        return self.nrIt/self.maxIt

class maxRuntimeTerminator(Terminator):

    def __init__(self, maxRuntime):
        """
        create terminator that terminates after maxRuntime seconds
        :param maxRuntime:
        """
        self.maxRuntime = maxRuntime
        self.startTime = None

    def checkTermination(self, aco) -> bool:
        """
        check if the maximum runtime was reached
        :param aco: ACO optimizer
        :return: true if runtime maximum has been surpassed, else false
        """
        if self.startTime is None:
            self.startTime = time.time()
            return False
        else:
            return ((self.startTime+self.maxRuntime) <= time.time())

    def estimateProgress(self) -> bool:
        """
        return the percentage of the time intervall that allready has passed
        :return:
        """
        return (time.time()-self.startTime) / self.maxRuntime


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

    def checkTermination(self, aco) -> bool:
        """
        checks if the model is converged or didn't exceeded the maximum number of iterations
        :param aco: ACO optimizer
        :return: True if converged (or maxIter iterations reached) else False
        """
        perf = aco.iteration_best_score
        if np.isclose(perf, self.lastPerf, rtol=self.rtol, atol=0):
            self.counter += 1
        self.lastPerf = perf
        if self.counter >= self.maxIter:
            return True
        return False
