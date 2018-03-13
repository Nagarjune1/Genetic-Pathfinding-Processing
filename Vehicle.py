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
    size = 0
    id = None
    goal = None
    DNA = None
    currentMove = 0
    
    topSpeed = 6
    location = None
    velocity = None 
    
    def __init__(self, id, startingPoint, goal, lifetime):
        self.size = 10
        self.id = id
        self.lifetime = lifetime
        self.timeArrived = lifetime
        self.goal = goal
        self.lowestDistance = float('inf')
        self.DNA = []
        self.velocity = PVector(0.0,0.0)
        self.velocity.setMag(self.topSpeed)
        self.location = PVector(startingPoint[0],startingPoint[1])
        self.display()
    # calculate the next move and update the current location
    def move(self):
        if self.arrived:
            return 1
        if self.currentMove >= len(self.DNA)-1:
            return
        toMake = self.DNA[self.currentMove]
        self.currentMove += 1
        # Compute a vector that points from location to mouse
        force = toMake
        # Velocity changes according to acceleration
        self.velocity.add(force);
        self.velocity.limit(self.topSpeed)
        # Location changes by velocity
        self.location.add(self.velocity);               
        
        d = self.calcDistance()
        if  d < self.lowestDistance:
            self.lowestDistance = d
        if self.lowestDistance <= 10:
            print("Reached end of path")
            print(self.id,self.currentMove)
            self.arrived = True
            self.timeArrived = self.currentMove
    # print the vehicle
    def display(self):
        theta = self.velocity.heading() + (PI / 2)
        pushMatrix()
        translate(self.location.x, self.location.y)
        rotate(theta)
        fill(11,224,36)
        stroke(255,255,255)
        if self.stuck:
            fill(200,50,50)
        s = createShape()
        s.beginShape()
        s.vertex(0, -5 * 2)
        s.vertex(-5, 5 * 2)
        s.vertex(5, 5 * 2)
        s.endShape(CLOSE)
        shape(s)
        popMatrix()
        
    # crossover this vehicle with another vehicle - mate
    def crossover(self, mate):
        child_DNA = []
        chance = random(0.0,1.0)
        if chance < 0.01 and False:
            for i in range(len(self.DNA)):
                child_DNA.append(PVector.random2D())
                return child_DNA
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
        goalCoords = self.goal
        d = (self.location.x - goalCoords[0])
        d = pow(d,2)
        d = d + pow((self.location.y - goalCoords[1]),2)
        d = sqrt(d)
        return d