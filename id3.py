import fileinput
import math
import re
import copy

attributes = []
data = []
resultIndex = 0
possibleResults = []
def parser():
    input = fileinput.input()
    state = 0
    index = 0
    for line in input:
        if state == 1 and "%" not in line:
            data.append(line.strip("\n").split(","))
        if "@attribute" in line:
            raw_line = re.sub('\s+', '', line)
            raw_list = raw_line.replace("@attribute", "").strip("}").split("{")
            attr = raw_list[0]
            possibleValues = raw_list[1].split(",")
            attributes.append([attr, possibleValues, index])
            index +=1
        if "@data" in line:
            state = 1
    global resultIndex
    global possibleResults
    resultIndex = index - 1
    possibleResults = attributes[resultIndex][1]
    #print attributes, resultIndex
    #print data
    #print possibleResults


def attrIndex(attr):
    index = 0
    for a in attributes:
        if a[0] == attr:
            index = a[2]
    return index


def getSet(s, attr, value):
    index = attrIndex(attr)
    newS = []
    for row in s:
        if row[index] == value:
            newS.append(row)
    #print "getSet", len(newS)
    #print newS
    return newS

def entropy2(attr, value, data, initial):
    global resultIndex
    countRes = []
    total = 0
    entropy = 0
    for i in range(0, len(possibleResults)):
        countRes.append([possibleResults[i], 0])
    if initial:
        for row in data:
            #print row
            total += 1
            indexRes = possibleResults.index(row[resultIndex])
            countRes[indexRes][1] += 1 
        for i in range(0, len(countRes)):
            division = 0
            if total > 0:
                division = countRes[i][1] / float(total)
            #print countRes[i][1], division, total
            if  division > 0:
                entropy -= (division) * math.log(division, 2)

    else:
        #print "here"
        aIndex = attrIndex(attr)

        for row in data:
            if row[aIndex] == value:
         #       print row
                total += 1
                indexRes = possibleResults.index(row[resultIndex])
                countRes[indexRes][1] += 1   
        for i in range(0, len(countRes)):
            division = 0
            if total > 0:
                division = countRes[i][1] / float(total)
            #print countRes[i][1], division, total
            if  division > 0:
                entropy -= (division) * math.log(division, 2)

    #print entropy, total
    return entropy, total



def attrValues(attr):
    global attributes
    for a in attributes:
        if attr == a[0]:
            return a[1]


def gain(s, attr, entropyS):

    acum = 0
    denominator = len(s)
    for val in attrValues(attr):
        entr, numerator = entropy2(attr, val, s, False)
        acum += float(numerator) / denominator * entr
    result = entropyS - acum
    #print "gain",attr, result, s
    return result 

def best(s, remainAttrs):
    highest = float(-1)
    best = []
    entropyS, tot = entropy2('', '', s, True)
    if entropyS == 0:
        #print "ANSWER: " + s[0][resultIndex]
        return "ANSWER: " + s[0][resultIndex], 0
    #print "entropyS",entropyS

    for a in remainAttrs:
        gainResult = gain(s, a, entropyS)
        if gainResult > highest:
            highest = gainResult
            best = a
    #print best
    return best, 1

def id3(level, remainAttrs, data):
    if (remainAttrs):
        res, flag = best (data, remainAttrs)
        if (flag == 0):
                print "  " * level + res
        else:
            for a in attrValues(res):
                print "  " * level + res + ": " + a
                remain = copy.copy(remainAttrs)
                if len(remain) > 1:
                    remain.remove(res)    
                s = getSet(data, res, a)
                id3(level + 1, remain, s)




parser()
#s = getSet(data, 'age', 'young')
#entropy2('tear-prod-rate', 'normal', s, True)

#print resultIndex, attributes[resultIndex]
#resultColum = getAttrColumn(attributes[resultIndex][0])
#getAttrColumn(attributes[1][0])
#print possibleResults
#entropy('A','TRUE')
#gain('A','FALSE','B')
#best('tear-prod-rate','normal',['age','spectacle-prescrip','astigmatism'])
#print "jadadasd"
#print attributes
#best(data,['age','spectacle-prescrip','astigmatism', 'tear-prod-rate'])
#s = getSet(data, 'tear-prod-rate', 'normal')
#best(s,['age','spectacle-prescrip','astigmatism'])
#s2 = getSet(s, 'astigmatism', 'no')
#best(s2,['age','spectacle-prescrip'])
#s3 = getSet(s2, 'age', 'young')
#best(s3,['spectacle-prescrip'])
#s = getSet(data, 'tear-prod-rate', 'reduced')
#best(s,['age','spectacle-prescrip','astigmatism'])
#id3(0,['age','spectacle-prescrip','astigmatism', 'tear-prod-rate'], data)
#id3(0,['A','B'], data)
remainAttrs = []
for a in attributes:
    remainAttrs.append(a[0])
remainAttrs.pop()
id3(0,remainAttrs, data)



#entropy('astigmatism','no')