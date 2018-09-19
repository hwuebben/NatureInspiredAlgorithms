import os
import pickle
import numpy as np


def calcOverallRes(vehicleRes, problemName):
    if problemName == "VRP1":
        VRPcosts = np.array(
            [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 3, 13, 13, 13, 13, 13, 13, 15, 15, 15, 15,
             18, 18])
    if problemName == "VRP2":
        VRPcosts = np.array(
            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 12, 12, 12, 12, 12, 12, 12, 16, 16, 16, 16, 19,
             19])
    vehicleResArr = np.zeros(VRPcosts.size)
    problems = np.zeros(VRPcosts.size, dtype=object)
    solutions = np.zeros(VRPcosts.size, dtype=object)
    for i, results in vehicleRes.items():
        vehicleResArr[i] = results[2]
        problems[i] = results[0]
        solutions[i] = results[1]
    return problems, solutions, np.sum(vehicleResArr * VRPcosts)


problemName = "VRP1"
directory = "finalResults"
resultsVRP1 = {}
resultsVRP2 = {}
for filename in os.listdir(directory):
    currentProblemName, _, runtime, _, _, vehicleID, timestamp = filename.split("_")
    runtime = int(runtime)
    vehicleID = int(vehicleID)
    # print(filename)
    results = pickle.load(open(directory + "\\" + filename, "rb"))
    problem, bestSol, bestScore = results

    if currentProblemName != problemName:
        continue

    if currentProblemName == "VRP1":
        resultDict = resultsVRP1
    if currentProblemName == "VRP2":
        resultDict = resultsVRP2
    try:
        runtimeDict = resultDict[runtime]
    except:
        resultDict[runtime] = {}
        runtimeDict = resultDict[runtime]
    try:
        runtimeDict[timestamp][vehicleID] = results
    except:
        runtimeDict[timestamp] = {}
        runtimeDict[timestamp][vehicleID] = results

if problemName == "VRP1":
    resultsVRP = resultsVRP1
if problemName == "VRP2":
    resultsVRP = resultsVRP2
allBestScore = np.inf
allBestProbsAndSols = np.empty(2, dtype=object)
print("start loop")
bestScore = np.inf
for runtimeRes, timesRes in resultsVRP.items():
    for time, vehicleRes in timesRes.items():
        # print("time: ",time)
        problem, solution, score = calcOverallRes(vehicleRes, problemName)
        if score >= bestScore:
            continue
        bestScore = score
        bestRunTime = time
        bestAcoProblems = problem
        bestAcoSolutions = solution

file2write = open("bestSol" + problemName, 'w')
file2write.write(problemName + "\n")
file2write.write(str(bestScore) + "\n")
file2write.write(bestRunTime + "\n")
file2write.write("problems by vehicles:" + "\n")
for i, prob in enumerate(bestAcoProblems):
    if isinstance(prob, int):
        file2write.write(str(i) + ": " + str(prob) + "\n")
    else:
        file2write.write(str(i) + ": " + np.array2string(prob.distance_matrix) + "\n")
for i,sol in enumerate(bestAcoSolutions):
    if isinstance(sol, int):
        file2write.write(str(i) + ": " + str(sol) + "\n")
    else:
        file2write.write(str(i) + ": " + np.array2string(sol) + "\n")

file2write.close()

# np.savetxt("bestSol"+problemName,bestAcoProblems)
# np.savetxt("bestSol"+problemName,bestAcoSolutions)
# np.savetxt("bestSol"+problemName,bestScore)
# np.savetxt("bestSol"+problemName,bestRunTime)
