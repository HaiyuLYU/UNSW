import math
import re
from collections import defaultdict
import copy

# Question 1
def calculateTranProbability(State_File,q):
    stateDataset = open(State_File).readlines()
    numOfStates = 0
    states = []
    transList = []
    for i in range(stateDataset.__len__()):
        if i == 0:
            numOfStates = int(stateDataset[i])
        elif 0 < i and i <= numOfStates:
            states.append(stateDataset[i].split()[0])
        else:
            oneTransList = []
            stateLine = stateDataset[i].split()
            for word in stateLine:
                oneTransList.append(int(word))
            transList.append(oneTransList)
    countTransTimes = {}
    for i in range(len(transList)):
        if states[transList[i][0]] not in countTransTimes:
            countTransTimes[states[transList[i][0]]] = transList[i][2]
        else:
            countTransTimes[states[transList[i][0]]] += transList[i][2]
    transProbability = defaultdict(dict)
    if q == 3 and 'UnitNumber' in countTransTimes:
        countTransTimes['UnitNumber'] += 1000
    for i in range(len(transList)):
        transProbability[states[transList[i][0]]][states[transList[i][1]]] \
        = (transList[i][2]+1)/(countTransTimes[states[transList[i][0]]]+numOfStates-1)
    return numOfStates, states, transList, countTransTimes, transProbability

def calculateEmissProbability(Symbol_File,states):
    symbolDataset = open(Symbol_File).readlines()
    numOfSymbol = 0
    symbol = []
    emissList = []
    for i in range(symbolDataset.__len__()):
        if i == 0:
            numOfSymbol = int(symbolDataset[i])
        elif 0 < i and i <= numOfSymbol:
            symbol.append(symbolDataset[i].split()[0])
        else:
            oneEmissList = []
            symbolLine = symbolDataset[i].split()
            for word in symbolLine:
                oneEmissList.append(int(word))
            emissList.append(oneEmissList)
    countEmissTimes={}
    for i in range(len(emissList)):
        if states[emissList[i][0]] not in countEmissTimes:
            countEmissTimes[states[emissList[i][0]]] = emissList[i][2]
        else:
            countEmissTimes[states[emissList[i][0]]] += emissList[i][2]
    emissProbability = defaultdict(dict)
    for i in range(len(emissList)):
        emissProbability[states[emissList[i][0]]][symbol[emissList[i][1]]] \
            = (emissList[i][2]+1)/(countEmissTimes[states[emissList[i][0]]]+numOfSymbol+1)
    return numOfSymbol, symbol, emissList, countEmissTimes, emissProbability

def viterbi_algorithm(State_File, Symbol_File, Query_File):
    numOfStates, states, transList, countTransTimes, transProbability = calculateTranProbability(State_File,1)
    numOfSymbol, symbol, emissList, countEmissTimes, emissProbability = calculateEmissProbability(Symbol_File,states)
    queryDataset = open(Query_File).readlines()
    probList = []
    pathList = []
    results = []
    for q in range(queryDataset.__len__()):
        xx= re.split(r'([-/&,()\s])',queryDataset[q])
        queryLine = []
        for e in xx:
            if e!=' ' and e !='\n' and len(e)!=0:
                queryLine.append(e)
        for s in range(len(queryLine)):
            sProbList=[]
            sPathList=[]
            if s == 0:
                for i in range(numOfStates-2):
                    sPathList.append([numOfStates-2])
                pathList.append(sPathList)
                sPathList = []
                for stateIndex in range(numOfStates-2):
                    if states[stateIndex] in transProbability['BEGIN']:
                        if queryLine[s] in emissProbability[states[stateIndex]]:
                            sProbList.append(transProbability['BEGIN'][states[stateIndex]] * emissProbability[states[stateIndex]][queryLine[s]])
                        else:
                            sProbList.append(transProbability['BEGIN'][states[stateIndex]] * (1/(countEmissTimes[states[stateIndex]]+numOfSymbol+1)))
                    else:
                        if queryLine[s] in emissProbability[states[stateIndex]]:
                            sProbList.append((1/(countTransTimes['BEGIN']+numOfStates-1)) * emissProbability[states[stateIndex]][queryLine[s]])
                        else:
                            sProbList.append((1/(countTransTimes['BEGIN']+numOfStates-1)) * (1/(countEmissTimes[states[stateIndex]]+numOfSymbol+1)))
                    sPathList.append(pathList[s][stateIndex]+[stateIndex])
                probList.append(sProbList)
                pathList.append(sPathList)
            else:     
                for stateIndex in range(numOfStates-2):
                    maxS = -1
                    maxPath = []
                    for j in range(numOfStates-2):
                        if states[stateIndex] in transProbability[states[j]]:
                            if queryLine[s] in emissProbability[states[stateIndex]]:
                                theO = probList[s-1][j] * transProbability[states[j]][states[stateIndex]] * emissProbability[states[stateIndex]][queryLine[s]]
                            else:
                                theO = probList[s-1][j] * transProbability[states[j]][states[stateIndex]] * (1/(countEmissTimes[states[stateIndex]]+numOfSymbol+1))
                        else:
                            if queryLine[s] in emissProbability[states[stateIndex]]:
                                theO = probList[s-1][j] * (1/(countTransTimes[states[j]]+numOfStates-1)) * emissProbability[states[stateIndex]][queryLine[s]]
                            else:
                                theO = probList[s-1][j] * (1/(countTransTimes[states[j]]+numOfStates-1)) * (1/(countEmissTimes[states[stateIndex]]+numOfSymbol+1))
                        if theO > maxS:
                            maxS = theO
                            maxPath = pathList[s][j]+[stateIndex]
                    sProbList.append(maxS)
                    sPathList.append(maxPath)
                probList.append(sProbList)
                pathList.append(sPathList)
        maxP = -1
        flag = -1
        for i in range(len(probList[-1])):
            if 'END' not in transProbability[states[i]]:
                probability = probList[-1][i] * (1/(countTransTimes[states[i]]+numOfStates-1))
            else:
                probability = probList[-1][i] * transProbability[states[i]]['END']
            if probability>maxP:
                maxP = probability
                flag = i
        result = pathList[-1][flag]+[numOfStates-1]+[math.log(maxP)]
        results.append(result)
        probList = []
        pathList=[]
    return results


