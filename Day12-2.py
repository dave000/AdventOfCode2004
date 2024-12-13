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
            'id': str(i) + "#" + str(j),
            'type': type,
            'elements' : {},
            'fences' : {}
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
def getFenceKey(row, col, p):
    return'{}#{}#{}'.format(row, col, p)

def parseFenceKey(key):
    keys = key.split("#")
    return (int(keys[0]), int(keys[1]), keys[2])

def getSides(regions, region):
    global elementToRegionMap
    sides = 0
    regionId =  region['id']
    t =  region['type']
    fences = region['fences']
    elementsInRows = {}
    for element in region["elements"]:
        row = element[0]
        col = element[1]
        elementsInRows.setdefault(row, {})
        elementsInRows[row][col] = element

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
                fenceKey = getFenceKey(row, col, "U")    
                fences[fenceKey] = True
            if  neighborRegions["down"] != None or row == orederedRows[-1]:
                fenceKey = getFenceKey(row, col, "D")    
                fences[fenceKey] = True
            if neighborRegions["left"] != None or col == orderedCols[0]: #something else on the left side or first element
                fenceKey = getFenceKey(row, col, "L")    
                fences[fenceKey] = True
            if neighborRegions["right"] != None or col == orderedCols[-1]: #something else on the right side or last element:
                fenceKey = getFenceKey(row, col, "R")
                print(fenceKey)
                fences[fenceKey] = True
    def clearFences(row, col, f):
        key = getFenceKey(row, col, f)
        if key in fences:
            fences[key] = False
            return True
        return False
    while any(fences.values()):
        notCountedFences = sorted({k:v for (k,v) in fences.items() if v})
        for fenceKey in notCountedFences:
            (row, col, f) = parseFenceKey(fenceKey)
            if not fences[fenceKey]:
                continue
            fences[fenceKey] = False
            sides += 1
            if f == "U" or f == "D":
                for i in range(col + 1, dimension[1]):
                    if i >= dimension[1]:
                        break
                    hasKey = clearFences(row, i, f)
                    if not hasKey:
                        break
                for i in range(col - 1, 0, -1):
                    if i < 0:
                        break
                    hasKey = clearFences(row, i, f)
                    if not hasKey:
                        break
            else:
                for i in range(row + 1, dimension[0]):
                    if i >= dimension[0]:
                        break
                    hasKey = clearFences(i, col, f)
                    if not hasKey:
                        break
                for i in range(row - 1, 0, -1):
                    if i < 0:
                        break
                    hasKey = clearFences(i, col, f)
                    if not hasKey:
                        break
    return sides
    

    # if all(len(n) > 0 for n in allNeighbourRegions):
    #     nRegions = []
    #     for n in allNeighbourRegions:
    #         nRegions.extend(allNeighbourRegions[n])
    #     distRegions = set(nRegions)
    #     if len(distRegions) == 1:
    #         sides += sides

    #we add the last row after counting already used fences as if above is different we add another fence either way
    #elementsInLastRow = len(elementsInRows[lastRow])
    #sides += elementsInLastRow

    #return sides


fencePrices = 0
for region in regions:
    A = getArea(region)
    P = getSides(regions, region)
    fencePrice = A * P
    print("A region of " + region['type'] + ' plans with price ' + str(A) + ' * ' + str(P) + ' = ' + str(fencePrice))
    fencePrices += fencePrice

print(fencePrices)

