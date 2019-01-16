import networkx as nx
#import numpy as np
import  csv
import time
from functools import  partial

data_file="/home/gnl/Desktop/mankul/flask_project/sdnProject0.2/equipments.csv"
current_deployed_topology_file="current_topology.csv"### this file contain the current deployed topology
#####3 dictionary is in format **** :" ", longitude=" ", latitude="  ",equipment_1=" ",equipment_2=" ", equipment_3=" "...##
### equipment subcategory is card type..
## cad type subcategory is interface type

component_name='component name'
ports_per_cards='ports on cards/equipment'
throughput='Throughput'
line_rate='Mpps'
line_cards='line cards'
protocol='Feature and protocols'
layer_2="Layer 2 features"
layer_3='Layer 3 features'
usage='usage'
equipment_vendors=['cisco','juniper','nokia','ciena','huawei','fujitsu']#'arista',
line_cards_supported="types of line cards supported" # in the spreadsheet, line cards supported are seperated by ":"
equipment_properties=[component_name,ports_per_cards,throughput,line_rate,line_cards,protocol,layer_2,layer_3,usage]


canvas_height=1000
canvas_width=1500
#from topology import Topology
try:
    from tkinter import *
except ImportError:
    from Tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
#from variables import *
from math import *
#from network_equipment import *

node_type={"Aggregation_DC_Node":{"color":"coral","radius":"13","name":"Ag","distance":290,},\
           "Edge_DC_Node":{"color":"orangered","radius":"13","name":"Edg","distance":250},\
           "Core_DC_Node":{"color":"cyan","radius":"14","name":"CD","distance":200},\
           "P_Network_Node":{"color":"pink","radius":"14","name":"P","distance":170},\
           "Core_Network_Node":{"color":"blue","radius":"14","name":"CN","distance":0},\
           "Metro_Network_Node":{"color":"brown","radius":"13","name":"M","distance":100},\
           "Access_Network_Node":{"color":"orange","radius":"12","name":"Acc","distance":350},\
           "Server":{"color":"salmon","radius":"10","name":"S","distance":300},\
           "Client_Node":{"color":"green","radius":"10","name":"Cl","distance":380},
           "White Box":{"color":"white","radius":"12","name":"WB","distance":0},
           "Controller":{"color":"lightblue","radius":"14","name":"Cntrlr","distance":0},\
           "Probe Node":{"color":"yellow","side":"10","name":"Prb","distance":0}}


core_ring_radius=30
metro_ring_radius=25
metro_rings_distance=100
data_center_distance=200
access_rings_distance=350
inter_node_distance=70


############################################################################################
###############################################################Equipment loading###########3


class Load_Network_Information():
    def __init__(self):
        ne = Network_Equipments()
        ne.loading_equipments_list()
        self.ne = ne
        self.vendor_name = ""
        self.network_deployed_equipment_dictionary = {}
        ######self.network_equipment_dictionary = {}
        self.current_deployed_equipments = []

        self.deployed_nodes={}
        self.deployed_equipments=[]

        #self.deployed_equipments_properties={}

        self.topology=""
        try:
            self.create_minimal_topology()
        except:
            print("erorr in topology creation")
        try:
            self.load_current_deployed_topology()
        except:
            print("no initial topology")


    def create_minimal_topology(self):
        self.topology=Topology()
        print("topology created")

    def load_current_deployed_topology(self):
        try:
            if current_deployed_topology_file[-3:]=="csv":
                self.read_topology_from_csv()
                print("file is csv")
            elif current_deployed_topology_file[-3:]=="xml":
                self.read_topology_from_xml()
                print("xml file")
        except:
            print("no file selected ")#type of elementi.e node, link
        # for node,2nd,3rd and 4th column are node_id, the latitude and longitude respectively
        # 5th column is equipment_id
        # 6th equipment_name
        # 7th column is sub_equipment_id
        # 8th is  sub_equipment_name
        # 9th column is interface type

        #line=csv.DictReader(current_deployed_topology_file,'r')
    def read_topology_from_csv(self):
        try:
            file=open(current_deployed_topology_file,'r')
            data=csv.reader(file)
            data_list=list(data)         # 2-dimesnion list
            for data_record in data_list:
                self.load_data_record(data_record)
                self.current_deployed_equipments.append(data_record)
            # load current deployed topo;ogy

        except:
            print("no initial topology provided")



    def load_data_record(self,data_record):
        if data_record[0].lower()=="NODE".lower():
            #load te node attributes
            node_id=data_record[1]
            node_name=data_record[2]###### Core node, aggregation node, metro node,, etc name in node_type
            longitude=data_record[3]
            latitude=data_record[4]
            equipment_id=data_record[5]
            equipment_name=data_record[6]
            subequipment_id=data_record[7]
            subequipment_name=data_record[8]
            interface_type=data_record[9]
            self.create_node(node_id,node_name,longitude,latitude,equipment_id,equipment_name,subequipment_id,subequipment_name,interface_type)


        elif data_record[1].lower()=="LINK".lower():
            #load the link attributes
            pass

    def create_node(self,node_id,node_name,longitude,latitude,equipment_id,equipment_name,subequipment_id,subequipment_name,interface_type):
        if node_id not in self.deployed_nodes.values():
            width=canvas_width/(360*60*60)
            height=canvas_height/(180*60*60)
            l, m, s = longitude[:-1].split("-")
            node_width = (s + (m * 60 + l * 60 * 60)) * 360
            h, m, s = latitude[:-1].split("-")
            node_height = (s + (m * 60 + h * 60 + 60)) * 180
            if latitude[-1:]!="N":
                node_height=-1*node_height
            if longitude[-1:]!= "E":
                node_width=-1*node_width
            node_height=node_height+height/2
            node_width=node_width+width/2
            attributes=node_type[node_name]
            radius=attributes["radius"]
            coords=node_width-radius,node_height-radius,node_width+radius,node_height+radius
            node_instance=self.create_node_instance(node_name,coords)
            node_instance.longitude=longitude
            node_instance.latitude=latitude
            #print("node added ")
            self.topology.graph.add_node(node_instance)
            self.deployed_nodes[node_id]=node_instance
            #self.deployed_equipments_properties[node_instance]

        self.create_equipments_on_nodes(node_id,equipment_id,equipment_name,subequipment_id,subequipment_name,interface_type)

    def create_equipments_on_nodes(self,node_id,equipment_id,equipment_name,subequipment_id,subequipment_name,interface_type):
        node_instance=self.deployed_nodes[node_id]
        if equipment_id not in node_instance.node_equipment_dictionary.values():
            equipment=Equipment()
            equipment.name=equipment_name
            equipment.id=equipment_id
            node_instance.node_equipment_dictionary[equipment_id]=equipment
            ###############
            ##
            ### add the equipment graph and respective edges
            ##
            ###############

        else:
            equipment=node_instance.node_equipment_dictionary[equipment_id]
        if subequipment_id not in equipment.node_subequipment_dictionary.values():
            subequipment=SubEquipment()
            subequipment.name=subequipment_name
            subequipment.id=subequipment_id
        else:
            subequipment=equipment.node_subequipment_dictionary[subequipment_id]
        ##########3
             ###3   add subequipment graph and edges and interface_type
            ##
        ############
    ############**********
    def create_node_instance(self,node_name,coords):#node_id,node_name,longitude,latitude,equipment_name,subequipment_name):
        #print("creating node instance on the canvas")
        attributes=node_type[node_name]
        name=attributes["name"]
        if name=="Cl":
            node=Client_Node(self.topology.node_numbers)
            self.topology.node_numbers+=1
            node.canvas_coords=coords
            #client
        elif name=="S":
            node= Server(self.topology.node_numbers)
            self.topology.node_numbers += 1
            node.canvas_coords = coords
            #Server
        elif name=="Acc":
            node=Access_Node(self.topology.node_numbers,0)
            self.topology.node_numbers += 1
            node.canvas_coords = coords
            #Access_Network_Node
            #Access_Network_Node
        elif name=="M":
            node=Metro(self.topology.node_numbers,0)
            self.topology.node_numbers += 1
            node.canvas_coords = coords
            #Metro_Network_Node
        elif name=="CN":
            node=Core(self.topology.node_numbers,0)
            self.topology.node_numbers += 1
            node.canvas_coords = coords
            #Core_Network_Node
        elif name=="P":
            node=P_Node(self.topology.node_numbers,0)
            self.topology.node_numbers += 1
            node.canvas_coords = coords
            #P_Network_Node
        elif name=="CD":
            node=Core_Node(self.topology.node_numbers,0)
            self.topology.node_numbers += 1
            node.canvas_coords = coords
            #Core_DC_Node
        elif name=="Edg":
            node=Edge_Node(self.topology.node_numbers,0,0)
            self.topology.node_numbers += 1
            node.canvas_coords = coords
            #Edge_DC_Node
        elif name=="Ag":
            node=Aggregation_Node(self.topology.node_numbers,0,0)
            self.topology.node_numbers += 1
            node.canvas_coords = coords
            #Aggregation_DC_Node
        elif name=="Prb":
            node=Probe()
        else :
            print("node not identified")
            node=""
            #new node
        return node




    def read_topology_from_xml(self):
        pass





