import re
import requests
import json
import os

import nltk
from nltk.corpus import stopwords
stopwords = set(stopwords.words('english'))

from export import GetPKName
from load import StringProcess

def NodeForSearchTransform(nodeData, tablePKNameForSearch):
    # 1. Transform
    searchResults = {}

    for tableName, PKList in tablePKNameForSearch.items():
        if len(PKList) == 1:
            searchResults.update({tableName: {PKList[0]: []}})
        else:
            searchResults.update({tableName: {' '.join(PKList): []}})

    for wordResult in nodeData:
        for tablekey, PKList in tablePKNameForSearch.items():
            if (wordResult['TABLE'] == tablekey):
                if len(PKList) == 1:
                    searchResults[tablekey][PKList[0]].append(wordResult[PKList[0]])
                else:
                    eachTableResult = []
                    for PK in PKList:
                        eachTableResult.append(wordResult[PK])
                    searchResults[tablekey][' '.join(PKList)].append(tuple(eachTableResult))

    # 2. Remove empty PK list
    finalResult = {}

    for table in searchResults.keys():
        if list(searchResults[table].values())[0] != []:
            finalResult.update({table: searchResults[table]})

    return finalResult

def GetFrequency(wordList):
    wordFrequency = {}

    for word in sorted(wordList, reverse=False):
        if word not in wordFrequency:
            wordFrequency[word] = 1
        else:
            wordFrequency[word] += 1

    wordFrequency = sorted(wordFrequency.items(), key=lambda x: x[1], reverse=True)

    return wordFrequency

def ShowSingleWordsResult(word,show_frequency):
    FinalResult = {}
    for table in word.keys():
        eachResult = {}
        for PK in word[table]:
            eachPKResult = []
            for eachword in GetFrequency(word[table][PK]):
                if show_frequency:
                    eachPKResult.append(eachword)
                else:
                    eachPKResult.append(eachword[0])
            eachResult.update({PK: eachPKResult})
        FinalResult.update({table: eachResult})

    return FinalResult

def GetCombinedKey(combinedWords):
    keyList = []
    for a in combinedWords:
        keyList.append(list(a.keys()))

    newList = []
    for key in keyList:
        if type(key)!= list:
            newList = newList + [key]
        else:
            newList = newList + list(key)
    return list(set(newList))

def GetCombinedWords(a,b):
    Combine = [a,b]
    keyList = GetCombinedKey(Combine)
    FrequencyDict = {}
    for key in keyList:
        if ((key in a.keys()) and (key in b.keys())):
            FrequencyDict.update({key:a[key]+b[key]})

        elif (key in a.keys()) and (key not in b.keys()):
            FrequencyDict.update({key:a[key]})
        elif (key not in a.keys()) and (key in b.keys()):
            FrequencyDict.update({key:b[key]})
        else:
            continue
    return FrequencyDict

def GetTwoCombinedWordsFrequency(a,b):
    Combine = [a,b]
    keyList = GetCombinedKey(Combine)
    FrequencyDict = {}
    for key in keyList:
        if ((key in a.keys()) and (key in b.keys())):
            FrequencyDict.update({key:GetFrequency(a[key]+b[key])})

        elif (key in a.keys()) and (key not in b.keys()):
            FrequencyDict.update({key:GetFrequency(a[key])})
        elif (key not in a.keys()) and (key in b.keys()):
            FrequencyDict.update({key:GetFrequency(b[key])})
        else:
            continue
    return FrequencyDict

def GetCombinedWordsFrequency(combinedWords):
    FrequencyDict = {}
    combinedWordsDict = {}

    FrequencyDict.update(GetTwoCombinedWordsFrequency(combinedWords[0], combinedWords[1]))
    combinedWordsDict.update(GetCombinedWords(combinedWords[0], combinedWords[1]))

    for i in range(2, len(combinedWords)):
        word = combinedWords[i]
        FrequencyDict.update(GetTwoCombinedWordsFrequency(combinedWordsDict, word))
        combinedWordsDict.update(GetCombinedWords(combinedWordsDict, word))

    return FrequencyDict

