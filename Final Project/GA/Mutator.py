from abc import ABC, abstractmethod
import numpy as np
from Individual import Individual
from ProblemDefinition import ProblemDefinition


class Mutator(ABC):

    @abstractmethod
    def mutate(self,toMutate:Individual,probDef:ProblemDefinition)->Individual:
        pass

    def dynamicAdaptation(self, progress):
        pass

class RandomMutator(Mutator):

    def mutate(self, toMutate:Individual,probDef:ProblemDefinition):
        """
        :param toMutate:
        :return: mutated individual
        """
        #TODO: how many mutation should be performed per function call?
        #calculate currently delivered goods (loads) per vehicle
        loads = np.sum(toMutate.assign, 0)
        for i,NodeAssign in enumerate(toMutate.assign):
            #calculate redInd, the indice that should be reduced
            redInd = np.random.choice(np.argwhere(NodeAssign > 0).flatten())
            #and incInd the one that should be increased
            incInds = np.argwhere(loads < probDef.capacity).flatten()
            #make sure not to choose the same index as redInd (would do nothing then)
            #leaving this line out allows strength of mutation to vary randomly, might not be bad
            #incInds = np.delete(incInds,np.argwhere(incInds == redInd))
            incInd = np.random.choice(incInds)

            toMutate.assign[i,redInd] -= 1
            toMutate.assign[i,incInd] += 1
            loads[redInd] -= 1
            loads[incInd] += 1
            #toMutate.checkConsistency(probDef)



class RearrangeRecombiner(Mutator):
    def mutate(self,toMutate:Individual,probDef:ProblemDefinition):
        loads = np.sum(toMutate.assign,0)
        #for each node
        for assigned in toMutate.assign:
            # get indices of fractal assignments
            fracInds = np.argwhere(assigned%1 != 0).flat
            # get those inds that have to be reduced (because capacity is already full)
            capInds = np.intersect1d(np.argwhere(loads - probDef.capacity == 0).flat, fracInds)
            #boolean mask of fracInds to keep track of indices that have been processed
            mask = np.ones(len(fracInds), dtype=bool)
            #first process the indices that have to be reduced
            deficit = 0
            for capInd in capInds:
                toMutate.assign[capInd] -= 0.5
                deficit += 0.5
                mask[fracInds==capInd] = False
            #then process the rest of fracInds
            while mask.any():
                maxInd = np.argmax(assigned[fracInds[mask]])
                assigned[fracInds[mask][maxInd]] += 0.5
            #TODO: stopped here


class SwapMutator(Mutator):
    def __init__(self,swapRatio = 0.1):
        self.swapRatio = swapRatio
        self.origSwapRatio = swapRatio
    def mutate(self,toMutate:Individual,probDef:ProblemDefinition):
        nrSwaps = max(1,int(probDef.nrNodes * self.swapRatio))
        for _ in range(nrSwaps):
            #calculate free capacities
            loads = np.sum(toMutate.assign, 0)
            freeCaps = probDef.capacity - loads
            #find random index to swap
            randInd = [np.random.randint(0,probDef.nrNodes),np.random.randint(0,probDef.nrVehicles)]
            #get corresponding assignment
            assignment = toMutate.assign[randInd[0]]
            #create shuffled indices
            randIndsSwap = np.arange(0,probDef.nrVehicles)
            np.random.shuffle(randIndsSwap)
            #try them 1 by 1
            for randIndSwap in randIndsSwap:
                isSuited = (assignment[randIndSwap] <= freeCaps[randInd[1]]) and (assignment[randInd[1]] <= freeCaps[randIndSwap])
                #also make sure to not swap two identical values
                isSuited = isSuited and (assignment[randIndSwap] != assignment[randInd[1]])
                if isSuited:
                    #do the swap:
                    ass = assignment[randIndSwap]
                    assignment[randIndSwap] = assignment[randInd[1]]
                    assignment[randInd[1]] = ass
                    break
        toMutate.recalcFitness()
        #return toMutate

    def dynamicAdaptation(self, progress):
        self.swapRatio = (1-progress) * self.origSwapRatio

class IdleMutator(Mutator):
    def mutate(self,toMutate:Individual,probDef:ProblemDefinition):
        pass

class assignMutator(Mutator):
    def __init__(self,remProb:float = 0.5):
        """
        set remProb
        :param remProb:
        """
        self.remProb = remProb
    def mutate(self,toMutate:Individual,probDef:ProblemDefinition):
        """
        remove vehicle from node with prob remProb
        add vehicle to node with prob 1-remProb
        :param toMutate:
        :param probDef:
        :return:
        """
        shallRem = np.random.rand() <= self.remProb
        #TODO: implement