class Network_Equipments:
    def __init__(self):
        self.network_equipment_vendor_dictionary = {}
        self.per_vendors_equipments_list = []

        # for items in equipment_properties:
        #    print items

    def loading_equipments_list(self):  # equipment list is loaded in vendor_instance's variable component_list dictionary with all names in list equipment_properties
        self.dictionary_list = []
        dictionary_equipments = []
        data = csv.DictReader(open(data_file, 'r'))
        for row in data:
            self.dictionary_list.append(row)  # row is an open dictionary object


        for items in self.dictionary_list:
            flag_for_vendor = False
            # loading equipments for all known vendors.
            for vendor_name in equipment_vendors:
                if vendor_name.lower() in (items[component_name]).lower():
                    flag_for_vendor = True
                    if vendor_name not in self.network_equipment_vendor_dictionary :
                        ####
                        ####Creating new vendor instance for new vendor in list....... vendor instances are in nw_eq_vndr_lst
                        ####
                        vendor_instance = Equipments_per_Vendor()
                        self.network_equipment_vendor_dictionary [vendor_name] = vendor_instance
                        self.per_vendors_equipments_list.append(vendor_instance)

                    else:
                        ####
                        ####adding new equipment in list information to vendor instance
                        ####
                        vendor_instance = self.network_equipment_vendor_dictionary [vendor_name]
                    # print(vendor_instance.func())
                    if items[component_name] not in vendor_instance.equipment_names_list:  # to avoid reloading same properties if present in csv file
                        vendor_instance.equipment_names_list.append(items[component_name])
                        new_equipment = Equipment()
                        try:
                            sub_equipment_list=new_equipment.identify_all_subequipments()
                            for sub_eq in sub_equipment_list:
                                if sub_eq not in vendor_instance.subequipment_list:
                                    vendor_instance.subequipment_list.append(sub_eq)
                        except:
                            print("no subequipments, only builtin components")

                        new_equipment.equipment_properties(items)
                        vendor_instance.equipment_dictionary[items[component_name]] = new_equipment
                    else:
                        #if items[component_name] not in vendor_instance.equipment_dictionary.keys():
                        new_equipment = SubEquipment()#Equipment()
                        #vendor_instance.equipment_dictionary[items[card_name]]= new_equipment
                        new_equipment.equipment_properties(items)
                        vendor_instance.equipment_dictionary[items[component_name]] = new_equipment
                        # print(vendor_instance.equipment_dictionary .values())



            if flag_for_vendor == False:
                print("vendor name not identified for ", items[component_name])

    def calling_vendor_names(self):
        # forwarding json  file to app to gorward it to the web page
        return equipment_vendors

    def calling_equipment_names(self, vendor_name):
        return self.network_equipment_vendor_dictionary [vendor_name].returning_equipment_names()


###each time new instance created, vendor instance is added to network_equipment_vendor_dictionary dictionary of ne

class Equipments_per_Vendor:
    # equipment_dictionary={}
    # component_property={}
    def __init__(self):
        self.equipment_dictionary = {}
        self.component_list = {}
        self.component_properties_list = []
        self.equipment_names_list = []
        self.subequipment_list=[] # use this sub equipment list to put the sub equipments to the equipment to be selected
        # print("equipment per vendor created")

    def returning_equipment_names(self):
        print("returning equipment names for specific vendor")
        return self.equipment_names_list


class Equipment():
    # equipment_properties_dictionary={}
    def __init__(self):
        self.name = ""
        self.id=""
        self.node_subequipment_dictionary={}
        self.equipment_properties_dictionary = {}
        self.subequipment_list=[]
        #self.card_list=[]

    def equipment_properties(self, items):
        for element in items:
            self.equipment_properties_dictionary[element] = items[element]

    def identify_all_ports(self):
        try:
            self.equipment_properties_dictionary[ports_per_cards]
        except:
            print("Selected equipment has not mentioned number and types of ports in respective datasheet")

    def identify_all_subequipments(self):
        try:

            self.subequipments_list_function(self.equipment_properties_dictionary[line_cards])
            return self.subequipment_list

        except:
            print("no data for cards")

    def subequipments_list_function(self,line_cards):
        subequipment_list=[]
        for words in line_cards.split(","):
            subequipment_list.append(words)
        #return subequipment_list
        ##### filling the subequipment_list for use while creating the device
        self.subequipment_list=subequipment_list
            #for eq in words.split(":"):
                #card=Card()
                #card_list.append(card)
