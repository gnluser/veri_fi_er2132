from all_dependencies import *
from addresses import *
import re


class Node():
    def __init__(self, node_id):
        self.node_id = node_id
        self.mac_address = ""
        self.ip_address = ""
        self.canvas_coords = ""
        self.latitude = 0
        self.longitude = 0
        self.connecting_node_instance_list = []
        self.subequipment_dictionary_of_port_lists = {}
        self.create_addresses()
        self.queue_size = ""
        self.packet_queue = []  ## queuing packets instances
        self.subequipment_list = []
        self.canvas_label_window_id=""
        self.port_list=[]
        self.port_counter=0


    def update_ports(self,ports,subpart,subequipment,equipment):
    #def update_ports(self,**kwargs):
        #if len(kwargs) == 1:
        #    pass
        #else:
        #ports=kwargs[0]
        #        subequipment=kwargs[1]
        #    equipment=kwargs[2]
        self.identify_ports_from_entry(ports)

        #### need to put options for type of ports selection to gui

    def identify_ports_from_entry(self,ports):
        '''
        port_list=ports.split(",")
        for port in port_list:
            print(port)
            port_property=port.split("X")
            num_of_ports=port_property[0]
            port_capacity=port_property[1]
            port = Port(self.port_counter,port_capacity)  # port_id, port_capacity, subequipment_instance, node_instance
            self.port_list.append(port)
            self.port_counter += 1
        '''
        # split ports on bases of space and new line
        if ports!="":
            print("lnbnmk;",ports)
            port_list_entry=ports.split("\n")
            for fixed_port_slots in port_list_entry:
                port_config=fixed_port_slots.split("or")
                for port_config_option in port_config:
                    port_options=port_config_option.split(" ")
                    num_ports=port_options[0]
                    if port_options[1].lower()=='x':
                        port_configs=port_options[2]
                        if len(port_options)>3:
                        #if port_options.len()>3:
                            port_type=port_options[3]
                        else:
                            port_type=""
                        type_of_port_options=port_configs.split("/")
                        list_of_port_capacity_options=[]
                        for type in type_of_port_options:
                            #x=re.search("G",type)
                            x=re.split("\s*G",type)[0]
                            list_of_port_capacity_options.append(int(x)*1000)
                            y=re.split("\s*M",type)[0]
                            y=re.search("M",type)
                            list_of_port_capacity_options.append(int(y))
                        port_capacity=max(list_of_port_capacity_options)
                        ### need to make port selection for the port types
                        for port_no in range(num_ports):
                            port=Port(port_no,port_capacity,subequipment_instance="",node_instance=self) ###, port_id, port_capacity, subequipment_instance, node_instance)
                            port.port_type=port_type
                            self.port_list.append(port)

                    else:
                        port_type=port_options[1]
                        for port_no in range(int(num_ports)):
                            port=Port(port_no,port_capacity="",subequipment_instance="",node_instance=self)
                            port.port_type=port_type
                            self.port_list.append(port)

    def create_subequipment(self):
        # initialize only one subequipment by default
        subequipment = SubEquipment()
        return subequipment

    def create_addresses(self):
        self.create_mac_address()
        self.create_ip_address()

    def create_mac_address(self):
        self.mac_address = MAC_Address()
        self.mac_address.create_mac_address_id()
        mac_addresses_allotted_to_node[self.mac_address.mac_address] = self

    def create_ip_address(self):
        self.ip_address = Ip_Address(parent_ip_address="")
        self.ip_address.create_ip_address()
        ip_addresses_allotted_to_node[self.ip_address.ip_address] = self


class Switch(Node):
    def __init__(self, node_id):
        Node.__init__(self, node_id)
        self.type = "Switch"


class Router(Node):
    def __init__(self, node_id):
        Node.__init__(self, node_id)
        self.type = "Router"


class Firewall(Node):
    def __init__(self, node_id):
        Node.__init__(self, node_id)
        self.type = "Firewall"


class Gateway(Node):
    def __init__(self, node_id):
        Node.__init__(self, node_id)
        self.type = "Gateway"


class DataCenter_Interconnect(Node):
    def __init__(self, node_id):
        Node.__init__(self, node_id)
        self.type = DataCenter_Interconnect