# Question 2
def top_k_viterbi(State_File, Symbol_File, Query_File, k):
    numOfStates, states, transList, countTransTimes, transProbability = calculateTranProbability(State_File,2)
    numOfSymbol, symbol, emissList, countEmissTimes, emissProbability = calculateEmissProbability(Symbol_File,states)
    queryDataset = open(Query_File).readlines()
    probList = []
    results = []
    for q in range(queryDataset.__len__()):
        xx= re.split(r'([-/&,()\s])',queryDataset[q])
        queryLine = []
        for e in xx:
            if e!=' ' and e !='\n' and len(e)!=0:
                queryLine.append(e)
        probLevel = defaultdict(list)
        for s in range(len(queryLine)):
            probList=[]
            sProbList=[]
            if s == 0:
                for stateIndex in range(numOfStates-2):
                    sProbList=[]
                    if states[stateIndex] in transProbability['BEGIN']:
                        if queryLine[s] in emissProbability[states[stateIndex]]:
                            sProbList.append(transProbability['BEGIN'][states[stateIndex]] * emissProbability[states[stateIndex]][queryLine[s]])
                        else:
                            sProbList.append(transProbability['BEGIN'][states[stateIndex]] * (1/(countEmissTimes[states[stateIndex]]+numOfSymbol+1)))
                    else:
                        if queryLine[s] in emissProbability[states[stateIndex]]:
                            sProbList.append((1/(countTransTimes['BEGIN']+numOfStates-1)) * emissProbability[states[stateIndex]][queryLine[s]])
                        else:
                            sProbList.append((1/(countTransTimes['BEGIN']+numOfStates-1)) * (1/(countEmissTimes[states[stateIndex]]+numOfSymbol+1)))
                    sProbList.append([stateIndex])
                    probList.append(sProbList)
            else:
                probList=[]
                sProbList=[]
                for stateIndex in range(numOfStates-2):
                    tempList = []
                    for i in range(len(probLevel[s-1])):
                        sProbList = []
                        prevv = probLevel[s-1][i][1][-1]
                        nextt = stateIndex
#                         print(f'key:',key,'pre:',prevv,'nextt:',nextt)
                        if states[nextt] in transProbability[states[prevv]]:
                            if queryLine[s] in emissProbability[states[nextt]]:
                                sProbList.append(probLevel[s-1][i][0] * transProbability[states[prevv]][states[nextt]] * emissProbability[states[nextt]][queryLine[s]])
                            else:
                                sProbList.append(probLevel[s-1][i][0] * transProbability[states[prevv]][states[nextt]] * (1/(countEmissTimes[states[nextt]]+numOfSymbol+1)))
                        else:
                            if queryLine[s] in emissProbability[states[nextt]]:
                                sProbList.append(probLevel[s-1][i][0] * (1/(countTransTimes[states[prevv]]+numOfStates-1)) * emissProbability[states[nextt]][queryLine[s]])
                            else:
                                sProbList.append(probLevel[s-1][i][0] * (1/(countTransTimes[states[prevv]]+numOfStates-1)) * (1/(countEmissTimes[states[nextt]]+numOfSymbol+1)))
                        before= copy.deepcopy(probLevel[s-1][i][1])
                        sProbList.append(before)
                        sProbList[1].append(stateIndex)
