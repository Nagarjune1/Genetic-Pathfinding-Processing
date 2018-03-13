#
#Genetic Algorithm for pathfinding between two points with obstacles
#Kyle Thorpe, 2018
#http://github.com/KyleThorpe


from Vehicle import Vehicle
from Population import Population

# SETTINGS
# change these variables to experiment with the behaviour of the system
# how often does a mutation happen?
mutation_rate = 0.01

# how many agents per generation?
population_size = 50

# how long should each generation take?
lifetime = 500


# how wide should the screen be in pixels?
width = 1280

# how tall should the screen be in pixels?
height = 1280
# END SETTINGS
# ----------------------------------------------------------

# current generation number
generation = 0
# total distance of all of the agents from all of the generations
totalDistance = 0
# average distance of all the agents
average_distance = 0
# global variable which stores the Population object
population = None
# global list which stores the coordinates of all obstacles
obstacles = []
# ccoordinates of goal
goal = [int(width*.9),int(height/2)]
# coordinates of starting point
startingPoint = [int(width*.05),int(height/2)]
# distance between the ending point and starting point in pixels
toTravel = sqrt(pow((goal[0] - startingPoint[0]),2) + pow((goal[1] - startingPoint[1]),2))
# current move of the current generation
currentMove = 0
# global variable to store coordinates of new obstacle to make while mouse is held
newObsX1 = 0
newObsY1 = 0
newObsX2 = 0
newObsY2 = 0

# the setup function, this is run once at the start
def setup():
    size(width,height)
    background(0)
    global population
    population = Population(lifetime)
    for i in range(population_size):
        V = Vehicle(i,startingPoint,goal,lifetime)
        population.addVehicle(V)
    population.generateDNA()

# log the current mouse location when mouse is pressed down to create a new obstacle
def mousePressed():
    global newObsX1
    global newObsY1
    global newObsX2
    global newObsY2
    newObsX1 = mouseX
    newObsY1 = mouseY
    newObsX2 = mouseX
    newObsY2 = mouseY
#updates the new obstacle coordinate variable while the mouse is dragged so the box can be rendered (as a preview) before the mouse is released
def mouseDragged():
    global newObsX2
    global newObsY2
    newObsX2 = mouseX
    newObsY2 = mouseY
#updates the new obstacle coordinate variable when the mouse is released and creates the new obstacle
def mouseReleased():
    global newObsX2
    global newObsY2
    newObsX2 = mouseX
    newObsY2 = mouseY
    if newObsX2 != newObsX1 or newObsY2 != newObsY1:
        xy1 = [newObsX1,newObsY1]
        xy2 = [newObsX2,newObsY2]
        if xy1[0] == xy2[0]:
            xy2[0] += 1
        if xy1[1] == xy2[1]:
            xy2[1] += 1
        createObstacle(xy1,xy2)
# creates an obstacle using two points (xy1[0],xy1[1]) and (xy2[0],xy2[1])
def createObstacle(xy1,xy2):
    global newObsX1
    global newObsX2
    global newObsY1
    global newObsY2
    ob = [xy1[0],xy1[1],xy2[0],xy2[1]]
    obstacles.append(ob)
    newObsX1 = 0
    newObsY1 = 0
    newObsX2 = 0
    newObsY2 = 0
# renders a particular obstacle
def renderObstacle(ob):
    x1 = ob[0]
    y1 = ob[1]
    x2 = ob[2]
    y2 = ob[3]
    widthBox = abs(x2-x1)
    heightBox = abs(y2-y1)
    stroke(200,200,200)
    fill(200,200,200)
    rect(min(x1,x2),min(y1,y2),widthBox,heightBox)
# check if vehicle is out of the screen
def outOfScreen(vehicle):
    x = vehicle.location.x
    y = vehicle.location.y
    if x > width or x < 0 or y > height or y < 0:
        return True
    return False
# checks to see if a point intersects with any obstacles
def intersectObstacles(point):
    pointX = point[0]
    pointY = point[1]
    for x in obstacles:
        x1 = x[0]
        y1 = x[1]
        x2 = x[2]
        y2 = x[3]
        xLeft = min(x1,x2)
        xRight = max(x1,x2)
        yTop = min(y1,y2)
        yBottom = max(y1,y2)
        if pointX >= xLeft and pointX <= xRight and pointY >= yTop and pointY <= yBottom:
            return True
    return False
# resets variables and sets the global population to the new population made
def newGeneration(P):
    global population
    global currentMove
    global generation
    population = P
    currentMove = 0
    generation += 1
