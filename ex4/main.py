import Initializer, Mutator, Recombiner,Selector, Terminator
from DifferentialEvolution import DifferentialEvolution

"""Set up DE parameters"""
#pop size
NP = 100
#scale Factor
F = 1
#crossover rate
Cr = 1


# Choose your operators
initializer = Initializer.RandomInitializer()
mutator = Mutator.DEmutator(F)
recombiner = Recombiner.BinomialCrossover(Cr)
selector = Selector.DEselector()
terminator = Terminator.maxRuntimeTerminator(10)

# Create Genetic Algorithm instance
DE = DifferentialEvolution(NP,F,Cr,initializer, selector, recombiner, mutator, terminator)
bestIndividual, results = DE.run()
print("best Individuals fitness: ", bestIndividual.tarFuncVal)

