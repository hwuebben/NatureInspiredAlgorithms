from VRPsolver import VRPsolver
from Parser import Parser
from GA.ProblemDefinition import ProblemDefinition
import pickle
from GA.GeneticAlgorithm import GeneticAlgorithm
from GA.ProblemDefinition import ProblemDefinition
import multiprocessing as mp



from GA import Initializer, Mutator, Recombiner, Selector, Replacer, Terminator, LocalSearcher
gaParams = {
            "initializer":Initializer.HeuristicInitializer(),
            "mutators": [Mutator.RandomSwapMutator(mutationProb=0.0,dynAdapt=True),
                         #Mutator.RandomMutator()
            ],
            "recombiner":Recombiner.SmartInspirationalRecombiner(recombineRatio=0.0,dynAdapt=True),
            "selector": Selector.RouletteSelector(),
            "replacer": Replacer.RouletteReplacer(includeBest=True,dynAdapt=True),
            "terminators": [#Terminator.convergenceTerminator(100,0.001),
                           Terminator.maxRuntimeTerminator(5*60)],
            "localSearcher": LocalSearcher.TspTourSimplifierQuick(singleIteration=False),
            "popSize": 100,
            "includeUnmutated": True,
            "offspringProp": 0.5,
            "verbose": False

}

from ACO import Initializer, Evaporator, Intensifier, Heuristics,Terminator
acoParams = {
            "initializer": Initializer.TSP_Initializer(),
            "evaporator":Evaporator.Evaporator(rho=0.05),
            "intensifier":Intensifier.Intensifier(delta=0.05),
            "heuristic":Heuristics.TSPHeuristic,
            "nrAnts":50,
            "alpha":1,
            "beta":1,
            "terminators":[
                Terminator.convergenceTerminator(100,0.0),
                Terminator.maxRuntimeTerminator(60)
            ],
            "qualityDependence": True,
            "verbose": False

}

def runWithRuntime(runtime):
    print("start with runtime: ", runtime)
    terminators = [Terminator.maxRuntimeTerminator(runtime * 60)]
    gaParams["terminators"] = terminators
    gaParams["popSize"] = min(runtime * 50, 5000)
    return vrpSolver.optimizeWithParamsMP(gaParams, acoParams, nameOfVRP)

if __name__ == '__main__':
    mp.freeze_support()

    nameOfVRP = "VRP1"
    capacity, demand, distance, transCost = Parser.readVRP(nameOfVRP)
    probDef = ProblemDefinition(capacity, demand, distance, transCost)
    vrpSolver = VRPsolver(probDef)

    runtime = 10
    bestSol = runWithRuntime(runtime)
    print("best Score: ",bestSol.solution["score"])
    print(bestSol.solution)
    pickle._dump(bestSol, open("bestSol"+str(runtime)+"MinuteRun"+nameOfVRP+".p","wb"))

    # for problem in ["VRP1","VRP2"]:
    #     nameOfVRP = problem
    #     capacity, demand, distance, transCost = Parser.readVRP(nameOfVRP)
    #     probDef = ProblemDefinition(capacity, demand, distance, transCost)
    #     vrpSolver = VRPsolver(probDef)
    #     for runtime in [1,5,10,20,30,60]:
    #
    #         print("start with runtime: ",runtime)
    #         bestSol = runWithRuntime(runtime)


