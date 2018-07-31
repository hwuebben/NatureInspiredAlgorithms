from abc import ABC, abstractmethod
import numpy as np
from Individual import Individual
from ProblemDefinition import ProblemDefinition
import copy
import random

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
            incInds = np.argwhere(np.logical_and(loads < probDef.capacity, NodeAssign > 0)).flatten()
            #make sure not to choose the same index as redInd (would do nothing then)
            #leaving this line out allows strength of mutation to vary randomly, might not be bad
            #incInds = np.delete(incInds,np.argwhere(incInds == redInd))
            if incInds.size == 0:
                break
            incInd = np.random.choice(incInds)

            toMutate.assign[i,redInd] -= 1
            toMutate.assign[i,incInd] += 1
            loads[redInd] -= 1
            loads[incInd] += 1
            toMutate.recalcFitness()
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

class RandomSwapMutator(Mutator):
    def __init__(self,mutationProb=0.5,dynAdapt = True):
        self.mutationProb = mutationProb
        self.origMutationProb = mutationProb
        self.dynAdapt = dynAdapt

    def mutate(self,toMutate:Individual,probDef:ProblemDefinition):
        #toMutate.checkConsistency(probDef)
        # calculate free capacities
        loads = np.sum(toMutate.assign, 0)
        freeCaps = probDef.capacity - loads
        # try node indices each entry one by one in random order
        mask = np.random.rand(probDef.nrNodes)
        nInds = np.nonzero(mask < self.mutationProb)[0]
        if nInds.size == 0:
            nInds = np.array([np.random.randint(0,probDef.nrNodes)])
        #np.random.shuffle(nInds)
        # try vehicle indices each entry one by one in random order
        vInds = np.arange(probDef.nrVehicles)
        np.random.shuffle(vInds)
        for nInd0 in nInds:
            NodeAssign = toMutate.assign[nInd0]
            nodeIndiceDone = False
            for i,vInd0 in enumerate(vInds):
                if nodeIndiceDone:
                    break
                for vInd1 in vInds[i+1::]:
                    isSuited0 = (NodeAssign[vInd0] != NodeAssign[vInd1])
                    if not isSuited0:
                        continue
                    isSuited1 = (NodeAssign[vInd0] <= (freeCaps[vInd1]+NodeAssign[vInd1])) and (NodeAssign[vInd1] <= (freeCaps[vInd0]+NodeAssign[vInd0]))
                    isSuited = isSuited0 and isSuited1
                    #also make sure to not swap two identical values

                    if isSuited:
                        # do the swap:
                        ass = NodeAssign[vInd0]
                        NodeAssign[vInd0] = NodeAssign[vInd1]
                        NodeAssign[vInd1] = ass
                        #repair freeCaps
                        diff = NodeAssign[vInd0] - NodeAssign[vInd1]
                        freeCaps[vInd0] -= diff
                        freeCaps[vInd1] += diff
                        nodeIndiceDone = True
                        break
            #assert(nodeIndiceDone)
        toMutate.recalcFitness()
        #toMutate.checkConsistency(probDef)

    def dynamicAdaptation(self, progress):
        if not self.dynAdapt:
            return
        self.mutationProb = self.origMutationProb * (1-progress)

class RandomSwapMutator2(Mutator):
    def __init__(self,mutationProb=0.5,dynAdapt = True):
        self.mutationProb = mutationProb
        self.origMutationProb = mutationProb
        self.dynAdapt = dynAdapt

    def mutate(self,toMutate:Individual,probDef:ProblemDefinition):
        #toMutate.checkConsistency(probDef)
        # calculate free capacities
        loads = np.sum(toMutate.assign, 0)
        freeCaps = probDef.capacity - loads
        # try node indices each entry one by one in random order
        mask = np.random.rand(probDef.nrNodes)
        nInds = np.nonzero(mask < self.mutationProb)[0]
        if nInds.size == 0:
            nInds = np.array([np.random.randint(0,probDef.nrNodes)])
        #np.random.shuffle(nInds)
        # try vehicle indices each entry one by one in random order
        vInds = np.arange(probDef.nrVehicles)
        np.random.shuffle(vInds)
        for nInd0 in nInds:
            NodeAssign = toMutate.assign[nInd0]
            for vInd0 in vInds:

                suited0 = (NodeAssign[vInd0] != NodeAssign)
                suited1 = np.logical_and(NodeAssign[vInd0] <= (freeCaps + NodeAssign),NodeAssign <= (freeCaps[vInd0] + NodeAssign[vInd0]))
                suited = np.logical_and(suited0,suited1)
                suitedInds = np.nonzero(suited)[0]
                if suitedInds.size == 0:
                    continue
                #choose random suited
                vInd1 = np.random.choice(suitedInds)
                # do the swap:
                ass = NodeAssign[vInd0]
                NodeAssign[vInd0] = NodeAssign[vInd1]
                NodeAssign[vInd1] = ass
                #repair freeCaps
                diff = NodeAssign[vInd0] - NodeAssign[vInd1]
                freeCaps[vInd0] -= diff
                freeCaps[vInd1] += diff
                break

        toMutate.recalcFitness()
        #toMutate.checkConsistency(probDef)

    def dynamicAdaptation(self, progress):
        if not self.dynAdapt:
            return
        self.mutationProb = self.origMutationProb * (1-progress)


