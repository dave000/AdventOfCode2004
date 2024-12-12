import math
stones = [2, 54, 992917, 5270417, 2514, 28561, 0, 990]

remember = {}

#stones = [125, 17]
stonesCount = len(stones)
stoneCounter = len(stones)
maxBlink = 75
def blinkStone(stone, blink, newStones = 0):
    global stoneCounter, maxBlink, remember

    if (blink >= maxBlink):
        return newStones

    if ((stone, blink, newStones) in remember):
        #print("remembering",(stone, blink), remember[(stone, blink, newStones)])
        return remember[(stone, blink, newStones)]

    stoneStr = str(int(stone))
    l = len(stoneStr)
    if stone == 0:
        remember[(stone, blink, newStones)] = newStones + blinkStone(1, blink + 1)       
    elif l % 2 == 0:
        m = l // 2
        firstStone = stoneStr[0:m]
        secondStone = stoneStr[m:]
        remember[(stone, blink, newStones)] =  newStones + blinkStone(int(firstStone), blink + 1) + blinkStone(int(secondStone), blink + 1, 1)
    else:
        remember[(stone, blink, newStones)] =  newStones + blinkStone(stone * 2024, blink + 1)
    return remember[(stone, blink, newStones)]



for stone in stones:
    print(stone)
    stonesCount += blinkStone(stone, 0)

print(stonesCount)

