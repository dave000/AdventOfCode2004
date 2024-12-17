f = open("Day14.input.txt", "r")
matrix = []
input = f.read().splitlines()
robots = {
    'q1' : 0, # [],
    'q2' : 0, #[],
    'q3' : 0, #[],
    'q4' : 0, #[],
}
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

def inQ(p, q):
     return p[0] < q[0] and p[1] < q[1]

for line in input:
   
    (initValues, velocityValues) = line.split(' ')
    startValues =  initValues.split('=')[1].split(',')
    velocityValues = velocityValues.split('=')[1].split(',')

    s = (int(startValues[0]), int(startValues[1]))
    v = (int(velocityValues[0]), int(velocityValues[1]))


    pos100 = ((s[0] + afterSec * v[0]) % maxX, (s[1] + afterSec * v[1]) % maxY)
    robot = {
        's' : s,
        'v' : v,
        'pos100' : pos100
    }

    if midX == pos100[0] or midY == pos100[1]:
         continue

    if inQ(pos100, q1Max):
         robots['q1'] = robots['q1'] + 1
    elif inQ(pos100, q2Max):
         robots['q2'] = robots['q2'] + 1
    elif inQ(pos100, q3Max):
         robots['q3'] = robots['q3'] + 1
    else:
         robots['q4'] = robots['q4'] + 1

mul = 1
for q in robots:
     mul *= robots[q]

print(mul)


