import flask
from flask import request
from flask_cors import CORS
from main import SearchExecution, QueryExecution, Rate
from gevent import pywsgi

server = flask.Flask(__name__)
CORS(server)

@server.route('/search', methods=['get'])

def search():
    databaseName = request.values.get('databasename')
    tableList = request.values.get('tablelist')
    input = [request.values.get('searchwords')]

    #newInput = [re.sub(r'[^\w\s]','',input.replace('_',''))]


    return SearchExecution(databaseName, tableList, input)

@server.route('/query', methods=['get'])

def query():

    databaseName = request.values.get('databasename')
    tableList = request.values.get('tablelist')
    value = request.values.get('value')

    return QueryExecution(databaseName, tableList,value)

@server.route('/rate', methods=['get', 'post'])

def rate():
    if request.method == 'GET':
        rate = request.values.get('rate')
        comment = request.values.get('comment')
    else:
        data = request.json
        rate = data.get('rate')
        comment = data.get('comment')

    return Rate(rate, comment)

if __name__ == '__main__':
    host = '0.0.0.0'   # 'Localhost'
    port = 8000
    print('run server...')
    deployed_server = pywsgi.WSGIServer((host, port), server)
    deployed_server.serve_forever()

    #server.run(debug=True, port=port, host=host)

