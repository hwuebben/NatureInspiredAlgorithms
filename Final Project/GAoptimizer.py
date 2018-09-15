from VRPsolver import VRPsolver
from Parser import Parser
from GA.ProblemDefinition import ProblemDefinition
import pickle
from GeneticAlgorithm import GeneticAlgorithm
from ProblemDefinition import ProblemDefinition
import multiprocessing as mp
from GA import Initializer, Mutator, Recombiner, Selector, Replacer, Terminator, LocalSearcher
import numpy as np
import datetime
class GAoptimizer:
    def __init__(self):

        nameOfVRP = "VRP1"
        capacity, demand, distance, transCost = Parser.readVRP(nameOfVRP)
        self.probDef = ProblemDefinition(capacity, demand, distance, transCost)

        self.gaParams = {
                    "initializer":Initializer.HeuristicInitializer(),
                    "mutators": [Mutator.RandomSwapMutator(mutationProb=0.0,dynAdapt=False),
                                 #Mutator.RandomMutator()
                    ],
                    "recombiner":Recombiner.SmartInspirationalRecombiner(recombineRatio=0.0,dynAdapt=False),
                    "selector": Selector.RouletteSelector(),
                    "replacer": Replacer.RouletteReplacer(includeBest=True,dynAdapt=True),
                    #"replacer": Replacer.PlainReplacer(keepMax=True),

                    "terminators": [#Terminator.convergenceTerminator(100,0.001),
                                   Terminator.maxRuntimeTerminator(10*60)],
                    "localSearcher": LocalSearcher.TspTourSimplifierQuick(),
                    #"localSearcher": LocalSearcher.TspTourSimplifierQuick(singleIteration=True),
                    "popSize": 50,
                    "includeUnmutated": True,
                    "offspringProp": 0.1,
                    "verbose": False

        }
    def run(self):

        vrpSolver = VRPsolver(self.probDef)

        finalGA = vrpSolver.runGAPipe(self.gaParams)
        print("Overall best Sol value: ",np.max(finalGA.pop).fitness)
        finalGA.pickleStore(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))

    def runRecombMutaParams(self):
        print(self.gaParams)
        print("self.gaParams['replacer'].dynAdapt ", self.gaParams["replacer"].dynAdapt)
        #params0 = np.linspace(0,0.2,1)
        #params1 = np.linspace(0,1,5)
        params0 = np.array([10,30,50,70,90,110])
        params1 = np.array([0.1,0.3,0.5])
        sampleSize = 2
        results = np.empty((params0.size,params1.size,sampleSize))
        for p0Ind, param0 in enumerate(params0):
            for p1Ind,param1 in enumerate(params1):
                self.gaParams["popSize"] = param0
                self.gaParams["offspringProp"] = param1

                for sInd in range(sampleSize):
                    vrpSolver = VRPsolver(self.probDef)
                    finalGA = vrpSolver.runGAPipe(self.gaParams)
                    bestIndi = np.max(finalGA.pop)
                    results[p0Ind,p1Ind,sInd] = bestIndi.fitness
                    print("param0: ",param0," param1: ",param1," best fitness: ",bestIndi.fitness)
                    finalGA.pickleStore(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
                print("param0: ", param0, " param1: ", param1, " AVG fitness: ", np.mean(results[p0Ind,p1Ind,:]))
        #pickle.dump(results,open("resultsRecombMuta.p","w"))

    def runWithParams(self):
        self.gaParams0 = {
                    "initializer":Initializer.HeuristicInitializer(),
                    "mutators": [Mutator.RandomSwapMutator(mutationProb=0.0,dynAdapt=False),
                    ],
                    "recombiner":Recombiner.SmartInspirationalRecombiner(recombineRatio=0.0,dynAdapt=False),
                    "selector": Selector.RouletteSelector(),
                    "replacer": Replacer.RouletteReplacer(includeBest=True,dynAdapt=False),
                    "terminators": [#Terminator.convergenceTerminator(100,0.001),
                                   Terminator.maxRuntimeTerminator(30*60)],
                    "localSearcher": LocalSearcher.TspTourSimplifierQuick(),
                    "popSize": 50,
                    "includeUnmutated": True,
                    "offspringProp": 0.1,
                    "verbose": False
        }
        self.gaParams2 = {
                    "initializer":Initializer.HeuristicInitializer(),
                    "mutators": [Mutator.RandomSwapMutator(mutationProb=0.,dynAdapt=False),
                    ],
                    "recombiner":Recombiner.SmartInspirationalRecombiner(recombineRatio=0.0,dynAdapt=False),
                    "selector": Selector.RouletteSelector(),
                    "replacer": Replacer.RouletteReplacer(includeBest=True,dynAdapt=False),
                    "terminators": [#Terminator.convergenceTerminator(100,0.001),
                                   Terminator.maxRuntimeTerminator(30*60)],
                    "localSearcher": LocalSearcher.TspTourSimplifierQuick(),
                    "popSize": 50,
                    "includeUnmutated": True,
                    "offspringProp": 0.5,
                    "verbose": False
        }
        self.gaParams0 = {
                    "initializer":Initializer.HeuristicInitializer(),
                    "mutators": [Mutator.RandomSwapMutator(mutationProb=0.0,dynAdapt=False),
                    ],
                    "recombiner":Recombiner.SmartInspirationalRecombiner(recombineRatio=0.0,dynAdapt=False),
                    "selector": Selector.RouletteSelector(),
                    "replacer": Replacer.RouletteReplacer(includeBest=True,dynAdapt=False),
                    "terminators": [#Terminator.convergenceTerminator(100,0.001),
                                   Terminator.maxRuntimeTerminator(30*60)],
                    "localSearcher": LocalSearcher.TspTourSimplifierQuick(),
                    "popSize": 50,
                    "includeUnmutated": True,
                    "offspringProp": 0.1,
                    "verbose": False
        }
        self.gaParams1 = {
                    "initializer":Initializer.RandomInitializer(),
                    "mutators": [Mutator.RandomSwapMutator(mutationProb=1,dynAdapt=True),
                    ],
                    "recombiner":Recombiner.SmartInspirationalRecombiner(recombineRatio=0.1,dynAdapt=True),
                    "selector": Selector.RouletteSelector(),
                    "replacer": Replacer.PlainReplacer(keepMax=True),
                    "terminators": [#Terminator.convergenceTerminator(100,0.001),
                                   Terminator.maxRuntimeTerminator(30*60)],
                    "localSearcher": LocalSearcher.TspTourSimplifierQuick(),
                    "popSize": 50,
                    "includeUnmutated": True,
                    "offspringProp": 0.5,
                    "verbose": False
        }
        vrpSolver = VRPsolver(self.probDef)
        params= self.gaParams1
        print(params)
        finalGA = vrpSolver.runGAPipe(params)

        print("Overall best Sol value: ",np.max(finalGA.pop).fitness)
        finalGA.pickleStore(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))

if __name__ == '__main__':
    gao = GAoptimizer()
    gao.runRecombMutaParams()

    #mp.freeze_support()