#                         print(sProbList)
                        tempList.append(sProbList)
                    tempList.sort(key=lambda x:x[0],reverse=True)
                    probList += tempList[:k]
            probLevel[s] = probList
        for i in range(len(probLevel[len(queryLine)-1])):
            prevv = probLevel[len(queryLine)-1][i][1][-1]
            if 'END' in transProbability[states[prevv]]:
                probLevel[len(queryLine)-1][i][0] = probLevel[len(queryLine)-1][i][0] * transProbability[states[prevv]]['END']
            else:
                probLevel[len(queryLine)-1][i][0] = probLevel[len(queryLine)-1][i][0] * (1/(countTransTimes[states[prevv]]+numOfStates-1))
        probLevel[len(queryLine)-1].sort(key=lambda x:x[0],reverse=True)
        res = probLevel[len(queryLine)-1][:k]
        for e in res:
            result = []
            result = result + [numOfStates-2]
            result = result + e[1]
            result = result + [numOfStates-1]
            result = result + [math.log(e[0])]
            results.append(result)
    return results
# Question 3 + Bonus
def advanced_decoding(State_File, Symbol_File, Query_File): # do not change the heading of the function
    numOfStates, states, transList, countTransTimes, transProbability = calculateTranProbability(State_File,3)
    numOfSymbol, symbol, emissList, countEmissTimes, emissProbability = calculateEmissProbability(Symbol_File,states)
    queryDataset = open(Query_File).readlines()
    probList = []
    pathList = []
    results = []
    for q in range(queryDataset.__len__()):
        xx= re.split(r'([-/&,()\s])',queryDataset[q])
        queryLine = []
        for e in xx:
            if e!=' ' and e !='\n' and len(e)!=0:
                queryLine.append(e)
        for s in range(len(queryLine)):
            sProbList=[]
            sPathList=[]
            if s == 0:
                for i in range(numOfStates-2):
                    sPathList.append([numOfStates-2])
                pathList.append(sPathList)
                sPathList = []
                for stateIndex in range(numOfStates-2):
                    if states[stateIndex] in transProbability['BEGIN']:
                        if queryLine[s] in emissProbability[states[stateIndex]]:
                            sProbList.append(transProbability['BEGIN'][states[stateIndex]] * emissProbability[states[stateIndex]][queryLine[s]])
                        else:
                            sProbList.append(transProbability['BEGIN'][states[stateIndex]] * (1/(countEmissTimes[states[stateIndex]]+numOfSymbol+1)))
                    else:
                        if queryLine[s] in emissProbability[states[stateIndex]]:
                            sProbList.append((1/(countTransTimes['BEGIN']+numOfStates-1)) * emissProbability[states[stateIndex]][queryLine[s]])
                        else:
                            sProbList.append((1/(countTransTimes['BEGIN']+numOfStates-1)) * (1/(countEmissTimes[states[stateIndex]]+numOfSymbol+1)))
                    sPathList.append(pathList[s][stateIndex]+[stateIndex])
                probList.append(sProbList)
                pathList.append(sPathList)
            else:     
                for stateIndex in range(numOfStates-2):
                    maxS = -1
                    maxPath = []
                    for j in range(numOfStates-2):
                        if states[stateIndex] in transProbability[states[j]]:
                            if queryLine[s] in emissProbability[states[stateIndex]]:
                                theO = probList[s-1][j] * transProbability[states[j]][states[stateIndex]] * emissProbability[states[stateIndex]][queryLine[s]]
                            else:
                                theO = probList[s-1][j] * transProbability[states[j]][states[stateIndex]] * (1/(countEmissTimes[states[stateIndex]]+numOfSymbol+1))
                        else:
                            if queryLine[s] in emissProbability[states[stateIndex]]:
                                theO = probList[s-1][j] * (1/(countTransTimes[states[j]]+numOfStates-1)) * emissProbability[states[stateIndex]][queryLine[s]]
                            else:
                                theO = probList[s-1][j] * (1/(countTransTimes[states[j]]+numOfStates-1)) * (1/(countEmissTimes[states[stateIndex]]+numOfSymbol+1))
                        if theO > maxS:
                            maxS = theO
                            maxPath = pathList[s][j]+[stateIndex]
                    sProbList.append(maxS)
                    sPathList.append(maxPath)
                probList.append(sProbList)
                pathList.append(sPathList)
        maxP = -1
        flag = -1
        for i in range(len(probList[-1])):
            if 'END' not in transProbability[states[i]]:
                probability = probList[-1][i] * (1/(countTransTimes[states[i]]+numOfStates-1))
            else:
                probability = probList[-1][i] * transProbability[states[i]]['END']
            if probability>maxP:
                maxP = probability
                flag = i
        result = pathList[-1][flag]+[numOfStates-1]+[math.log(maxP)]
        results.append(result)
        probList = []
        pathList=[]
    return results
