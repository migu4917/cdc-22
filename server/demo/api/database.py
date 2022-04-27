from py2neo import Graph, NodeMatcher, RelationshipMatcher
from pymongo import MongoClient

# MongoDB
mongo_path = MongoClient(
    "mongodb://%s:%s@localhost:27017" % ("admin", "123456"))
db = mongo_path["surveys"]
col = db["production"]  # 患者表
col_contacts = db["contacts"]  # 密接者表
col_epidemic = db["epidemic"]  # 疫情表

# Neo4j
neo4j_path = "http://localhost:7474/"
graph = Graph(neo4j_path, user="neo4j", password="123456")
node_matcher = NodeMatcher(graph)
rel_matcher = RelationshipMatcher(graph)
