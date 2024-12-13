f = open("Day12.input.txt", "r")
matrix = []
input = f.readlines()


for line in input:
    lineGraph = []
    matrix.append(lineGraph)
    for i in line:
        if i == '\n':
            continue
        lineGraph.append(i)

dimension = (len(matrix), len(matrix[0]))


def notOnMap(seg):
    global dimension
    return seg[0] >= dimension[0] or seg[0] < 0 or seg[1] >= dimension[1] or seg[1] < 0


regions = []
elementToRegionMap = {}
alreadyVisited = {}

def getType(matrix, element):
    return matrix[element[0]][element[1]]

def isSame(type, matrix, element):
    return type == getType(matrix, element)
    

def getNextNeighbours(type, element, matrix):
    neighbours = []
    possibleNeighbours = []
    possibleNeighbours.append((element[0], element[1] - 1))
    possibleNeighbours.append((element[0], element[1] + 1))
    possibleNeighbours.append((element[0] - 1, element[1]))
    possibleNeighbours.append((element[0] + 1, element[1]))

    for pn in possibleNeighbours:
        if not notOnMap(pn) and isSame(type, matrix, pn):
            neighbours.append(pn)
    return neighbours

def dfs(type, start, matrix, region):
    global elementToRegionMap, alreadyVisited
    elementToRegionMap[start] = region['id']
    neighbours = getNextNeighbours(type, start, matrix)
    region["elements"][start] = type
    for n in neighbours:
        if n not in region["elements"] and n not in alreadyVisited:
            region["elements"][n] = type
            dfs(type, n, matrix, region)

def addAllFound(alreadyVisited, region):
    for e in region["elements"]:
        alreadyVisited[e] = True


for i in range(dimension[0]):
    for j in range(dimension[1]):
        element = (i, j)
        if element in alreadyVisited:
            continue
        type = getType(matrix, (i, j))
        region = {
            'firstRegionElement' : element,
            'id': str(i) + str(j),
            'type': type,
            'elements' : {}
        }
        dfs(type, element, matrix, region)
        addAllFound(alreadyVisited, region)
        regions.append(region)

def getArea(region):
    return len(region["elements"])

def getDifferentRegionFromElement(element, elementToRegionMap, currentRegion):
    return None if notOnMap(element) or elementToRegionMap[element] == currentRegion else elementToRegionMap[element]

def getNeighbourRegions(element, elementToRegionMap, currentRegion):
    upElement =    (element[0] - 1, element[1])
    downElement =  (element[0] + 1, element[1])
    leftElement =  (element[0],     element[1] - 1)
    rightElement = (element[0],     element[1] + 1)
    #print(element)
    return {
        "up": getDifferentRegionFromElement(upElement, elementToRegionMap, currentRegion),
        "down": getDifferentRegionFromElement(downElement, elementToRegionMap, currentRegion),
        "left": getDifferentRegionFromElement(leftElement, elementToRegionMap, currentRegion),
        "right": getDifferentRegionFromElement(rightElement, elementToRegionMap, currentRegion),
    }


def getPerimeter(regions, region):
    global elementToRegionMap
    if len(region["elements"]) == 1:
        return 4
    fencesNeeded = 0
    regionId =  region['id']
    t =  region['type']
    elementsInRows = {}
    for element in region["elements"]:
        row = element[0]
        col = element[1]
        elementsInRows.setdefault(row, {})
        elementsInRows[row][col] = element
    lastRow = None
    allNeighbourRegions = {
        "up" : [],
        "down": [],
        "left": [],
        "right": []
    }
    orederedRows = sorted(elementsInRows)
    for row in sorted(elementsInRows):
        orderedCols = sorted(elementsInRows[row])
        for col in orderedCols:
            element = elementsInRows[row][col]
            neighborRegions = getNeighbourRegions(element, elementToRegionMap, regionId)
            for n in neighborRegions:
                if neighborRegions[n] != None:
                    allNeighbourRegions[n].append(neighborRegions[n])
            if  neighborRegions["up"] != None or row == orederedRows[0]:
                fencesNeeded += 1
            if  neighborRegions["down"] != None or row == orederedRows[-1]:
                fencesNeeded += 1
            if neighborRegions["left"] != None or col == orderedCols[0]: #something else on the left side or first element
                fencesNeeded += 1
            if neighborRegions["right"] != None or col == orderedCols[-1]: #something else on the right side or last element:
                fencesNeeded += 1
    

    # if all(len(n) > 0 for n in allNeighbourRegions):
    #     nRegions = []
    #     for n in allNeighbourRegions:
    #         nRegions.extend(allNeighbourRegions[n])
    #     distRegions = set(nRegions)
    #     if len(distRegions) == 1:
    #         fencesNeeded += fencesNeeded

    #we add the last row after counting already used fences as if above is different we add another fence either way
    #elementsInLastRow = len(elementsInRows[lastRow])
    #fencesNeeded += elementsInLastRow

    return fencesNeeded


fencePrices = 0
for region in regions:
    A = getArea(region)
    P = getPerimeter(regions, region)
    fencePrice = A * P
    print("A region of " + region['type'] + ' plans with price ' + str(A) + ' * ' + str(P) + ' = ' + str(fencePrice))
    fencePrices += fencePrice

print(fencePrices)