# randomly select parents from the current population and create a new population
def selection(P):
    global average_distance
    global totalDistance
    #Selection
    # list which contains a fitness level for each vehicle/agent
    fitnessList = []
    for x in population.vehicles:
        fitness = x.calcFitness()
        fitnessList.append(fitness)
        distance = (toTravel - x.lowestDistance)/toTravel
        totalDistance += distance
    average_distance = totalDistance/(population_size*(generation+1))
    maxFitness = max(fitnessList)
    if maxFitness == 0:
        print("Max fitness is 0, returning")
        return
    for x in range(len(fitnessList)):
        fitnessList[x] = fitnessList[x]/maxFitness
    for x in range(len(fitnessList)):
        fitnessList[x] = pow(10,fitnessList[x]) # bring each fitness level up to the range [1,10]
        fitnessList[x] = pow(2,fitnessList[x]) # amplify good fitness levels
    maxFitness = max(fitnessList)
    for x in range(len(fitnessList)):
        fitnessList[x] = fitnessList[x]/maxFitness    
    # list which contains the chance (between 0.0 and 1.0) for a particular vehicle to be selected for reproducing
    chances = []
    totalFitness = sum(fitnessList)
    for x in range(len(fitnessList)):
        chances.append(fitnessList[x]/totalFitness)
    # list which contains elements of the form [low,high] where high-low = chance of reproduction and 0 <= low < high <= 1.0
    genePool = []
    geneIndex = 0.0
    for x in range(len(chances)):
        genePool.append([geneIndex,geneIndex+chances[x]])
        geneIndex += chances[x]
    #Crossover        
    for i in range(population_size):
        r1i = None
        r2i = None
        while r1i is None or r2i is None:
            r1 = random(0.0,1.0)
            r2 = random(0.0,1.0)
            for x in range(len(genePool)):
                low = genePool[x][0]
                high = genePool[x][1]
                if r1i is None and r1 >= low and r1 <= high:
                    r1i = x
                elif r2i is None and r2 >= low and r2 <= high:
                    r2i = x
        mom = population.vehicles[r1i]
        dad = population.vehicles[r2i]
        child_DNA = mom.crossover(dad)
        child = Vehicle(i,startingPoint,goal,lifetime)
        child_DNA = mutate(child_DNA)
        child.inputDNA(child_DNA)
        P.addVehicle(child)
# randomly pick a direction to mutate in a particular agent's DNA list
def mutate(DNA):
    rate = mutation_rate
    for i in range(len(DNA)):
        chance = random(0.0,1.0)
        if chance < rate:
            newMove = PVector.random2D()
            DNA[i] = newMove
    return DNA
# the draw function, this is looped continuosly until the program stops
def draw():
    global population
    global currentMove
    global lifetime
    global generation
    global startingPoint
    global average_fitness
    global fitness_levels
    allStuck = True
    background(0)
    for i in obstacles:
        renderObstacle(i)
    if mousePressed:
        widthBox = abs(newObsX2-newObsX1)
        heightBox = abs(newObsY2-newObsY1)
        stroke(255,255,255)
        fill(200,200,200)
        rect(min(newObsX1,newObsX2),min(newObsY1,newObsY2),widthBox,heightBox)
    if(currentMove < lifetime):
        for x in range(len(population.vehicles)):
            vehicle = population.vehicles[x]
            # if the vehicle is not stuck, calculate the new position in vehicle.move() and then check if it is stuck in an obstacle or stuck into the edge of the screen
            if not vehicle.stuck:
                allStuck = False
                vehicle.move()
                if intersectObstacles([vehicle.location.x,vehicle.location.y]):
                    vehicle.stuck = True
                if outOfScreen(vehicle):
                    vehicle.stuck = True
            vehicle.display()
        if allStuck:
            print("allstuck")
            currentMove = lifetime
        currentMove += 1
    else:
        P = Population(lifetime)
        selection(P)
        newGeneration(P)  
    #Print learning information
    stroke(255)
    fill(255,255,255)
    s = "Lifetime length "+str(lifetime)+"\nCurrent move "+str(currentMove)+"\nGeneration "+str(generation)+"\nAverage Fitness "+str(average_distance*100)+"%\nPopulation Size "+str(population_size)+"\nMutation Rate "+str(mutation_rate*100)+"%"
    textSize(32)
    text(s, 20, 40)  # Text wraps within text box
    # Draw Goal circle
    stroke(0,0,0)
    fill(0,255,100)
    ellipse(goal[0],goal[1],10,10)
    
    
    
    