class RandomSwapMutatorGen(Mutator):
    def __init__(self,mutationProb=1,dynAdapt = True):
        self.mutationProb = mutationProb
        self.origMutationProb = mutationProb
        self.dynAdapt = dynAdapt

    def mutate(self,toMutate:Individual,probDef:ProblemDefinition):
        #toMutate.checkConsistency(probDef)
        # calculate free capacities
        loads = np.sum(toMutate.assign, 0)
        freeCaps = probDef.capacity - loads
        # try node indices each entry one by one in random order
        nIndsGen = self.shuffledRangeGen(probDef.nrNodes)
        for nInd0 in nIndsGen:
            NodeAssign = toMutate.assign[nInd0]
            nodeIndiceDone = False
            vIndsGen = self.shuffledRangeGen()
            i = -1
            for vInd0 in vIndsGen:
                i+=1
                if nodeIndiceDone:
                    break
                for vInd1 in vInds[i+1::]:
                    isSuited0 = (NodeAssign[vInd0] != NodeAssign[vInd1])
                    if not isSuited0:
                        continue
                    isSuited1 = (NodeAssign[vInd0] <= (freeCaps[vInd1]+NodeAssign[vInd1])) and (NodeAssign[vInd1] <= (freeCaps[vInd0]+NodeAssign[vInd0]))
                    isSuited = isSuited0 and isSuited1
                    #also make sure to not swap two identical values

                    if isSuited:
                        # do the swap:
                        ass = NodeAssign[vInd0]
                        NodeAssign[vInd0] = NodeAssign[vInd1]
                        NodeAssign[vInd1] = ass
                        #repair freeCaps
                        diff = NodeAssign[vInd0] - NodeAssign[vInd1]
                        freeCaps[vInd0] -= diff
                        freeCaps[vInd1] += diff
                        mutationHappened = True
                        nodeIndiceDone = True
                        break
        toMutate.recalcFitness()
        #toMutate.checkConsistency(probDef)

    def dynamicAdaptation(self, progress):
        if not self.dynAdapt:
            return
        self.mutationProb = self.origMutationProb * (1-progress)


    def shuffledRangeGen(self,maxVal):
        sequence = range(maxVal)
        maxSlice = maxVal
        while len(sequence):
            i = random.randint(0, maxSlice - 1)
            ele = sequence[i]
            sequence[i] = sequence[-1]
            maxSlice -= 1
            yield ele

class SwapMutator(Mutator):
    def __init__(self,swapRatio = 0.1,dynAdapt=True):
        self.swapRatio = swapRatio
        self.origSwapRatio = swapRatio
        self.dynAdapt = dynAdapt
    def mutate(self,toMutate:Individual,probDef:ProblemDefinition):
        #debugCopy = copy.deepcopy(toMutate)
        nrSwaps = max(3,int(probDef.problemSize * self.swapRatio))
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

                isSuited = (assignment[randIndSwap] <= (freeCaps[randInd[1]] + assignment[randInd[1]])) and (assignment[randInd[1]] <= (freeCaps[randIndSwap] + assignment[randIndSwap]))
                #also make sure to not swap two identical values
                isSuited = isSuited and (assignment[randIndSwap] != assignment[randInd[1]])
                if isSuited:
                    #do the swap:
                    ass = assignment[randIndSwap]
                    assignment[randIndSwap] = assignment[randInd[1]]
                    assignment[randInd[1]] = ass
                    break
        toMutate.recalcFitness()
        toMutate.checkConsistency(probDef)
        #assert((toMutate.assign != debugCopy.assign).any())
        #return toMutate

    def dynamicAdaptation(self, progress):
        if not self.dynAdapt:
            return
        self.swapRatio = min(1,(1.1-progress)) * self.origSwapRatio

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


