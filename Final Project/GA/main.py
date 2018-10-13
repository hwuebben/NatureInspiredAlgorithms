import Initializer, Mutator, Recombiner,Selector, Replacer, Terminator, LocalSearcher
from GeneticAlgorithm import GeneticAlgorithm
from ProblemDefinition import ProblemDefinition
from Benchmark import Benchmark
from Parser import Parser

nameOfVRP = "VRP1"

# Set up an example problem
capacity,demand,distance,transCost = Parser.readVRP(nameOfVRP)
probDef = ProblemDefinition(capacity,demand,distance,transCost)

gaParams = {
            "initializer":Initializer.RandomInitializer(),
            "mutators": [Mutator.RandomSwapMutatorJit(mutationProb=0.01,dynAdapt=True),
                         #Mutator.RandomMutator()
            ],
            "recombiner":Recombiner.SmartInspirationalRecombinerJit(recombineRatio=0.01,dynAdapt=True),
            "selector": Selector.RouletteSelector(),
            "replacer": Replacer.RouletteReplacer(includeBest=True,dynAdapt=True),
            "terminators": [#Terminator.convergenceTerminator(100,0.001),
                           Terminator.maxRuntimeTerminator(5*60)],
            "localSearcher": LocalSearcher.TspTourSimplifierQuickJit(singleIteration=False),
            #"localSearcher": LocalSearcher.Idle(),
            "popSize": 1000,
            "includeUnmutated": True,
            "offspringProp": 0.5,
            "verbose": True
}


# Create Genetic Algorithm instance
GA = GeneticAlgorithm(gaParams["initializer"], gaParams["selector"], gaParams["recombiner"], gaParams["mutators"],
                      gaParams["replacer"], gaParams["terminators"],probDef, gaParams["popSize"], gaParams["offspringProp"],
                      gaParams["localSearcher"],gaParams["includeUnmutated"],gaParams["verbose"])
bestIndividual = GA.run()
print("best Individuals fitness: ", bestIndividual.fitness)

