from ACO import *
from Evaporator import *
from Initializer import *
from Intensifier import *
from Problem import VehicleRoutingProblem
from SolutionGenerator import *
from Heuristics import TSPHeuristic
from Terminator import *
import time


problem = VehicleRoutingProblem(problem=1, selection='sufficient', criterion='cost_per_item_and_capacity', objective='min')
initializer = VRP_Initializer()
evaporator = Evaporator(rho=0.05)
intensifier = Intensifier(delta=0.05)
heuristic = TSPHeuristic
solution_gen = PermutationSolutionGenerator(number_of_ants=80, alpha=1, beta=2, heuristic=heuristic,
                                            problem=problem, parallel=True)
terminator = [maxItTerminator(maxIt=1000), convergenceTerminator(maxIter=20)]

num_of_vehicles = problem.capacity.shape[0]
num_of_nodes = problem.demand.shape[0] + 1
print('Number of vehicles: ' + str(num_of_vehicles))
print('Number of customers: ' + str(num_of_nodes-1))
print('Total demand: ' + str(np.sum(problem.demand)))
print('Total capacity: ' + str(np.sum(problem.capacity)))
print('Capacity: ' + str(problem.capacity))
print('Transportation cost: \n' + str(problem.transportation_cost))
print('Transportation cost per item: \n' + str(problem.transportation_cost / problem.capacity))
print('Preferred sufficient vehicles: \n' + str(problem.selected_vehicles))
print('Size of integrated search space: ' + str(2*(num_of_nodes**num_of_vehicles)))
print('Size of sequential search space: ' + str(num_of_nodes**2 * num_of_vehicles))

aco = Ant_Colony_Optimizer(problem, initializer, evaporator, intensifier, solution_gen, terminator, 4, True, True)

startTime = time.time()
solutions, scores = aco.run()
print('Runtime: ' + str(time.time() - startTime) + ' seconds')

all_nodes = None
for vehicle_solution in aco.best_solution[0]:
    if all_nodes is None:
        all_nodes = vehicle_solution
    else:
        all_nodes = np.concatenate((all_nodes, vehicle_solution))
all_nodes = np.arange(num_of_nodes)[np.bincount(all_nodes) > 1]
print('Redundant customers: \n' + str(all_nodes))
print('Best score: ' + str(aco.best_score))
print('Best solution: \n' + str(aco.best_solution))