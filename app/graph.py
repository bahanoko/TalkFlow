import networkx as nx
from networkx.readwrite import json_graph

class TopicGraph:
    def __init__(self):
        self.G = nx.Graph()
        self.result = None

    def topics_to_graph(self, topics):
        for t in topics.topics:
            main_topic = t.topic
            self.G.add_node(main_topic)
            for rel in t.related_topics:
                self.G.add_edge(main_topic, rel.topic, weight=rel.weight)
        data = json_graph.node_link_data(self.G)
        for node in data["nodes"]:
            if "id" not in node and "name" in node:
                node["id"] = node.pop("name")
        self.result = {"nodes": data["nodes"], "links": data["links"]}
        print("グラフ化")
        return self.result

    def get_result(self):
        return self.result

    def reset(self):
        self.G.clear()
        self.result = None

