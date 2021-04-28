import flask
from flask import request
from flask_cors import CORS
from Backend.main import reco_execution, search_execution, find_execution, rate_execution
from gevent import pywsgi

server = flask.Flask(__name__)
CORS(server, resources=r'/*')


@server.route('/recommend', methods=['post'])
def recommend():
    request_data = request.json
    print(request_data)

    return reco_execution(request_data)


@server.route('/search', methods=['post'])
def search():
    request_data = request.json
    print(request_data)

    return search_execution(request_data)


@server.route('/find_similar', methods=['post'])
def find():
    request_data = request.json
    print(request_data)

    return find_execution(request_data)


@server.route('/rate', methods=['get', 'post'])
def rate():
    if request.method == 'GET':
        rate_value = request.values.get('rate')
        comment = request.values.get('comment')
    else:
        data = request.json
        rate_value = data.get('rate')
        comment = data.get('comment')

    return rate_execution(rate_value, comment)


if __name__ == '__main__':
    host = '0.0.0.0'  # 'Localhost'
    port = 8000
    print('run server...')
    # deployed_server = pywsgi.WSGIServer((host, port), server)
    # deployed_server.serve_forever()

    server.run(debug=True, port=port, host=host)
