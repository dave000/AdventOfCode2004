f = open("Day3.input.txt", "r")
input = f.read()

c = 0
l = len(input)

def tryGetDigit(delimiter):
    global input
    global c
    hadDigit = False
    for i in range(0, 4):
        if isMul(c+i, False) or isDo(c+i, False) or isDont(c+i, False):
            c += i
            return None
        d = input[c+i]
        if d == delimiter and hadDigit:
            number = int(input[c:c+i])
            c+=i+1
            return number
        if d.isdigit():
            hadDigit = True
        else:
            c+=i+1
            return None
    c+=4
    return None
          

def tryGetMul():
    x = tryGetDigit(',')
    y = tryGetDigit(')')
    if x == None or y == None:
         return -1
    return x * y
   

def isMul(startIndex, doInc):
    global input
    global c
    if input[startIndex] == 'm':
        if input[startIndex: startIndex+4] == 'mul(':
            if doInc:
                c += 4
            return True
    return False

def isDo(startIndex, doInc):
    global input
    global c
    if input[startIndex] == 'd':
        if input[startIndex: startIndex+4] == 'do()':
            if doInc:
                c += 4
            return True
    return False

def isDont(startIndex, doInc):
    global input
    global c
    if input[startIndex] == 'd':
        if input[startIndex: startIndex+7] == "don't()":
            if doInc:
                c += 7
            return True
    return False


sumOfMul = 0
do = True
while c < l:
    if isDo(c, True) and not do:
        do = True
        continue
    elif isDont(c, True) and do:
        do = False
        continue
    elif isMul(c, True):
        m = tryGetMul()
        if do and m >= 0:
            sumOfMul += m
        continue
    c += 1

print(sumOfMul)