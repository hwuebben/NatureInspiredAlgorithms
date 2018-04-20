import numpy as np
import Initializer,Mutator,Recombiner,Selector,Replacer, Terminator, LocalSearcher
from GeneticAlgorithm import GeneticAlgorithm
#from ProblemDefinition import ProblemDefinition as PD
from Individual import Individual
from Benchmark import Benchmark

#choose your modules
initializer = Initializer.RandomInitializer()
mutator = Mutator.RandomMutator(0.5)
recombiner = Recombiner.CrossoverRecombiner()
selector = Selector.TournamentSelector(2)
replacer = Replacer.bottomReplacer()
terminator = Terminator.maxRuntimeTerminator(10)
#add a local searcher if you want LocalSearcher.Idle() does nothing
localSearcher = LocalSearcher.HillClimber()

#set up the module set
moduleSet = [initializer,mutator,recombiner,selector,replacer,terminator]

#set up an example problem
probDef = Benchmark.benchmark1()

#set up GA parameters
popSize = 100
nrOffspring = int(popSize/10)

#create Genetic Algorithm instance
GA = GeneticAlgorithm(moduleSet,probDef,popSize,nrOffspring,localSearcher)
bestIndividual = GA.run()
print("best Individuals fitness: ",bestIndividual.getFitness())

