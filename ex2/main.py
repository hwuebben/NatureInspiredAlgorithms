import numpy as np
import Initializer,Mutator,Recombiner,Selector,Replacer, Terminator
from GeneticAlgorithm import GeneticAlgorithm
from ProblemDefinition import ProblemDefinition as PD
from Individual import Individual

#choose your modules
initializer = Initializer.RandomInitializer()
mutator = Mutator.RandomMutator()
recombiner = Recombiner.CrossoverRecombiner()
selector = Selector.RouletteSelector()
replacer = Replacer.bottomReplacer()
terminator = Terminator.maxRuntimeTerminator(10)

#set up the module set
moduleSet = [initializer,mutator,recombiner,selector,replacer,terminator]

#set up an example problem
probDef = [10,np.arange(100)]

#set up GA parameters
popSize = 100
nrOffspring = int(popSize/10)

#create Genetic Algorithm instance
GA = GeneticAlgorithm(moduleSet,probDef,popSize,nrOffspring)
bestIndividual = GA.run()
print("best Individuals fitness: ",bestIndividual.getFitness())

