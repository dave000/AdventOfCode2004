f = open("Day8.input.txt", "r")
matrix = []
input = f.readlines()

currentY = 0
for line in input:
    lineGraph = []
    matrix.append(lineGraph)
    for i in line:
        if i == '\n':
            continue
        lineGraph.append(i)

dimension = (len(matrix), len(matrix[0]))


def notOnMap(antinode):
    global dimension
    return antinode[0] >= dimension[0] or antinode[0] < 0 or antinode[1] >= dimension[1] or antinode[1] < 0

def getAntennaDistance(a, b):
    return (b[0] - a[0], b[1] - a[1])

def calcAntiNodeFromAntenna(antenna, d):
    return tuple(map(sum, zip(antenna, d)))

def getAntiNodeLocation(antenna, d):
    antiNodeLoc = calcAntiNodeFromAntenna(antenna, d)
    if notOnMap(antiNodeLoc):
        return None
    return antiNodeLoc

antennas = {}
anti_nodes = {}
for row in range(0, len(matrix)):
    for col in range(0, len(matrix[row])):
        cel = (row, col)
        f = matrix[row][col]
        if f != ".":
            antennas.setdefault(f, []).append(cel)
#rint(antennas)
for f in antennas:
    f_antennas = antennas[f]
    f_antenna_count = len(f_antennas)
    for i in range(0, f_antenna_count):
        for j in range(0, f_antenna_count):
            if i != j:
                firstAntenna = None
                secondAntenna = None
                if j > i:
                    firstAntenna = f_antennas[i]
                    secondAntenna = f_antennas[j]
                else:
                    firstAntenna = f_antennas[j]
                    secondAntenna = f_antennas[i]
                anti_nodes[firstAntenna] = True
                anti_nodes[secondAntenna] = True
                d = getAntennaDistance(firstAntenna, secondAntenna)
                antiNode1 = getAntiNodeLocation(firstAntenna, (-d[0], -d[1]))
                antiNode2 = getAntiNodeLocation(secondAntenna, d)
                if antiNode1 != None:
                    anti_nodes[antiNode1] = True
                if antiNode2 != None:
                    anti_nodes[antiNode2] = True
                while antiNode1 != None:
                    antiNode1 = getAntiNodeLocation(antiNode1, (-d[0], -d[1]))
                    if antiNode1 != None:
                        anti_nodes[antiNode1] = True
                while antiNode2 != None:
                    antiNode2 = getAntiNodeLocation(antiNode2, d)
                    if antiNode2 != None:
                        anti_nodes[antiNode2] = True

                   
#print(anti_nodes)
print(len(anti_nodes))