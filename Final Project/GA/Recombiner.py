from __future__ import division
from abc import ABC, abstractmethod
import numpy as np
from ProblemDefinition import ProblemDefinition
from Individual import Individual
import copy
import random


class Recombiner(ABC):
    @abstractmethod
    def recombine(self, probDef, ind0, ind1):
        """
        perform recombination operation on two individuals constrained by problem definition
        :param probDef:
        :param ind0:
        :param ind1:
        :return: recombinated child
        """
        pass
    def dynamicAdaptation(self,progress):
        pass

class InspirationalRecombiner(Recombiner):
    def __init__(self,recombineRatio,dynAdapt = True):
        self.originalrecombineRatio = recombineRatio
        self.recombineRatio = recombineRatio
        self.dynAdapt = dynAdapt

    def recombine(self, probDef, ind0, ind1):
        #print("in Recombine")
        #ind0.checkConsistency(probDef)
        #ind1.checkConsistency(probDef)
        newAssign = copy.deepcopy(ind0.assign)
        loads = np.sum(newAssign, 0)
        freeCaps = probDef.capacity - loads
        potInds = np.argwhere((ind0.assign > 0) != (ind1.assign > 0))
        np.random.shuffle(potInds)
        counter = 0
        lastCounter = 0
        nrInspirations = max(1,int(self.recombineRatio*probDef.problemSize))
        for potInd in potInds:
            if counter == nrInspirations:
                break
            #if newAssign was edited recalculate loads and freeCaps
            if counter > lastCounter:
                loads = np.sum(newAssign, 0)
                freeCaps = probDef.capacity - loads
                lastCounter = counter


            newAss = newAssign[potInd[0]]
            newVal = ind1.assign[potInd[0],potInd[1]]
            oldVal = newAss[potInd[1]]

            if newVal == 0:
                # assign the new Value then try to make it work
                newAss[potInd[1]] = newVal
                #get only the non zero entries (0entries shouldn't be vhanged)
                nonZeros = np.nonzero(newAss)[0]
                #check whether it can be done
                if np.sum(freeCaps[nonZeros]) >= oldVal:
                    #if so iterate over nonzero indices and repair
                    np.random.shuffle(nonZeros)
                    left = oldVal
                    for nz in nonZeros:
                        addVal = min(freeCaps[nz], left)
                        newAss[nz] += addVal
                        left -= addVal
                        if left == 0:
                            counter+=1
                            break
                    assert(left == 0)
                    #print("case 0")

                #else revert changes
                else:
                    newAss[potInd[1]] = oldVal

            else:

                #check whether it can be done
                potential = np.sum(newAss)
                if freeCaps[potInd[1]] > 0 and potential > 0:
                    #if so do it
                    nonZeros = np.nonzero(newAss)[0]
                    newVal = min(newVal,potential,freeCaps[potInd[1]])
                    newAss[potInd[1]] = newVal
                    np.random.shuffle(nonZeros)
                    left = newVal
                    for nz in nonZeros:
                        subVal = min(newAss[nz], left)
                        newAss[nz] -= subVal
                        left -= subVal
                        if left == 0:
                            counter += 1
                            break
                    assert(left == 0)
                    #print("case else")
        newIndi = Individual(newAssign)
        #assert((newIndi.assign != ind0.assign).any() and (newIndi.assign != ind1.assign).any())
        #assert(success)
        #newIndi.checkConsistency(probDef)
        return newIndi
    def dynamicAdaptation(self,progress):
        if not self.dynAdapt:
            return
        self.recombineRatio = (1-progress)*self.originalrecombineRatio


