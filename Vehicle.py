class Vehicle(object):
    lifetime = None
    lowestDistance = None
    timeArrived = None
    arrived = False
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
    def inputDNA(self,DNA):
        self.DNA = DNA
    def calcFitness(self):
        if(self.lowestDistance == 0):
            return 1/(self.timeArrived/self.resolution)
        return 1/((self.lowestDistance+self.lifetime)/self.resolution)
    def calcDistance(self):
        goalCoords = self.getCoordsFromCell(self.goal)
        self.updateCoordsFromCell()
        #d = pow(pow((self.x - goalCoords[0]),2) + pow((self.y - goalCoords[1]),2),(1/2))
        d = (self.x - goalCoords[0])
        d = pow(d,2)
        d = d + pow((self.y - goalCoords[1]),2)
        d = sqrt(d)
        return d
    def getCellFromCoords(self, coords):
        x = coords[0]
        y = coords[1]
        x = (x-(x%self.resolution))/self.resolution
        y = (y-(y%self.resolution))/self.resolution
        Pos = [x,y]
        return Pos
    def getCoordsFromCell(self, Pos):
        x = Pos[0]
        y = Pos[1]
        x = x*self.resolution
        y = y*self.resolution
        Coords = [x,y]
        return Coords
    def updateCoordsFromCell(self):
        newCoords = self.getCoordsFromCell([self.col,self.row])
        self.x = newCoords[0]
        self.y = newCoords[1]
    def updateCellFromCoords(self):
        Coords = [self.x,self.y]
        newCell = self.getCellFromCoords(Coords)
        self.col = newCell[0]
        self.row = newCell[1]
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
        
    def display(self):
        #print(self.col,self.row)
        Pos = self.getCoordsFromCell([self.col,self.row])
        x = Pos[0]
        y = Pos[1]
        stroke(0,0,0)
        fill(11,224,36)
        rect(x,y,self.resolution,self.resolution)