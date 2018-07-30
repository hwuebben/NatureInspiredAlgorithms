from matplotlib import pyplot as plt

results = open("Results.txt")

costs  = []
fitnesses = []

for line in results:
   cue0 = "next individual fitness:"
   if line[0:len(cue0)] == cue0:
       fitness = float(line[len(cue0)::])
       fitnesses.append(fitness)
   cue1 = "result:"
   if line[0:len(cue1)] == cue1:
        cost = float(line[len(cue1)::])
        costs.append(cost)


plt.plot(fitnesses,costs,"bo")
plt.show()