########################################################################################
########################################################################################



class SubEquipment(Equipment):
    def __init__(self):
        Equipment.__init__(self)
        self.name=""
        self.id=""



##################################################################  Node Attributes
####################################################################################



class Network_Node():
    def __init__(self,node_id,ports):
        self.ports=ports
        self.node_id=node_id

        self.port_dictionary={}

        self.direction=0
        self.canvas_coords=""
        self.latitude=""
        self.longitude=""
        self.node_equipment_dictionary={}
        self.connecting_node_instance_list=[]
        self.network_edge_labels_list = []
        self.equipment_list=[]



    def create_ports(self):
        for ports in range(self.ports):
            self.port_dictionary[ports]=Port(ports,self.node_id)


class Access_Node(Network_Node):
    def __init__(self,node,ports):
        Network_Node.__init__(self,node, ports)
        self.type="Access_Network_Node"
        self.create_ports()
        self.unused_ports = list(self.port_dictionary.keys())
        self.distance=300


class Metro(Network_Node):
    def __init__(self,node,ports):
        Network_Node.__init__(self,node,ports)
        self.create_ports()
        self.type="Metro_Network_Node"
        self.unused_ports = list(self.port_dictionary.keys())
        self.distance=200

class Core(Network_Node):
    def __init__(self,node,ports):
        Network_Node.__init__(self,node,ports)
        self.type="Core_Network_Node"
        self.create_ports()
        self.unused_ports=list(self.port_dictionary.keys())
        self.distance=30



class P_Node(Network_Node):
    def __init__(self,node_id,number_of_ports):
        Network_Node.__init__(self,node_id, number_of_ports)
        self.type="P_Network_Node"
        #self.node_id=node_id
        #self.ports=number_of_ports
        self.create_ports()
        self.unused_ports = list(self.port_dictionary.keys())
        #Node.__init__(self,node_id,number_of_ports)
        #pass
        self.distance=100







class Card():
    def __init__(self):
        self.card_id=""
        self.ports=""
        self.rate=""
        self.network=""

    def ports_allocation(self):
        port=Port()
        pass


class Port():
    def __init__(self,port_id,node_id):
        self.port_id=port_id
        self.node_id=node_id
        self.network=""
        self.capacity=""
        self.protocol=""
        #self.unused_ports=[]




# for data centres, port_dictionary are distributed among north_port_dictionary and south_port_dictionary


class DC_Node():
    def __init__(self,node_id,number_of_ports):
        self.node_id=node_id
        self.capacity=""
        self.type_of_network=""
        self.connecting_switches_up=[]
        self.connecting_switches_down=[]
        self.number_of_ports=number_of_ports
        self.south_port={}#to, this port key has corresponding connecting north port of next connected node
        self.north_port={}#from, this port has key  value pair of current north port to next node south connected node
        self.network=""


        self.south_ports_dictionary={}
        self.north_ports_dictionary={}


        self.direction=0
        self.canvas_coords=""
        self.latitude = ""
        self.longitude = ""
        self.node_equipment_dictionary=[]
        self.connecting_node_instance_list=[]
        self.network_edge_labels_list=[]
        self.equipment_list=[]

    def create_ports(self):
        self.create_north_ports(self.number_of_ports)
        self.create_south_ports(self.number_of_ports)

    def create_south_ports(self,number_of_ports):
        for port in range(number_of_ports):
            self.south_ports_dictionary[port] = Port(port, self.node_id)

    def create_north_ports(self,number_of_ports):
        for port in range(number_of_ports):
            self.north_ports_dictionary[port] = Port(port, self.node_id)


    def cards_allocation(self):
        card=Card()
        pass


class Server():
    def __init__(self,server_id):
        self.node_id=server_id
        self.port=Port(1,self.node_id)
        self.type="Server"
        self.distance=350
        self.latitude=""
        self.longitude=""
        self.connecting_node_instance_list=[]
        self.network_edge_labels_list=[]
        self.equipment_list=[]


class Pod():
    def __init__(self,pod_count,fat_tree_k_index,p_node):
        self.k=fat_tree_k_index
        self.pod_id=pod_count
        self.aggregation_node_dictionary={}
        self.edge_node_dictionary={}
        self.num_of_servers=pow(int(fat_tree_k_index/2),2)
        self.server_dictionary={}
        self.create_aggregation_nodes(fat_tree_k_index)
        self.create_edge_nodes(fat_tree_k_index)
        self.create_servers()
        self.p_node=p_node


    def create_servers(self):

        for num in range(self.num_of_servers):
            server=Server(num)
            server.pod_id=self.pod_id
            self.server_dictionary[server.node_id]=server

    def create_aggregation_nodes(self,fat_tree_k_index):
        number_of_aggr_nodes=int(fat_tree_k_index/2)
        for node in range(number_of_aggr_nodes):
            #creating k/2 aggregation nodes per pod
            self.aggregation_node_dictionary[node]=Aggregation_Node(self.pod_id,node,fat_tree_k_index)


    def create_edge_nodes(self,fat_tree_k_index):
        number_of_edge_nodes=int(fat_tree_k_index/2)
        for node in range(number_of_edge_nodes):
            self.edge_node_dictionary[node]=Edge_Node(self.pod_id,node,fat_tree_k_index)




class Core_Node(DC_Node):
    def __init__(self,node_name,number_of_ports):
        DC_Node.__init__(self,node_name,number_of_ports)
        self.type="Core_DC_Node"
        #Node.node_id=node_name
        #Node.number_of_ports=number_of_ports
        #self.port_dictionary={}
        self.create_north_ports(1)# only one north port
        self.create_south_ports(self.number_of_ports)
        self.distance=180

class Edge_Node(DC_Node):
    def __init__(self,pod_id,node,fat_tree_k_index):
        number_of_ports=int(fat_tree_k_index/2)
        DC_Node.__init__(self,node,number_of_ports)
        self.type="Edge_DC_Node"
        self.pod_id=pod_id
        self.create_ports()
        self.distance=240



class Aggregation_Node(DC_Node):
    def __init__(self,pod_id,node_name,fat_tree_k_index):
        #number_of_ports = int(fat_tree_k_index / 2)
        DC_Node.__init__(self,node_name, int(fat_tree_k_index / 2))
        self.type="Aggregation_DC_Node"
        self.pod_id=pod_id
        #self.node_id=node
        #self.number_of_ports=int(fat_tree_k_index/2)
        #self.south_ports_dictionary={}
        #self.north_ports_dictionary={}
        #self.north_port={}
        #self.south_port={}
        #self.pod_id=pod_id
        #self.ports_dictionary={}
        self.create_ports()
        self.distance=220


