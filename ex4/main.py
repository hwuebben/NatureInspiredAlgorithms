import Initializer, Mutator, Recombiner,Selector, Terminator
from DifferentialEvolution import DifferentialEvolution
import numpy as np
"""Set up DE parameters"""
#pop size
NP = 100
#scale Factor
F = 1
#crossover rate
Cr = 1
#set xMin
xMin = np.zeros(9)
#set xMax (what are good values here?)
xMax = np.ones(9) * 100


# Choose your operators
initializer = Initializer.RandomInitializer(NP,xMin,xMax)
mutator = Mutator.DEmutator(F)
recombiner = Recombiner.BinomialCrossover(Cr)
selector = Selector.DEselector()
terminator = Terminator.maxRuntimeTerminator(10)

# Create Genetic Algorithm instance
DE = DifferentialEvolution(initializer, selector, recombiner, mutator, terminator)
bestIndividual, results = DE.run()
print("best Individuals fitness: ", bestIndividual.tarFuncVal)

