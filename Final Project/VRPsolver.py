import numpy as np
from GA.ProblemDefinition import ProblemDefinition as PD
import time
import copy
import datetime
import pickle
import threading
from ACO.ACO import Ant_Colony_Optimizer

class VRPsolver:

    def __init__(self,vrpProblem:PD):
        self.vrpProblem = vrpProblem

    def optimizeWithParams(self,gaParams:dict, acoParams:dict, nrThreads = 3):
        print("init GA")
        ga = self.__class__.__initGA(self.vrpProblem, gaParams)
        print("start running GA")
        startTime = time.time()
        bestIndividual, results = ga.run()
        ga.pickleStore(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
        print("GA finished, runtime: ",time.time() - startTime,"best Fitness: ",bestIndividual.fitness)
        distMatrices = bestIndividual.extractDistMatrices()
        startTime = time.time()
        print("start optimizing TSPs with ACO")
        bestSolutions,bestScores = self.optimizeTSPs(distMatrices,acoParams)
        print("done with ACO, runtime: ",time.time()-startTime)
        return self.evalSol(bestScores)

    def optimizeWithParamsThread(self,gaParams:dict, acoParams:dict, nrThreads = 3):
        print("init GA Thread")
        ga = self.__class__.__initGA(self.vrpProblem, gaParams)
        startTime = time.time()
        gaThread = threading.Thread(target=ga.run)
        print("start running GA Thread")
        gaThread.start()
        distMatrices = ga.getNthbestInd(0).extractDistMatrices()
        startTime = time.time()
        print("start optimizing TSPs with ACO")
        acos = self.optimizeTSPs(distMatrices,acoParams)
        bestScores = np.empty(len(distMatrices))
        for i in range(acos.size):
            if acos[i] is None:
                bestScores[i] = 0
            else:
                self.waitForIt(aco=acos[i],period=0.01)
                bestScores[i] = acos[i].getBestSolScore()[1]
        print("done with ACO, runtime: ",time.time()-startTime)
        return self.evalSol(bestScores)

    def waitForIt(self,aco,period=0.01):
        while True:
            if aco.hasSolScore(): return
            time.sleep(period)


    def optimizeTSPs(self,distMatrices,acoParams):
        from ACO import Problem
        #bestSolutions = np.empty(distMatrices.size)
        #bestScores = np.empty(distMatrices.size)
        acos = np.empty(len(distMatrices),dtype=Ant_Colony_Optimizer)
        for i,distMatrix in enumerate(distMatrices):
            if not (distMatrix == 0).all():
                aco=self.__class__.initACO(Problem.TSPProblem(distMatrix),acoParams)
                acoThread = threading.Thread(target=aco.run)
                acoThread.start()
                acos[i] = aco
            else:
                #bestScores[i] = [0]
                #bestSolutions[i] = [0]
                acos[i] = None
        return acos

    def evalSol(self, bestScores):
            bestScoresFinal = np.array([np.min(x) for x in bestScores])
            return np.sum(bestScoresFinal*self.vrpProblem.transCost)

    def optimizeWithGAinstance(self,acoParams,gaInstName):
        print("load GA instance with name: "+gaInstName)
        ga = pickle.load(open( gaInstName, "rb" ))

        results = []
        for ind in ga.pop:
            print("next individual fitness: ",ind.fitness)
            distMatrices = ind.extractDistMatrices()
            startTime = time.time()
            print("start optimizing TSPs with ACO")
            bestSolutions,bestScores = self.optimizeTSPs(distMatrices,acoParams)
            print("done with ACO, runtime: ",time.time()-startTime)
            res = self.evalSol(bestScores)
            print("result: ",res)
            results.append([ind.fitness,res])
        return results



    @classmethod
    def __initGA(cls,vrpProblem, gaParams):
        from GeneticAlgorithm import GeneticAlgorithm
        try:
            initializer = gaParams["initializer"]
            mutators = gaParams["mutators"]
            recombiner = gaParams["recombiner"]
            selector = gaParams["selector"]
            replacer = gaParams["replacer"]
            terminators = gaParams["terminators"]
            localSearcher = gaParams["localSearcher"]
            includeUnmutated = gaParams["includeUnmutated"]

            popSize = gaParams["popSize"]
            offspringProp = gaParams["offspringProp"]
            verbose = gaParams["verbose"]

        except(ValueError):
            raise ValueError("gaParams needs the following entries..")

        return GeneticAlgorithm(initializer, selector, recombiner, mutators, replacer, terminators,
                                  vrpProblem, popSize, offspringProp, localSearcher, includeUnmutated,verbose)



    @classmethod
    def initACO(cls,tspProblem, acoParams):

        from ACO import ACO,SolutionGenerator
        initializer = copy.deepcopy(acoParams["initializer"])
        evaporator = copy.deepcopy(acoParams["evaporator"])
        intensifier = copy.deepcopy(acoParams["intensifier"])
        heuristic = copy.deepcopy(acoParams["heuristic"])
        nrAnts = copy.deepcopy(acoParams["nrAnts"])
        alpha =copy.deepcopy(acoParams["alpha"])
        beta = copy.deepcopy(acoParams["beta"])
        solutionGen = copy.deepcopy(SolutionGenerator.PermutationSolutionGenerator(nrAnts,alpha,beta,heuristic,tspProblem))
        terminators = copy.deepcopy(acoParams["terminators"])
        qualityDependence = copy.deepcopy(acoParams["qualityDependence"])
        verbose = copy.deepcopy(acoParams["verbose"])
        return ACO.Ant_Colony_Optimizer(tspProblem, initializer, evaporator, intensifier, solutionGen, terminators, 3,
                                       qualityDependence, verbose)