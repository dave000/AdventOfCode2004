import copy

f = open("Day16.input.txt", "r")
matrix = []
input = f.read().splitlines()



start = None
end = None
endKey = (end, (0, 0))
v = (0, 1)

currentY = 0
for line in input:
    lineGraph = []
    matrix.append(lineGraph)
    currentX = 0
    for i in line:
        if i == 'S':
            start = (currentY, currentX)
        if i == 'E':
            end = (currentY, currentX)
        lineGraph.append(i)
        currentX += 1
    currentY += 1

stepCounter = 0
dimension = (len(matrix), len(matrix[0]))

def printMatrix(currentMatrix, path):
    for row in range(0, len(currentMatrix)):
        line = ""
        for col in range(0, len(currentMatrix[row])):
            cel = (row, col)
            if cel in path:
                line += "O"
            else:
                line += currentMatrix[cel[0]][cel[1]]
        print(line)

    print(" ")
    print(" ")
    print(" ")


def isBlocked(coordinate):
    global matrix
    return matrix[coordinate[0]][coordinate[1]] == '#'

def calcNextStep(currentDeer, v):
    return tuple(map(sum, zip(currentDeer, v)))

def turnRight(currentV):
    return (currentV[1], -currentV[0])

def turnLeft(currentV):
    return (-currentV[1], currentV[0])

visitedCoordinates = {}
bestPaths = {}
def dfs(start, end, v, visited, cost, d, path):
    global bestPaths
    if (d > 900):
        return

    #print(start)
    if (start == end):
        path.append(end)
        visited[endKey] = cost
        bestPaths.setdefault(cost, []).extend(path)
        return

    if (start, v) in visited and visited[(start, v)] < cost:
        #print("Already in visited with lower cost", start, visited[(start, v)], cost)
        return

    if endKey in visited and visited[endKey] < cost:
        return
    
    
    visited[(start, v)] = cost
    nextStep = calcNextStep(start, v)
    myPath = list(path)
    myPath.append(start)
    if not isBlocked(nextStep):
      dfs(nextStep, end, v, visited, cost + 1, d + 1, myPath)
    vl = turnLeft(v)
    vr = turnRight(v)
    dfs(start, end, vl, visited, cost + 1000, d + 1,  myPath)
    dfs(start, end, vr, visited, cost + 1000, d + 1,  myPath)

print("Startin", start, end)
dfs(start, end, v, visitedCoordinates, 0, 0, [])

if endKey in visitedCoordinates:
    print("End", visitedCoordinates[endKey])
else:
    print("NOt found")


for c in sorted(bestPaths.keys()):
    print("Best paths", c, len(set(bestPaths[c])))


# printMatrix(matrix, bestPaths[99448])
# print(len(bestPaths[99448]))