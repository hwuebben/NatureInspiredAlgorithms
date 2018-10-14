from ACO import *
from Evaporator import *
from Initializer import *
from Intensifier import *
from Problem import VehicleRoutingProblem
from SolutionGenerator import *
from Heuristics import TSPHeuristic
from Terminator import *
import time

# Setup of all ACO components
problem = VehicleRoutingProblem(problem=2)
initializer = VRP_Initializer()
evaporator = Evaporator(rho=0.05)
intensifier = Intensifier(delta=0.075)
heuristic = TSPHeuristic
solution_gen = VRPSolutionGenerator(number_of_ants=100, alpha=2, beta=5, heuristic=heuristic, problem=problem)
terminator = [maxItTerminator(maxIt=3), convergenceTerminator(maxIter=20)]

# Print the Vehicle Routing Problem
vehicles = problem.capacity.shape[0]
items = problem.demand.shape[0] + 1
print('Number of vehicles: ' + str(vehicles))
print('Number of customers: ' + str(items - 1))
print('Total demand: ' + str(np.sum(problem.demand)))
print('Total capacity: ' + str(np.sum(problem.capacity)))
print('Capacity: ' + str(problem.capacity))
print('Transportation cost: \n' + str(problem.transportation_cost))
print('Transportation cost per item: \n' + str(problem.transportation_cost / problem.capacity))


# Instantiate the ACO
aco = AntColonyOptimizer(problem, initializer, evaporator, intensifier, solution_gen, terminator, 3, True, True)

# Run the ACO optimizer
startTime = time.time()
solutions, scores = aco.run()
print('Runtime: ' + str(time.time() - startTime) + ' seconds')
print('Runtime per iteration: ' + str((time.time() - startTime) / solutions.shape[0]) + ' seconds')

all_nodes = None
best_solution = np.array(aco.best_solution)
for vehicle in range(problem.vehicles):
    if all_nodes is None:
        all_nodes = (best_solution[vehicle] - 1) % aco.problem.get_size()
    else:
        all_nodes = np.concatenate((all_nodes, (best_solution[vehicle] - 1) % aco.problem.get_size()))
all_nodes = np.arange(problem.get_size())[np.bincount(all_nodes) > 1]
print('Redundant customers: \n' + str(all_nodes))

print('Best score: ' + str(aco.best_score))

# Receive best solution and print some additional info
zero_vehicles = list()
selected_vehicles = list()
best_solution = np.array(aco.best_solution[:, 1:])
for vehicle in range(problem.vehicles):
    if np.sum((best_solution[vehicle] - 1) % aco.problem.get_size()) == 0:
        zero_vehicles.append(vehicle)
    else:
        best_solution[vehicle][best_solution[vehicle] > 0] \
            = (best_solution[vehicle][best_solution[vehicle] > 0] - 1) % problem.get_size()
        selected_vehicles.append(vehicle)
best_solution = np.delete(best_solution, zero_vehicles, 0)
print('Selected vehicles: \n' + str(selected_vehicles))
print('Capacity of Selected vehicles: \n' + str(problem.capacity[selected_vehicles]))
print('Best solution: \n' + str(best_solution))