def ShowCombinedWordsResult(combinedWords,show_frequency):
    CombinedwordFrequency = GetCombinedWordsFrequency(combinedWords)
    if show_frequency:
        return CombinedwordFrequency
    else:
        FinalResult = {}
        for key in CombinedwordFrequency.keys():
            eachResult = []
            for eachword in CombinedwordFrequency[key]:
                eachResult.append(eachword[0])

            FinalResult.update({key:eachResult})
        return FinalResult

def GetSearchList(connect,databaseName,tableList):
    tablePKName = GetPKName(connect, databaseNameList=databaseName)[databaseName[0]]

    if tableList == '':
        return tablePKName
    else:
        tableList = tableList.split(' ')
        tablePKNameForSearch = {}
        for table in tableList:
            if table in tablePKName.keys():
                tablePKNameForSearch.update({table: tablePKName[table]})
        return tablePKNameForSearch

def GetAllSearchData(url,PKResults,inputword,tablePKNameForSearch,single,FrequencyResult=None,sortList = None):
    if single:
        originalData = requests.get(url + 'AllDataNode/' + inputword + '.json').json()
        for table in PKResults:
            for PK in PKResults[table]:
                PKResultList = PKResults[table][PK]
                if len(PK.split(' ')) == 1:
                    for i, eachPK in enumerate(PKResultList):
                        for eachOriginalData in originalData[table]:
                            if eachOriginalData[PK] == eachPK:
                                PKResults[table][PK][i] = eachOriginalData
                else:
                    PK1 = PK.split(' ')[0]
                    PK2 = PK.split(' ')[1]
                    for i, eachPK in enumerate(PKResultList):
                        for eachOriginalData in originalData[table]:
                            if eachOriginalData[PK1] == eachPK[0] and eachOriginalData[PK2] == eachPK[1]:
                                PKResults[table][PK][i] = eachOriginalData

        for table in sortList:
            if table in PKResults:
                if len(tablePKNameForSearch[table]) == 1:
                    key = tablePKNameForSearch[table][0]
                else:
                    key = ' '.join(tablePKNameForSearch[table])
                eachresult = PKResults[table][key]
                PKResults.update({table:{key:sorted(eachresult, key=lambda x: float(x[sortList[table]]), reverse=True)}})

    else:
        for searchword in StringProcess(inputword):
            originalData = requests.get(url + 'AllDataNode/' + searchword + '.json').json()
            if originalData != None:
                for table in PKResults:
                    for PK in PKResults[table]:
                        PKResultList = PKResults[table][PK]

                        if len(PK.split(' ')) == 1:
                            for i, eachPK in enumerate(PKResultList):
                                if table in originalData:
                                    for eachOriginalData in originalData[table]:
                                        if eachOriginalData[PK] == eachPK:
                                            PKResults[table][PK][i] = eachOriginalData

                        else:
                            PK1 = PK.split(' ')[0]
                            PK2 = PK.split(' ')[1]
                            for i, eachPK in enumerate(PKResultList):
                                if table in originalData:
                                    if type(eachPK) == tuple:
                                        for eachOriginalData in originalData[table]:
                                            if eachOriginalData[PK1] == eachPK[0] and eachOriginalData[PK2] == eachPK[1]:
                                                PKResults[table][PK][i] = eachOriginalData

        if FrequencyResult != None:

            for table in sortList:
                if len(tablePKNameForSearch[table]) == 1:
                    key = tablePKNameForSearch[table][0]
                else:
                    key = ' '.join(tablePKNameForSearch[table])
                frequencyList = FrequencyResult[key]
                mostFrequentList = []
                for frequency in frequencyList:
                    if frequency[1] == frequencyList[0][1]:
                        mostFrequentList.append(frequency[0])

                eachresult = PKResults[table][key]
                needsortList = []
                notSortList = []
                for eachdata in eachresult:
                    if len(tablePKNameForSearch[table]) == 1:
                        if eachdata[key] in mostFrequentList:
                            needsortList.append(eachdata)
                        else:
                            notSortList.append(eachdata)
                    else:
                        if (eachdata[tablePKNameForSearch[table][0]],eachdata[tablePKNameForSearch[table][1]]) in mostFrequentList:
                            needsortList.append(eachdata)
                        else:
                            notSortList.append(eachdata)

                try:
                    finalsortList = sorted(needsortList, key=lambda x: float(x[sortList[table]]), reverse=True) + notSortList
                    PKResults.update({table: {key:finalsortList}})
                except:
                    continue