class Network_Node(Node):
    def __init__(self, node_id, ports):
        self.ports = ports
        # self.node_id=node_id
        Node.__init__(self, node_id)
        self.port_dictionary = {}
        self.direction = 0
        # self.canvas_coords=""
        # self.latitude=""
        # self.longitude=""
        self.node_equipment_dictionary = {}
        # self.connecting_node_instance_list=[]
        self.network_edge_labels_list = []
        self.subequipment_list = []

    '''
    def create_ports(self):
        for ports in range(self.ports):
            self.port_dictionary[ports]=Port(ports,self.node_id,port_capacity=0)
    '''


class Access_Node(Network_Node):
    def __init__(self, node, ports):
        Network_Node.__init__(self, node, ports)
        self.type = "Access_Network_Node"
        # self.create_ports()
        self.unused_ports = list(self.port_dictionary.keys())
        self.distance = 300


class Metro(Network_Node):
    def __init__(self, node, ports):
        Network_Node.__init__(self, node, ports)
        # self.create_ports()
        self.type = "Metro_Network_Node"
        self.unused_ports = list(self.port_dictionary.keys())
        self.distance = 200


class Core(Network_Node):
    def __init__(self, node, ports):
        Network_Node.__init__(self, node, ports)
        self.type = "Core_Network_Node"
        # self.create_ports()
        self.unused_ports = list(self.port_dictionary.keys())
        self.distance = 30


class Aggregation_Node(Network_Node):
    def __init__(self, node):
        Network_Node.__init__(self, node, ports=3)
        self.type = "Aggregation_Node"


class P_Node(Network_Node):
    def __init__(self, node_id, number_of_ports):
        Network_Node.__init__(self, node_id, number_of_ports)
        self.type = "P_Network_Node"
        # self.node_id=node_id
        # self.ports=number_of_ports
        # self.create_ports()
        self.unused_ports = list(self.port_dictionary.keys())
        # Node.__init__(self,node_id,number_of_ports)
        # pass
        self.distance = 100


'''
class Card(): # subequipment class created alias
    def __init__(self):
        self.card_id=""
        self.ports=""
        self.rate=""
        self.network=""

    def ports_allocation(self):
        #port=Port()
        pass
'''


class Port():
    def __init__(self, port_id, port_capacity, subequipment_instance, node_instance):
        self.port_id = port_id
        self.node_instance = node_instance
        self.subequipment_instance = subequipment_instance
        self.port_capacity = port_capacity
        self.protocol = ""
        self.network = ""
        self.port_type=""
        # self.unused_ports=[]


# for data centres, port_dictionary are distributed among north_port_dictionary and south_port_dictionary


class DC_Node(Node):
    def __init__(self, node_id, number_of_ports):
        # self.node_id=node_id
        Node.__init__(self, node_id)
        self.capacity = ""
        self.type_of_network = ""
        self.connecting_switches_up = []
        self.connecting_switches_down = []
        self.number_of_ports = number_of_ports
        self.south_port = {}  # to, this port key has corresponding connecting north port of next connected node
        self.north_port = {}  # from, this port has key  value pair of current north port to next node south connected node
        self.network = ""

        self.south_ports_dictionary = {}
        self.north_ports_dictionary = {}

        self.direction = 0
        # self.canvas_coords=""
        # self.latitude = ""
        # self.longitude = ""
        self.node_equipment_dictionary = []
        # self.connecting_node_instance_list=[]
        self.network_edge_labels_list = []
        self.subequipment_list = []

    '''
    def create_ports(self):
        self.create_north_ports(self.number_of_ports)
        self.create_south_ports(self.number_of_ports)

    def create_south_ports(self,number_of_ports):
        for port in range(number_of_ports):
            self.south_ports_dictionary[port] = Port(port, self.node_id,port_capacity=0)

    def create_north_ports(self,number_of_ports):
        for port in range(number_of_ports):
            self.north_ports_dictionary[port] = Port(port, self.node_id,port_capacity=0)


    def cards_allocation(self):
        card = Card()
        pass

    '''

class Aggregation_DC_Node(DC_Node):
    def __init__(self, node_id):
        DC_Node.__init__(self, node_id, number_of_ports=0)
        self.type = "Aggregation_DC_Node"


class Server(Node):
    def __init__(self, server_id):
        # self.node_id=server_id
        Node.__init__(self, server_id)
        # self.port=Port(1,self.node_id,port_capacity=0)
        self.type = "Server"
        self.distance = 350
        # self.latitude=""
        # self.longitude=""
        # self.connecting_node_instance_list=[]
        self.network_edge_labels_list = []
        self.subequipment_list = []


