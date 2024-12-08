f = open("Day6.input.txt", "r")
matrix = []
input = f.readlines()

guard = None
v = (-1, 0)

currentY = 0
for line in input:
    lineGraph = []
    matrix.append(lineGraph)
    currentX = 0
    for i in line:
        if i == '\n':
            continue
        if i == '^':
            guard = (currentY, currentX)
        lineGraph.append(i)
        currentX += 1
    currentY += 1

stepCounter = 0
dimension = (len(matrix), len(matrix[0]))

def hasLeftMap(guard):
    global dimension
    return guard[0] == dimension[0] or guard[0] < 0 or guard[1] == dimension[1] or guard[1] < 0

def isBlocked(coordinate):
    if not hasLeftMap(coordinate):
        return matrix[coordinate[0]][coordinate[1]] == '#'
    return False

def calcNextStep(currentGuard, v):
    return tuple(map(sum, zip(currentGuard, v)))

def turnRight(currentV):
    return (currentV[1], -currentV[0])

visitedCoordinates = {}

while not hasLeftMap(guard):
    visitedCoordinates[guard] = True
    nextStep = calcNextStep(guard, v)
    print(guard, nextStep)
    if isBlocked(nextStep):
        v = turnRight(v)
    else:
        guard = nextStep
    stepCounter += 1

print(len(visitedCoordinates))