def Search(inputList,url,tablePKNameForSearch,needPrinted,show_frequency,searchWholeData,stopWords,sortList):
    finalSearchResults = {}
    importantTableDict = {}
    resultPKDict = {}

    for inputword in inputList:
        try:
            count = 0
            nodeDataDict = {}
            searchNodesDict = {}
            importantWordsList = []
            stopWordsList = []
            for stringProcess in StringProcess(inputword):
                nodeData = requests.get(url+'Node/'+stringProcess+'.json').json()
                if nodeData != None:
                    searchNodes = NodeForSearchTransform(nodeData=nodeData,tablePKNameForSearch=tablePKNameForSearch)
                    for key in tablePKNameForSearch:
                        if key in searchNodes:

                            nodeDataDict.update({stringProcess: nodeData})
                            searchNodesDict.update({stringProcess:searchNodes})

                    for key in tablePKNameForSearch:
                        if key in searchNodes:
                            count = count + 1
                            if stringProcess in stopwords:
                                stopWordsList.append(stringProcess)
                            else:
                                importantWordsList.append(stringProcess)
                            break

            if count == 1:
                if needPrinted:
                    print('############# Searching Word: {} ###############'.format(inputword.replace(' ', '')))
                    print('Single word, no matter what, sort')
                    print('Search Result:')
                for stringProcess in StringProcess(inputword):
                    if stringProcess in nodeDataDict.keys():
                        searchNodes = NodeForSearchTransform(nodeData=nodeDataDict[stringProcess], tablePKNameForSearch=tablePKNameForSearch)
                        PKResults = ShowSingleWordsResult(searchNodes, show_frequency=show_frequency)
                        PKResultsFrequency = ShowSingleWordsResult(searchNodes, show_frequency = True)

                        importantTable = []
                        maxFrequencyDict = {}
                        for table in PKResultsFrequency:
                            if len(tablePKNameForSearch[table]) == 1:
                                key = tablePKNameForSearch[table][0]
                            else:
                                key = ' '.join(tablePKNameForSearch[table])
                            maxFrequencyDict.update({table:[max([data[1] for data in PKResultsFrequency[table][key]]),
                                                            len(PKResultsFrequency[table][key])]})

                        maxFrequency = max([data[0] for data in list(maxFrequencyDict.values())])
                        maxData = max([data[1] for data in list(maxFrequencyDict.values())])

                        for table in maxFrequencyDict:
                            if maxFrequencyDict[table][0] > 1 or maxFrequencyDict[table][1] == maxData:
                                importantTable.append(table)

                        importantTableDict.update({' '.join(StringProcess(inputword)): importantTable})


                        if searchWholeData:
                            GetAllSearchData(url=url, PKResults=PKResults, inputword=stringProcess,
                                             tablePKNameForSearch=tablePKNameForSearch,single = True,sortList = sortList)

                        if needPrinted:
                            print(json.dumps({stringProcess:PKResults},indent=4))
                        finalSearchResults.update({' '.join(StringProcess(inputword)):PKResults})

                        for table in PKResults:
                            resultPKDict.update({table: ' '.join(tablePKNameForSearch[table])})

            else:
                if stopWords and stopWordsList != [] and importantWordsList !=[]:

                    if needPrinted:
                        print('############# Searching Phrase: {} #############'.format(inputword))
                        print(stopWordsList, importantWordsList)
                        print('Has stop words')
                        print('Search Result:')

                    if len(importantWordsList) == 1:
                        if needPrinted:
                            print('one important words')
                        searchNodes = searchNodesDict[importantWordsList[0]]
                        importantResult1 = ShowSingleWordsResult(searchNodes, show_frequency=show_frequency)
                        importantResult = {}
                        for key in importantResult1:
                            importantResult.update(importantResult1[key])

                        importantFrequencyResult1 = ShowSingleWordsResult(searchNodes, show_frequency=True)
                        importantFrequencyResult = {}
                        for key in importantFrequencyResult1:
                            importantFrequencyResult.update(importantFrequencyResult1[key])
                        if needPrinted:
                            print('importantFrequencyResult', importantFrequencyResult)

                    else:
                        if needPrinted:
                            print('multiple important words')
                        combinedWords = []

                        for eachinput in importantWordsList:
                            searchNodes = searchNodesDict[eachinput]
                            for table in tablePKNameForSearch:
                                if table in searchNodes:
                                    combinedWords.append(searchNodes[table])

                        importantResult = ShowCombinedWordsResult(combinedWords, show_frequency=show_frequency)
                        importantFrequencyResult = GetCombinedWordsFrequency(combinedWords)
                        if needPrinted:
                            print('importantFrequencyResult',importantFrequencyResult)

                    if len(stopWordsList) == 1:
                        if needPrinted:
                            print('one stops words')
                        searchNodes = searchNodesDict[stopWordsList[0]]
                        stopWordsResult1 = ShowSingleWordsResult(searchNodes, show_frequency=show_frequency)
                        stopWordsResult = {}
                        for key in stopWordsResult1:
                            stopWordsResult.update(stopWordsResult1[key])

                    else:
                        if needPrinted:
                            print('multiple stops words')
                        combinedWords = []
                        for eachinput in stopWordsList:
                            searchNodes = searchNodesDict[eachinput]
                            for table in tablePKNameForSearch:
                                if table in searchNodes:
                                    combinedWords.append(searchNodes[table])
                        stopWordsResult = ShowCombinedWordsResult(combinedWords, show_frequency=show_frequency)


                    Result = importantResult
                    for key in stopWordsResult:
                        if key in importantResult:
                            for word in stopWordsResult[key]:
                                if word not in Result[key]:
                                    Result[key] = Result[key] + [word]
                    for key in stopWordsResult:
                        if key not in importantResult:
                            Result.update({key:stopWordsResult[key]})

                    FrequencyResult = importantFrequencyResult

                else:
                    if needPrinted:
                        print('############# Searching Phrase: {} #############'.format(inputword))
                        print('no stopwords or all stopwords')
                        print('Search Result:')

                    combinedWords = []
                    for eachinput in StringProcess(inputword):
                        if eachinput in nodeDataDict.keys():
                            searchNodes = searchNodesDict[eachinput]
                            for table in tablePKNameForSearch:
                                if table in searchNodes:
                                    combinedWords.append(searchNodes[table])

                    Result = ShowCombinedWordsResult(combinedWords, show_frequency=show_frequency)
                    FrequencyResult = GetCombinedWordsFrequency(combinedWords)

                FinalResult = {}
                for table in tablePKNameForSearch.keys():
                    key1 = tablePKNameForSearch[table]
                    for key2 in Result:
                        if ' '.join(key1) == key2:
                            FinalResult.update({table: {key2: Result[key2]}})

                if searchWholeData:
                    allTFList = []
                    for table in sortList:
                        if table in tablePKNameForSearch:
                            if len(tablePKNameForSearch[table]) != 1:
                                key = ' '.join(tablePKNameForSearch[table])
                                allTFList.append(key not in FrequencyResult)
                            else:
                                allTFList.append(tablePKNameForSearch[table][0] not in FrequencyResult)
                        else:
                            allTFList.append(True)

                    if needPrinted:
                        print(FrequencyResult,allTFList)

                    if all(allTFList) or sortList == {}:
                        if needPrinted:
                            print('not sort')
                        GetAllSearchData(url=url, PKResults=FinalResult,inputword=inputword,
                                                 tablePKNameForSearch=tablePKNameForSearch,single=False)
                    else:
                        if needPrinted:
                            print('Sort')
                        newSortList = {}
                        for i,each in enumerate(allTFList):
                            if each == False:
                                key = list(sortList.keys())[i]
                                newSortList.update({key:sortList[key]})

                        if needPrinted:
                            print(newSortList)

                        GetAllSearchData(url=url, PKResults=FinalResult, inputword=inputword,
                                         tablePKNameForSearch=tablePKNameForSearch, single=False,
                                         FrequencyResult=FrequencyResult,sortList=newSortList)

                    importantTable = []
                    maxFrequencyDict = {}
                    maxDataDict = {}

                    for key in FrequencyResult:
                        maxFrequencyDict.update({key: max([data[1] for data in FrequencyResult[key]])})
                        maxDataDict.update({key: len(FrequencyResult[key])})

                    for key in maxFrequencyDict:
                        if maxFrequencyDict[key] == max(list(maxFrequencyDict.values())) \
                                and maxDataDict[key] == max(list(maxDataDict.values())):
                            importantTable.append(key)
                        elif maxFrequencyDict[key] == max(list(maxFrequencyDict.values())):
                            importantTable.append(key)

                    for i, key in enumerate(importantTable):
                        for table in tablePKNameForSearch:
                            if len(tablePKNameForSearch[table]) == 1 and key == tablePKNameForSearch[table][0]:
                                importantTable[i] = table
                            elif len(tablePKNameForSearch[table]) != 1 and key == ' '.join(tablePKNameForSearch[table]):
                                importantTable[i] = table

                    if importantTable!= []:
                       importantTableDict.update({' '.join(StringProcess(inputword)):importantTable})


                if needPrinted:
                    print('Result of "{}". Most relevant table: {}'.format(list(importantTableDict.keys())[0],
                                                                                     ' and '.join(list(importantTableDict.values())[0])))
                    print(json.dumps({' '.join(StringProcess(inputword)): FinalResult},indent=4))

                finalSearchResults.update({' '.join(StringProcess(inputword)): FinalResult})

                for table in FinalResult:
                    resultPKDict.update({table:' '.join(tablePKNameForSearch[table])})

        except:

            print('Get wrong for searching: "{}". You should input in standard format, or try to search each individual word!'.format(inputword))
            continue

    return finalSearchResults,importantTableDict,resultPKDict

