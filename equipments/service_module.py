from all_dependencies import *



class Service_Nodes():

    def __init__(self):
        self.left_nodes_dict={}
        self.right_nodes_dict={}
        self.nodes_pair={}


class Node_Pair():
    def __init__(self,pair):
        self.pair=pair
        self.shortest_paths=[]
        self.services_configured=[]



class Service():
    def __init__(self,service_name,service_nodes,topology):
        self.service_dictionary={}
        self.service_allotted={}
        for node_pair,node_pair_instance in service_nodes.nodes_pair.items():
            print(node_pair)
            source=node_pair[0]
            destination=node_pair[1]
            print(topology.graph.edges)
            node_pair_instance.shortest_paths=nx.all_shortest_paths(topology.graph,source,destination)
            for short_path in node_pair_instance.shortest_paths:
                # find capacity of the link
                print(short_path)

        if service_name=="ECMP":
            print("ECMP selected between: ",service_nodes.nodes_pair.keys())
            ecmp=ECMP(service_nodes)


    def configure_service(self,service_list,service_nodes):
        for service_name in service_list:
            self.allot_service(service_nodes.nodes_pair,service_name)


    def allot_service(self,nodes_pair,service_name):
        pass


class ECMP():
    def __init__(self,service_nodes):
        for node_pair in service_nodes.nodes_pair:
            self.configure_ecmp(node_pair)



    def hash_algorithm(self):
        pass

    def configure_ecmp(self,node_pair):
        pass





class Create_Service():
    def __init__(self):
        pass

    def create_service_instance():
        pass