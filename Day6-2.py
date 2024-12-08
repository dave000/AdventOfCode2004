import copy
import time

start = time.time()
f = open("Day6.input.txt", "r")
matrix = []
input = f.readlines()

originGuard = None
v0 = (-1, 0)

currentY = 0
for line in input:
    lineGraph = []
    matrix.append(lineGraph)
    currentX = 0
    for i in line:
        if i == '\n':
            continue
        if i == '^':
            originGuard = (currentY, currentX)
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

def beenHereWithThisDirection(here, visitedCoordinates, v):
    return here in visitedCoordinates and v in visitedCoordinates[here]


def printMatrix(currentMatrix, pos, v, possibleBlock, printIt):
    global originGuard
    currentLog = currentMatrix[pos[0]][pos[1]]
    newLog = "-" if v[0] == 0 else "|"

    if currentLog in ["-", "|"] and currentLog != newLog:
        newLog = "+"
    if pos != originGuard:
        currentMatrix[pos[0]][pos[1]] = newLog
    if possibleBlock != None:
        currentMatrix[possibleBlock[0]][possibleBlock[1]] = "O"

    if not printIt:
        return

    for row in range(0, len(currentMatrix)):
        line = ""
        for col in range(0, len(currentMatrix[row])):
            cel = (row, col)
            line += currentMatrix[cel[0]][cel[1]]
        print(line)

    print(" ")
    print(" ")
    print(" ")

def findCircle(matrix, guardStart, possibleNewBlock, visitedCoordinates, v, possibleBlock = None):
    global originGuard
    guard = guardStart
    while not hasLeftMap(guard):   
        #printMatrix(matrix, guard, v, possibleBlock, False)
        visitedCoordinates.setdefault(guard, []).append(v)
        nextStep = calcNextStep(guard, v)
        if beenHereWithThisDirection(nextStep, visitedCoordinates, v):
            #print("Been here", nextStep, v)
            return True
        if isBlocked(nextStep) or possibleBlock == nextStep:
            v = turnRight(v)
        elif possibleBlock == None:
            if nextStep != originGuard and nextStep not in possibleNewBlock and nextStep not in visitedCoordinates:
                currentVisitedCoordinates = copy.deepcopy(visitedCoordinates)
                newMatrix = copy.deepcopy(matrix)
                #print("Testing circle", nextStep, len(visitedCoordinates))
                if findCircle(newMatrix, guard, possibleNewBlock, currentVisitedCoordinates, v, nextStep):
                    #print("Found circle", len(possibleNewBlock))
                    #if nextStep == (49, 49):
                        #printMatrix(newMatrix, guard, v, nextStep, True)
                    #    return True
                    possibleNewBlock[nextStep] = True
                #else:
                #    print("No circle", len(visitedCoordinates))     
            guard = nextStep
        else:
            guard = nextStep
    #if possibleBlock != None:
    #   print("Guard left map")     
    return False

possibleNewBlock = {}
visitedCoordinates = {}

findCircle(matrix, originGuard, possibleNewBlock, visitedCoordinates, v0)
print(len(possibleNewBlock))
end = time.time()
print("It took", end - start, "seconds!")
#findCircle(matrix, originGuard, possibleNewBlock, visitedCoordinates, v0, (49, 49))
#printMatrix(matrix, originGuard, v0,  (49, 49), True)
exit(0)

notCircle = []
for newBlock in possibleNewBlock:
    print("testCircle", newBlock)
    if not findCircle(matrix, originGuard, {}, {}, v0, newBlock):
        print("Not circle")
        notCircle.append(newBlock)

print("Not circle", len(notCircle), notCircle)

for b in notCircle:
    del possibleNewBlock[b]

#print(possibleNewBlock)
print(len(possibleNewBlock))


