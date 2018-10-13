import numpy as np
import os
class Parser:

    @staticmethod
    def readVRP(folderName):
        """
        read VRP, hast to be in VRP_Examples
        :param path:
        :return:
        """
        abspath = os.path.abspath(__file__)
        dname = os.path.dirname(abspath)
        os.chdir(dname)
        capacity = np.loadtxt("VRP_Examples\\"+folderName+"\\capacity.txt",dtype=int)
        demand = np.loadtxt("VRP_Examples\\"+folderName+"\\demand.txt",dtype=int)
        distance = np.loadtxt("VRP_Examples\\"+folderName+"\\distance.txt",dtype=float)
        transCost = np.loadtxt("VRP_Examples\\"+folderName+"\\transportation_cost.txt",dtype=float)

        return capacity,demand,distance,transCost

    @staticmethod
    def readTSP(file):
        """
        read TSP
        :param file:
        :return:
        """
        pass
