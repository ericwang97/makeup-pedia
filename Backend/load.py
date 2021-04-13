import json
import requests
import csv
import re
import os

from export import GetPKName,GetTextualAttributes,ExportTableToCSV

def WriteCSVFile(fileName,data):
    if os.path.exists(fileName + ".csv"):
        os.remove(fileName + ".csv")
    csvFile = open(fileName + ".csv", 'a+', encoding='latin1')
    writer = csv.writer(csvFile)
    for i in data:
        writer.writerow(i)
    csvFile.close()

def DetectComma(stringList):
    newstring = []
    for i,word in enumerate(stringList):
        if re.search(r"'\w",re.sub(r'[^\w\s\']','',word)) and re.search(r"\w'",re.sub(r'[^\w\s\']','',word)):
            newstring.append(word)
        elif re.search(r"'\w",re.sub(r'[^\w\s\']','',word)) and not re.search(r"\w'",re.sub(r'[^\w\s\']','',word)):
            newstring.append(stringList[i]+stringList[i+1])
        elif not re.search(r"'\w",re.sub(r'[^\w\s\']','',word)) and re.search(r"\w'",re.sub(r'[^\w\s\']','',word)):
            continue
        else:
            newstring.append(word)

    return newstring

def CleanCSVFile(tablePKName,Mute):

    # Meaning that we need to clean all files in the database

    for fileName in tablePKName.keys():
        try:
            if not Mute:
                print('Cleaned {} ...'.format(fileName))

            # Doing (1)
            if fileName == 'country':
                # print('First Change country data into 15 columns')
                csvFile = open("country.csv", 'r', encoding='latin1')
                reader = csv.reader(csvFile)
                data = []

                readline = list(reader)[0]
                data.append(readline)

                csvFile = open("country.csv", 'r', encoding='latin1')
                reader = csv.reader(csvFile)

                for readline in list(reader)[1:]:
                    newreadline = DetectComma(readline)
                    data.append(newreadline)
                WriteCSVFile("country_cleaned", data)
                csvFile = open(fileName + "_cleaned.csv", 'r', encoding='latin1')
            else:
                csvFile = open(fileName + ".csv", 'r', encoding='latin1')

            readerMeta = csv.reader(csvFile)
            metadata = []

            # Doing (2), title and key -- meta
            readline = list(readerMeta)[0]
            for i, line in enumerate(readline):
                if re.search(r' # ', line):
                    readline[i] = re.sub(r' # ', "", line)
                elif re.search(r'# ', line):
                    readline[i] = re.sub(r'# ', "", line)
                else:
                    readline[i] = line[1:]
            metadata.append(readline)
            csvFile.close()

            # Dealing with Data, finishing (3) and (4)
            data = []
            if fileName == 'country':
                csvFile = open(fileName + "_cleaned.csv", 'r', encoding='latin1')
            else:
                csvFile = open(fileName + ".csv", 'r', encoding='latin1')
            reader = csv.reader(csvFile)

            for readline in list(reader)[1:]:
                if readline == []:
                    continue
                else:
                    # Doing (3) values
                    for i, line in enumerate(readline):
                        #Doing (4)
                        if line in [' NULL'," ''"]:
                            readline[i] = None
                        else:
                            readline[i] = eval(line)
                    data.append(readline)
            csvFile.close()
            WriteCSVFile(fileName+"_cleaned", metadata+data)
            if not Mute:
                print('Completed!')

            os.remove(fileName + ".csv")
        except:
            print("Something wrong when cleaning table: {}".format(fileName))
            continue

