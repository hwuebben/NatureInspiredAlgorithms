from VRPsolver import VRPsolver
from Parser import Parser
from GA.ProblemDefinition import ProblemDefinition

from GeneticAlgorithm import GeneticAlgorithm
from ProblemDefinition import ProblemDefinition

nameOfVRP = "VRP1"
capacity, demand, distance, transCost = Parser.readVRP(nameOfVRP)
probDef = ProblemDefinition(capacity, demand, distance, transCost)

from GA import Initializer, Mutator, Recombiner, Selector, Replacer, Terminator, LocalSearcher
gaParams = {
            "initializer":Initializer.HeuristicInitializer(),
            "mutator": Mutator.SwapMutator(0.1),
            "recombiner":Recombiner.InspirationalRecombiner(),
            "selector": Selector.RouletteSelector(),
            "replacer": Replacer.BottomReplacer(),
            "terminator": [Terminator.convergenceTerminator(100,0.001),
                           Terminator.maxRuntimeTerminator(60*60)],
            "localSearcher": LocalSearcher.Idle(),
            "popSize": 50,
            "includeUnmutated": True,
            "offspringProp": 0.2

}

from ACO import Initializer, Evaporator, Intensifier, Heuristics,Terminator
acoParams = {
            "initializer": Initializer.TSP_Initializer(),
            "evaporator":Evaporator.Evaporator(rho=0.05),
            "intensifier":Intensifier.Intensifier(delta=0.05),
            "heuristic":Heuristics.TSPHeuristic,
            "nrAnts":100,
            "alpha":1,
            "beta":1,
            "terminators":[Terminator.convergenceTerminator(100,0.0001)],
            "qualityDependence": True,
            "verbose": False

}

vrpSolver = VRPsolver(probDef)
#bestScore = vrpSolver.optimizeWithParams(gaParams,acoParams)
bestScore = vrpSolver.optimizeWithGAinstance(acoParams,"2018-07-25-16-17-42_best.p")

print("Overall best Sol value: ",bestScore)
