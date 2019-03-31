from all_dependencies import *

class Topology():
    def __init__(self):
        self.graph = nx.Graph()
        self.port_graph=nx.Graph()
        self.ip_address_graph = nx.Graph()

        self.network_node_instance_list = []
        self.node_numbers = 1
        self.node_instance_dictionary_by_node_id = {}
        self.port_graph = nx.Graph()
        self.port_numbers = 1

    def draw_Network(self):
        pass

    def find_shortest_path(self, node_instance_1, node_instance_2):
        shortest_path = nx.shortest_path(self.graph, node_instance_1, node_instance_2)
        return shortest_path

    def find_all_shortest_paths(self,node_instance1,node_instance2):
        shortest_paths=nx.all_shortest_paths(self.graph,node_instance1,node_instance2)

    def add_edge_to_topology(self, node_instance_1, node_instance_2):
        self.graph.add_edge(node_instance_1, node_instance_2)
        print(node_instance_1)
        print(node_instance_2)
        print("edge added to topology graph")
        self.ip_address_graph.add_edge(node_instance_1.ip_address, node_instance_2.ip_address)
        print("edge added to ip address graph")

    def add_nodes_to_topology(self, node_instance):
        self.graph.add_node(node_instance)
        self.ip_address_graph.add_node(node_instance)

    def upload_topology(self):
        for node in self.graph.nodes:
            print(node)
            node.controller_ip = "127.0.0.1"
            node.controller_port = "6640"

    def upgrade_topology(self):
        pass
