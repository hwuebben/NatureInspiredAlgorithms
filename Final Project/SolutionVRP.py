class SolutionVRP:

    # def __init__(self,nameOfVRP,capacities,demands,distances,transportCosts,
    #              solScore, assignments, probsByVehicle,solsByVehicle):
    def __init__(self,nameOfVRP, probDef,solScore, assignments, probsByVehicle, solsByVehicle):

        #problem definition of VRP
        # self.probDef = dict()
        # self.probDef["name"] = nameOfVRP
        # self.probDef["capacities"] = capacities
        # self.probDef["demands"] = demands
        # self.probDef["distances"] = distances
        # self.probDef["transportCosts"] = transportCosts

        self.probName = nameOfVRP
        #self.probDef = probDef
        #solution of VRP
        self.solution = dict()
        self.solution["score"] = solScore
        self.solution["assignments"] = assignments
        self.solution["probsByVehicle"] = probsByVehicle
        self.solution["solsByVehicle"] = solsByVehicle


