from Initializer import *
from Mutator import *
from Recombiner import *
from Selector import *
from Terminator import *
from DifferentialEvolution import DifferentialEvolution

"""Set up DE parameters"""
#pop size
NP = 90
#scale Factor
F = 0.6
#crossover rate
Cr = 0.5

# choose problem
problem = Problem(1)
#set xMin
xMin = np.zeros(9)
#set xMax (what are good values here?)
xMax = np.concatenate((np.array(problem.k) * np.array(problem.m), problem.md, problem.mp))
xMax *= [1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1]

# Choose your operators
initializer = RandomInitializer(NP, xMin, xMax, problem)
#mutator = randMutator(F, problem)
mutator = bestMutator(F, problem)
#recombiner = ExponentialCrossover(Cr, problem)
recombiner = BinomialCrossover(Cr, problem)
selector = DEselector()
terminator = [maxItTerminator(2000), convergenceTerminator(200)]

# Create Genetic Algorithm instance
DE = DifferentialEvolution(initializer, selector, recombiner, mutator, terminator, True)
bestIndividual, results, generations = DE.run()
print("best Individuals fitness: ", problem.targetFunc(bestIndividual.x))
print("best individual: ", bestIndividual.x.reshape(3,3))
print(np.sum(bestIndividual.x.reshape(3,3), axis=1))
print(Problem.validate(bestIndividual))
