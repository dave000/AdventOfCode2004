import math
stones = [2, 54, 992917, 5270417, 2514, 2856, 0, 990]
#stones = [125, 17]
print(len(stones))

for blink in range(25):
    newStones = []
    for i in range(len(stones)):
        stone = stones[i]
        stoneStr = str(float(stone)).split(".")[0]
        l = len(stoneStr)
        if stone == 0:
            newStones.append(1)
        elif l % 2 == 0:
            m = math.floor(l/2)
            firstStone = stoneStr[0:m]
            secondStone = stoneStr[m:]
            newStones.append(float(firstStone))
            newStones.append(float(secondStone))
        else:
            newStones.append(stone * 2024)
    stones = newStones
    print(len(stones))

#print(len(stones))

