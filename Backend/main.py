import mysql.connector
import json
import time
from py2neo import Graph

from Backend.backend_features.reco import reco_main
from Backend.backend_features.search import search_main
from Backend.backend_features.find_similar import find_main


def reco_execution(request):

    result = reco_main(request)

    if result:
        result = {'status': 0, 'response': result}
    else:
        result = {'status': 1, 'msg': 'Sorry, no recommend results here.'}

    return json.dumps(result, indent=4, ensure_ascii=False)


def search_execution(request):

    result = search_main(request)

    if result:
        result = {'status': 0, 'response': result}
    else:
        result = {'status': 1, 'msg': 'Sorry, no search results here.'}

    return json.dumps(result, indent=4, ensure_ascii=False)


def find_execution(request):

    result = find_main(request)

    if result:
        result = {'status': 0, 'response': result}
    else:
        result = {'status': 1, 'msg': 'Sorry, no similar results here.'}

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

def search_graph_execution(product_id_list):
    g = Graph(
        host="127.0.0.1",
        http_port=7474,
        user="neo4j",
        password="makeuppedia")

    try:
        product_id_list = [int(i) for i in product_id_list]
        print(product_id_list)
        query = "match path=(m:Product)-[r]->(n) where m.product_id in $s return relationships(path) as relationships  limit 200"
        data = g.run(query, s=product_id_list)

        nodes = []
        rels = []

        node_dict = {}

        while data.forward():
            cursor = data.current
            for relation in cursor['relationships']:

                source_node = relation.start_node
                target_node = relation.end_node
                source_node_name = source_node['name']
                target_node_name = target_node['name']

                relation_type = list(relation.types())[0]
                source_node_label = str(source_node.labels).strip(":")
                target_node_label = str(target_node.labels).strip(":")

                cur_source_node = {'name': source_node_name, 'label': source_node_label }
                cur_target_node = {'name': target_node_name, 'label': target_node_label }

                if cur_source_node['name']+"|||"+cur_source_node['label'] not in node_dict.keys():
                    node_dict[cur_source_node['name']+"|||"+cur_source_node['label']] = len(node_dict)
                    nodes.append(cur_source_node)

                if cur_target_node['name']+"|||"+cur_target_node['label'] not in node_dict.keys():
                    node_dict[cur_target_node['name']+"|||"+cur_target_node['label']] = len(node_dict)
                    nodes.append(cur_target_node)

                cur_source_node['id'] = node_dict[cur_source_node['name']+"|||"+cur_source_node['label']]
                cur_target_node['id'] = node_dict[cur_target_node['name'] + "|||" + cur_target_node['label']]

                rels.append(
                    {
                        'source':  cur_source_node['id'],
                        'target':  cur_target_node['id'],
                        'relation': relation_type
                    }
                )
        return json.dumps({'nodes': nodes, 'links': rels}, indent=4)

    except Exception as e:
        print(e)