class Pod():
    def __init__(self, pod_count, fat_tree_k_index, p_node):
        self.k = fat_tree_k_index
        self.pod_id = pod_count
        self.aggregation_node_dictionary = {}
        self.edge_node_dictionary = {}
        self.num_of_servers = pow(int(fat_tree_k_index / 2), 2)
        self.server_dictionary = {}
        self.create_aggregation_nodes(fat_tree_k_index)
        self.create_edge_nodes(fat_tree_k_index)
        self.create_servers()
        self.p_node = p_node

    def create_servers(self):

        for num in range(self.num_of_servers):
            server = Server(num)
            server.pod_id = self.pod_id
            self.server_dictionary[server.node_id] = server

    def create_aggregation_nodes(self, fat_tree_k_index):
        number_of_aggr_nodes = int(fat_tree_k_index / 2)
        for node in range(number_of_aggr_nodes):
            # creating k/2 aggregation nodes per pod
            self.aggregation_node_dictionary[node] = Aggregation_Node(self.pod_id, node, fat_tree_k_index)

    def create_edge_nodes(self, fat_tree_k_index):
        number_of_edge_nodes = int(fat_tree_k_index / 2)
        for node in range(number_of_edge_nodes):
            self.edge_node_dictionary[node] = Edge_Node(self.pod_id, node, fat_tree_k_index)


class Core_Node(DC_Node):
    def __init__(self, node_name, number_of_ports):
        DC_Node.__init__(self, node_name, number_of_ports)
        self.type = "Core_DC_Node"
        # Node.node_id=node_name
        # Node.number_of_ports=number_of_ports
        # self.port_dictionary={}
        self.create_north_ports(1)  # only one north port
        self.create_south_ports(self.number_of_ports)
        self.distance = 180


class Edge_Node(DC_Node):
    def __init__(self, pod_id, node, fat_tree_k_index):
        number_of_ports = int(fat_tree_k_index / 2)
        DC_Node.__init__(self, node, number_of_ports)
        self.type = "Edge_DC_Node"
        self.pod_id = pod_id
        # self.create_ports()
        self.distance = 240


class Client_Node(Node):
    def __init__(self, node_id):
        # self.node_id=node_id
        Node.__init__(self, node_id)
        self.type = "Client_Node"
        self.direction = 0
        self.distance = 380
        # self.latitude=""
        # self.longitude=""
        # self.connecting_node_instance_list=[]
        self.network_edge_labels_list = []
        self.subequipment_list = []
        self.port_dictionary = {}


#######################################################################################
#######################################################################################


class Probe_Node(Node):
    def __init__(self, node_id):
        # self.node_id=node_id
        Node.__init__(self, node_id)
        self.ports = 2
        self.type = "Probe_Node"
        # self.canvas_coords=""
        # self.latitude = ""
        # self.longitude = ""
        # self.connecting_node_instance_list = []
        self.network_edge_labels_list = []
        self.port_dictionary = {}


class Controller(Node):
    def __init__(self, node_id):
        Node.__init__(self, node_id)
        self.type = "Controller"
        # self.node_id = node_id
        # by default let's assume 3 ports
        self.north_ports = 1
        self.south_ports = 2
        # self.canvas_coords = ""
        # self.latitude = ""
        # self.longitude = ""
        # self.connecting_node_instance_list = []
        self.network_edge_labels_list = []
        self.port_dictionary = {}
        self.controller_ip = '127.0.0.1'
        self.port = "6640"

    # def create_connection(self,ip_address="127.0.0.1",port="6640"):

    def start_controller(self, topology):
        import sys
        import os

        try:
            directory_name = "/home/gnl/Desktop/mankul/opendaylight-0.9.1/bin"
            odl_command = "./karaf"
            os.system("cd " + directory_name)
            os.system(odl_command)
            os.system("telnet -e A %d %d", self.controller_ip, self.port)
            topology.upload_topology()
        except:
            print("controller is not running")

    def stop_controller(self):
        pass


class White_Box(Node):
    def __init__(self, node_id):
        # self.node_id = node_id
        Node.__init__(self, node_id)
        self.north_ports = 1
        self.ports = 2
        self.type = "White Box"
        # self.canvas_coords = ""
        # self.latitude = ""
        # self.longitude = ""
        # self.connecting_node_instance_list = []
        self.network_edge_labels_list = []
        self.port_dictionary = {}
