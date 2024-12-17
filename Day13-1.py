from decimal import Decimal as D

f = open("Day13.input.txt", "r")
matrix = []
input = f.read().splitlines()

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
        px = int(x.split('=')[1])
        py = int(y.split('=')[1])
        currentMachine['prize'] = (px, py)

foundPrizes = {}

def dfs(machine, start, end, visited, aCount, bCount, tokenCount, foundPrizes):
    if aCount > 100 or bCount > 100:
        #print("Too many buttons")
        return
    
    if (start[0] < 0 or start[1] < 0):
        #print("negative")
        return

    if start in visited: # and visited[start] < tokenCount:
        return

    visited[start] = tokenCount
    if start == end:
        prize = machine['prize']
        if prize not in foundPrizes or foundPrizes[prize] > tokenCount:
            foundPrizes[prize] = tokenCount
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

def isInt(x):
    return x%1 == 0

for machine in machines:
    #print(machine)
    dfs(machine,  machine['prize'], (0, 0), {}, 0, 0, 0, foundPrizes)
    tokensNeeded = round(solveMachine(machine), 10)
    if machine['prize'] in foundPrizes:
        dfsNeeded = foundPrizes[machine['prize']]
        if dfsNeeded != tokensNeeded:
            print("Found prize for machine {} -> tokenCount: {}, mathReturned: {}, Same: {}".format(machine, foundPrizes[machine['prize']], tokensNeeded, dfsNeeded == tokensNeeded))
    elif isInt(tokensNeeded):
        print("Math retunrned", tokensNeeded)


print(sum(foundPrizes.values()))