def MainSearch(input,firebaseURL,databaseName,tablePKNameForSearch,Mute,needPrinted,show_frequency,
               searchWholeData,writeResultJson,stopWords,sortList):


    if not Mute:
        print('-----Search Keywords-----')

    url = firebaseURL + databaseName
    #inputList = [re.sub(r'[^\w\s]', '', word.replace('_', '')) for word in input]
    inputList = [re.sub(r'[^\w\s]', '',word) for word in input]
    finalSearchResults,importantTableDict,resultPKDict = Search(inputList=inputList,url = url,
                                                                tablePKNameForSearch = tablePKNameForSearch,
                                                                needPrinted = needPrinted,show_frequency=show_frequency,
                                                                searchWholeData=searchWholeData,stopWords=stopWords,sortList = sortList)

    if (os.path.exists("results.json")):
        os.remove("results.json")

    if finalSearchResults != {}:
        if len(list(finalSearchResults.keys())) == 1:  # Server only search one word/phrase/sentence, so we don't need the word title

            if importantTableDict!={}:
                finalSearchResults = json.dumps({'status':0,'Recommendation':importantTableDict[list(importantTableDict.keys())[0]][0],
                                                'tableKey':resultPKDict,'data':finalSearchResults[list(finalSearchResults.keys())[0]]},indent=4)
            else:
                finalSearchResults = json.dumps(
                    {'status': 0, 'Recommendation': 'No recommended tables','tableKey':resultPKDict,
                     'data': finalSearchResults[list(finalSearchResults.keys())[0]]}, indent=4)
            if writeResultJson:
                jsonFile = open("results.json", 'w')
                jsonFile.write(finalSearchResults)
                jsonFile.close()

        else:
            if importantTableDict!={}:
                finalSearchResults = json.dumps({'status':0,'Recommendation':importantTableDict[list(importantTableDict.keys())[0]][0],
                                             'data':finalSearchResults},indent=4)
            else:
                finalSearchResults = json.dumps(
                    {'status': 0, 'Recommendation': 'No recommended tables',
                     'data': finalSearchResults[list(finalSearchResults.keys())[0]]}, indent=4)

            # Test searching several word/phrase/sentence, we need the word title
            if writeResultJson:
                jsonFile = open("results.json", 'w')
                jsonFile.write(finalSearchResults)
                jsonFile.close()

        return finalSearchResults

    else:
        return None


# README.
# #North, ,/., CHina, "America\ America america America", "English", "North America"./., a, " South America China"
# "North America", "Aachen AmeRIca Ago", "A CHina", "English", "Aachen AmeRIca Ago China"