def WriteAllJson(tablePKName,outputName,Mute):

    jsonFile = open(outputName+".json",'w')
    jsonFile.write('{\n ' + '"' + outputName + '" : {\n')

    if not Mute:
        print("Transforming {} tables of {} into {}.json ...".format(len(list(tablePKName.keys())),outputName,outputName))

    for fileName in tablePKName.keys():
        try:
            csvFile = open(fileName+"_cleaned.csv",'r',encoding='latin1')
            reader = csv.DictReader(csvFile)

            data = []
            for readline in reader:
                data.append(readline)

            csvFile.close()
            os.remove(fileName+"_cleaned.csv")

        except:
            print("Something wrong when writing table into Json: {}".format(fileName))
            os.remove(fileName + ".csv")
            continue

        jsonFile.write('"' + fileName + '" : [\n')
        for row in data[0:-1]:
            json.dump(row, jsonFile, indent=4)
            jsonFile.write(',\n')
        json.dump(data[-1], jsonFile, indent=4)

        if fileName != list(tablePKName.keys())[-1]:
            jsonFile.write('\n\t],\n')
        else:
            jsonFile.write('\n\t]\n')

    jsonFile.write('\n}\n}')

def LoadJson(fileName,url,Mute,method = 'PATCH'):
    url = url + '.json'
    if Mute:
        data = json.load(open(fileName + ".json", 'r', encoding='utf-8'))
        requests.request(method, url, json=data)
        os.remove(fileName + ".json")


    else:
        if requests.get(url).status_code == 200:
            print('Firebase Successfully Connected')
            print('Uploading '+fileName+".json to Firebase...")
            data = json.load(open(fileName+".json",'r',encoding='utf-8'))
            requests.request(method, url, json=data)
            print('Completed!')
            os.remove(fileName + ".json")
        else:
            print('Connection Failed')

def StringProcess(string):
    return re.sub(r'[^\w\s]', '', string).lower().split()

def GetAllWords(data,textualAttributes):

    allWords = []
    for table in data.keys():
        if table in textualAttributes:
            for text in data[table]:
                for key in textualAttributes[table]:
                    allWords = allWords + (StringProcess(text[key]))

    return allWords

def GetWordSet(data,textualAttributes):
    allWords = GetAllWords(data,textualAttributes)
    return sorted(set(allWords),reverse = False)

def GetWordOccurrence(data,textualAttributes,tablePKName):
    wordOccurrence = []

    for table in data.keys():
        if table in textualAttributes:
            for text in data[table]:
                for key in textualAttributes[table]:
                    if StringProcess(text[key]) != []:
                        for stringProcess in StringProcess(text[key]):
                            occur = {}
                            for PK in tablePKName[table]:
                                occur.update({'TABLE': table,'COLUMN': key, PK: text[PK]})
                            wordOccurrence = wordOccurrence + [{stringProcess: occur}]

    return wordOccurrence

def GetWordIndex(data,textualAttributes,tablePKName,Mute):
    wordSet = GetWordSet(data,textualAttributes)
    wordOccurrence = GetWordOccurrence(data,textualAttributes,tablePKName)
    wordIndexDict = {}
    if Mute:
        for keyword in wordSet:
            occurPerKeyword = []
            for occur in wordOccurrence:
                if keyword in occur.keys():
                    occurPerKeyword = occurPerKeyword + list(occur.values())
            wordIndex = {keyword: occurPerKeyword}
            wordIndexDict.update(wordIndex)
    else:
        for keyword in wordSet:
            occurPerKeyword = []
            for occur in wordOccurrence:
                if keyword in occur.keys():
                    occurPerKeyword = occurPerKeyword + list(occur.values())
            wordIndex = {keyword: occurPerKeyword}
            wordIndexDict.update(wordIndex)
    return wordIndexDict

def GetAllDataNode(firebaseURL,databaseName,tablePKName):
    result = {}

    originalData = requests.get(firebaseURL + databaseName + '.json').json()
    nodeData = requests.get(firebaseURL + databaseName + 'Node.json').json()

    for node in nodeData:
        result.update({node: {}})
        for eachdata in nodeData[node]:
            table = eachdata['TABLE']
            PKList = tablePKName[table]
            if table not in result[node].keys():
                result[node].update({table:[]})
            if len(PKList) == 1:
                PK = tablePKName[table][0]
                PKName = eachdata[PK]
                for data in originalData[table]:
                    if PKName == data[PK]:
                        result[node][table].append(data)
            else:
                PK1 = PKList[0]
                PK2 = PKList[1]
                PKName1 = eachdata[PK1]
                PKName2 = eachdata[PK2]
                for data in originalData[table]:
                    if PKName1 == data[PK1] and PKName2 == data[PK2]:
                        result[node][table].append(data)

    return result

