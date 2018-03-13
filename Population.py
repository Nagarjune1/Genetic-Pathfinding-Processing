class Population(object):
    vehicles = None
    lifetime = None
    def __init__(self,lifetime):
        self.lifetime = lifetime
        self.vehicles = []
    # add a particular vehicle to the vehicle list of this Population
    def addVehicle(self,vehicle):
        self.vehicles.append(vehicle)
    # generate DNA for all of the vehicles in the global vehicle list of this Population
    def generateDNA(self):
        size = self.lifetime * len(self.vehicles)
        DNA = []
        for i in range(size):
            DNA.append(int(random(0,4)))
        for i in range(len(DNA)):
            dnaIndex = i%self.lifetime
            whichVehicle = ((i-dnaIndex)/self.lifetime)
            self.vehicles[whichVehicle].DNA.append(DNA[i])
            #print("Appending ",dnaIndex,whichVehicle,DNA[i])