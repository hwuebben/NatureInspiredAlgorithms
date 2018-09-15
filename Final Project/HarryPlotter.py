import os
import matplotlib.pyplot as plt
import pickle

gaInsts = []
for filename in os.listdir("C:\\Users\\Henning\\git\\NatureInspiredAlgorithms\\Final Project"):
    if not filename.endswith(".p"):
        continue
    #print(filename)
    gaInst = pickle.load(open(filename,"rb"))
    gaInsts.append(gaInst)

plt.plot([x.nrIt for x in gaInsts],[x.getNthbestInd(0).fitness for x in gaInsts],"bo")
plt.show()