import json


# 测试数据集
def loadDataSet():
    return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]


# 将元素映射成单独的集合
def createCells(dataSet, columnList):
    cell = []
    for data, row in dataSet.iterrows():
        # print(transaction)
        for column in columnList:
            if not [row[column]] in cell:
                cell.append([row[column]])

    cell.sort()
    # print(cell)
    return list(map(frozenset, cell))  # use frozen set so we
    # can use it as a key in a dict


# 求大于最小支持度的项集
def scanD(dataSet, cells, minSupport):
    ssCnt = {}
    for data, row in dataSet.iterrows():
        for can in cells:
            if can.issubset(row):
                if can not in ssCnt:
                    ssCnt[can] = 1
                else:
                    ssCnt[can] += 1
    numItems = float(len(dataSet))
    retList = []
    supportData = {}
    for key in ssCnt:
        support = ssCnt[key] / numItems
        if support >= minSupport:
            retList.insert(0, key)
        supportData[key] = support
    return retList, supportData


# 得到频繁项集的组合
def aprioriGen(Lk, k):  # creates Ck
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i + 1, lenLk):
            L1 = list(Lk[i])[:k - 2];
            L2 = list(Lk[j])[:k - 2]
            L1.sort();
            L2.sort()
            if L1 == L2:  # if first k-2 elements are equal
                retList.append(Lk[i] | Lk[j])  # set union
    return retList


# 获得满足最小支持度的候选项集
def apriori(dataSet, columnList, minSupport=0.1):
    cells = createCells(dataSet, columnList)
    L1, supportData = scanD(dataSet, cells, minSupport)
    L = [L1]
    k = 2
    while len(L[k - 2]) > 0:
        Ck = aprioriGen(L[k - 2], k)
        Lk, supK = scanD(dataSet, Ck, minSupport)  # scan DB to get Lk
        supportData.update(supK)
        L.append(Lk)
        k += 1
    return L, supportData


# 获得大于最小可信度的关联规则
def generateRules(L, supportData, minConf=0.1):  # supportData is a dict coming from scanD
    bigRuleList = []
    jsonList = []
    for i in range(1, len(L)):  # only get the sets with two or more items
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            if i > 1:
                rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
            else:
                calcConf(freqSet, H1, supportData, bigRuleList, minConf, jsonList)
    return bigRuleList, jsonList


# 对规则进行评估
def calcConf(freqSet, H, supportData, brl, minConf=0.7, jsonList=None):
    prunedH = []  # create new list to return
    for conseq in H:
        conf = supportData[freqSet] / supportData[freqSet - conseq]  # calc confidence
        if conf >= minConf:
            # print freqSet-conseq,'-->',conseq,'conf:',conf
            print(''.join(freqSet - conseq) + ' --> ' + ''.join(conseq) + ' conf: ' + str(conf))
            jsonList.append({'from': ''.join(freqSet - conseq), 'to': ''.join(conseq), 'conf': str(conf)})
            brl.append((freqSet - conseq, conseq, conf))
            prunedH.append(conseq)
    return prunedH


# 生成候选规则集合以及对规则进行评估
def rulesFromConseq(freqSet, H, supportData, brl, minConf=0.7):
    m = len(H[0])
    if len(freqSet) > (m + 1):  # try further merging
        Hmp1 = aprioriGen(H, m + 1)  # create Hm+1 new candidates
        Hmp1 = calcConf(freqSet, Hmp1, supportData, brl, minConf)
        if len(Hmp1) > 1:  # need at least two sets to merge
            rulesFromConseq(freqSet, Hmp1, supportData, brl, minConf)
