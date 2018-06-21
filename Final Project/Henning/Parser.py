import numpy as np

class Parser:

    def readVRP(self, folderName):
        """
        read VRP, hast to be in VRP_Examples
        :param path:
        :return:
        """
        capacity = np.loadtxt("..\\VRP_Examples\\"+folderName+"\\capacity.txt")
        demand = np.loadtxt("..\\VRP_Examples\\"+folderName+"\\demand.txt")
        distance = np.loadtxt("..\\VRP_Examples\\"+folderName+"\\distance.txt")
        transCost = np.loadtxt("..\\VRP_Examples\\"+folderName+"\\transportation_cost.txt")


    def readTSP(self,file):
        """
        read TSP
        :param file:
        :return:
        """
        pass
    


parser = Parser()
parser.readVRP("VRP1")