import numpy as np
import Initializer,Mutator,Recombiner,Selector,Replacer
from GeneticAlgorithm import GeneticAlgorithm
from ProblemDefinition import ProblemDefinition as PD
from Individual import Individual

#choose your modules
initializer = Initializer.RandomInitializer()
mutator = Mutator.BoundaryMutator()
recombiner = Recombiner.CrossoverRecombiner()
selector = Selector.RouletteSelector()
replacer = Replacer.bottomReplacer()

#set up an example problem
probDef = [10,100,np.arange(100)]
popSize = 100

#create Genetic Algorithm instance
GA = GeneticAlgorithm(initializer,mutator,recombiner,selector,replacer,probDef,popSize)
bestIndividual = GA.run()
print("best Individuals fitness: ",bestIndividual.getFitness())