class Client_Node:
    def __init__(self,node_id):
        self.node_id=node_id
        self.type="Client_Node"
        self.direction=0
        self.distance=380
        self.latitude=""
        self.longitude=""
        self.connecting_node_instance_list=[]
        self.network_edge_labels_list = []
        self.equipment_list=[]
        self.port_dictionary={}

#######################################################################################
#######################################################################################


class Probe():
    def __init__(self):
        pass




class Topology():
    def __init__(self):
        self.graph=nx.Graph()
        self.network_node_instance_list=[]
        self.node_numbers=0
        print("topolog vbg")

    def draw_Network(self):
        pass



####################################################################################### display
#######################################################################################

class Network():
    def __init__(self,topology):
        #self.topology=Three_Tier_Topology()
        self.node_list=""
        self.topology=topology#)
        self.topology.draw_Network()

        #self.topology.create_network()
        #self.node_list=self.topology.nodes_list
        #self.edge_list=self.topology.edge_list
        #print(self.edge_list)
        #self.display_instance()

    def display_instance(self,master,le):
        #master=Tk()
        self.information_frame = Information_Frame(master,le)
        self.network_frame = Network_Frame(master, self.topology,self.information_frame)


class Network_Frame():
    def __init__(self,master,topology,information_frame):
        self.information_frame=information_frame
        self.canvas=Canvas(master,height=canvas_height,width=20,bg="steelblue")
        self.canvas.pack(side=LEFT,expand=YES,fill=BOTH)
        self.frame=Frame(master,height=200,bg="orange")
        self.frame.pack(side=RIGHT)
        self.node_label_dictionary={}
        self.text_label_dictionary={}
        self.node_id_dictionary={}
        self.current_label = ""
        self.topology = topology
        self.node_entry=""
        self.entry_window=[]
        self.network_node_instance_list=topology.network_node_instance_list

        self.network_edge_labels={}

        self.edge_entry_point_label_list=[]

        #self.canvas_click_function()

        self.connecting_node_instance=""
        self.show_topology_on_frame()
        self.node_numbers = topology.graph.number_of_nodes()
        self.network_node_instances_labels={}
        self.create_node_labels()

        #print(self.node_numbers)
        #pass

    def canvas_click_function(self):
        # on clicking on canvas reset all the labels on canvas
        self.canvas.bind("<Button-1>",self.reset_entries_and_labels())


    def show_topology_on_frame(self):
        for node in self.network_node_instance_list:
            self.create_node_in_display_from_topology(node)
            #elf.network_node_instances_labels[]#
            ####need to create links


    def create_node_in_display_from_topology(self,node_instance):
        coords=node_instance.canvas_coords
        name=node_instance.name
        attributes=node_type[name]
        new_node_label = self.canvas.create_oval(coords, fill=attributes["color"])

        self.canvas.bind(new_node_label, "<Motion>", self.move_cursor_over_node)

        # node_text = self.canvas.create_text(x, y, text=attributes["name"])
        self.current_label = new_node_label
        self.node_label_dictionary[new_node_label] = name
        # self.text_label_dictionary[new_node_label]=node_text

        self.network_node_instances_labels[new_node_label] = node_instance
        # text_at_previous_node_place=node_text

        #self.identify_nodes_on_position(node_instance,coords)


        #current_node_instance = self.network_node_instances_labels[self.current_label]

        self.canvas.tag_bind(new_node_label, "<Button-1>",
                             self.node_clicked_on_canvas)  # lambda event: self.node_clicked(event)#, new_node_label,text_at_previous_node_place,x,y))
        self.canvas.tag_bind(new_node_label, "<ButtonRelease-1>",
                             self.move_node)  # lambda event : self.move_node(event,new_node_label,text_at_previous_node_place,new_node_instance,attributes))
        self.canvas.update()
        # print("node jfnj")
        self.information_frame.property_selection(self.node_numbers, node_instance)

        #pass

    def create_edge_between_drop_and_positioned_nodes(self,new_node_instance):
        # direction is left
        print("new edge created between ",new_node_instance.node_id," ",self.connecting_node_instance.node_id)

        coords1=new_node_instance.canvas_coords
        coords2=self.connecting_node_instance.canvas_coords
        #x1,y1,x2,y2
        #''
        x1,y1=coords1[2],int(coords1[1] + (coords1[3]-coords1[1]) * 0.8)
        x2,y2=coords2[0],int(coords2[1] + (coords2[3]-coords2[1]) * 0.2)
        #''
        edge_label=self.canvas.create_line(x1,y1,x2,y2)
        new_node_instance.connecting_node_instance_list.append(self.connecting_node_instance)
        self.connecting_node_instance.connecting_node_instance_list.append(new_node_instance)

        self.network_edge_labels[(new_node_instance,self.connecting_node_instance)]=edge_label
        new_node_instance.network_edge_labels_list.append(edge_label)
        self.connecting_node_instance.network_edge_labels_list.append(edge_label)

        self.connecting_node_instance=""
        #pass




    def identify_new_position_to_place_node(self,node_instance,list_of_labels,coords,direction):
        label=list_of_labels[0]
        node_at_canvas_instance=self.network_node_instances_labels[label]
        print(node_at_canvas_instance)
        if direction == "left":
            coords= [(x-inter_node_distance) for x in coords]
            #direction="left"
        else:
            coords= [(x+inter_node_distance) for x in coords]
            #direction="right"
        
            x1, y1, x2, y2 = coords
        try:
            item = self.canvas.find_overlapping(x1, y1, x2, y2)
            coords=self.identify_new_position_to_place_node(node_at_canvas_instance,item,coords,direction)

        except:
            print("node is provided with coordinates")


        return coords


    def identify_nodes_on_position(self,node_instance,event,coords):#coords,x,y):
        x,y= event.x, event.y
        x1,y1,x2,y2=coords
        print("coordinates are",x,y)
        try:

            item = self.canvas.find_overlapping(x1,y1,x2,y2)
            if item !="":
                print("node super imposed on ")
                print("node", self.network_node_instances_labels[item[0]])

                self.connecting_node_instance= self.network_node_instances_labels[item[0]]
                for element in item:
                    print("element label is ",element)
                    #for k,v in self.node_label_dictionary.items():
                    #    print("new",k,v)
                    #for element in item:
                    print("node present here is ",self.node_label_dictionary[element])
            # return  item[0]

            coords=self.identify_new_position_to_place_node(node_instance,item,coords,"left")
            # for the newly created node in network by callback
        except:
            print("isolated node created on canvas")
        return coords
        # print("item is ",item[0])
        #self.current_label = item[0]
        # def move_node(self,event,node_label):
        # entry=Entry(self.canvas,text="node created",width=20)
        # print(event.widget)


    def create_network_node_instance(self,name,coords):

        if name=="Cl":
            node=Client_Node(self.topology.node_numbers)
            self.topology.node_numbers+=1
            self.canvas_coords=coords
            #client
        elif name=="S":
            node= Server(self.topology.node_numbers)
            self.topology.node_numbers += 1
            self.canvas_coords=coords
            #Server
        elif name=="Acc":
            node=Access_Node(self.topology.node_numbers,0)
            self.topology.node_numbers += 1
            self.canvas_coords = coords
            #Access_Network_Node
            #Access_Network_Node
        elif name=="M":
            node=Metro(self.topology.node_numbers,0)
            self.topology.node_numbers += 1
            self.canvas_coords = coords
            #Metro_Network_Node
        elif name=="CN":
            node=Core(self.topology.node_numbers,0)
            self.topology.node_numbers += 1
            self.canvas_coords = coords
            #Core_Network_Node
        elif name=="P":
            node=P_Node(self.topology.node_numbers,0)
            self.topology.node_numbers += 1
            self.canvas_coords = coords
            #P_Network_Node
        elif name=="CD":
            node=Core_Node(self.topology.node_numbers,0)
            self.topology.node_numbers += 1
            self.canvas_coords = coords
            #Core_DC_Node
        elif name=="Edg":
            node=Edge_Node(self.topology.node_numbers,0,0)
            self.topology.node_numbers += 1
            self.canvas_coords = coords
            #Edge_DC_Node
        elif name=="Ag":
            node=Aggregation_Node(self.topology.node_numbers,0,0)
            self.topology.node_numbers += 1
            self.canvas_coords = coords
            #Aggregation_DC_Node
        else :
            print("node not identified")
            node=""
            #new node
        return node

    def create_node_in_graph(self,node,attributes,coords):
        node=self.create_network_node_instance(attributes["name"],coords)
        self.topology.graph.add_node(node)
        return node
    #def move_node(self,event,node):#,circle_id,radius):
        #print(self.canvas.canvasx(event),self.canvas.canvasy(event))
        #self.canvas.coords(circle_id,event.x-radius,event.x+radius,event.y-radius,event.y+radius)
        #self.canvas.move(node,event.x,event.y)
        #circle_id.move()

    def move_cursor_over_node(self,event):
        #message_box=messagebox.showinfor("hi, cursor moved over the node")
        print("cursor moved")


    def create_node_labels(self):
        a=b=50
        print("creating the drag and drop part")

        label=Label(self.canvas,text="Drag and Drop the respective node", width=30)
        label.place(x=20,y=20)
        width=20

        displacement=200
        self.movement_objects={}
        #c=d=50
        for node,attributes in node_type.items():
            #print(node,attributes)
            try:
                radius=int(attributes["radius"])
                label = Label(self.canvas, text=node, width=width)
                label.place(x=a, y=b)
                coords = a + displacement, b, a + displacement + 20, b + 20
                # node_label=IntVar()
                node_label = self.canvas.create_oval(coords, fill=attributes["color"])

            except:
                side=int(attributes["side"])
                label = Label(self.canvas, text=node, width=width)
                label.place(x=a, y=b)
                coords = a + displacement, b, a + displacement + 20, b + 20
                node_label=self.canvas.create_rectangle(coords,fill=attributes["color"])

            #node_label=Button(self.canvas,text=node,bd=2,bg="green")#
            self.canvas.bind(node_label, "<Motion>", self.move_cursor_over_node)

            self.node_label_dictionary[node_label]=node
            self.text_label_dictionary[node_label]=attributes["name"]
            #self.text_label_dictionary[node_label]=node
            #movements=Node_Movements()
            #movements.set_variables(self.canvas,self.node_label_dictionary,self.current_label,self.information_frame)
            self.canvas.tag_bind(node_label,"<Button-1>",self.node_clicked)#partial(self.node_clicked,event,node))#laambda event : self.node_clicked(event,node))#attributes))
            #print(self.current_label)
            #DN=Display_Node(self)#.canvas,self.node_label_dictionary,self.current_label,self.information_frame)
            self.canvas.tag_bind(node_label, "<ButtonRelease-1>",self.create_node_in_display)# lambda event: (event,self.current_label))#, attributes))

            self.canvas.update()
            #self.canvas.tag_bind(node_label,'<ButtonPress-1>',self.create_node)
            # ,command=partial(self.hold,node,attributes))
            #self.canvas.tag_bind(node_label,'<Motion>',lambda event: self.move_circle(event,node_label,attributes["radius"]))#,attributes.color))
            #node_label.pack(side=LEFT)
            #self.node_label_dictionary[node_label]=node
            #self.node_id_dictionary[node_label]=attributes
            b+=30


    def testing_function(self,events    ):
        print("yes function ois wojbnvj")
    def create_links(self):
        pass


    def node_clicked(self,event):
        x,y=event.x,event.y
        item=self.canvas.find_closest(x,y)
        #return  item[0]
        #print("item is ",item[0])
        try:
            self.current_label=item[0]
            #def move_node(self,event,node_label):
            #entry=Entry(self.canvas,text="node created",width=20)
            #print(event.widget)
            current_node_instance=self.network_node_instances_labels[self.current_label]
            self.delete_edge_entry_labels(current_node_instance)
            self.create_edge_entry_point(current_node_instance)
        except:
            print("new node is created")
        self.canvas.update()
        #coords=500,500,530,530
        #self.canvas.create_oval(coords)


    def reset_entries_and_labels(self):

        #self.delete_edge_entry_labels()
        for window in self.entry_window:
            self.canvas.delete(window)
        self.entry_window=[]
        self.information_frame.node_property_display.delete(1.0,END)
        #self.canvas.delete(self.node_entry)

    def node_clicked_on_canvas(self,event):
        #self.delete_all_edge_entry_labels()
        self.reset_entries_and_labels()
        x,y=event.x,event.y
        item=self.canvas.find_closest(x,y)
        #return  item[0]
        #print("item is ",item[0])
        current_node_instance=self.network_node_instances_labels[self.current_label]
        self.delete_edge_entry_labels(current_node_instance)
        #self.create_edge_entry_point(event,current_node_instance)
        self.current_label=item[0]
        #self.current_node_instance=current_node_instance
        #self.node_entry=Entry(self.canvas)
        #window=self.canvas.create_window(x-100,y,window=self.node_entry,height=70,width=150)
        #self.entry_window.append(window)
        node_property="Longitude is "+ str(current_node_instance.longitude), "\nLatitude is "+str(current_node_instance.latitude)
        #self.node_entry.insert(0,node_property)
        self.information_frame.node_property_display.insert(END,node_property)

        self.create_edge_entry_point(current_node_instance)
        self.node_entry.update()
        #print(self.current_label)

        #def move_node(self,event,node_label):
        #entry=Entry(self.canvas,text="node created",width=20)
        #print(event.widget)

        self.canvas.update()
    '''

class Display_Node():
    def __init__(self,network_frame):#canvas,node_label_dictionary,current_label,information_frame):#,canvas,node_label_dictionary,current_label)::
        self.network_frame=network_frame
        self.canvas = network_frame.canvas
        self.node_label_dictionary = network_frame.node_label_dictionary
        #self.current_label = network_frame.current_label
        self.information_frame = network_frame.information_frame
        print("new display object")
    '''

    def create_node_in_display(self, event):#,node_label):  # ,network_frame,event,node_label):#,node,attributes):
        # widget=event.GetEventObject()
        # print(widget)
        self.reset_entries_and_labels()
        time.sleep(0.25)
        node = self.node_label_dictionary[self.current_label]
        #text=self.text_label_dictionary[self.current_label]
        attributes = node_type[node]
        print("new node created on canvas ", node)
        radius = int(attributes["radius"])
        x, y = event.x, event.y


        coords = x - radius, y - radius, x + radius, y + radius
        new_node_instance = self.create_node_in_graph(node, attributes, coords)
        #print(new_node_instance)
        # identifying, if any node is present in the background. for drop  and add edge to work

        coords=self.identify_nodes_on_position(new_node_instance, event,coords)

        new_node_instance.canvas_coords = coords

        new_node_label = self.canvas.create_oval(coords, fill=attributes["color"])
        #self.canvas.bind(new_node_label, "<Motion>", self.move_cursor_over_node)

        try:
            print("trace")
            print(coords,new_node_instance)
            print("tr",type(self.connecting_node_instance),type(new_node_instance))
            if self.connecting_node_instance!="":
                self.create_edge_between_drop_and_positioned_nodes(new_node_instance)
        except:
            print("no edge to add")


        self.create_edge_entry_point(new_node_instance)

        #node_text = self.canvas.create_text(x, y, text=attributes["name"])
        self.current_label=new_node_label
        self.node_label_dictionary[new_node_label]=node# node is mapped to new node label in canvas
        #self.text_label_dictionary[new_node_label]=node_text


        self.network_node_instances_labels[new_node_label]=new_node_instance
        #text_at_previous_node_place=node_text



        current_node_instance = self.network_node_instances_labels[self.current_label]
        # print(self.current_label)

        node_property = "Enter node's longitude\n and latitude, seperated by space"
        self.label_entry = Label(self.canvas,text=node_property)
        window1 = self.canvas.create_window(100, canvas_height-500, window=self.label_entry, height=200, width=200)
        self.entry_window.append(window1)

        node_property=StringVar()
        self.node_entry=Entry(self.canvas,textvariable=node_property)
        window2= self.canvas.create_window(100,canvas_height-300,window=self.node_entry,height=200,width=200)
        self.entry_window.append(window2)
        self.node_entry.bind('<Key-Return>',lambda event : self.set_node_property_by_entry(event,current_node_instance,window1,window2))


        self.canvas.tag_bind(new_node_label, "<Button-1>",self.node_clicked_on_canvas)  # lambda event: self.node_clicked(event)#, new_node_label,text_at_previous_node_place,x,y))
        self.canvas.tag_bind(new_node_label, "<ButtonRelease-1>", self.move_node)  # lambda event : self.move_node(event,new_node_label,text_at_previous_node_place,new_node_instance,attributes))
        self.canvas.update()
        #print("node jfnj")
        self.information_frame.property_selection(self.node_numbers, new_node_instance)
        #elf.node_entry.insert(0,node_property)
        #elf.node_entry.update()
    def set_node_property_by_entry(self,event,current_node_instance,window1,window2):
        node_property = self.node_entry.get()
        #white_space = [" ", ",", "\t", "\n"]
        node_property = node_property.split(" ")
        print(node_property)
        current_node_instance.longitude = node_property[0]
        current_node_instance.latitude = node_property[1]
        self.entry_window.remove(window1)
        self.entry_window.remove(window2)
        self.canvas.delete(window1)
        self.canvas.delete(window2)

        '''
        self.node_with_movements(new_node_label,coords, x, y,node_text)

        # print(attributes)

        # print(node_label)
        # print(tuple(self.canvas.canvasx(event)))
        # print(event.x,event.y,event.widget)
        # coords=event.x-radius,event.y-radius,event.x+radius,event.y+radius
        # print(attributes["color"])
        #
        # self.canvas.bind('<Motion>',self.move_circle)
        # print(self.canvas.coords(node_label))
        # a,b,c,d=self.canvas.coords(node_label)#event.widget)
        # self.canvas.create_oval(a,b,c,d)
        # self.move_circle()
        # self.create_oval()
        # self.canvas.tag_bind()
        # coords=20,20,100,100
        # circle_id=self.canvas.create_oval(coords,fill=attributes["color"])
        # self.canvas.tag_bind(circle_id,'<M otion>',lambda event: self.move_circle(event,circle_id,attributes["radius"]))#,attributes.color))
        # print(node,attributes)
        # create_oval

    def node_with_movements(self,new_node_label,coords,x,y,text_at_previous_node_place):
        time.sleep(0.25)
        
        node=self.node_label_dictionary[new_node_label]
        attributes=node_type[node]
        '''
        #movement = Node_Movements(self.canvas, self.node_label_dictionary, new_node_label, self.information_frame,self.network_frame)
        #movement.set_variables(self.canvas, self.node_label_dictionary, new_node_label, self.information_frame)
        #print("DN",new_node_label)
        #self.canvas.create_text(x, y, text=attributes["name"])

    '''
class Node_Movements():
    def __init__(self,canvas,node_label_dictionary,current_label,information_frame,network_frame):#,canvas,node_label_dictionary,current_label):
        #print("node movements object")
        #self.canvas=""#canvas
        #self.node_label_dictionary=""#node_label_dictionary
        #self.current_label=""#current_label
        #self.information_frame=""
        #def set_variables(self,canvas,node_label_dictionary,current_label,information_frame):
        self.network_frame=network_frame
        self.canvas = canvas
        self.node_label_dictionary = node_label_dictionary
        self.current_label = current_label
        self.information_frame = information_frame

    '''

    def move_node(self,event):#,new_node_label,text,new_node_instance,attributes):
        self.reset_entries_and_labels()
        print("move node method")
        print("current label is ",self.current_label)
        node=self.node_label_dictionary[self.current_label]
        current_node_instance=self.network_node_instances_labels[self.current_label]
        self.network_node_instances_labels.pop(self.current_label)

        self.delete_edge_entry_labels(current_node_instance)

        #text=self.text_label_dictionary[self.current_label]
        attributes=node_type[node]
        self.canvas.delete(self.current_label)
        #self.canvas.delete(text)
        #self.text_label_dictionary.pop(self.current_label)
        self.node_label_dictionary.pop(self.current_label)
        x,y=event.x,event.y
        radius=int(attributes["radius"])
        coords=x-radius,y-radius,x+radius,y+radius

        #updating the coords for the moved node
        current_node_instance.canvas_coords=coords
        new_node_label=self.canvas.create_oval(coords,fill=attributes["color"])

        self.create_edge_entry_point(current_node_instance)

        #self.canvas.bind(new_node_label, "<Motion>", lambda event:self.move_cursor_over_node(event))

        self.network_node_instances_labels[new_node_label]=current_node_instance
        self.node_label_dictionary[new_node_label]=node
        self.current_label=new_node_label
        #self.canvas.bind(new_node_label,"<Motion>",self.move_cursor_over_node)
        #text=self.canvas.create_text(x,y,text=attributes["name"])
        #self.text_label_dictionary[self.current_label]=text
        #print("ffdsf")
        #self.canvas.move(new_node_label,x,y)
        #self.canvas.move(text,x,y)
        #self.canvas.create_text(x,y,text=text)
        self.canvas.tag_bind(new_node_label, "<Button-1>", lambda event: self.node_clicked(event))#, self.current_label,text,x,y))
        #self.canvas.tag_bind(text, "<Button-1>", lambda event: self.node_tinkered(event, new_node_label,text,x,y))
        self.canvas.tag_bind(new_node_label,"<ButtonRelease-1>",self.move_node)#lambda event : self.move_node(event,self.current_label,text.text,new_node_instance,attributes))
        self.move_edges(current_node_instance)
        self.canvas.update()
        #pass

    def create_edge_entry_point(self,current_node_instance):
        print("creating edge entry point")
        x1,y1,x2,y2=current_node_instance.canvas_coords
        #self.delete_all_edge_entry_labels()
        current_node_instance.edge_entry_label=self.canvas.create_oval(x2+3,y2+3,x2+7,y2+7)
        self.canvas.tag_bind(current_node_instance.edge_entry_label,"<ButtonRelease-1>",lambda event:self.create_new_edge_between_existing_nodes(event,current_node_instance))



    def create_new_edge_between_existing_nodes(self,event,current_node_instance):
        x,y=event.x,event.y
        item=self.canvas.find_closest(x,y)
        node_label=item[0]
        connecting_node_instance=self.network_node_instances_labels[node_label]
        print("edge created jere mnds",connecting_node_instance)
        self.create_edge_between_two_nodes(current_node_instance,connecting_node_instance)
        #self.delete_edge_entry_labels()

    def delete_edge_entry_labels(self,current_node_instance):
        try:
            self.canvas.delete(current_node_instance.edge_entry_label)
        except:
            print("no edge entry label existed")

    def find_coordinates_to_plot_edge(self,coords1,coords2):

        a1,b1,a2,b2=coords1
        x1,y1,x2,y2=coords2
        a=(a1+a2)/2
        b=(b1+b2)/2
        x=(x1+x2)/2
        y=(y1+y2)/2

        #try:
        if a <= x and b <= y:
            #m=(b-y)/(a-x)
            return a2,b2,x1,y1
        elif a <= x and b > y:
            return a2,b1,x1,y2

        elif a > x and b <= y:
            return x2,y1,a1,b2
        else:
            return x2,y2,a1,b1
        #print("we reached")

    def create_edge_between_two_nodes(self,current_node_instance, connecting_node_instance):


        try:
            print(current_node_instance,connecting_node_instance)
            print(current_node_instance.canvas_coords)
            print(connecting_node_instance.canvas_coords)
            x1,y1,x2,y2 = self.find_coordinates_to_plot_edge(current_node_instance.canvas_coords,connecting_node_instance.canvas_coords)
            #x1, y1 = coords1[2], int(coords1[1] + (coords1[3] - coords1[1]) * 0.8)
            #x2, y2 = coords2[0], int(coords2[1] + (coords2[3] - coords2[1]) * 0.2)
            edge_label=self.canvas.create_line(x1, y1, x2, y2)
            self.network_edge_labels[(current_node_instance,connecting_node_instance)]=edge_label
            #current_node_instance.network_edge_labels_list.append(edge_label)
            #connecting_node_instance.network_edge_labels_list.append(edge_label)
            if connecting_node_instance not in current_node_instance.connecting_node_instance_list:
                current_node_instance.connecting_node_instance_list.append(connecting_node_instance)
            if current_node_instance not in connecting_node_instance.connecting_node_instance_list:
                connecting_node_instance.connecting_node_instance_list.append(current_node_instance)
        except:
            print("edge is not created between existing nodes")



    def move_edges(self,current_node_instance):
        for connecting_node_instance in current_node_instance.connecting_node_instance_list:
            try:
                edge_label=self.network_edge_labels[(connecting_node_instance,current_node_instance)]
                self.network_edge_labels.pop((connecting_node_instance,current_node_instance))
            except:
                edge_label=self.network_edge_labels[(current_node_instance,connecting_node_instance)]
                self.network_edge_labels.pop((current_node_instance,connecting_node_instance))
            self.canvas.delete(edge_label)
            '''
            for edge_label in current_node_instance.network_edge_labels_list:
                try:
                    current_node_instance.network_edge_labels_list.remove(edge_label)
                    connecting_node_instance.network_edge_labels_list.remove(edge_label)
                    self.canvas.delete(edge_label)
                    print("past edge removed")
                except:
                    print("dangling edge deleted")
            '''
            self.create_edge_between_two_nodes(current_node_instance,connecting_node_instance)
        pass

    def node_tinkered(self,event,new_node_label,text,x,y):
        #print(event.widget)
        print("node ",new_node_label," moved to new place ")
        #self.current_label=self.node_clicked()
        #self.canvas.delete(text_at_previous_node_place)
        #print(node)



