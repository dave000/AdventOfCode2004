f = open("Day4.input.txt", "r")
matrix = []
input = f.readlines()
max_depth = 4


for line in input:
    lineGraph = []
    matrix.append(lineGraph)
    for i in line:
        if i == '\n':
            continue
        lineGraph.append(i)

foundXmas = {}

dimension = (len(matrix), len(matrix[0]))

def buildGraphFrom(i, j, graph = {}, parent = None, v = None, level = 0):
    global dimension
    
    if (level > 3):
        return graph
    element = (i, j)
    children = []
    if (element not in graph):
        graph[element] = children
    if parent == None and v == None:
        graph = buildGraphFrom(element[0], element[1], graph, element, (0, 1), level + 1)
        graph = buildGraphFrom(element[0], element[1], graph, element, (0, -1), level + 1)
        graph = buildGraphFrom(element[0], element[1], graph, element, (1, 0), level + 1)
        graph = buildGraphFrom(element[0], element[1], graph, element, (1, 1), level + 1)
        graph = buildGraphFrom(element[0], element[1], graph, element, (1, -1), level + 1)
        graph = buildGraphFrom(element[0], element[1], graph, element, (-1, 0), level + 1)
        graph = buildGraphFrom(element[0], element[1], graph, element, (-1, 1), level + 1)
        graph = buildGraphFrom(element[0], element[1], graph, element, (-1, -1), level + 1)
    else:
        nextElement = tuple(map(sum, zip(element, v)))
        if (level > 3 or nextElement[0] < 0 or nextElement[1] < 0 or nextElement[0] == dimension[0] or nextElement[1] == dimension[1]):
            return graph
        graph[parent].append(nextElement)
        return buildGraphFrom(nextElement[0], nextElement[1], graph, nextElement, v, level + 1)
    
    return graph

def isXmasStart(c):
    return c == 'X'

def getCharFromElement(e):
    global matrix
    return matrix[e[0]][e[1]]

def isXmasText(text):
    return text == 'XMAS'

def getAllChildren(start, graph, aggregatorText):
    aggregatorText += getCharFromElement(start)
    if start in graph:
        for element in graph[start]:
            return getAllChildren(element, graph, aggregatorText)
    return (aggregatorText, start)
foundXmasCounter = 0
def findXmasFrom(i, j):
    global matrix,foundXmasCounter
    start = (i, j)
    #print((i, j))
    graph = buildGraphFrom(i, j, {})
    startChar = getCharFromElement(start)

    for element in graph[start]:
        aggregatorText = startChar
        #print("getAllChildern", start)
        result = getAllChildren(element, graph, aggregatorText)
        aggregatorText = result[0]
        lastElement = result[1]
        isXmas = isXmasText(aggregatorText)
        if isXmas and (lastElement not in foundXmas or start not in foundXmas[lastElement]):
            if start not in foundXmas:
                foundXmas[start] = [lastElement]
            else:
                foundXmas[start].append(lastElement)
            foundXmasCounter += 1
            #print("is it XMAS/SAMX", aggregatorText, isXmas, (i,j), lastElement)

def tryFindXmasFrom(i, j):
    if isXmasStart(matrix[i][j]):
        findXmasFrom(i, j)



for i in range(0, dimension[0]):
    for j in range(0, dimension[1]):
        tryFindXmasFrom(i, j)


#print(foundXmas)
print(foundXmasCounter)