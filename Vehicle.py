class Vehicle(object):
    # how many moves have been made by this vehicle
    lifetime = None
    # the closest this vehicle has gotten to the goal cell
    lowestDistance = None
    # how long it took the vehicle to make it to the goal cell
    timeArrived = None
    # if the vehicle has arrived to the goal cell
    arrived = False
    # if the vehicle has run into an obstacle
    stuck = False
    id = None
    resolution = 0
    numColumns = 0
    numRows = 0
    col = 0
    row = 0
    x = 0
    y = 0
    goal = None
    DNA = None
    currentMove = 0
    def __init__(self, id, startingPoint, goal, resolution, numColumns, numRows, lifetime):
        self.id = id
        self.lifetime = lifetime
        self.timeArrived = lifetime
        self.col = startingPoint[0]
        self.row = startingPoint[1]
        self.updateCoordsFromCell()
        self.goal = goal
        self.resolution = resolution
        self.numColumns = numColumns
        self.numRows = numRows
        self.lowestDistance = numColumns*numRows*resolution
        self.DNA = []
        self.display()
    # crossover this vehicle with another vehicle - mate
    def crossover(self, mate):
        child_DNA = []
        mom_DNA = self.DNA
        dad_DNA = mate.DNA
        for i in range(len(mom_DNA)):
            chance = random(0.0,1.0)
            if(chance < 0.5):
                child_DNA.append(mom_DNA[i])
            else:
                child_DNA.append(dad_DNA[i])
        return child_DNA
    # set the DNA of this vehicle
    def inputDNA(self,DNA):
        self.DNA = DNA
    # calculate the fitness of this vehicle
    def calcFitness(self):
        if(self.lowestDistance == 0):
            return 1/(self.timeArrived)
        if self.stuck:
            return 1/((self.lowestDistance+self.lifetime)*2)
        return 1/(self.lowestDistance+self.lifetime)
    # calculate the distance between two points in 2D space
    def calcDistance(self):
        goalCoords = self.getCoordsFromCell(self.goal)
        self.updateCoordsFromCell()
        d = (self.x - goalCoords[0])
        d = pow(d,2)
        d = d + pow((self.y - goalCoords[1]),2)
        d = sqrt(d)
        return d
    # convert pixel coordinates to cell coordinates
    def getCellFromCoords(self, coords):
        x = coords[0]
        y = coords[1]
        x = (x-(x%self.resolution))/self.resolution
        y = (y-(y%self.resolution))/self.resolution
        Pos = [x,y]
        return Pos
    # convert cell coordinates to pixel coordinates
    def getCoordsFromCell(self, Pos):
        x = Pos[0]
        y = Pos[1]
        x = x*self.resolution
        y = y*self.resolution
        Coords = [x,y]
        return Coords
    # update the pixel coordinate variables from the cell coordinate variables
    def updateCoordsFromCell(self):
        newCoords = self.getCoordsFromCell([self.col,self.row])
        self.x = newCoords[0]
        self.y = newCoords[1]
    # update the cell coordinate variables from the pixel coordinate variables
    def updateCellFromCoords(self):
        Coords = [self.x,self.y]
        newCell = self.getCellFromCoords(Coords)
        self.col = newCell[0]
        self.row = newCell[1]
    # calculate the next move and update the current location
    def move(self):
        if self.arrived:
            return 1
        # self.updateCoordsFromCell()
        # fill(255,255,255)
        # rect(self.x,self.y,self.resolution,self.resolution)
        if self.currentMove >= len(self.DNA)-1:
            return
        toMake = self.currentMove
        toMake = self.DNA[toMake]
        self.currentMove += 1
        if toMake == 0 and self.col < self.numColumns:
            self.col += 1
        if toMake == 1 and self.row > 0:
             self.row -= 1
        if toMake == 2 and self.col > 0:
            self.col -= 1
        if toMake == 3 and self.row < self.numRows:
            self.row += 1
        self.updateCoordsFromCell()
        d = self.calcDistance()
        if  d < self.lowestDistance:
            self.lowestDistance = d
        if self.lowestDistance == 0:
            print("Reached end of path")
            print(self.id,self.currentMove)
            self.arrived = True
            self.timeArrived = self.currentMove
    # print the vehicle
    def display(self):
        #print(self.col,self.row)
        Pos = self.getCoordsFromCell([self.col,self.row])
        x = Pos[0]
        y = Pos[1]
        stroke(0,0,0)
        fill(11,224,36)
        if self.stuck:
            fill(50,50,200)
        rect(x,y,self.resolution,self.resolution)