class Information_Frame():
    def __init__(self,master,le):
        self.frame=Frame(master,height=1000,width=300,bg="grey")
        self.frame.pack(side=RIGHT)
        self.ne=le.ne

##############


        #self.information_of_action=Entry(self.frame)

        self.node_property_display = Text(self.frame, height=5)
        self.node_property_display.grid(row=0, column=0, columnspan=3)

        self.shortest_path_label = Label(self.frame, text="Shortest Path")
        #self.shortest_path_label.pack(side=TOP)
        self.shortest_path_label.grid(row=1,column=0,sticky=N+E+S+W)
        self.shortest_path_box = Entry(self.frame)
        #self.shortest_path_box.pack(side=TOP)
        self.shortest_path_box.grid(row=1,column=1,columnspan=2,sticky=N+E+S+W)
        #self.information_of_action.pack(side=TOP)

        self.node_entry_label=Label(self.frame,text="Selected Node Attributes")
        self.node_entry_box=Entry(self.frame)
        #self.node_entry_box.pack(side=TOP)
        self.node_entry_label.grid(row=2,column=0,sticky=N+E+S+W)
        self.node_entry_box.grid(row=2,column=1,columnspan=2,sticky=N+E+S+W)

        self.vendor_list_box = Listbox(self.frame, bd=5, exportselection=0, height=50, bg="skyblue1")
        self.equipment_list_box = Listbox(self.frame, bd=5, exportselection=0, height=50, bg="skyblue3")
        self.cards_list_box = Listbox(self.frame, bd=5, exportselection=0, height=50,bg="deepskyblue")
        self.vendor_label=Label(self.frame, text="Vendor List")
        self.equipment_label=Label(self.frame,text="Equipment")
        self.cards_label=Label(self.frame,text="Cards and Prop")
        self.vendor_label.grid(row=3,column=0,pady=5)
        self.equipment_label.grid(row=3,column=1,pady=5)
        self.cards_label.grid(row=3,column=2,pady=5)
        self.vendor_list_box.grid(row=4,column=0,rowspan=20,sticky=N+E+S+W,pady=1)
        self.equipment_list_box.grid(row=4,column=1,rowspan=20,sticky=N+E+S+W,pady=1)
        self.cards_list_box.grid(row=4,column=2,rowspan=20,sticky=N+E+S+W,pady=1)



        self.current_node = ""
        self.current_vendor_name = ""
        self.network_equipments_on_nodes = {}
        self.load_frame()
        # self.shortest_path_label.bind(<<)

        #vendor_label = Label(self.frame, text="Select Equipment for each node")
        #vendor_label.grid(row=2,column=0,columnspan=3,sticky=N+E+S+W)#pack()# dictionary of network equipment loaded per node

        # self.test_text="rttt"
        # self.property_selection()

    def shortest_path(self, node):
        pass

    def equipment_property_load(self, event):
        # print("function traced")
        index = int(event.widget.curselection()[0])
        equipment_name = event.widget.get(index)
        print("Equipment selected", equipment_name, "Equipment instance created for node", self.current_node)
        self.cards_list_box.delete(0,END)
        new_equipment = Equipment()
        self.current_node.equipment_list.append(new_equipment)
        self.network_equipments_on_nodes[self.current_node] = new_equipment
        new_equipment.equipment_properties_dictionary = \
            self.ne.network_equipment_vendor_dictionary[self.current_vendor_name].equipment_dictionary[
                equipment_name].equipment_properties_dictionary

        if self.cards_list_box != "":
           self.cards_list_box.forget()

        #self.cards_list_box = Listbox(self.frame, bd=5, exportselection=0, height=300)
        for k, v in new_equipment.equipment_properties_dictionary.items():
            print("equipment ", k, v)
            self.cards_list_box.insert(END, v)
        #self.cards_list_box.pack(side=LEFT)

        # self.cards_list_box.delete(0,END)
        for prop in new_equipment.equipment_properties_dictionary.values():
            print(prop)
            #    self.equipment_list_box.insert(END, prop)

    def constraints_per_node(self, equipment, properties):
        pass

    def equipment_load(self, event):
        # print("venjgbnbfdjnlgkdmnlbfkn")
        index = int(event.widget.curselection()[0])
        self.equipment_list_box.delete(0, END)
        self.current_vendor_name = event.widget.get(index)
        print("current vendor", self.current_vendor_name)
        #if self.equipment_list_box != "":
        #    self.equipment_list_box.forget()

        #self.equipment_list_box = Listbox(self.frame, bd=5, exportselection=0, height=300, bg="yellow")
        self.equipment_options = self.ne.calling_equipment_names(self.current_vendor_name)
        for items in self.equipment_options:
            print(items)
            self.equipment_list_box.insert(END, items)
        self.equipment_list_box.bind('<<ListboxSelect>>', self.equipment_property_load)
        #self.equipment_list_box.pack(side=LEFT)
        # self.equipment_options = self.ne.calling_equipment_names(vendor_name)
        # self.equipment_list_box.delete(0,END)
        # for eq in self.equipment_options:
        #    self.equipment_list_box.insert(END,eq)

    def load_frame(self):
        self.vendor_options = []
        # test_option=[1,2,3,4,5]
        self.equipment_options = []
        self.cards_option = []
        #self.equipment_list_box = ""
        #self.cards_list_box = ""
        #self.vendor_list_box = Listbox(self.frame, bd=5, exportselection=0, height=300, bg="green")
        # self.equipment_list_box = Listbox(self.frame, bd=5, exportselection=0, height=300, bg="yellow")
        # self.cards_list_box = Listbox(self.frame, bd=5, exportselection=0, height=300)
        # self.vendor_list_box.pack(side=TOP)
        self.vendor_list_box.bind('<<ListboxSelect>>', self.equipment_load)

        # self.vendor_list_box.bind('<<ListboxSelect>>', self.equipment_property_load)
        # self.equipment_list_box.bind('<<ListboxSelect>>', self.equipment_property_load)

        #self.vendor_list_box.pack(side=LEFT)
        # self.equipment_list_box.pack(side=LEFT)
        # self.cards_list_box.pack(side=LEFT)
        # '''
        # vendor_default_name=StringVar()
        # equipment_default_name=StringVar()
        # cards_default_name=StringVar()
        # equipment_default_name.set("equipment_name")
        # cards_default_name.set("cards")
        # vendor_default_name.set("vendor_name")
        # self.equipment_option = OptionMenu(self.frame, equipment_default_name, self.equipment_options)
        # self.cards_option = OptionMenu(self.frame, cards_default_name, self.cards_option)
        # OptionMenu(self.frame,"num",test_option).pack()
        # self.vendor_option = OptionMenu(self.frame, vendor_default_name, self.vendor_options)
        # self.vendor_option.pack()

        # self.equipment_option.pack()
        # self.cards_option.pack()
        # '''

    def property_selection(self, node_id,new_node_instance):
        self.vendor_options = self.ne.calling_vendor_names()
        self.current_node = new_node_instance
        self.vendor_list_box.delete(0, END)
        for ven in self.vendor_options:
            self.vendor_list_box.insert(END, ven)
            # print(self.vendor_options)

############
            #pass


le=Load_Network_Information()
print("network graph ",le.topology.graph)
network=Network(le.topology)
master=Tk()
network.display_instance(master,le)
master.mainloop()
#network.
