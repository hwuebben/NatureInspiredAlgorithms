from VRPsolver import VRPsolver
from Parser import Parser
from GA.ProblemDefinition import ProblemDefinition
import pickle
from GA.GeneticAlgorithm import GeneticAlgorithm
from GA.ProblemDefinition import ProblemDefinition
import multiprocessing as mp
import datetime


from GA import Initializer, Mutator, Recombiner, Selector, Replacer, Terminator, LocalSearcher
gaParams = {
            "initializer":Initializer.HeuristicInitializer2(),
            "mutators": [Mutator.RandomSwapMutatorJit(),
                         #Mutator.RandomMutator()
            ],
            "recombiner":Recombiner.SmartInspirationalRecombinerJit(recombineRatio=0.001,dynAdapt=True),
            "selector": Selector.RouletteSelector(),
            "replacer": Replacer.KeepBestReplacer(dynAdapt=True),
            "terminators": [#Terminator.convergenceTerminator(100,0.001),
                           Terminator.maxRuntimeTerminator(5*60)],
            #"localSearcher": LocalSearcher.TspTourSimplifierJit(singleIteration=False),
            "localSearcher": LocalSearcher.Idle(),
            "popSize": 500,
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
                Terminator.convergenceTerminator(50,0.0),
                #Terminator.maxRuntimeTerminator(120)
            ],
            "qualityDependence": True,
            "verbose": False

}

def runWithRuntime(runtime,vrpSolver,nameOfVRP):
    print("start with runtime: ", runtime)
    terminators = [Terminator.maxRuntimeTerminator(runtime * 60)]
    gaParams["terminators"] = terminators
    gaParams["popSize"] = min(runtime * 50, 5000)
    #gaParams["popSize"] = 500
    return vrpSolver.optimizeWithParamsMP(gaParams, acoParams, nameOfVRP)

if __name__ == '__main__':
    mp.freeze_support()
    def singleTest():
        nameOfVRP = "VRP2"
        capacity, demand, distance, transCost = Parser.readVRP(nameOfVRP)
        probDef = ProblemDefinition(capacity, demand, distance, transCost)
        vrpSolver = VRPsolver(probDef,verbose=True)

        runtime = 20
        bestSol = runWithRuntime(runtime,vrpSolver,nameOfVRP)
        print("best Score: ",bestSol.solution["score"])
        print(bestSol.solution)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        pickle._dump(bestSol, open("bestSol"+str(runtime)+"MinuteRun"+nameOfVRP+"_"+timestamp+".p","wb"))
    def fullTest():
        for problem in ["VRP2"]:
            nameOfVRP = problem
            capacity, demand, distance, transCost = Parser.readVRP(nameOfVRP)
            probDef = ProblemDefinition(capacity, demand, distance, transCost)
            vrpSolver = VRPsolver(probDef,verbose=True)
            for runtime in [20,30,60]:

                print("start with runtime: ",runtime, " with: ", problem)
                bestSol = runWithRuntime(runtime,vrpSolver,nameOfVRP)
                print("best Score: ", bestSol.solution["score"])
                print(bestSol.solution)
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
                pickle._dump(bestSol, open("bestSol" + str(runtime) + "MinuteRun" + nameOfVRP + "_" + timestamp+".p", "wb"))
    fullTest()

