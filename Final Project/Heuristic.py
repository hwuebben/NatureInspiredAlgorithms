import numpy as np
from abc import ABC, abstractmethod
from GA.ProblemDefinition import ProblemDefinition
from ACO.ACO import Ant_Colony_Optimizer
#from VRPsolver import VRPsolver.initACO
from ACO import Problem


class Heuristic:

    @classmethod
    @abstractmethod
    def calcHeuVal(cls,ind, probDef: ProblemDefinition):
        pass

# class AcoHeuristic(Heuristic):
#     from ACO import Initializer, Evaporator, Intensifier, Heuristics, Terminator
#     acoParams = {
#         "initializer": Initializer.TSP_Initializer(),
#         "evaporator": Evaporator.Evaporator(rho=0.05),
#         "intensifier": Intensifier.Intensifier(delta=0.05),
#         "heuristic": Heuristics.TSPHeuristic,
#         "nrAnts": 10,
#         "alpha": 1,
#         "beta": 2,
#         "terminators": [Terminator.convergenceTerminator(1, 0.0001), Terminator.maxRuntimeTerminator(1)],
#         "qualityDependence": True,
#         "verbose": False
#     }
#
#     @classmethod
#     def calcHeuVal(cls,ind:Individual, probDef: ProblemDefinition):
#
#         heuVals = np.empty(probDef.nrVehicles)
#         for vehicleInd in range(probDef.nrVehicles):
#             distMatrix = ind.extractDistMatrix(vehicleInd)
#             if (distMatrix == 0).all():
#                 heuVals[vehicleInd] = 0
#             else:
#                 aco = VRPSolver.initACO(Problem.TSPProblem(distMatrix), cls.acoParams)
#                 heuVals[vehicleInd] = np.min(aco.run()[1]) * probDef.transCost[vehicleInd]
#         return -np.sum(heuVals)
class BeardwoodHeuristic(Heuristic):
    """
    'In 1959,´Beardwood et al. [1] derived an asymptotic expected tour length formula.
    T* ~ b(NA)½, for euclidean distances
    N = number of points
    A = Area
    b=0.75 has been approximated for large N'
    Since A only exists in euclidean problems it will be replaced by
    the average distance between all points
    the value of b is irrelevant since the heuristic only need to correlate with the actual value
    """
    @classmethod
    def calcHeuVal(cls,ind, probDef: ProblemDefinition):
        heuVals = np.empty(probDef.nrVehicles)
        #get nodes for each vehicle (graph)
        for vehicleInd in range(probDef.nrVehicles):
            distMatrix = ind.extractDistMatrix(vehicleInd)
            heuVals[vehicleInd] = np.mean(distMatrix) * distMatrix.shape[0] * probDef.transCost[vehicleInd]
        return -np.sum(heuVals)


class DaganzoHeuristic(Heuristic):
    """
    'In 1984, Daganzo [3] developed distance formulas for a vehicle routing problem (VRP). In
    particular, he derived a formula for determining the length of a tour through N points located in a
    subregion of A that does not include the depot. A vehicle can make at most C stops. Letting the
    density of points be given by 6 = N / A and the average straight-line distance from the points in the
    subregion to the depot be denoted by D, the optimal tour length (denoted by L*) is given by
    L* ,~ 2D(N/C) + 0.57(N6-½)
    This can be used to estimate the length of the optimal TSP tour through the N points. In
    this case, N = C and substituting 6 = N / A yields
    T* ~ 2D + 0.57(NA)½'

    """
    def calcHeuVal(cls,ind, probDef: ProblemDefinition):
        pass







