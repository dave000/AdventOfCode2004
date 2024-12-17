from decimal import Decimal as D
f = open("Day14.input.txt", "r")
matrix = []
input = f.read().splitlines()
robots = []
maxX = 101
maxY = 103
midX = (maxX - 1) // 2
midY = (maxY - 1) // 2
q1Max = (midX, midY)
q2Max = (midX, maxY)
q3Max = (maxX, midY)
q4Max = (maxX, maxY)


currentMachine = None

afterSec = 100

robotPositions = {}
maxT = 10000
def xMasTreeLeft(x):
     b = D(102)
     a = D(-102) / D(50) 
     return round(D(a) * D(x) + b, 5)


def inQ(p, q):
     return p[0] < q[0] and p[1] < q[1]


def robotPos(s, v, t):
     global maxX, maxY
     return ((s[0] + t * v[0]) % maxX, (s[1] + t * v[1]) % maxY)

for i in range(maxT):
    robotPositions[i] = []
    for r in range(maxY):
        cols = []
        robotPositions[i].append(cols)
        for c in range(maxX):
            cols.append(str("."))

def is50(s, v):
    whenIs50x = []

    for i in range(maxT):
       (x, y) = robotPos(s, v, i)
       if x == 50:
            whenIs50x.append(i)
    return whenIs50x



for line in input:
    #line = input[1]
    (initValues, velocityValues) = line.split(' ')
    startValues =  initValues.split('=')[1].split(',')
    velocityValues = velocityValues.split('=')[1].split(',')

    s = (int(startValues[0]), int(startValues[1]))
    v = (int(velocityValues[0]), int(velocityValues[1]))

    #pos100 = robotPos(s, v, afterSec)
    beenHere = set()
    for i in range(0, maxT):
        (x, y) = robotPos(s, v, i)
        if (x, y) in beenHere:
            print("Stopped after", i)
            break
        beenHere.add((x, y))
        robotPositions[i][y][x] = "8"
       
    robot = {
        's' : s,
        'v' : v
    }
    print(robot)
    robots.append(robot)

#exit(0)

def notOnMap(seg):
    return seg[0] >= maxX or seg[0] < 0 or seg[1] >= maxY or seg[1] < 0

def findClusters(x, y, robotPositions, foundElements):
    pos = (x, y)
    if notOnMap(pos) or robotPositions[y][x] != '8' or pos in foundElements:
        return

    foundElements[(x, y)] = True
        
    findClusters(x, y - 1, robotPositions, foundElements)
    findClusters(x, y + 1, robotPositions, foundElements)
    findClusters(x + 1, y, robotPositions, foundElements)
    findClusters(x + 1, y + 1, robotPositions, foundElements)
    findClusters(x + 1, y - 1, robotPositions, foundElements)
    findClusters(x - 1, y, robotPositions, foundElements)
    findClusters(x - 1, y + 1, robotPositions, foundElements)
    findClusters(x - 1, y - 1, robotPositions, foundElements)


maxCluster = 0
maxClusterT = 0
printT = 7286
for t in [7286]:
    for rowX in range(len(robotPositions[t])):
        row = ""
        for a in range(len(robotPositions[t][rowX])):
            row += str(robotPositions[t][rowX][a])
            foundClusters = {}
            findClusters(rowX, a, robotPositions[t], foundClusters)
            clusters = len(foundClusters)
            if maxCluster < clusters:
                maxCluster = clusters
                maxClusterT = t
                print("Cluster at", t, maxCluster)
        if t == printT:
            print(row)
    if t == printT:
        print("#####################################################################################################")

print(maxCluster, maxClusterT)