class SmartInspirationalRecombiner(Recombiner):
    def __init__(self,recombineRatio,dynAdapt = True):
        self.originalrecombineRatio = recombineRatio
        self.recombineRatio = recombineRatio
        self.dynAdapt = dynAdapt

    def recombine(self, probDef, ind0, ind1):

        newAssign = copy.deepcopy(ind0.assign)
        loads = np.sum(newAssign, 0)
        freeCaps = probDef.capacity - loads
        """calculate potential inspiration points"""
        potInds = np.argwhere((ind0.assign > 0) != (ind1.assign > 0))
        """prefer those points that affect vehicles already used by ind0"""
        vehiclesUsed = []
        for vehicleInd in range(probDef.nrVehicles):
            if (ind0.assign[:,vehicleInd] != 0).any():
                vehiclesUsed.append(vehicleInd)
        otherInds = []
        prefInds = []
        for potInd in potInds:
            if potInd[1] in vehiclesUsed:
                prefInds.append(potInd)
            else:
                otherInds.append(potInd)
        random.shuffle(prefInds)
        random.shuffle(otherInds)
        potInds = prefInds + otherInds

        counter = 0
        lastCounter = 0
        nrInspirations = max(1,int(self.recombineRatio*probDef.problemSize))
        for potInd in potInds:
            if counter == nrInspirations:
                break
            #if newAssign was edited recalculate loads and freeCaps
            if counter > lastCounter:
                loads = np.sum(newAssign, 0)
                freeCaps = probDef.capacity - loads
                lastCounter = counter

            newAss = newAssign[potInd[0]]
            newVal = ind1.assign[potInd[0],potInd[1]]
            oldVal = newAss[potInd[1]]

            if newVal == 0:
                # assign the new Value then try to make it work
                newAss[potInd[1]] = newVal
                #get only the non zero entries (0entries shouldn't be vhanged)
                nonZeros = np.nonzero(newAss)[0]
                #check whether it can be done
                if np.sum(freeCaps[nonZeros]) >= oldVal:
                    #if so iterate over nonzero indices and repair
                    np.random.shuffle(nonZeros)
                    left = oldVal
                    for nz in nonZeros:
                        addVal = min(freeCaps[nz], left)
                        newAss[nz] += addVal
                        left -= addVal
                        if left == 0:
                            counter+=1
                            break
                    assert(left == 0)
                    #print("case 0")

                #else revert changes
                else:
                    newAss[potInd[1]] = oldVal

            else:

                #check whether it can be done
                potential = np.sum(newAss)
                if freeCaps[potInd[1]] > 0 and potential > 0:
                    #if so do it
                    nonZeros = np.nonzero(newAss)[0]
                    newVal = min(newVal,potential,freeCaps[potInd[1]])
                    newAss[potInd[1]] = newVal
                    np.random.shuffle(nonZeros)
                    left = newVal
                    for nz in nonZeros:
                        subVal = min(newAss[nz], left)
                        newAss[nz] -= subVal
                        left -= subVal
                        if left == 0:
                            counter += 1
                            break
                    assert(left == 0)
                    #print("case else")
        newIndi = Individual(newAssign,probDef)
        #assert((newIndi.assign != ind0.assign).any() and (newIndi.assign != ind1.assign).any())
        #assert(success)
        #newIndi.checkConsistency(probDef)
        return newIndi
    def dynamicAdaptation(self,progress):
        if not self.dynAdapt:
            return
        self.recombineRatio = (1-progress)*self.originalrecombineRatio


class MeanRecombiner(Recombiner):

    def recombine(self, probDef: ProblemDefinition, ind0: Individual, ind1: Individual):


        # change all fraction assignments to even ones (is this necessary?)
        # create a mask that is added on newAssign
        # mask needs the same amount of +0.5 and -0.5 values in each column and row
        # or:
        # round up all fractions, where capacity constraint is violated reduce prior fractions if demand is overfullfilled:
        newAssign = ind0.assign + ind1.assign
        np.divide(newAssign,2.,newAssign)
        np.ceil(newAssign,newAssign)
        #this procedure could potentially break the cap limits of vehicles, therefore repair
        #identify broken Caps
        brokenCaps = np.sum(newAssign, 0) - probDef.capacity
        brokenCapInds = np.nonzero(brokenCaps > 0)[0]
        #iterate over broken caps
        for brokenCapInd in brokenCapInds:
            #iterate over all nodes (shuffled to avoid bias)
            inds = np.arange(newAssign[:,brokenCapInd].size)
            np.random.shuffle(inds)
            for j in inds:
                #check whether node has a surplus
                assigned = np.sum(newAssign[j,:])
                hasSurplus = (assigned - probDef.demand[j]) > 0
                #if so relieve brokenCap
                if hasSurplus:
                    newAssign[j,brokenCapInd] -= 1
                    brokenCaps[brokenCapInd] -= 1
                    if brokenCaps[brokenCapInd] == 0:
                        break
        #remove oversupply
        oversupply = np.sum(newAssign,1) - probDef.demand
        oversupplyInds = np.nonzero(oversupply > 0)[0]
        #iterate over oversupplied nodes
        for osInd in oversupplyInds.flat:
            # dcecrement the smallest value oversupply[osInd] times
            #(this remvoves vehicles that visit the node unneccessarily)
            for _ in range(int(oversupply[osInd])):
                min = np.min(newAssign[osInd,np.nonzero(newAssign[osInd])])
                minInds = np.nonzero(newAssign[osInd] == min)[0]
                newAssign[osInd,np.random.choice(minInds)] -= 1




        # or do integer division, then fix demands:
        # newAssign = np.ceil((ind0.assign + ind1.assign) // 2)
        # deficits = probDef.demand - np.sum(newAssign,0)
        # defInds = np.argwhere(deficits > 0)
        # openCaps = probDef.capacity - np.sum(newAssign, 1)
        # openCapInds = np.argwhere(openCaps > 0)
        #iterate over nodes that have deficits
        # for i,defInd in enumerate(defInds):
        #     #indices of the vehicles that visit that node
        #     visInds = np.argwhere(newAssign[defInd] > 0)
        #     #increase supply as calculated in deficits, always choose the vehicle with the highest openCap
        #     for _ in deficits[i]:
        #
        #         assign = newAssign[defInd]

        newInd = Individual(newAssign)
        #DEBUG:
        newInd.checkConsistency(probDef)
        return newInd


