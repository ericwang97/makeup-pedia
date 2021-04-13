import mysql.connector
import sys
import requests
import json
import time

from search import GetSearchList, MainSearch
from load import MainLoad
from export import GetPKName


def CheckStatus(param, other=None):
    if param == 'firebase connection failed':
        return (json.dumps({'status': 1, 'msg': "Connection Failed. Please connect your Firebase first!"},
                           ensure_ascii=False))
    elif param == 'query all table':
        return (json.dumps({'status': 1, 'msg': "Sorry, some problems here. You might need to "
                                                "first press Reset button then re-input your search words. ".format(
            other)}, ensure_ascii=False))
    elif param == 'mysql connection failed':
        return (json.dumps({'status': 1, 'msg': "You should connect to MySQL first!"}, ensure_ascii=False))
    elif param == 'search failed':
        return (json.dumps({'status': 1, 'msg': 'Sorry, no matching data for: {}. Try to input in standard format, '
                                                'or try more tables!'.format(other)}, ensure_ascii=False))
    elif param == 'query failed':
        return (json.dumps({'status': 1, 'msg': 'Sorry, no relocated data for Primary key: {}.'.format(other)},
                           ensure_ascii=False))

    elif param == 'unknown fails':
        return (json.dumps({'status': 1, 'msg': "Unkonwn fails! Please debug!"}, ensure_ascii=False))


def SearchExecution(databaseName, tableList, input):
    firebaseURL = 'https://inf551-a79f9.firebaseio.com/'

    Mute = True
    needPrinted = False
    writeResultJson = False
    show_frequency = False
    searchWholeData = True
    stopWords = True

    sortDict = {}
    if databaseName == 'world':
        sortDict = {'city': 'Population', 'country': 'Population', 'countrylanguage': 'Percentage'}
    elif databaseName == 'sakila':
        sortDict = {'film': 'rental_rate'}
    elif databaseName == 'customers_order':
        sortDict = {'customers': 'creditLimit', 'payments': 'amount', 'products': 'quantityInStock'}
    elif databaseName == 'news':
        sortDict = {'tweet': 'favorite_count'}

    try:
        connect = mysql.connector.connect(
            host='127.0.0.1',
            user='inf551',
            passwd='inf551',
            port=3306,
            charset='utf8',
            use_unicode=True)

    except:
        print('You should connect to MySQL first!')
        # return CheckStatus('mysql connection failed')

    # url = firebaseURL + databaseName + '.json'
    # urlNode = firebaseURL + databaseName + 'Node.json'
    # urlAllDataNode = firebaseURL + databaseName + 'AllDataNode.json'
    #
    # if requests.get(url).status_code != 200 or requests.get(urlNode).status_code != 200:
    #     print("Connection Failed. Please connect your Firebase first!")
    #     return CheckStatus('firebase connection failed')
    #
    # else:
    #    if requests.get(url).json() == None or requests.get(urlNode).json() == None or requests.get(urlAllDataNode).json() == None:
    #        print("Index file doesn't exist, Initializing will take a while..")
    #        MainLoad(firebaseURL, connect, Mute, [databaseName])

    tablePKNameForSearch = GetSearchList(connect, databaseName=[databaseName], tableList=tableList)

    result = MainSearch(firebaseURL=firebaseURL, databaseName=databaseName, input=input,
                        tablePKNameForSearch=tablePKNameForSearch, Mute=Mute, needPrinted=needPrinted,
                        writeResultJson=writeResultJson, show_frequency=show_frequency,
                        searchWholeData=searchWholeData, stopWords=stopWords, sortList=sortDict)

    if result != None:
        return result
    else:
        return CheckStatus('search failed', "'" + input[0] + "'")


def QueryExecution(databaseName, tableList, value=None):
    firebaseURL = 'https://inf551-a79f9.firebaseio.com/'
    Mute = True

    try:
        connect = mysql.connector.connect(
            host='127.0.0.1',
            user='inf551',
            passwd='inf551',
            port=3306,
            charset='utf8',
            use_unicode=True)

    except:
        print('You should connect to MySQL first!')

    # if requests.get(firebaseURL + databaseName + '.json').status_code != 200:
    #    print("Connection Failed. Please connect your Firebase first!")

    if databaseName == 'rating':
        requests.request('PUT', firebaseURL + 'rating.json', json={})
        requests.request('PUT', firebaseURL + 'ratingAllDataNode.json', json={})
        requests.request('PUT', firebaseURL + 'ratingNode.json', json={})
        MainLoad(firebaseURL, connect, Mute, [databaseName])

    if tableList == '':
        return CheckStatus('query all table')

    else:
        # if requests.get(firebaseURL + databaseName  + '.json').json() == None:
        #    print("Index file doesn't exist, Initializing will take a while..")
        #    MainLoad(firebaseURL, connect, Mute, [databaseName])

        data = requests.get(firebaseURL + databaseName + '/' + tableList + '.json').json()

        if value == None:
            return json.dumps({'status': 0, 'data': data}, indent=4)
        else:
            tablePKName = GetPKName(connect, [databaseName])
            for eachData in data:
                for attribute in tablePKName[databaseName][tableList]:
                    if eachData[attribute] == value:
                        return json.dumps({'status': 0, 'data': [eachData]}, indent=4)

            return CheckStatus('query failed', "'" + value + "'")


def Rate(rate, comment):

    try:
        connect = mysql.connector.connect(
            host='127.0.0.1',
            user='inf551',
            passwd='inf551',
            port=3306,
            charset='utf8',
            use_unicode=True)

    except:
        print('You should connect to MySQL first!')

    try:

        if rate == "":
            return json.dumps({'status': 1, 'msg': 'Sorry, please rate it before sending'}, indent=4)

        else:

            current_time = time.asctime(time.localtime(time.time()))
            cursor = connect.cursor()
            cursor.execute("insert into rating.rating(Rating, Comment, Created_time) values('{}','{}','{}')".format(rate, comment, current_time))
            connect.commit()
            cursor.close()

            if comment == "":
                return json.dumps({'status': 0, 'msg': "Successfully received! I will improve myself for sure. "
                                                           "It would be better if you can leave some "
                                                           "comment here. Thank you again!"}, indent=4,
                                  ensure_ascii=False)
            else:
                if float(rate) >= 4.5:
                    return json.dumps({'status': 0, 'msg': "Successfully received! I am go glad you satisfied with my work!"},
                                      indent=4,ensure_ascii=False)
                else:
                    return json.dumps({'status': 0, 'msg': "Successfully received! I will review your comment and "
                                                           "improve myself for sure. Thank you again!"}, indent=4,ensure_ascii=False)
    except:
        return json.dumps({'status': 1, 'msg': 'Sorry, sth wrong here..'}, indent=4)


if __name__ == "__main__":
    databaseName = sys.argv[1]
    tableList = sys.argv[2]
    input = sys.argv[3:]
    SearchExecution(databaseName, tableList, input)

    # databaseName = 'sakila'
    # tableList = ''
    # input = ['Japanese Animation R trailers']
