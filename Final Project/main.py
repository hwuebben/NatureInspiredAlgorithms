from VRPsolver import VRPsolver
from Parser import Parser
from GA.ProblemDefinition import ProblemDefinition
import pickle
from GeneticAlgorithm import GeneticAlgorithm
from ProblemDefinition import ProblemDefinition
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


if __name__ == '__main__':
    mp.freeze_support()

    for problem in ["VRP1","VRP2"]:
        nameOfVRP = problem
        capacity, demand, distance, transCost = Parser.readVRP(nameOfVRP)
        probDef = ProblemDefinition(capacity, demand, distance, transCost)
        vrpSolver = VRPsolver(probDef)
        for runtime in [1,5,10,20,30,60]:

            print("start with runtime: ",runtime)
            terminators = [Terminator.maxRuntimeTerminator(runtime * 60)]
            gaParams["terminators"] = terminators
            #terminatorsACO = [Terminator.convergenceTerminator(100,0.0),Terminator.maxRuntimeTerminator(max(60,runtime*5))]
            #acoParams["terminators"] = terminatorsACO
            #bestScore = vrpSolver.optimizeWithParams(gaParams,acoParams)
            vrpSolver.optimizeWithParamsMP(gaParams,acoParams,nameOfVRP)


# file = "2018-07-25-16-17-42_best.p"
# file = "2018-07-26-15-18-03.p"
# bestScore = vrpSolver.optimizeWithGAinstance(acoParams,file)
# pickle.dump(bestScore, open("FitnessAndActual_"+file, "wb"))

#print("Overall best Sol value: ",bestScore)

# nrEqual = 0
# for i,ind in enumerate(ga.pop):
#     for ind1 in ga.pop[0:i]:
#         if (ind.assign == ind1.assign).all():
#             assert (ind.fitness == ind1.fitness)
#             nrEqual += 1
#             break
# print(nrEqual)

# nrUnique = 0
# for i,ind in enumerate(ga.pop):
#     unique = True
#     for ind1 in ga.pop[0:i]:
#         if (ind.assign == ind1.assign).all():
#             assert (ind.fitness == ind1.fitness)
#             unique = False
#             break
#     if unique:
#         nrUnique += 1
# print(nrUnique)
