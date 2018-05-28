import numpy as np

class DifferentialEvolution:

    def __init__(self,initializer, selector, recombiner, mutator, terminator, verbose):
        self.initializer = initializer
        self.selector = selector
        self.recombiner = recombiner
        self.mutator = mutator
        self.terminator = terminator
        self.verbose = verbose

        self.pop = self.initializer.initialize()
        self.nrIt = 0
        self.best_score = 0

    def run(self):
        results = list()
        while not any([t.checkTermination(self) for t in self.terminator]):
            donor_pop = self.mutator.mutate_population(self.pop)
            trial_pop = self.recombiner.get_trials(self.pop,donor_pop)
            self.pop = self.selector.select(self.pop, trial_pop)
            results.append([x.targFuncVal for x in self.pop])

            self.nrIt += 1
            self.best_score = np.max(self.pop).targFuncVal
            if (self.verbose): print('Iteration: ', self.nrIt,'- Score: ', self.best_score)

        return np.max(self.pop), np.array(results)