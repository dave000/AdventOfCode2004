import copy
import time

f = open("Day16.input.txt", "r")
matrix = []
input = f.read().splitlines()

robot = None

currentY = 0
movements = None
for line in input:
    lineGraph = []
    currentX = 0

    if (line == ""):
        movements = []
        continue

    if movements == None:
        matrix.append(lineGraph)

    for i in line:
        if movements != None:
            movements.append(i)
            continue

        if i == '@':
            robot = (currentY, currentX)
            lineGraph.append(i)
            lineGraph.append('.')
        elif i == "O":
            lineGraph.append("[")
            lineGraph.append("]")
        else:
            lineGraph.append(i)
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

def printMatrix(currentMatrix):
    shouldExit = False
    for row in range(0, len(currentMatrix)):
        line = ""
        for col in range(0, len(currentMatrix[row])):
            cel = (row, col)
            line += currentMatrix[cel[0]][cel[1]]
        if "]]" in line or ".]" in line or "[[" in line:
            shouldExit = True
        print(line)

    print(" ")
    print(" ")
    print(" ")
    if shouldExit:
        print("gond van")
        exit()

def findRobot():
    global matrix
    for row in range(0, len(matrix)):
        line = ""
        for col in range(0, len(matrix[row])):
            cel = (row, col)
            if matrix[cel[0]][cel[1]] == "@":
                return cel
    return None

def calcNextStep(currentRobot, v):
    return tuple(map(sum, zip(currentRobot, v)))

def nextFreeSpace(dir, robot):
    nextPosition = calcNextStep(robot, dir)
    while not doesNotExist(nextPosition) and not isWall(nextPosition):
        if isFree(nextPosition):
            return nextPosition
        nextPosition = calcNextStep(nextPosition, dir)
    return None

def moveLateralAll(robotSpace, v):
    global matrix
    invertV = (-v[0], -v[1])
    freeSpace = nextFreeSpace(v, robot)
    if freeSpace == None:
        return robotSpace
    lastNotFree = calcNextStep(freeSpace, invertV)
    nextRobotSpace = calcNextStep(robotSpace, v)
    matrix[freeSpace[0]][freeSpace[1]] = matrix[lastNotFree[0]][lastNotFree[1]]
    matrix[robotSpace[0]][robotSpace[1]] = '.'
    matrix[nextRobotSpace[0]][nextRobotSpace[1]] = '@'
    return nextRobotSpace

def tryMoveAll(robotSpace, v, isLateral, newMatrix):
    global matrix
   
    newRobotSpace = moveAll(robotSpace, v, isLateral, newMatrix, {})
    if newRobotSpace != None:
        matrix = newMatrix
        return newRobotSpace
    return robotSpace
    

def getItemAt(loc):
    global matrix

    if doesNotExist(loc):
        return None

    return matrix[loc[0]][loc[1]]

def moveAll(startSpace, v, isLateral, newMatrix, movedAlready, level = 0):
    global matrix
    nextSpace = calcNextStep(startSpace, v)
    
    if startSpace in movedAlready:
        return startSpace

    if isWall(nextSpace):
        return None

    if level == 0:
        newMatrix[startSpace[0]][startSpace[1]] = "."
    newMatrix[nextSpace[0]][nextSpace[1]] = matrix[startSpace[0]][startSpace[1]]
    movedAlready[startSpace] = True
    if not isFree(nextSpace):
        moveSuccess = moveAll(nextSpace, v, isLateral, newMatrix, movedAlready, level + 1)
        if moveSuccess == None:
            return None
        if not isLateral:
            d = None
            item = getItemAt(nextSpace)
            if item == '[':
                d = 1
            elif item == ']':
                d = -1

            moveSuccess = moveAll((nextSpace[0], nextSpace[1] + d), v, isLateral, newMatrix, movedAlready, 0)
            if moveSuccess == None:
                return None
        
    return nextSpace
    
printMatrix(matrix)

c = 0
robot =  findRobot()
for i in movements:
    isLateral = False
    print(i, c)
    c += 1
    v = (0, 0)
    if i == '<':
        v = (0, -1)
        isLateral = True
    elif i == '>':
        v = (0, 1)
        isLateral = True
    elif i == 'v':
        v = (1, 0)
    else:
        v = (-1, 0)

    newMatrix = copy.deepcopy(matrix)
    robot = tryMoveAll(robot, v, isLateral, newMatrix)
    #printMatrix(matrix)
    #time.sleep(1.5)


#printMatrix(matrix)
sumGPS = 0

for row in range(0, len(matrix)):
    for col in range(0, len(matrix[row])):
        cel = (row, col)
        c = matrix[cel[0]][cel[1]]
        if c == "[":
            gps = 100 * row + col
            sumGPS += gps

print(sumGPS)
