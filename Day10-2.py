f = open("Day10.input.txt", "r")
matrix = []
input = f.readlines()

trailHeads = []
currentY = 0
for line in input:
    lineGraph = []
    matrix.append(lineGraph)
    currentX = 0
    for i in line:
        if i == '\n':
            continue
        h = int(i)
        if h == 0:
            trailHeads.append((currentY, currentX))
        lineGraph.append(h)
        currentX+=1
    currentY+=1
dimension = (len(matrix), len(matrix[0]))

def doesNotExist(step):
    global dimension
    return step[0] >= dimension[0] or step[0] < 0 or step[1] >= dimension[1] or step[1] < 0

def getHeight(matrix, element):
    return matrix[element[0]][element[1]]

def isNext(matrix, step, currentH):
    h = getHeight(matrix, step)
    return h == currentH + 1

def getNextNeighbours(currentH, element, matrix):
    neighbours = []
    possibleNeighbours = []
    possibleNeighbours.append((element[0], element[1] - 1))
    possibleNeighbours.append((element[0], element[1] + 1))
    possibleNeighbours.append((element[0] - 1, element[1]))
    possibleNeighbours.append((element[0] + 1, element[1]))

    for pn in possibleNeighbours:
        if not doesNotExist(pn) and isNext(matrix, pn, currentH):
            neighbours.append(pn)
    return neighbours

def dfs(matrix, start, end, visited, found9):
    h = getHeight(matrix, start)
    if (h == end):
        found9.setdefault(start, []).append(visited)
        return
    
    nextElements = getNextNeighbours(h, start, matrix)
    for e in nextElements:
        if e not in visited:
            visited[e] = True
            dfs(matrix, e, end, visited.copy(), found9)

sumOfScore = 0
for start in trailHeads:
    found9 = {}
    visited = {}
    visited[start] = True
    dfs(matrix, start, 9, visited.copy(), found9)
    for f9 in found9:
         #uniqueTrailers = set(found9[f9])
         sumOfScore += len(found9[f9])
   

print(sumOfScore)