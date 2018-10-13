class SolutionVRP:

    # def __init__(self,nameOfVRP,capacities,demands,distances,transportCosts,
    #              solScore, assignments, probsByVehicle,solsByVehicle):
    def __init__(self,nameOfVRP, probDef,solScore, assignments, probsByVehicle, solsByVehicle):

        self.probName = nameOfVRP
        #self.probDef = probDef
        #solution of VRP
        self.solution = dict()
        self.solution["score"] = solScore
        self.solution["assignments"] = assignments
        self.solution["probsByVehicle"] = probsByVehicle
        self.solution["solsByVehicle"] = solsByVehicle


