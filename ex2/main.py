import Initializer, Mutator, Recombiner,Selector, Replacer, Terminator, LocalSearcher
from GeneticAlgorithm import GeneticAlgorithm
from ProblemDefinition import ProblemDefinition
from Benchmark import Benchmark

# Choose your operators
initializer = Initializer.RandomInitializer()
mutator = Mutator.RandomMutator(0.2, dynAdapt=True)
recombiner = Recombiner.CrossoverRecombiner()
selector = Selector.TournamentSelector(s=20, dynAdapt=True)
replacer = Replacer.bottomReplacer()
terminator = Terminator.maxRuntimeTerminator(10)
# Add a local searcher if you want LocalSearcher.Idle() does nothing
localSearcher = LocalSearcher.Idle()

# Set up the module set
moduleSet = [initializer, mutator, recombiner, selector, replacer, terminator]

# Set up an example problem
nrMachines, jobRuntimes = Benchmark.benchmark1()
probDef = ProblemDefinition(nrMachines, jobRuntimes)

# Set up GA parameters
popSize = 100
nrOffspring = int(popSize/10)

# Create Genetic Algorithm instance
GA = GeneticAlgorithm(moduleSet, probDef, popSize, nrOffspring, localSearcher)
bestIndividual = GA.run()
print("best Individuals fitness: ", bestIndividual.fitness)

