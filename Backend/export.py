import csv

def WordProcess(word):
    if word == None:
        processedWord = 'NULL'
    else:
        processedWord = ('"'+str(word)+'"').replace("\'","!").replace('"',"'").replace("!","\\'")
    return processedWord

def WordProcessSimplified(word):
    if type(word) == str and word.find(",")!= -1:
        word = '"' + word + '"'
    return word

def GetPKName(connect,databaseNameList):

    tablePKNameDict = {}
    for databaseName in databaseNameList:
        cursor = connect.cursor()
        sqltext = 'SELECT TABLE_NAME,COLUMN_NAME FROM information_schema.COLUMNS ' \
                  'WHERE TABLE_SCHEMA = "{}" AND COLUMN_KEY = "PRI";'.format(databaseName)
        cursor.execute(sqltext)

        tablePKName = {}
        tableList = []
        pkList = []
        for table in cursor:
            tableList.append(list(table)[0])
            pkList.append(list(table))
        tableDict = set(tableList)
        for table in tableDict:
            tablePKName.update({table:[]})
        for pk in pkList:
            for table in tablePKName:
                if pk[0] == table:
                    tablePKName[table].append(pk[1])
        #print(databaseName,tablePKName)
        cursor.close()

        tablePKNameDict.update({databaseName:tablePKName})

    return tablePKNameDict

def GetTextualAttributes(connect,databaseNameList):

    textualAttributesListDict = {}
    for databaseName in databaseNameList:
        cursor = connect.cursor()
        if databaseName == 'news':
            sqltext = 'SELECT TABLE_NAME,COLUMN_NAME FROM information_schema.COLUMNS ' \
                      'WHERE TABLE_SCHEMA = "{}" AND (DATA_TYPE = "datetime" ' \
                      'OR DATA_TYPE = "varchar" OR DATA_TYPE = "longtext" OR DATA_TYPE = "mediumtext");'.format(databaseName)
        elif databaseName == 'sakila':
            sqltext = 'SELECT TABLE_NAME,COLUMN_NAME FROM information_schema.COLUMNS ' \
                      'WHERE TABLE_SCHEMA = "{}" AND (DATA_TYPE = "char" ' \
                      'OR DATA_TYPE ="enum" OR DATA_TYPE = "varchar" OR DATA_TYPE = "text"' \
                      'OR DATA_TYPE = "year" OR DATA_TYPE = "set" OR DATA_TYPE = "mediumtext"' \
                      'OR DATA_TYPE = "smallint" OR DATA_TYPE = "tinyint" OR DATA_TYPE = "mediumint"' \
                      'OR DATA_TYPE = "int");'.format(databaseName)
        else:
            sqltext = 'SELECT TABLE_NAME,COLUMN_NAME FROM information_schema.COLUMNS ' \
                      'WHERE TABLE_SCHEMA = "{}" AND (DATA_TYPE = "char" ' \
                      'OR DATA_TYPE ="enum" OR DATA_TYPE = "varchar" OR DATA_TYPE = "text"' \
                      'OR DATA_TYPE = "year" OR DATA_TYPE = "set" OR DATA_TYPE = "mediumtext" ' \
                      'OR DATA_TYPE = "int");'.format(databaseName)
        cursor.execute(sqltext)
        textualAttributesDict = {}
        tableList = []
        attributeList = []
        for table in cursor:
            tableList.append(list(table)[0])
            attributeList.append(list(table))
        tableDict = set(tableList)

        for table in tableDict:
            textualAttributesDict.update({table:[]})
        for attribute in attributeList:
            for table in textualAttributesDict:
                if attribute[0] == table:
                    textualAttributesDict[table].append(attribute[1])
        #print(databaseName,textualAttributesDict)
        cursor.close()

        textualAttributesListDict.update({databaseName:textualAttributesDict})

    return textualAttributesListDict

