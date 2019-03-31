from all_dependencies import *



class Service_Nodes():

    def __init__(self):
        self.dictionary_left_nodes={}
        self.dictionary_right_nodes={}
        self.nodes_pair={}


class Node_Pair():
    def __init__(self,pair):
        self.pair=pair
        self.shortest_paths=[]
        self.services_configured=[]
        self.allocated_services=[]

    def add_service_name(self,service):
        self.allocated_services.append(service)


class Network_Functions():
    def __init__(self):
        pass



class Services_and_Operations():
    def __init__(self):
        self.service_and_op_dictionary={}
        self.network_functions_dictionary={}





class Service():
    def __init__(self,service_name,service_nodes,topology,services_and_operations):
        self.service_dictionary={}
        self.service_allotted={}
        self.service_name=service_name
        self.service_nodes=service_nodes
        self.services_and_operations=services_and_operations
        self.service_instance=""




    def allocate_service(self,topology):
        for node_pair,node_pair_instance in self.service_nodes.nodes_pair.items():
            node_pair_instance.add_service_name(service=self)
            print(node_pair)
            source=node_pair[0]
            destination=node_pair[1]
            print(topology.graph.edges)
            node_pair_instance.shortest_paths=[shortest_path for shortest_path in nx.all_shortest_paths(topology.graph,source,destination)]
            for short_path in node_pair_instance.shortest_paths:
                # find capacity of the link
                print(short_path)

        if self.service_name=="ECMP":
            print("ECMP selected between: ",self.service_nodes.nodes_pair.keys())
            ecmp=ECMP(self.service_nodes)
            self.service_instance=ecmp

    def apply_service_rule(self):
        pass
        #self.service_instance.

    def configure_service(self,service_list,service_nodes):
        for service_name in service_list:
            self.allot_service(service_nodes.nodes_pair,service_name)


    def allot_service(self,nodes_pair,service_name):
        pass


class Base_Service():
    def __init__(self,service_nodes):
        self.service_nodes=service_nodes
        for node_pair in service_nodes.nodes_pair:
            self.configure_service(node_pair)

    def configure_service(self,node_pair):
        pass

class ECMP(Base_Service):
    def __init__(self,service_nodes):
        Base_Service.__init__(self,service_nodes)
        print("ECMP service initialized ")
        for node_pair,node_pair_instance in service_nodes.nodes_pair.items():
            self.configure_ecmp(node_pair_instance)



    def hash_algorithm(self,node_instance,right_node_list,shortest_paths):
        next_hop_list=[]
        print(shortest_paths)
        for shortest_path in shortest_paths:
            print("shortest path is ",shortest_path)
            print(shortest_path[1])
            next_hop_list.append(shortest_path[1])
        print(next_hop_list)
        number_of_paths=len(next_hop_list)
        for dest_node in right_node_list:
            next_hop=self.modulo_n(number_of_paths,dest_node.ip_address)
            next_hop=next_hop_list[next_hop]
            node_instance.ip_lookup_table[dest_node]=next_hop



    def modulo_n(self,number_of_hops,dest_ip_address):
        print(dest_ip_address.ip_address)
        print(number_of_hops)
        last_octet=dest_ip_address.ip_address[24:]
        next_hop=int(last_octet,2)%number_of_hops
        print("last octet is ",last_octet)
        return next_hop

    def configure_nodes(self,node):
        pass

    def configure_ecmp(self,node_pair_instance):
        right_nodes_list=self.service_nodes.dictionary_right_nodes.values()
        shortest_paths=node_pair_instance.shortest_paths
        print("shortest paths between ",node_pair_instance.pair," : ",shortest_paths)
        for shortest_path in shortest_paths:
            print(shortest_path)
        for node_label, node_instance in self.service_nodes.dictionary_left_nodes.items():
            self.hash_algorithm(node_instance,right_nodes_list,shortest_paths)




class Create_Service():
    def __init__(self):
        pass

    def create_service_instance(self):
        pass