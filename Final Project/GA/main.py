import Initializer, Mutator, Recombiner,Selector, Replacer, Terminator, LocalSearcher
from GeneticAlgorithm import GeneticAlgorithm
from ProblemDefinition import ProblemDefinition
from Benchmark import Benchmark
from Parser import Parser
import datetime
nameOfVRP = "VRP2"

# Set up an example problem
capacity,demand,distance,transCost = Parser.readVRP(nameOfVRP)
probDef = ProblemDefinition(capacity,demand,distance,transCost)

gaParams = {
            "initializer":Initializer.HeuristicInitializer(),
            "mutators": [Mutator.RandomSwapMutatorJit(),
                         #Mutator.RandomMutator()
            ],
            "recombiner":Recombiner.SmartInspirationalRecombinerJit(recombineRatio=0.001,dynAdapt=True),
            "selector": Selector.RouletteSelector(),
            #"replacer": Replacer.RouletteReplacer(includeBest=True, dynAdapt=True),
            "replacer": Replacer.KeepBestReplacer(dynAdapt=True),
            "terminators": [#Terminator.convergenceTerminator(100,0.001),
                           Terminator.maxRuntimeTerminator(30*60)],
            #"localSearcher": LocalSearcher.TspTourSimplifierQuickJit(singleIteration=True),
            "localSearcher": LocalSearcher.Idle(),
            "popSize": 500,
            "includeUnmutated": False,
            "offspringProp": 0.5,
            "verbose": True
}
timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
print(timestamp)
print("initializer: ",type(gaParams["initializer"]).__name__)
print("Replacer: ",type(gaParams["replacer"]).__name__)

try:
    singleIter = gaParams["localSearcher"].singleIteration
except:
    singleIter = "---"
print("localSearcher: ",type(gaParams["localSearcher"]).__name__," singleIteration: ",singleIter)
print("popSize: ",gaParams["popSize"])
print("recombRatio: ",gaParams["recombiner"].recombineRatio)
# Create Genetic Algorithm instance
GA = GeneticAlgorithm(gaParams["initializer"], gaParams["selector"], gaParams["recombiner"], gaParams["mutators"],
                      gaParams["replacer"], gaParams["terminators"],probDef, gaParams["popSize"], gaParams["offspringProp"],
                      gaParams["localSearcher"],gaParams["includeUnmutated"],gaParams["verbose"])
bestIndividual = GA.run()
print("best Individuals fitness: ", bestIndividual.fitness)

