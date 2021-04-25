import os
import time
import json
from py2neo import Graph, Node


def create_node():

    pass


def create_graph_nodes():
    pass


def create_graph_rels():
    pass


def create_relationship():
    pass


def main():

    input_file = '../data/cleaned_data.json'

    input_data = json.load(open(input_file, 'r', encoding='utf-8'))
    print(input_data)

    graph = Graph('http://localhost:7474/', username='neo4j', password='xxx')
    print(type(graph))

    """
    @TODO: Load to Neo4J

    """


if __name__ == "__main__":
    main()
