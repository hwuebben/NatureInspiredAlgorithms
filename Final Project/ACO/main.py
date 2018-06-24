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
solution_gen = SolutionGenerator.PermutationSolutionGenerator(number_of_ants=50, alpha=1, beta=2, heuristic=heuristic, problem=problem)
terminator = [Terminator.maxItTerminator(maxIt=1), Terminator.convergenceTerminator(maxIter=50)]
aco = ACO.Ant_Colony_Optimizer(problem, initializer, evaporator, intensifier, solution_gen, terminator, 3, True, True)

solutions, scores = aco.run()