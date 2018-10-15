import numpy as np
from GA.ProblemDefinition import ProblemDefinition as PD
import time
import copy
import datetime
import pickle
import threading
from ACO.ACO import Ant_Colony_Optimizer
import multiprocessing as mp
from SolutionVRP import SolutionVRP
from GA.GeneticAlgorithm import GeneticAlgorithm

class VRPsolver:

    def __init__(self,vrpProblem:PD,verbose = False):
        self.vrpProblem = vrpProblem
        self.cpuCount = mp.cpu_count()
        self.verbose = verbose

    def runGAQueue(self,gaParams:dict):
        print("init GA")
        ga = self.__class__.__initGA(self.vrpProblem, gaParams)
        print("start running GA")
        queue = mp.Queue()
        gaPro = mp.Process(target=ga.runWithQueue,args=(queue,))
        gaPro.start()
        #gaPro.join()
        startTime = time.time()
        while gaPro.is_alive() or (not queue.empty()):
            print("best fitness: ",queue.get(block=True,timeout=None).fitness)
    def runGAPipe(self,gaParams:dict):
        print("init GA Thread")
        ga = self.__class__.__initGA(self.vrpProblem, gaParams)
        parent_conn, child_conn = mp.Pipe()
        gaPro = mp.Process(target=ga.runWithPipeFinalGA,args=(child_conn,))
        print("start running GA")
        gaPro.start()
        finalGA = parent_conn.recv()
        return finalGA


    def optimizeWithParamsMP(self,gaParams:dict, acoParams:dict,problemName = ""):
        #mp.freeze_support()
        print("init GA Process")
        ga = self.__class__.__initGA(self.vrpProblem, gaParams)
        parent_conn, child_conn = mp.Pipe()
        gaPro = mp.Process(target=ga.runWithPipe,args=(child_conn,))
        print("start running GA Process")
        gaPro.start()
        self.bestSolution = None
        #keepGoing = True
        #already optimized Individuals
        while gaPro.is_alive():
            #keepGoing = gaPro.is_alive()
            #get best GA indvidual(s)

            parent_conn.send(True)
            gaInd = parent_conn.recv()

            distMatrices = gaInd.extractDistMatrices()
            #bestScore = np.inf
            print("new distMatrix")
            startTime = time.time()
            print("start optimizing TSPs with ACO")
            #TODO: use MP here too
            acos,acoThreads = self.optimizeTSPsThread(distMatrices,acoParams)
            stillAlive = lambda: np.any([x.is_alive() for x in acoThreads])
            keepGoingACO = True
            #print("done with ACO, runtime: ",time.time()-startTime)
            while keepGoingACO:
                keepGoingACO = stillAlive()
                scoresAndSols = self.calcBestScoresSols(acos,distMatrices)
                score = self.evalSol(scoresAndSols[0])

                if (self.bestSolution is None) or (score < self.bestSolution.solution["score"]):
                    self.bestSolution = SolutionVRP(problemName,self.vrpProblem,score,gaInd.assign,
                                               distMatrices,scoresAndSols[1])
                    if self.verbose:
                        print("VRP score: ",score)
                # if score < bestScore:
                #     bestScore = score
                #     print("new best score: ",bestScore)
                #     self.storeAllACOs(problemName+"_maxRuntimeGA_"+str(ga.terminators[-1].maxRuntime),acos)
                time.sleep(1)
                #self.waitForIt(it=acoThread.is_alive,toBe=False)
        print("done")
        return self.bestSolution

    def getBestSeen(self):
        return self.bestSolution

    def storeAllACOs(self,name,acos):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        for i,aco in enumerate(acos):
            if aco is None:
                continue
            aco.pickleStoreBestSol(name+"_ACO_nr_"+str(i)+"_"+timestamp)

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
        while gaThread.is_alive():
            distMatrices = ga.getNthbestInd(0).extractDistMatrices()
            bestScore = np.inf
            print("new distMatrix")
            startTime = time.time()
            print("start optimizing TSPs with ACO")
            acos,acoThreads = self.optimizeTSPsThread(distMatrices,acoParams)
            #print("done with ACO, runtime: ",time.time()-startTime)
            for acoThread in acoThreads:
                if acoThread is None:
                    continue
                while True:
                    score = self.evalSol(self.calcBestScores(acos,distMatrices))
                    if score < bestScore:
                        bestScore = score
                        print("new best score: ",bestScore)
                    if not acoThread.is_alive():
                        break
                    time.sleep(2)
                #self.waitForIt(it=acoThread.is_alive,toBe=False)
        return
    def calcBestScoresSols(self,acos,distMatrices):
        bestScores = np.zeros(len(distMatrices))
        acoSols = np.zeros(len(distMatrices),dtype=object)
        for i in range(acos.size):
            if acos[i] is None:
                continue
            else:
                self.waitForIt(it=acos[i].hasSolScore, period=0.1)
                solScore = acos[i].getBestSolScore()
                bestScores[i] = solScore[1]
                acoSols[i] = solScore[0]
        return bestScores, acoSols
    def waitForIt(self,it,toBe=True,period=0.1):
        while True:
            if it() == toBe: return
            time.sleep(period)

    def optimizeTSPs(self, distMatrices, acoParams):
        from ACO import Problem
        bestSolutions = []
        bestScores = []
        for i, distMatrix in enumerate(distMatrices):
            if not (distMatrix == 0).all():
                aco = self.__class__.initACO(Problem.TSPProblem(distMatrix), acoParams)
                solutions, scores = aco.run()
            else:
                scores = [0]
                solutions = [0]
            bestSolutions.append(solutions)
            bestScores.append(scores)
        return bestSolutions, bestScores


    def optimizeTSPsThread(self,distMatrices,acoParams):
        from ACO import Problem
        #bestSolutions = np.empty(distMatrices.size)
        #bestScores = np.empty(distMatrices.size)
        acos = np.empty(len(distMatrices),dtype=Ant_Colony_Optimizer)
        acoThreads = []
        for i,distMatrix in enumerate(distMatrices):
            if not (distMatrix == 0).all():
                aco=self.__class__.initACO(Problem.TSPProblem(distMatrix),acoParams)
                acoThread = threading.Thread(target=aco.run)
                acoThread.start()
                acoThreads.append(acoThread)
                acos[i] = aco
            else:
                #bestScores[i] = [0]
                #bestSolutions[i] = [0]
                acos[i] = None
        return acos, acoThreads

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
        from GA.GeneticAlgorithm import GeneticAlgorithm
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


if __name__ == '__main__':
    mp.freeze_support()