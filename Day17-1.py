import math
import datetime
import time
registers = {
    'A': 47719761,
    'B': 0,
    'C': 0
}

pointer = 0

def getRegisterValue(register):
     global registers
     return registers[register]

def setRegisterValue(register, value):
     global registers
     registers[register] = value

def getComboValue(operand):
    global registers
    if operand in range(0, 4):
        return operand
    if operand == 4:
        return getRegisterValue('A')
    if operand == 5:
        return getRegisterValue('B')
    if operand == 6:
        return getRegisterValue('C')
    if operand == 7:
        raise Exception("7 in combo op")
    
def div(toR, operand):
    num = getRegisterValue('A')
    den = math.pow(2, getComboValue(operand))
    value = int(num // den)
    setRegisterValue(toR, value)
    return True

def adv(operand):
    return div('A', operand)

def bxl(operand):
    vb = getRegisterValue('B')
    value = operand ^ vb
    setRegisterValue('B', value)
    return True

def bst(operand):
    cb = getComboValue(operand)
    value = cb % 8
    setRegisterValue('B', value)
    return True

def jnz(operand):
    global pointer
    if getRegisterValue('A') != 0:
        pointer = operand
        return False
    return True

def bxc(operand):
    vb = getRegisterValue('B')
    vc = getRegisterValue('C')
    value = vc ^ vb
    setRegisterValue('B', value)
    return True

def out(operand):
    global output
    cb = getComboValue(operand)
    value = cb % 8
    output.append(str(value))
    return True

def bdv(operand):
    return div('B', operand)

def cdv(operand):
    return div('C', operand)

opCodeFunctions = {
    0 : adv,
    1 : bxl,
    2 : bst,
    3 : jnz,
    4 : bxc,
    5 : out,
    6 : bdv,
    7 : cdv
}
                                       # 0 ,  1,   2,   3,   4,   5,   6,   7
program = [2,4, # A % 8 ->   B         [000, 001, 010, 011, 100, 101, 110, 111] 
           1,5, # B XOR 5 (101) -> B   [101, 100, 111, 110, 001, 000, 011, 010]
           7,5, # A / 8 -> C             5 ,  4,   7,   6,   1,   0,   3,   2
           0,3, # A / 8 -> A
           4,1, #B XOR C -> B   7
           1,6, #6(110) XOR B -> B 
           5,5, #output register mod 8  B 
           3,0] #possible end jump nothign A == 0 or back to beginning
#program = [0,1,5,4,3,0]
output = []

expectedOutput = []
for p in program:
    expectedOutput.append(str(p))

def execute(opCode, operand):
    return opCodeFunctions[opCode](operand)

def executeProgram(registerA, maxoutput):
    global registers, output, program, pointer
    registers['A'] = registerA
    registers['B'] = 0
    registers['C'] = 0
    pointer = 0
    output = []
    while pointer < len(program) - 1:
        opCode = program[pointer]
        operand = program[pointer + 1]
        incPointer = execute(opCode, operand)
        if incPointer:
            pointer += 2
        if len(output) > maxoutput:
            #print('too long run', output)
            break


expectedFinalOutput = []
for p in  program:
    expectedFinalOutput.append(str(p))

def findGoodOutput(currentNumber, level):
    global output, program, expectedFinalOutput
    if len(program) < level:
        return

    for i in range(8):
        a = i + currentNumber*8
        expectedOutput = []
        for o in  program[-level::]:
            expectedOutput.append(str(o))
        #print('Running', i,a, expectedOutput)
        executeProgram(a, 16)
        if expectedFinalOutput == output:
            print("Found a", a, output)
            return

        if expectedOutput == output:
            #print('good', output, currentNumber, i, a, level)
            findGoodOutput(a, level + 1)
            #print('try', a, level + 1)
    
findGoodOutput(0, 1)
#136902953406217
#executeProgram(136902953406217, 16)
#print("Program", program)
#print("Output", ",".join(output))