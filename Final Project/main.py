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
            "mutator": Mutator.SwapMutator(0.5),
            "recombiner":Recombiner.SmartMeanRecombiner(),
            "selector": Selector.SmartRouletteSelector(),
            "replacer": Replacer.BottomReplacer(),
            "terminator": [Terminator.convergenceTerminator(100,0.001),
                           Terminator.maxRuntimeTerminator(1)],
            "localSearcher": LocalSearcher.Idle(),
            "popSize": 300
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
            "terminators":[Terminator.convergenceTerminator(100,0.0001)]

}

vrpSolver = VRPsolver(probDef)
bestScore = vrpSolver.optimizeWithParams(gaParams,acoParams)
print("Overall best Sol value: ",bestScore)
