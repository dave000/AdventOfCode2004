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

def getNextElement(element, v):
    global dimension
    nextElement = tuple(map(sum, zip(element, v)))
    if (nextElement[0] < 0 or nextElement[1] < 0 or nextElement[0] == dimension[0] or nextElement[1] == dimension[1]):
        return None
    else:
        return nextElement


def isXmasStart(c):
    return c == 'A'

def getCharFromElement(e):
    global matrix
    return matrix[e[0]][e[1]]

def isXmasText(text):
    return text == 'MAS' or text == 'SAM'

foundXmasCounter = 0

def getAllText(start, end, v):
    char = getCharFromElement(start)
    if (start == end):
        return char
    else:
        return char + getAllText(getNextElement(start, v), end, v)

def findXmasFrom(i, j):
    global matrix,foundXmasCounter
    start = (i, j)
    print((i, j))
    nwElement = getNextElement(start, (-1, -1))
    neElement = getNextElement(start, (-1, 1))
    seElement = getNextElement(start, (1, 1))
    swElement = getNextElement(start, (1, -1))
    if None in [nwElement, neElement, seElement, swElement]:
        return
    nwseText = getAllText(nwElement, seElement, (1, 1))
    neswText = getAllText(neElement, swElement, (1, -1))
    
    if isXmasText(nwseText) and isXmasText(neswText):
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