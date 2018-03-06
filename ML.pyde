from Vehicle import Vehicle
from Population import Population

showGrid = False
generation = 0
distance_levels = []
average_distance = 0
mutation_rate = 0.01
population_size = 100
lifetime = 250
height = 1280
width = 1280
resolution = 10
numColumns = width/resolution
numRows = height/resolution
population = None
goal = [int(numColumns*.9),int(numRows/2)]
startingPoint = [int(numColumns*.05),int(numRows/2)]
toTravel = pow((goal[0] - startingPoint[0]),2)
toTravel = toTravel + pow((goal[1] - startingPoint[1]),2)
toTravel = sqrt(toTravel)
toTravel = toTravel * resolution
currentMove = 0

def setup():
    size(width,height)
    background(255,255,255)
    global population
    population = Population(lifetime)
    #global goal
    #goal = [int(numColumns*.9),int(numRows/2)]
    #startingPoint = [int(numColumns*.05),int(numRows/2)]
    if showGrid:
        for x in range(width/resolution):
            for y in range(height/resolution):
                stroke(0,0,0)
                fill(255,255,255)
                rect(x*resolution,y*resolution,resolution,resolution)
    for x in range(population_size):
        V = Vehicle(x,startingPoint,goal,resolution,numColumns,numRows,lifetime)
        population.addVehicle(V)
    population.generateDNA()
    
def newGeneration(P):
    global population
    global currentMove
    global generation
    population = P
    currentMove = 0
    generation += 1

# def selection_old():
#     #Selection
#     fitnessArray = []
#     fitnessTotal = 0
#     for x in population.vehicles:
#         fitness = x.calcFitness()
#         fitnessArray.append(fitness)
#         fitnessTotal += fitness
#     fitness_levels.append(fitnessTotal/population_size)
#     average_fitness = sum(fitness_levels)/len(fitness_levels)
#     breedingChances = []
#     for i in range(len(fitnessArray)):
#         fitness = fitnessArray[i]
#         if(fitnessTotal != 0):
#             chance = fitness/fitnessTotal
#             breedingChances.append(chance)
#     genePool = []
#     j = 0
#     for i in breedingChances:
#         rang = [j,j+i]
#         genePool.append(rang)
#         j += i
#     #Crossover
#     P = Population(lifetime)        
#     for i in range(population_size):
#         momNum = random(0.0,1.0)
#         dadNum = random(0.0,1.0)
#         mom = None
#         dad = None
#         for k in range(len(genePool)):
#             if genePool[k][0] <= momNum and momNum <= genePool[k][1]:
#                 mom = k
#             if genePool[k][0] <= dadNum and dadNum <= genePool[k][1]:
#                 dad = k
#         if mom is None or dad is None:
#             print("Fatal error when selecting mom and dad")
#             print(momNum)
#             print(dadNum)
#             print(genePool)
#         mom = population.vehicles[mom]
#         dad = population.vehicles[dad]
#         child_DNA = mom.crossover(dad)
#         child = Vehicle(i,startingPoint,goal,resolution,numColumns,numRows)
#         child_DNA = mutate(child_DNA)
#         child.inputDNA(child_DNA)
#         P.addVehicle(child)

def selection(P):
    global average_distance
    global distance_levels
    #Selection
    fitnessArray = []
    for x in population.vehicles:
        fitness = x.calcFitness()
        distance = (toTravel - x.lowestDistance)/toTravel
        distance_levels.append(distance)
        fitnessArray.append(fitness)
    highest_fitness = max(fitnessArray)
    for x in range(len(fitnessArray)):
        fitnessArray[x] = fitnessArray[x] / highest_fitness

    average_distance = sum(distance_levels) / len(distance_levels)
    
    
    bestI = 0
    secondBestI = 0
    best = 0
    secondBest = 0
    for i in range(len(fitnessArray)):
        fitness = fitnessArray[i]
        if fitness > best:
            best = fitness
            bestI = i
        elif fitness > secondBest:
            secondBest = fitness
            secondBestI = i
    #Crossover        
    for i in range(population_size):
        mom = bestI
        dad = secondBestI
        mom = population.vehicles[mom]
        dad = population.vehicles[dad]
        child_DNA = mom.crossover(dad)
        child = Vehicle(i,startingPoint,goal,resolution,numColumns,numRows,lifetime)
        child_DNA = mutate(child_DNA)
        child.inputDNA(child_DNA)
        P.addVehicle(child)

def mutate(DNA):
    rate = mutation_rate
    for i in range(len(DNA)):
        chance = random(0.0,1.0)
        if chance < rate:
            newMove = int(random(0,4))
            DNA[i] = newMove
    return DNA
            
        
def draw():
    global population
    global currentMove
    global lifetime
    global generation
    global startingPoint
    global average_fitness
    global fitness_levels
    background(0)
    if showGrid:
        for x in range(width/resolution):
            for y in range(height/resolution):
                stroke(0,0,0)
                fill(255,255,255)
                rect(x*resolution,y*resolution,resolution,resolution)
    if(currentMove < lifetime):
        for x in range(len(population.vehicles)):
            vehicle = population.vehicles[x]
            vehicle.move()
            vehicle.display()
        currentMove += 1
    else:
        P = Population(lifetime)
        selection(P)
        newGeneration(P)  
        # print("Fitness Array ",fitnessArray)
        # print("Fitness Total ",fitnessTotal)
        # print("Breeding Chances ",breedingChances)
    # for x in population.vehicles:
    #     if x.col == goal[0] and x.row == goal[1]:
    #         x.arrived = True
    #     else:
    #         x.arrived = False
    
    #Print learning information
    stroke(255)
    fill(255,255,255)
    s = "Lifetime length "+str(lifetime)+"\nCurrent move "+str(currentMove)+"\nGeneration "+str(generation)+"\nAverage Fitness "+str(average_distance*100)+"%\nPopulation Size "+str(population_size)+"\nMutation Rate "+str(mutation_rate*100)+"%"
    textSize(32)
    text(s, 20, 40)  # Text wraps within text box
            
    # Draw Goal cell
    stroke(0,0,0)
    fill(255,6,2)
    goalCoords = getCoordsFromCell([goal[0],goal[1]])
    rect(goalCoords[0],goalCoords[1],resolution,resolution)
    
def getCellFromCoords(coords):
    x = coords[0]
    y = coords[1]
    x = (x-(x%self.resolution))/resolution
    y = (y-(y%self.resolution))/resolution
    Pos = [x,y]
    return Pos

def getCoordsFromCell(Pos):
    x = Pos[0]
    y = Pos[1]
    x = x*resolution
    y = y*resolution
    Coords = [x,y]
    return Coords
    
    
    
    