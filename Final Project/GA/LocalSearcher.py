from abc import ABC, abstractmethod
import numpy as np
from GA.ProblemDefinition import ProblemDefinition as PD
import numba

class LocalSearcher(ABC):
    @abstractmethod
    def search(self, ind, probDef):
        pass
    def dynamicAdaptation(self,progress):
        pass


class HillClimber(LocalSearcher):

    def search(self, ind, firstChoice=False, nh="swap"):
        done = False
        sol = ind
        while not done:
            sol0 = self.__climb(sol, firstChoice, nh)
            if sol0 == sol:
                done = True
            sol = sol0
        return sol

    def __climb(self, ind, firstChoice, nh):
        # currently best solution
        bq = ind.fitness
        bSol = ind
        for n in self.__getNeighborhood(ind, nh):
            cq = n.fitness
            if cq > bq:
                bq = cq
                bSol = n
                if firstChoice:
                    return bSol
        return bSol

    @staticmethod
    def __getNeighborhood(ind, nh):
        if nh == "swap":
            return ind.swapNH()
        elif nh == "transpose":
            return ind.transposeNH()

class TspTourSimplifierQuick(LocalSearcher):
    def __init__(self,singleIteration=True):
        self.singleIteration = singleIteration
    """
    Tries to simplify tsp tours, by identifying redundant vehicles.
    """
    def search(self, ind,probDef):
        # loads
        loads = np.sum(ind.assign, 0)
        # remaining capacities
        remCaps = probDef.capacity - loads
        changesMadeTotal = False
        while True:
            changesMadeIter = False
            for nodeAssign in ind.assign:
                inds = np.nonzero(nodeAssign > 0)[0]
                maxInd = np.argmax(remCaps[inds])
                minAssignInd = np.argmin(nodeAssign[inds])
                #check whether the smallest assignment can be removed (taken over)
                if (maxInd != minAssignInd) and (remCaps[inds[maxInd]] >= nodeAssign[inds[minAssignInd]]):
                    nodeAssign[inds[maxInd]] += nodeAssign[inds[minAssignInd]]
                    #fix remCaps
                    remCaps[inds[maxInd]] -= nodeAssign[inds[minAssignInd]]
                    remCaps[inds[minAssignInd]] += nodeAssign[inds[minAssignInd]]
                    #set to zero
                    nodeAssign[inds[minAssignInd]] = 0
                    changesMadeIter = True
                    changesMadeTotal = True
            #break if singleIteration or changes have been made
            if self.singleIteration or (not changesMadeIter):
                break
        if changesMadeTotal:
            ind.recalcFitness()
            #ind.checkConsistency(PD.probDef)
        return ind


@numba.jit(nopython=True, cache=True)
def simplifierQuickJit(assign, capacity, singleIteration):
    # loads
    loads = np.sum(assign, 0)
    # remaining capacities
    remCaps = capacity - loads
    changesMadeTotal = False
    while True:
        changesMadeIter = False
        for i in range(assign.shape[0]):
            nodeAssign = assign[i]
            inds = np.nonzero(nodeAssign > 0)[0]
            maxInd = np.argmax(remCaps[inds])
            minAssignInd = np.argmin(nodeAssign[inds])
            # check whether the smallest assignment can be removed (taken over)
            if (maxInd != minAssignInd) and (remCaps[inds[maxInd]] >= nodeAssign[inds[minAssignInd]]):
                nodeAssign[inds[maxInd]] += nodeAssign[inds[minAssignInd]]
                # fix remCaps
                remCaps[inds[maxInd]] -= nodeAssign[inds[minAssignInd]]
                remCaps[inds[minAssignInd]] += nodeAssign[inds[minAssignInd]]
                # set to zero
                nodeAssign[inds[minAssignInd]] = 0
                changesMadeIter = True
                changesMadeTotal = True
        # break if singleIteration or changes have been made
        if singleIteration or (not changesMadeIter):
            break
    return changesMadeTotal
class TspTourSimplifierQuickJit(LocalSearcher):
    def __init__(self,singleIteration=True):
        self.singleIteration = singleIteration
    """
    Tries to simplify tsp tours, by identifying redundant vehicles.
    """
    def search(self, ind,probDef):

        changesMadeTotal= simplifierQuickJit(ind.assign,probDef.capacity,self.singleIteration)
        if changesMadeTotal:
            ind.recalcFitness()
            #ind.checkConsistency(PD.probDef)
        return ind


