import pickle as pkl
import os
import numpy as np

def get_tc(problem):
    path = '.\\VRP_Examples\\'+vrp+'\\transportation_cost.txt'
    with open(path,'r') as fp:
        line = fp.readline()
        line = line.split(' ')[:-1]
        capacities = [int(x) for x in line]
    return capacities

def get_distance_matrix(problem):
    path = '.\\VRP_Examples\\'+vrp+'\\distance.txt'
    result = []
    with open(path,'r') as fp:
        for line in fp.readlines():
            line = line.split(' ')[:-1]
            capacities = [int(x) for x in line]
            result.append(np.array(capacities))
    return np.array(result)

def get_arvin_solutions(problem):
    if 'VRP1' == problem:
        path = 'arvin_'+vrp+'.txt'
    else:
        path = 'arvin_'+vrp+'.txt'
    with open(path,'r') as fp:
        selected = eval(fp.readline())
        routes = eval(fp.readline())
    return selected, routes

def get_transportation_cost_per_vehicle(route, dist_matrix, cost):
    if type(route) == int:
        return 0
    t_cost = np.sum(dist_matrix[route[:-1],route[1:]]) + dist_matrix[route[-1],0]
    if route[0] != 0:
        t_cost += dist_matrix[0,route[0]]
    t_cost = t_cost * cost
    return t_cost

def tc_for_all_vehicles(routes, dist_matrix, costs):
    final_result = 0
    for i in range(len(costs)):
        final_result += get_transportation_cost_per_vehicle(routes[i],dist_matrix,costs[i])
    return final_result

def get_henning_solution(vrp):
    file = pkl.load(open('bestSol10MinuteRun'+vrp+'.p','rb'))
    return pkl.load(open('bestSol10MinuteRun'+vrp+'.p','rb')).solution['solsByVehicle'], file.solution['assignments']

def decocde_single(car_id,route, assign):
    if type(route) == int:
        return np.array([0,0])
    indices = np.arange(0,len(assign))
    actual_route = indices[assign != 0] + 1
    actual_route = np.hstack((0,actual_route))
    actual_route = actual_route[route]
    return actual_route

def decode_henning_solution(num_cars, routes, assign):
    #routes = np.asarray(routes)
    for i in range(num_cars):
        if type(routes[i]) == int:
            continue
        routes[i] = decocde_single(i,routes[i][:],assign[:,i])
    return routes

def encode_arvin(num_cars,selected, routes):
    result = [0]*num_cars
    for i,car in enumerate(selected):
        result[car] = routes[i]
    return result


vrp = 'VRP2'

# get transportation cost per vehicle
file, assign = get_henning_solution(vrp)
routes = decode_henning_solution(len(file), file, assign)
tc = get_tc(vrp)
print(tc)
print(len(tc))

# get distance metric
dists = get_distance_matrix(vrp)
print(dists.shape)
print(dists)

print('Costs:',tc_for_all_vehicles(routes, dists, tc))

selected, routes = get_arvin_solutions(vrp)
enc_routes = encode_arvin(len(tc), selected, routes)
print(tc_for_all_vehicles(enc_routes, dists, tc))