class SmartMeanRecombiner(Recombiner):
    def __init__(self):
        self.nrFails = 0
        self.nrSuccesses = 0
    def recombine(self, probDef: ProblemDefinition, ind0: Individual, ind1: Individual):
        """

        :param probDef:
        :param ind0:
        :param ind1:
        :return:
        """
        #print("Fail-Success ratio: ",self.nrFails,self.nrSuccesses)
        """
        step 1: calculate ceiling of mean
        """
        # round up all fractions, where capacity constraint is violated reduce prior fractions if demand is overfullfilled:
        newAssign = ind0.assign + ind1.assign
        np.divide(newAssign, 2., newAssign)
        np.ceil(newAssign, newAssign)

        """
        step 2: repair broken capacity constraints (by trying to reduce size of graphs)
        """
        loads = np.sum(newAssign, 0)
        capDiffs = loads - probDef.capacity
        brokenCapInds = np.nonzero(capDiffs > 0)[0]
        #shuffle or sort by cost efficieny?
        np.random.shuffle(brokenCapInds)
        demDiffs = (np.sum(newAssign,1) -probDef.demand)#.reshape(probDef.nrNodes,1)
        #overCapInds = np.argwhere(capDiffs > 0)
        # iterate over broken caps
        for bkInd in brokenCapInds:
            assign = newAssign[:,bkInd]
            # get indices that could potentially be reduced to 0
            possInds = np.flatnonzero(np.logical_and(demDiffs >= assign, assign > 0))
            # if none of those exist, just take all that are greater than 0
            if possInds.size == 0:
                possInds = np.flatnonzero(np.logical_and(demDiffs > 0, assign > 0))
            # shuffle to remove bias
            np.random.shuffle(possInds)
            while capDiffs[bkInd] > 0:
                if possInds.size == 0:
                    """
                    Recombination failed, cap can't be repaired
                    """
                    #TODO: apply other fail safe recombiner
                    self.nrFails += 1
                    return copy.deepcopy(np.random.choice([ind0, ind1]))
                minInd = np.argmin(assign[possInds])
                reduceBy = min(assign[possInds[minInd]], demDiffs[possInds[minInd]])
                assign[possInds[minInd]] -= reduceBy
                demDiffs[possInds[minInd]] -= reduceBy
                capDiffs[bkInd] -= reduceBy
                possInds = np.delete(possInds,minInd)
        self.nrSuccesses += 1
        if np.sum(demDiffs) == 0:
            return Individual(newAssign)


        """
        step 3: try to eliminate vehicles (reduce number of graphs)
        """
        #iterate over vehicles in order from most to least costly
        #argSort = np.argsort(probDef.transCost)[::-1]
        #iterate over vehicles in order: vehicles with a bad transport/cost ratio first
        argSort = np.argsort(loads / probDef.transCost)
        for vehicleInd in argSort:
            assign = newAssign[:,vehicleInd]
            if not (assign <= demDiffs).all():
                continue
            demDiffs -= assign
            #assign = np.zeros((probDef.nrNodes,1))
            assign[:] = 0
        if np.sum(demDiffs) == 0:
            return Individual(newAssign)

        """
        step 4: use remaining oversupply to reduce size of graphs
        """
        #iterate over vehicles in order: vehicles with a bad transport/cost ratio first
        #argSort = np.argSort(np.sum(newAssign,1) / probDef.transCost)
        for vehicleInd in argSort:
            assign = newAssign[:, vehicleInd]
            mask = assign <= demDiffs
            demDiffs[mask] -= assign[mask]
            assign[mask] = 0

        if np.sum(demDiffs) == 0:
            return Individual(newAssign)

        """
        step 5: get rid of remaining oversupply
        """
        #iterate over vehicles in order: vehicles with a bad transport/cost ratio first
        for vehicleInd in argSort:
            assign = newAssign[:, vehicleInd]
            mask = demDiffs > 0
            reduceBy = np.minimum(assign[mask], demDiffs[mask])
            demDiffs[mask] -= reduceBy
            assign[mask] -= reduceBy

            if np.sum(demDiffs) == 0:
                break

        newInd = Individual(newAssign)
        # DEBUG:
        newInd.checkConsistency(probDef)
        return newInd


class SimpleMeanRecombiner(Recombiner):
    """
    should be used with the RearrangeRecombiner
    """

    def recombine(self, probDef: ProblemDefinition, ind0: Individual, ind1: Individual):
        newAssign = ind0.assign + ind1.assign
        np.divide(newAssign,2.,newAssign)
        newInd = Individual(newAssign)
        #DEBUG:
        #newInd.checkConsistency(probDef)
        return newInd
