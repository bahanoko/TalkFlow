import networkx as nx
from pyvis.network import Network

class TopicGraph:
    def __init__(self):
        self.G = nx.Graph()

    def topics_to_graph(self, topics):
        # for node in topics:
        #     if isinstance(node, tuple):
        #         topic, related_topics = node
        #     else:
        #         topic = node.topic
        #         related_topics = node.related_topics

        for t in topics.topics:
            main_topic = t.topic
            self.G.add_node(main_topic)
            for rel in t.related_topics:
                self.G.add_edge(main_topic,rel.topic,weight=rel.weight)
        self.visualize_graph_pyvis()


    def visualize_graph_pyvis(self, output_html="graph.html"):
        net = Network(height="600px", width="100%")
        net.from_nx(self.G)    
        net.write_html(output_html)


