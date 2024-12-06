import math

f = open("Day5.input.txt", "r")
rules = {}
input = f.read().splitlines()
max_depth = 4
prints = []

parse_rules = True
for line in input:
    if line == "":
        parse_rules = False
        continue
    if parse_rules:
        rule = line.split("|")
        before = int(rule[0])
        after = int(rule[1])
        if before in rules:
            rules[before].append(after)
        else:
            rules[before] = [after]
    else:
        printPages = []
        prints.append(printPages)
        for pageNumber in line.split(","):
            printPages.append(int(pageNumber))


middlePageSum = 0
for printPages in prints:
    hasBadRule = False
    tryAgain = True
    pageCount = len(printPages)
    for tryCounter in range(0, math.factorial(pageCount)):
        tryAgain = False
        goodPages = 0
        for i in range(0, pageCount):
            validatedPageNumber = printPages[i]
            goodBefore = 0
            for j in range(0, i):
                currentPageNumber = printPages[j]
                if validatedPageNumber in rules and currentPageNumber in rules[validatedPageNumber]:
                    hasBadRule = True
                    printPages[j] = validatedPageNumber
                    printPages[i] = currentPageNumber
                    tryAgain = True
                    break
                goodBefore += 1
            if goodBefore == i:
                goodPages += 1
        if goodPages == pageCount:
            break
        
           
    if hasBadRule and goodPages == pageCount:
        middlePageIndex = math.floor(pageCount/2)
        print(printPages, printPages[middlePageIndex])
        middlePageSum += printPages[middlePageIndex]

print(middlePageSum)