def ExportTableToCSV(connect,databaseName,tableName,PKName):

    if databaseName == "world":
        cursor = connect.cursor()
        csvFile = open("{}.csv".format(tableName),'w',newline='',encoding='utf-8')
        #mydialect = csv.register_dialect('mydialect', delimiter=',', quoting=csv.QUOTE_ALL)
        writer = csv.writer(csvFile,delimiter=',')

        # write metadata
        sqltext = 'SELECT COLUMN_NAME FROM information_schema.COLUMNS ' \
                  'WHERE TABLE_SCHEMA = "{}" AND TABLE_NAME = "{}" ORDER BY ORDINAL_POSITION;'.format(databaseName,tableName)
        cursor.execute(sqltext)
        metadataList = []

        for attribute in cursor:
            if (list(attribute)[0] == PKName[tableName][0]) or (list(attribute)[0] in PKName[tableName]):
                metadataList.append('# '+ str(attribute[0]))
            else:
                metadataList.append(list(attribute)[0])
        cursor.close()
        #print(metadataList)
        writer.writerow([metadataList[0]]+[" "+metadata for metadata in metadataList[1:]])

        # write data
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM {}.{};".format(databaseName,tableName))

        for row in cursor:
            row = [WordProcess(row[0])]+[' '+WordProcess(word) for word in row[1:]]
            row = ','.join([str(word) for word in list(row)]).split(',')

            #print(row)
            writer.writerow(row)
            #print(str(row))
            #writer.writerow(str(row))
        csvFile.close()

        cursor.close()

    else:

        cursor = connect.cursor()
        csvFile = open("{}_cleaned.csv".format(tableName), 'w', newline='', encoding='utf-8')
        writer = csv.writer(csvFile, delimiter=',')

        # write metadata
        if tableName == "staff":
            sqltext = 'SELECT COLUMN_NAME FROM information_schema.COLUMNS ' \
                      'WHERE TABLE_SCHEMA = "{}" AND TABLE_NAME = "{}" ' \
                      'AND COLUMN_NAME NOT LIKE "picture"' \
                      'ORDER BY ORDINAL_POSITION;'.format(databaseName,tableName)
        elif tableName == "address":
            sqltext = 'SELECT COLUMN_NAME FROM information_schema.COLUMNS ' \
                      'WHERE TABLE_SCHEMA = "{}" AND TABLE_NAME = "{}" ' \
                      'AND COLUMN_NAME NOT LIKE "location"' \
                      'ORDER BY ORDINAL_POSITION;'.format(databaseName,tableName)
        else:
            sqltext = 'SELECT COLUMN_NAME FROM information_schema.COLUMNS ' \
                      'WHERE TABLE_SCHEMA = "{}" AND TABLE_NAME = "{}" ORDER BY ORDINAL_POSITION;'.format(databaseName,tableName)
        cursor.execute(sqltext)

        metadata = [attribute for attribute in cursor]
        metadataList = [str(list(metadata[0])[0])] + [list(key)[0] for key in metadata[1:]]

        cursor.close()
        writer.writerow(metadataList)

        # write data
        cursor = connect.cursor()
        if tableName == "staff":
            cursor.execute("SELECT staff_id,first_name,last_name,address_id,email,store_id,"
                           "active,username,password,last_update FROM {}.{};".format(databaseName, tableName))
        elif tableName == "address":
            cursor.execute("SELECT address_id,address,address2,district,city_id,postal_code,"
                           "phone,last_update FROM {}.{};".format(databaseName, tableName))
        else:
            cursor.execute("SELECT * FROM {}.{};".format(databaseName, tableName))

        for row in cursor:
            row = [WordProcessSimplified(word) for word in row]
            writer.writerow(row)

        csvFile.close()
        cursor.close()

def MainExport(connect,databaseNameList):

    for databaseName in databaseNameList:
        print('Start exporting database: {}...'.format(databaseName))
        tablePKName = GetPKName(connect, databaseNameList)[databaseName]
        for tableName in tablePKName.keys():
            ExportTableToCSV(connect, databaseName, tableName, tablePKName)

