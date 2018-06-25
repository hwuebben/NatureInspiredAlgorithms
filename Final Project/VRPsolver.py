import numpy as np

class VRPsolver:

    def __init__(self,vrpProblem):
        self.vrpProblem = vrpProblem

    def optimizeWithParams(self,gaParams:dict, acoParams:dict):
        ga = self.__class__.__initGA(self.vrpProblem, gaParams)
        bestIndividual, results = ga.run()
        distMatrices = bestIndividual.extractDistMatrices()
        bestSolutions = self.optimizeTSPs(distMatrices,acoParams)
        return self.evalSol(bestSolutions)


    def optimizeTSPs(self,distMatrices,acoParams):
        bestSolutions = []
        for i,distMatrix in enumerate(distMatrices):
            from ACO import Problem
            aco=self.__class__.__initACO(Problem.TSPProblem(distMatrix),acoParams)
            solutions, scores = aco.run()
            bestSolutions.append(solutions[0])
        return bestSolutions

    def evalSol(self, bestSolutions):
        return self.vrpProblem,bestSolutions


    @classmethod
    def __initGA(cls,vrpProblem, gaParams):
        from GeneticAlgorithm import GeneticAlgorithm
        try:
            initializer = gaParams["initializer"]
            mutator = gaParams["mutator"]
            recombiner = gaParams["recombiner"]
            selector = gaParams["selector"]
            replacer = gaParams["replacer"]
            terminator = gaParams["terminator"]
            localSearcher = gaParams["localSearcher"]

            popSize = gaParams["popSize"]
            nrOffspring = int(popSize / 10)

            return GeneticAlgorithm(initializer, selector, recombiner, mutator, replacer, terminator,
                                  vrpProblem, popSize, nrOffspring, localSearcher)
        except(ValueError):
            raise ValueError("gaParams needs the following entries..")


    @classmethod
    def __initACO(cls,tspProblem, acoParams):

        from ACO import ACO,SolutionGenerator
        initializer = acoParams["initializer"]
        evaporator = acoParams["evaporator"]
        intensifier = acoParams["intensifier"]
        heuristic = acoParams["heuristic"]
        nrAnts = acoParams["nrAnts"]
        alpha =acoParams["alpha"]
        beta = acoParams["beta"]
        solutionGen = SolutionGenerator.PermutationSolutionGenerator(nrAnts,alpha,beta,heuristic,tspProblem)
        terminators = acoParams["terminators"]
        return ACO.Ant_Colony_Optimizer(tspProblem, initializer, evaporator, intensifier, solutionGen, terminators, 3,
                                       True, True)