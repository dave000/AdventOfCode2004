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
maxT = 10000000
def xMasTreeLeft(x):
     b = D(102)
     a = D(-102) / D(50) 
     return round(D(a) * D(x) + b, 5)


def inQ(p, q):
     return p[0] < q[0] and p[1] < q[1]


def robotPos(s, v, t):
     global maxX, maxY
     return ((s[0] + t * v[0]) % maxX, (s[1] + t * v[1]) % maxY)

robotPositions[0] = []
for i in range(1):
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

    pos100 = robotPos(s, v, afterSec)


    (x, y) = robotPos(s, v, 28)
    if (x == 50):
        robotPositions[0][y][x] = "|"
        print('its 50')
    else:
        robotPositions[0][y][x] = "8"

    fiftyTimes = is50(s, v)
    if len(fiftyTimes) == 0:
        continue
    robot = {
        's' : s,
        'v' : v,
        'fiftyTimes' : fiftyTimes
    }
    #print(robot)
    robots.append(robot)

most50 = {}

for r in robots:
    for i in r['fiftyTimes']:
        most50.setdefault(i, 0)
        most50[i] += 1

most = 0
mostT = -1
for t in most50:
    if most50[t] > most:
        most = most50[t]
        mostT = t

print("Most in 50", most, "at t", mostT)

#exit(0)
for t in robotPositions:
    for rowX in robotPositions[t]:
        row = ""
        for a in rowX:
            row += str(a)
        print(row)
    print("#####################################################################################################")
    break


