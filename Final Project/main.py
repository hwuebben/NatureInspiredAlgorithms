from VRPsolver import VRPsolver
from Parser import Parser
from GA.ProblemDefinition import ProblemDefinition

from GeneticAlgorithm import GeneticAlgorithm
from ProblemDefinition import ProblemDefinition

def initGA():

    from Benchmark import Benchmark
    nameOfVRP = "VRP1"
    # Set up an example problem
    capacity, demand, distance, transCost = Parser.readVRP(nameOfVRP)
    probDef = ProblemDefinition(capacity, demand, distance, transCost)
    # Choose your operators
    initializer = Initializer.RandomInitializer()
    mutator = Mutator.SwapMutator()
    recombiner = Recombiner.MeanRecombiner()
    selector = Selector.TournamentSelector(s=20, dynAdapt=True)
    replacer = Replacer.bottomReplacer()
    terminator = Terminator.maxRuntimeTerminator(100)
    # Add a local searcher if you want LocalSearcher.Idle() does nothing
    localSearcher = LocalSearcher.Idle()
    # Set up GA parameters
    popSize = 100
    nrOffspring = int(popSize / 10)
    # Create Genetic Algorithm instance
    ga = GeneticAlgorithm(initializer, selector, recombiner, mutator, replacer, terminator,
                          probDef, popSize, nrOffspring, localSearcher)
    return ga

def initACO():
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
    aco = ACO.Ant_Colony_Optimizer(problem, initializer, evaporator, intensifier, solution_gen, terminator, 3, True,
                                   True)
    return aco


nameOfVRP = "VRP1"
capacity, demand, distance, transCost = Parser.readVRP(nameOfVRP)
probDef = ProblemDefinition(capacity, demand, distance, transCost)

from GA import Initializer, Mutator, Recombiner, Selector, Replacer, Terminator, LocalSearcher
gaParams = {
            "initializer":Initializer.RandomInitializer(),
            "mutator": Mutator.SwapMutator(),
            "recombiner":Recombiner.MeanRecombiner(),
            "selector": Selector.TournamentSelector(s=20, dynAdapt=True),
            "replacer": Replacer.bottomReplacer(),
            "terminator": Terminator.maxRuntimeTerminator(10),
            "localSearcher": LocalSearcher.Idle(),
            "popSize": 100
}

from ACO import Initializer, Evaporator, Intensifier, Heuristics,Terminator
acoParams = {
            "initializer": Initializer.TSP_Initializer(),
            "evaporator":Evaporator.Evaporator(rho=0.05),
            "intensifier":Intensifier.Intensifier(delta=0.05),
            "heuristic":Heuristics.TSPHeuristic,
            "nrAnts":50,
            "alpha":1,
            "beta":2,
            "terminators":[Terminator.maxItTerminator(maxIt=1), Terminator.convergenceTerminator(maxIter=50)]

}

vrpSolver = VRPsolver(probDef)
bestScore = vrpSolver.optimizeWithParams(gaParams,acoParams)
print("Overall best Sol value: ",bestScore)
