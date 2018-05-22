import numpy as np

class DifferentialEvolution:

    def __init__(self,initializer, selector, recombiner, mutator, terminator):
        self.initializer = initializer
        self.selector = selector
        self.recombiner = recombiner
        self.mutator = mutator
        self.terminator = terminator

        self.pop = self.initializer.initialize()
        self.nrIt = 0

    def run(self):
        while not any([t.checkTermination(self) for t in self.terminator]):
            donor_pop = self.mutator.mutate_population(self.pop)
            trial_pop = self.recombiner.get_trials(self.pop,donor_pop)
            self.pop = self.selector.select(self.pop, trial_pop)
        return self.pop