from __future__ import division
import numpy as np


class Individual:

    def __init__(self, x: np.array, problem):
        """

        :param x = (e1, e2, e3,s1,s2,s3, p1, p2, p3)
        """
        self.x = x
        self.targFuncVal = problem.targetFunc(self.x)


    """
    overwrite compare methods for sorting
    """
    def __eq__(self, other):
        return self.targFuncVal == other.targFuncVal

    def __lt__(self, other):
        return self.targFuncVal < other.targFuncVal

    def __le__(self, other):
        return self.targFuncVal <= other.targFuncVal

    def __gt__(self, other):
        return self.targFuncVal > other.targFuncVal

    def __ge__(self, other):
        return self.targFuncVal >= other.targFuncVal








