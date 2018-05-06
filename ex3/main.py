from ACO import *
from Evaporator import *
from Initializer import *
from Intensifier import *
from Problem import TSPProblem
from SolutionGenerator import *
from Heuristics import TSPHeuristic
from Terminator import *


problem = TSPProblem(problem=2)
initializer = TSP_Initializer()
evaporator = Evaporator(rho=0.05)
intensifier = Intensifier(delta=0.05)
heuristic = TSPHeuristic
solution_gen = PermutationSolutionGenerator(number_of_ants=50, alpha=1, beta=2, heuristic=heuristic, problem=problem)
terminator = [maxItTerminator(maxIt=2000), convergenceTerminator(maxIter=50)]
aco = Ant_Colony_Optimizer(problem, initializer, evaporator, intensifier, solution_gen, terminator, 3, True, True)

solutions, scores = aco.run()