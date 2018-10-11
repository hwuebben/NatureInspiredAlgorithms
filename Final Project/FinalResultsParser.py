import os
from matplotlib import pyplot as plt
import numpy as np
import pickle
import copy

def timestampsToTimes(resultDict):
    out = {}
    for runtime,timestampRes in resultDict.items():
        items = timestampRes.items()
        newTSR = {}
        for timestamp,resultsDict in items:
            time = timestampToTime(timestamp)
            #replace the timestamp key with the time key
            newTSR[time] = timestampRes[timestamp]
        out[runtime] = newTSR
    return out
# def timestampsToTimes(resultDict):
#     for runtime,timestampRes in resultDict.items():
#         #items = timestampRes.items()
#         keys = list(timestampRes.keys())
#         for key in keys:
#             timestampRes[timestampToTime(key)] = timestampRes[key]
#             timestampRes.pop(key)
#     return resultDict


def timestampToTime(timestamp):
    #print(timestamp)
    year,month,day,hour,minute,second = timestamp.split("-")
    #ignore year month day
    time = int(hour+minute+second[0:-2])
    return time

def calcOverallRes(vehicleRes, problemName):
    if problemName == "VRP1":
        VRPcosts = np.array([9,9,9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9 ,9, 9, 9, 9, 1,3 ,13, 13, 13, 13, 13, 13, 15, 15, 15, 15, 18, 18])
    if problemName == "VRP2":
        VRPcosts = np.array([8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 12, 12, 12, 12, 12, 12, 12, 16, 16, 16, 16, 19, 19 ])
    vehicleResArr = np.zeros(VRPcosts.size)
    problems = np.zeros(VRPcosts.size,dtype=object)
    solutions = np.zeros(VRPcosts.size,dtype=object)
    for i,results in vehicleRes.items():
        vehicleResArr[i] = results[2]
        problems[i] = results[1]
        solutions[i] = results[0]
    return problems, solutions, np.sum(vehicleResArr * VRPcosts)
directory = "."

resultsVRP1 = {}
resultsVRP2 = {}
# nrVehiclesVRP1 = 10 #?
# nrVehiclesVRP2 = 10 #?
problemName = "VRP2"
for filename in os.listdir(directory):
    currentProblemName, _,runtime,_,_,vehicleID,timestamp = filename.split("_")
    runtime = int(runtime)
    vehicleID = int(vehicleID)
    #print(filename)
    results = pickle.load(open(directory+"\\"+filename,"rb"))
    problem, bestSol, bestScore = results

    if currentProblemName == "VRP1":
        resultDict = resultsVRP1
    if currentProblemName == "VRP2":
        resultDict = resultsVRP2
    try:
        runtimeDict = resultDict[runtime]
    except:
        resultDict[runtime] ={}
        runtimeDict = resultDict[runtime]
    try:
        runtimeDict[timestamp][vehicleID] = results
    except:
        runtimeDict[timestamp] = {}
        runtimeDict[timestamp][vehicleID] = results
if problemName == "VRP1":
    resultsVRP=timestampsToTimes(resultsVRP1)
if problemName == "VRP2":
    resultsVRP=timestampsToTimes(resultsVRP2)

allBestScore = np.inf
allBestProbsAndSols = np.empty(2,dtype=object)
print("start loop")
for runtimeRes, timesRes in resultsVRP.items():
    scores = []
    times = []
    problems = []
    solutions = []
    for time, vehicleRes in timesRes.items():
        print("time: ",time)
        problem,solution,score = calcOverallRes(vehicleRes,problemName)
        scores.append(score)
        problems.append(problem)
        solutions.append(solutions)
        times.append(time)
        #print("test")
    # fig = plt.figure("results for "+problemName+" "+str(runtimeRes)+" seconds runtime")
    # plt.xlabel("percent of runtime")
    # plt.ylabel("score")
    # plt.title("results for "+problemName+" "+str(runtimeRes)+" seconds runtime")

    sortArgs = np.argsort(times)
    times = np.array(times)[sortArgs]
    scores = np.array(scores)[sortArgs]
    problems = np.array(problems)[sortArgs]
    solutions = np.array(solutions)[sortArgs]

    bestScore = np.inf
    print("test1")
    for i,time in enumerate(times):
        print("test2")
        if scores[i] < bestScore:
            #plt.plot(time,scores[i],"ro")
            bestScore = scores[i]
            if bestScore < allBestScore:
                allBestScore = bestScore
                allBestProbsAndSols[0] = problems[i]
                allBestProbsAndSols[1] = solutions[i]

    print(runtimeRes)

    # plt.suptitle("best score: "+str(bestScore))
    # #plt.show()
    # fig.savefig("results for "+problemName+" "+str(runtimeRes)+" seconds runtime")
print("done")
np.savetxt("AllBest for "+problemName,allBestProbsAndSols)








