from GA import GeneticAlgorithm
from ACO import Ant_Colony_Optimizer

class VRPsolver:

    def __init__(self,ga:GeneticAlgorithm, aco:Ant_Colony_Optimizer):
        self.ga = ga
        self.aco = aco

    @classmethod
    def fromParameters(cls,gaParams:dict, acoParams:dict):
        return cls(cls.__initGA(gaParams), cls.__initACO(acoParams))

    @classmethod
    def __initGA(cls,gaParams):
        import Initializer, Mutator, Recombiner, Selector, Replacer, Terminator, LocalSearcher
        from GeneticAlgorithm import GeneticAlgorithm
        from ProblemDefinition import ProblemDefinition
        from Benchmark import Benchmark
        from Parser import Parser
        try:
            nameOfVRP = gaParams["nameOfVRP"]
            # Set up an example problem
            capacity, demand, distance, transCost = Parser.readVRP(nameOfVRP)
            probDef = ProblemDefinition(capacity, demand, distance, transCost)

            # Choose your operators
            initializer = gaParams["initializer"]
            mutator = gaParams["mutator"]
            recombiner = gaParams["recombiner"]
            selector = gaParams["selector"]
            replacer = gaParams["replacer"]
            terminator = gaParams["terminator"]
            # Add a local searcher if you want LocalSearcher.Idle() does nothing
            localSearcher = LocalSearcher.Idle()

            # Set up GA parameters
            popSize = 100
            nrOffspring = int(popSize / 10)

            # Create Genetic Algorithm instance
            GA = GeneticAlgorithm(initializer, selector, recombiner, mutator, replacer, terminator,
                                  probDef, popSize, nrOffspring, localSearcher)





        except(ValueError):
            raise ValueError("gaParams needs the following entries..")


    @classmethod
    def __initACO(cls, acoParams):

        import ACO
        import Evaporator
        import Initializer
        import Intensifier
        from Problem import TSPProblem
        import SolutionGenerator
        import Heuristics
        import Terminator

        problem = TSPProblem(problem=2)
        initializer = Initializer.TSP_Initializer()
        evaporator = Evaporator.Evaporator(rho=0.05)
        intensifier = Intensifier.Intensifier(delta=0.05)
        heuristic = Heuristics.TSPHeuristic
        solution_gen = SolutionGenerator.PermutationSolutionGenerator(number_of_ants=50, alpha=1, beta=2,
                                                                      heuristic=heuristic, problem=problem)
        terminator = [Terminator.maxItTerminator(maxIt=1), Terminator.convergenceTerminator(maxIter=50)]
        aco = ACO.Ant_Colony_Optimizer(problem, initializer, evaporator, intensifier, solution_gen, terminator, 3,
                                       True, True)
        return aco

    def __findPlan(self):
        bestIndividual, results = self.ga.run()


    def __optimizePlan(self):
        solutions, scores = self.aco.run()