def WriteNodeJson(wordNode,outputName,Mute):
    if Mute:
        if (os.path.exists(outputName+".json")):
            os.remove(outputName+".json")
    else:
        if (os.path.exists(outputName+".json")):
            print('Update the {}.json file.'.format(outputName))
            os.remove(outputName+".json")
        else:
            print('Create the {}.json file.'.format(outputName))

    jsonFile = open(outputName+".json", 'w')
    jsonFile.write(json.dumps({outputName: wordNode}, indent=4))
    jsonFile.close()

def LoadDatabase(firebaseURL,databaseName,tablePKName,textualAttributes,Mute):


    print('Loading All tables of Database: {} into Firebase...'.format(databaseName))

    if Mute:
        if databaseName == "world":
            CleanCSVFile(tablePKName,Mute)
        WriteAllJson(tablePKName,databaseName,Mute)
        LoadJson(databaseName,firebaseURL,Mute)               # Comment it if you only need Node.json in Firebase!!!!

        url = firebaseURL + databaseName + '.json'
        if requests.get(url).status_code != 200:
            print("Connection Failed. Please connect your Firebase first!")

        data = requests.get(url).json()
        wordNode = GetWordIndex(data,textualAttributes,tablePKName,Mute)
        WriteNodeJson(wordNode,databaseName + "Node",Mute)
        LoadJson(databaseName + "Node",firebaseURL,Mute,method='PATCH')

        wordAllDataNode = GetAllDataNode(firebaseURL,databaseName,tablePKName)
        WriteNodeJson(wordAllDataNode,databaseName + "AllDataNode",Mute)
        LoadJson(databaseName + "AllDataNode",firebaseURL,Mute,method='PATCH')

    else:
        print('-----BEGIN CLEANING-----')
        CleanCSVFile(tablePKName,Mute)
        print('-----BEGIN TRANSFORMING AND UPLOADING-----')
        WriteAllJson(tablePKName,databaseName,Mute)
        LoadJson(databaseName,firebaseURL,Mute)

        print('-----BEGIN CREATING INDEX IN FIREBASE-----')

        url = firebaseURL + databaseName + '.json'
        if requests.get(url).status_code != 200:
            print("Connection Failed. Please connect your Firebase first!")

        data = requests.get(url).json()
        wordNode = GetWordIndex(data,textualAttributes,tablePKName,Mute)
        WriteNodeJson(wordNode,databaseName + "Node",Mute)
        LoadJson(databaseName + "Node",firebaseURL,Mute,method='PATCH')

        wordAllDataNode = GetAllDataNode(firebaseURL,databaseName,tablePKName)
        WriteNodeJson(wordAllDataNode,databaseName + "AllDataNode",Mute)
        LoadJson(databaseName + "AllDataNode",firebaseURL,Mute,method='PATCH')

def MainLoad(firebaseURL,connect,Mute,databaseNameList):

    tablePKName = GetPKName(connect,databaseNameList = databaseNameList)
    textualAttributes = GetTextualAttributes(connect,databaseNameList = databaseNameList)

    for databaseName in databaseNameList:
        for tableName in tablePKName[databaseName].keys():
            ExportTableToCSV(connect, databaseName, tableName, tablePKName[databaseName])

        LoadDatabase(firebaseURL=firebaseURL, databaseName=databaseName,
                 tablePKName=tablePKName[databaseName],
                 textualAttributes=textualAttributes[databaseName],Mute=Mute)



