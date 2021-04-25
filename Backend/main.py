import mysql.connector
import json
import time

from Backend.Recommendation.Reco import reco_main


def reco_execution(request):

    print(request)
    result = reco_main(request)

    if result:
        result = {'status': 0, 'response': result}
    else:
        result = {'status': 1, 'msg': 'Sorry, no recommend results here.'}

    return json.dumps(result, indent=4, ensure_ascii=False)


def rate_execution(rate, comment):
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
            cursor.execute("insert into rating.rating(Rating, Comment, "
                           "Created_time) values('{}','{}','{}')".format(rate, comment, current_time))
            connect.commit()
            cursor.close()

            if comment == "":
                return json.dumps({'status': 0, 'msg': "Successfully received! I will improve myself for sure. "
                                                       "It would be better if you can leave some "
                                                       "comment here. Thank you again!"}, indent=4,
                                  ensure_ascii=False)
            else:
                if float(rate) >= 4.5:
                    return json.dumps(
                        {'status': 0, 'msg': "Successfully received! I am go glad you satisfied with my work!"},
                        indent=4, ensure_ascii=False)
                else:
                    return json.dumps({'status': 0, 'msg': "Successfully received! I will review your comment and "
                                                           "improve myself for sure. Thank you again!"}, indent=4,
                                      ensure_ascii=False)
    except:
        return json.dumps({'status': 1, 'msg': 'Sorry, sth wrong here..'}, indent=4)
