import networkx as nx
from pyvis.network import Network

class TopicGraph:
    def __init__(self):
        self.G = nx.Graph()
        net = Network(height="600px", width="100%")
        net.from_nx(self.G)    
        net.write_html("./app/static/graph.html")

    def topics_to_graph(self, topics):
        for t in topics.topics:
            main_topic = t.topic
            self.G.add_node(main_topic)
            for rel in t.related_topics:
                self.G.add_edge(main_topic,rel.topic,weight=rel.weight)
        self.visualize_graph_pyvis()


    def visualize_graph_pyvis(self, output_html="./app/static/graph.html"):
        net = Network(height="600px", width="100%")
        net.from_nx(self.G)    
        net.write_html(output_html)