class TspTourSimplifier(LocalSearcher):
    def __init__(self,singleIteration=True):
        self.singleIteration = singleIteration
    """
    Tries to simplify tsp tours, by identifying redundant vehicles.
    """
    def search(self, ind,probDef):
        # loads
        loads = np.sum(ind.assign, 0)
        # remaining capacities
        remCaps = probDef.capacity - loads
        changesMadeTotal = False
        while True:
            changesMadeIter = False
            for nodeAssign in ind.assign:
                inds = np.nonzero(nodeAssign > 0)[0]
                maxInd = np.argmax(remCaps[inds])
                minAssignInd = np.argmin(nodeAssign[inds])
                #check whether the smallest assignment can be removed (taken over)
                if (maxInd != minAssignInd) and (remCaps[inds[maxInd]] >= nodeAssign[inds[minAssignInd]]):
                    np.random.shuffle(inds)
                    # iterate over all inds randomly and try to do the trick
                    for i,idx in enumerate(inds):
                        suitableInds = np.nonzero(remCaps[idx] >= nodeAssign[inds[i+1::]])[0]
                        if suitableInds.size == 0:
                            continue
                        #get the absolute nodeAssign indice of suitable element
                        naInd = inds[np.random.choice(suitableInds)+i+1]
                        nodeAssign[idx] += nodeAssign[naInd]
                        #fix remCaps
                        remCaps[idx] -= nodeAssign[naInd]
                        remCaps[naInd] += nodeAssign[naInd]
                        #set to zero
                        nodeAssign[naInd] = 0
                        changesMadeIter = True
                        changesMadeTotal = True
            #break if singleIteration or changes have been made
            if self.singleIteration or (not changesMadeIter):
                break
        if changesMadeTotal:
            ind.recalcFitness()
            #ind.checkConsistency(PD.probDef)
        return ind

@numba.jit(nopython=True, cache=True)
def simplifierJit(assign, capacity, singleIteration):
    # loads
    loads = np.sum(assign, 0)
    # remaining capacities
    remCaps = capacity - loads
    changesMadeTotal = False
    while True:
        changesMadeIter = False
        for i in range(assign.shape[0]):
            nodeAssign = assign[i]
            inds = np.nonzero(nodeAssign > 0)[0]
            maxInd = np.argmax(remCaps[inds])
            minAssignInd = np.argmin(nodeAssign[inds])
            # check whether the smallest assignment can be removed (taken over)
            if (maxInd != minAssignInd) and (remCaps[inds[maxInd]] >= nodeAssign[inds[minAssignInd]]):
                np.random.shuffle(inds)
                # iterate over all inds randomly and try to do the trick
                for i, idx in enumerate(inds):
                    suitableInds = np.nonzero(remCaps[idx] >= nodeAssign[inds[i + 1::]])[0]
                    if suitableInds.size == 0:
                        continue
                    # get the absolute nodeAssign indice of suitable element
                    naInd = inds[np.random.choice(suitableInds) + i + 1]
                    nodeAssign[idx] += nodeAssign[naInd]
                    # fix remCaps
                    remCaps[idx] -= nodeAssign[naInd]
                    remCaps[naInd] += nodeAssign[naInd]
                    # set to zero
                    nodeAssign[naInd] = 0
                    changesMadeIter = True
                    changesMadeTotal = True
        # break if singleIteration or changes have been made
        if singleIteration or (not changesMadeIter):
            break
    return changesMadeTotal
class TspTourSimplifierJit(LocalSearcher):
    def __init__(self,singleIteration=True):
        self.singleIteration = singleIteration
    """
    Tries to simplify tsp tours, by identifying redundant vehicles.
    """
    def search(self, ind,probDef):
        changesMadeTotal = simplifierJit(ind.assign,probDef.capacity,self.singleIteration)
        if changesMadeTotal:
            ind.recalcFitness()
            #ind.checkConsistency(PD.probDef)
        return ind

class AdpativeTspTourSimplifier(LocalSearcher):
    def __init__(self):
        self.progress = 0
        adaSimp0 = TspTourSimplifierQuick(singleIteration=True)
        adaSimp1 = TspTourSimplifier(singleIteration=True)
        adaSimp2 = TspTourSimplifierQuick(singleIteration=False)
        adaSimp3 = TspTourSimplifier(singleIteration=False)
        self.adaSimps = [adaSimp0,adaSimp1,adaSimp2,adaSimp3]
    def search(self, ind, probDef):
        thresholds = np.array([0.,1./4.,2./4.,3./4.])
        #first idx where progress is smaller than thresholds
        idx = np.argwhere(self.progress >= thresholds)[-1][0]
        return self.adaSimps[idx].search(ind,probDef)
    def dynamicAdaptation(self,progress):
        self.progress = progress
class Idle(LocalSearcher):

    def search(self, ind,probDef):
        return ind
