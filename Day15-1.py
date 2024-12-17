f = open("Day16.input.txt", "r")
matrix = []
input = f.read().splitlines()

robot = None

currentY = 0
movements = None
for line in input:
    lineGraph = []
    matrix.append(lineGraph)
    currentX = 0

    if (line == ""):
        movements = []
        continue

    for i in line:
        if i == '@':
            robot = (currentY, currentX)
        if movements != None:
            movements.append(i)
            continue

        lineGraph.append(i)
        currentX += 1
    currentY += 1

dimension = (len(matrix), len(matrix[0]))

def doesNotExist(coordinate):
    global dimension
    return coordinate[0] == dimension[0] or coordinate[0] < 0 or coordinate[1] == dimension[1] or coordinate[1] < 0  

def isFree(coordinate):
    global matrix
    return matrix[coordinate[0]][coordinate[1]] == '.'

def isWall(coordinate):
    global matrix
    return matrix[coordinate[0]][coordinate[1]] == '#'

def nextFreeSpace(dir, robot):
    nextPosition = calcNextStep(robot, dir)
    while not doesNotExist(nextPosition) and not isWall(nextPosition):
        if isFree(nextPosition):
            return nextPosition
        nextPosition = calcNextStep(nextPosition, dir)
    return None


def printMatrix(currentMatrix):
    for row in range(0, len(currentMatrix)):
        line = ""
        for col in range(0, len(currentMatrix[row])):
            cel = (row, col)
            line += currentMatrix[cel[0]][cel[1]]
        print(line)

    print(" ")
    print(" ")
    print(" ")

def calcNextStep(currentRobot, v):
    return tuple(map(sum, zip(currentRobot, v)))

def moveAll(robotSpace, v, nextFreeSpace):
    global matrix
    invertV = (-v[0], -v[1])
    lastNotFree = calcNextStep(nextFreeSpace, invertV)
    nextRobotSpace = calcNextStep(robotSpace, v)
    matrix[nextFreeSpace[0]][nextFreeSpace[1]] = matrix[lastNotFree[0]][lastNotFree[1]]
    matrix[robotSpace[0]][robotSpace[1]] = '.'
    matrix[nextRobotSpace[0]][nextRobotSpace[1]] = '@'
    
printMatrix(matrix)
for i in movements:
    v = (0, 0)
    if i == '<':
        v = (0, -1)
    elif i == '>':
        v = (0, 1)
    elif i == 'v':
        v = (1, 0)
    else:
        v = (-1, 0)
    nextRobot = calcNextStep(robot, v)
    nextFree = nextFreeSpace(v, robot)
    if nextFree != None:
        moveAll(robot, v, nextFree)
        
        robot = nextRobot

printMatrix(matrix)
sumGPS = 0

for row in range(0, len(matrix)):
    for col in range(0, len(matrix[row])):
        cel = (row, col)
        c = matrix[cel[0]][cel[1]]
        if c == "O":
            gps = 100 * row + col
            sumGPS += gps

print(sumGPS)
