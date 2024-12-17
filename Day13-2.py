from decimal import Decimal as D
f = open("Day13.input.txt", "r")
matrix = []
input = f.read().splitlines()
BBBB = 10000000000000
machines = []
currentMachine = None
for line in input:
    if line == "" or currentMachine == None:
        currentMachine = {
            "A": {
                "cost": 3,
                "type" : "A"
            },
            "B": {
                "cost": 1,
                "type" : "B"
            }
        }
        machines.append(currentMachine)
    
    if line == "":
        continue

    (button, controls) = line.split(':')
    buttonType =  button[-1]

    (x, y) = controls.split(',')
    x = x.strip()
    y = y.strip()
    if buttonType == 'A' or buttonType == 'B':
        dx = x.split('+')[1]
        dy = y.split('+')[1]
        currentMachine[buttonType]['dx'] = int(dx)
        currentMachine[buttonType]['dy'] = int(dy)
    else:
        px = int(x.split('=')[1]) + BBBB
        py = int(y.split('=')[1]) + BBBB
        currentMachine['prize'] = (px, py)

foundPrizes = {}

def createQueueItem(start, cost, aCount = 0, bCount = 0):
    return {
        'element' : start,
        'tokenCount': cost,
        'aCount': aCount,
        'bCount': bCount
    }

def getToBBBB(machine):
    global BBBB
    maxA = min(BBBB // machine['A']['dx'], BBBB // machine['A']['dy'])
    maxB = min(BBBB // machine['B']['dx'], BBBB // machine['B']['dy'])
    for b in range(maxB, -1, -1000):
        x = b * machine['B']['dx']
        y = b * machine['B']['dy']

        for a in range(maxA):
            newX = x + a * machine['A']['dx']
            newY = y + a * machine['A']['dy']
            if (newX, newY) == (BBBB, BBBB):
                print("Found  (BBBB, BBBB) at", (a, b))
                return (a, b)
            if newX > BBBB or newY > BBBB:
                break
            print('({0: <14}, {1: <14})'.format(a, b), end='\r')
    print("Couldn't find  (BBBB, BBBB)")
    

def dfs(machine, start, end, visited, aCount, bCount, tokenCount, foundPrizes):
    if (start[0] < 0 or start[1] < 0):
        #print("negative")
        return

    if start in visited: # and visited[start] < tokenCount:
        return
    
    if (aCount + bCount) > 800:
        #print("Too many buttons")
        return
    
    prize = machine['prize']
    visited[start] = tokenCount
    if start == end:
        if prize not in foundPrizes or foundPrizes[prize] > tokenCount:
            foundPrizes[prize] = tokenCount
        return
    
    if start[0] <= BBBB and start[1] <= BBBB:
        b = start[0] // machine['B']['dx']
        if start[0] % machine['B']['dx'] == 0 and start[1] == b * machine['A']['dy']:
            #print('can divide evenly with A')
            newTokenCount = tokenCount + (b * machine['B']['cost'])
            foundPrizes[prize] = newTokenCount
            return
        a = start[0] // machine['A']['dx']
        if start[0] % machine['A']['dx'] == 0 and start[1] == a * machine['A']['dy']:
            #print('can divide evenly with A')
            newTokenCount = tokenCount + (a * machine['A']['cost'])
            foundPrizes[prize] = newTokenCount
            return
        

    for button in [machine['A'], machine['B']]:
        newAcount = aCount + 1 if button['type'] == 'A' else aCount
        newBcount = bCount + 1 if button['type'] == 'B' else bCount
        newX = start[0] - button['dx']
        newY = start[1] - button['dy']
        newTokenCount = tokenCount + button['cost']
        # if (newTokenCount % 10 == 0):
        #     print('({}, {})'.format(newX, newY), end='\r')
        dfs(machine, (newX, newY), end, visited, newAcount, newBcount, newTokenCount, foundPrizes)


def bfs(machine, start, end, visited, foundPrizes, startCost = 0):
    queue = []
    startItem = createQueueItem(start, startCost)
    queue.append(startItem)
    prize = machine['prize']
    while(len(queue) > 0):
        item = queue.pop()
        element = item['element']
        tokenCount = item['tokenCount']
        
        if element[0] < 0 or element[1] < 0:
            return

        if prize in foundPrizes and foundPrizes[prize] < tokenCount:
            return

        if start[0] < BBBB and start[1] < BBBB and start[0] %  machine['A']['dx'] == 0 and start[1] % machine['A']['dy']:
            print('can divide evenly with A')
            newTokenCount = tokenCount + start[0] / machine['A']['dx'] * machine['A']['cost']
            foundPrizes[prize] = tokenCount
            return

        if start[0] < BBBB and start[1] < BBBB and start[0] %  machine['B']['dx'] == 0 and start[1] % machine['B']['dy']:
            print('can divide evenly with B')
            newTokenCount = tokenCount + start[0] / machine['B']['dx'] * machine['B']['cost']
            foundPrizes[prize] = tokenCount
            return

        if element in visited: # and visited[start] < tokenCount:
            return

        visited[element] = tokenCount
        if element == end:
            if prize not in foundPrizes or foundPrizes[prize] > tokenCount:
                foundPrizes[prize] = tokenCount
            return
        for button in [machine['A'], machine['B']]:
            newX = element[0] - button['dx']
            newY = element[1] - button['dy']
            newAcount = item['aCount'] + 1 if button['type'] == 'A' else item['aCount']
            newBcount = item['bCount'] + 1 if button['type'] == 'B' else item['bCount']
            newTokenCount = tokenCount + button['cost']
            newItem = createQueueItem((newX, newY), newTokenCount, newAcount, newBcount)
            queue.append(newItem)

def isInt(x):
    return x%1 == 0

def solveMachine(machine):
    prize = machine['prize']
    Px = D(prize[0])
    #Py = prize[1]
    dxa = D(machine['A']['dx'])
    dxb = D(machine['B']['dx'])
    dya = D(machine['A']['dy'])
    dyb = D(machine['B']['dy'])
    SP = D(sum(prize))
    SA = D(sum([dxa, dya]))
    SB = D(sum([dxb, dyb]))
    A = (Px - dxb*SP/SB) / (dxa - SA*dxb/SB)
    B = (SP - A * SA) / SB

    A = round(A, 5)
    B = round(B, 5)

    if not isInt(A) or not isInt(B):
        return 1.1234

    return A * machine['A']['cost'] + B * machine['B']['cost']

for machine in machines:
    print(machine)
    tokensNeeded = solveMachine(machine)
    if isInt(tokensNeeded):
        foundPrizes[machine['prize']] = tokensNeeded
        print("Found prize for machine {} -> tokenCount: {}".format(machine, foundPrizes[machine['prize']]))

print(sum(foundPrizes.values()))
