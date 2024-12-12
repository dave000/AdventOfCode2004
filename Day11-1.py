import math
stones = [2, 54, 992917, 5270417, 2514, 28561, 0, 990]
#stones = [125, 17]
print(len(stones))

for blink in range(25):
    newStones = []
    for i in range(len(stones)):
        stone = stones[i]
        stoneStr = str(stone)
        l = len(stoneStr)
        if stone == 0:
            newStones.append(1)
        elif l % 2 == 0:
            m = math.floor(l/2)
            firstStone = stoneStr[0:m]
            secondStone = stoneStr[m:]
            newStones.append(int(firstStone))
            newStones.append(int(secondStone))
        else:
            newStones.append(stone * 2024)
    stones = newStones
    print(len(stones))

print(len(stones))

