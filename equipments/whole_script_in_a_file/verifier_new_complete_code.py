
try:
    import networkx as nx
    import simpy
    import csv
    import time
    from functools import partial
    import random
    import numpy as np
    import re
except ValueError as error:
    print("import error", error.args)
    exit(1)
#
try:
    from tkinter import *
except ImportError:
    from Tkinter import *



portal_width=200
portal_height=200


onboarding_dependency_file=""

data_file = "/home/gnl/Desktop/mankul/verifier/verifier/csv_files/Network Equipments (Updated) - Sheet1.csv"#network_equipments_2_Sheet1.csv"#equipments.csv"
current_deployed_topology_file = "current_topology.csv"  ### this file contain the current deployed topology
#####3 dictionary is in format **** :" ", longitude=" ", latitude="  ",equipment_1=" ",equipment_2=" ", equipment_3=" "...##
### equipment subcategory is card type..
## cad type subcategory is interface type
component_series="Equipment series"
component_name = "Equipment name"#'component name'
#subequipments_supported="subequipments/ports supported"
subequipments_supported="subequipments supported"
subequipment_name="Subequipment"
type="type of equipment/subequipment"

number_of_subeqpmnt="number of interface cards"
subpart="subpart"
subeqpmnt_subpart="sub parts on subequipments"
number_of_subport_per_subeqpmnt="number of subparts per subequipments"
ports= 'ports on equipment/subequipment'
#ports="ports"
throughput = 'Throughput'
line_rate = 'Mpps'
line_cards = 'line cards'
protocol = 'Feature and protocols'
layer_2 = "Layer 2 features"
layer_3 = 'Layer 3 features'
services = 'services'
equipment_vendors = ['cisco', 'juniper', 'nokia', 'ciena', 'huawei', 'fujitsu']  # 'arista',
line_cards_supported = "types of line cards supported"  # in the spreadsheet, line cards supported are seperated by ":"
#interface_name = "Interface name"  # subequipment or card
equipment_properties = [component_series,component_name,subequipments_supported,subpart, subequipment_name,type,number_of_subport_per_subeqpmnt,subeqpmnt_subpart,ports, throughput, line_rate, line_cards, protocol,
                        layer_2, layer_3, services]
#subequipment_name="Interface name"
#subequipments_supported = "Interfaces supported"
mac_addresses_allotted = []
ip_addresses_allotted = []
mac_addresses_allotted_to_node = {}
ip_addresses_allotted_to_node = {}

canvas_height = 1000
canvas_width = 1500
# from topology import Topology

# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from matplotlib.figure import Figure
# from variables import *
from math import *


general_node_type = {"Switch": {"color": "steelblue1", "radius": "12", "name": "Sw", "distance": 0}, \
                     "Router": {"color": "steelblue2", "radius": "13", "name": "R", "distance": 0}, \
                     "Gateway": {"color": "skyblue1", "radius": "14", "name": "G", "distance": 0}, \
                     "Firewall": {"color": "skyblue2", "radius": "14", "name": "F", "distance": 0}, \
                     "DataCenter_InterConnect": {"color": "skyblue3", "radius": "14", "name": "Dci", "distance": 0}}
network_node_type = {
    "Provider Node": {"color": "pink", "radius": "14", "name": "P", "distance": 170}, \
    "Core Node": {"color": "blue", "radius": "14", "name": "CN", "distance": 0}, \
    "Metro Node": {"color": "brown", "radius": "13", "name": "M", "distance": 100}, \
    "Access Node": {"color": "orange", "radius": "12", "name": "Acc", "distance": 350}, \
    "Aggregation_Node": {"color": "lightgreen", "radius": "12", "name": "Ag", "distance": 0}}

data_center_node_type = {"Aggregation_DC_Node": {"color": "coral", "radius": "13", "name": "Agdc", "distance": 290, }, \
                         "Edge DC Node": {"color": "orangered", "radius": "13", "name": "Edg", "distance": 250}, \
                         "Core DC Node": {"color": "cyan", "radius": "14", "name": "CD", "distance": 200}}

sdn_node_type = {"White Box": {"color": "white", "radius": "12", "name": "WB", "distance": 0}, \
                 "Controller": {"color": "lightblue", "length": "50", "breadth": "20", "name": "Cntrlr", "distance": 0}}
client_server_node_type = {"Server": {"color": "salmon", "radius": "10", "name": "S", "distance": 300}, \
                           "Client_Node": {"color": "green", "radius": "10", "name": "Cl", "distance": 380}}

probe_node_type = {"Probe Node": {"color": "yellow", "length": "10", "breadth": "10", "name": "Prb", "distance": 0}}

try:
    node_type = {}
    node_type.update(network_node_type)
    node_type.update(sdn_node_type)
    node_type.update(probe_node_type)
    node_type.update(data_center_node_type)
    node_type.update(client_server_node_type)
    node_type.update(general_node_type)
except:
    print("error in declaration of global variable dictionary items of node type")
core_ring_radius = 30
metro_ring_radius = 25
metro_rings_distance = 100
data_center_distance = 200
access_rings_distance = 350
inter_node_distance = 70
Default="Default"





####################################3
######################################
####################################3
######################################
####################################3
######################################
####################################3
######################################

#from all_dependencies import *


class IP_Domain():
    def __init__(self):
        self.ip_domain_range = ""
        self.ip_addresses_for_hosts = []
        self.ip_address_host_map = {}
        self.subnet_domain_pool = []
        # self.create_ip_host_range(ip_address_of_network,number_of_hosts)

    def create_ip_host_range(self, ip_address_of_network, number_of_hosts):
        host_bits = int(log(number_of_hosts, 2)) + 1
        add_to_host_bits = "".join([str(1) for bits in range(host_bits)])
        # for bits in host_bits:
        #    add_to_host_bits += str(1)
        # add_to_host_bits=
        for ip_no in range(pow(2, host_bits)):
            ip_addr = Ip_Address()
            ip_addr.subnet_mask = (ip_address_of_network.subnet_mask.split('1', 1)[0] + add_to_host_bits).ljust(32, '0')
            # ip_addr.host_id=
            # +str(int(ip_no,2))
            mask = "".join([ord(a) and ord(b) for a, b in
                            zip(ip_address_of_network.ip_address, ip_address_of_network.subnet_mask)])
            ip_addr.ip_address = (mask + bin(ip_no)[2:]).ljust(32, "0")
            self.subnet_domain_pool.append(ip_addr)
            ip_address_of_network.subnet_addresses_pool = []


class Ip_Address():
    def __init__(self, parent_ip_address):
        self.type = ""
        self.parent_ip_address = parent_ip_address
        self.ip_address = ""
        self.host_id = ""
        self.subnet_mask = ""
        self.gateway_id = ""
        self.domain_id = ""
        self.subnet_addresses_pool = []
        self.subnet_distributed_addresses = []
        self.ip_domain = IP_Domain()

    def dafault_ip_address(self):
        if self.parent_ip_address == "":
            self.create_ip_address()
        else:
            try:
                self.ip_address = self.parent_ip_address.subnet_addresses_pool.pop(0)
            except:
                self.create_ip_address()

    def create_ip_address(self):
        i = 0
        while (i < 100000):
            b1 = bin(random.randint(0, 15))[2:]
            b1 = b1.rjust(24, "0")
            address = ("1010" + b1).rjust(32, "0")
            if address not in ip_addresses_allotted:
                ip_addresses_allotted.append(address)
                self.ip_address = address
                print("ip address created ", address)
                break
            i += 1
            # self.ip_address="".join(['0' for i in range(32)])


###############################################################################################
###############################################################################################



class Traffic():
    def __init__(self):
        pass


############################################################################################
############################################################################################


class MAC_Address():
    def __init__(self):
        self.mac_address = ""
        # self.mac_address_alotted=[]
        # self.create_mac_address_id()

    def create_mac_address_id(self):
        # for i in range(48)
        while (True):
            address = ""
            for i in range(6):
                # b1=b2=""
                b1 = bin(random.randint(0, 15))[2:]
                b2 = bin(random.randint(0, 15))[2:]
                b1 = b1.ljust(4, "0")
                b2 = b2.ljust(4, "0")
                # string=""
                # for i in range(4-len(b1)):
                #    string+=str(0)
                # b1+=string
                # string = ""
                # for i in range(4 - len(b2)):
                #    string += str(0)
                # b2+=string
                slot = b1 + b2  # +":"
                address += slot

            if address not in mac_addresses_allotted:
                mac_addresses_allotted.append(address)
                self.mac_address = address
                break

####################################3
######################################
####################################3
######################################
####################################3
######################################
####################################3
######################################
####################################3
######################################
#from all_dependencies import *
#import re

class Network_Equipments:
    def __init__(self):
        self.network_equipment_vendor_dictionary = {}
        self.per_vendors_equipments_list = []
        # self.vendor_dictionary = {}
        # for items in equipment_properties:
        #    print items

    def loading_equipments_list(
            self):  # equipment list is loaded in vendor_instance's variable component_list dictionary with all names in list equipment_properties
        self.dictionary_list = []

        dictionary_equipments = []
        data = csv.DictReader(open(data_file, 'r'))
        for row in data:
            self.dictionary_list.append(row)  # row is an open dictionary object

        for items in self.dictionary_list:
            flag_for_vendor = False

            for vendor_name in equipment_vendors:
                if vendor_name.lower() in items[component_series].lower():
                    flag_for_vendor = True
                    if vendor_name not in self.network_equipment_vendor_dictionary.keys():
                        vendor_instance = Vendor()
                        self.network_equipment_vendor_dictionary[vendor_name] = vendor_instance
                        self.per_vendors_equipments_list.append(vendor_instance)

                    else:
                        vendor_instance = self.network_equipment_vendor_dictionary[vendor_name]
            # loading equipments for all known vendors.
            if items[component_name] != "":
                # for vendor_name in equipment_vendors:
                '''
                    if vendor_name.lower() in (items[component_name]).lower():
                        flag_for_vendor = True
                        if vendor_name not in self.network_equipment_vendor_dictionary:
                            ####
                            ####Creating new vendor instance for new vendor in list....... vendor instances are in nw_eq_vndr_lst
                            ####
                            vendor_instance = Vendor()
                            self.network_equipment_vendor_dictionary[vendor_name] = vendor_instance
                            self.per_vendors_equipments_list.append(vendor_instance)

                        else:
                            ####
                            ####adding new equipment in list information to vendor instance
                            ####
                            vendor_instance = self.network_equipment_vendor_dictionary[vendor_name]
                        # print(vendor_instance.func())
                '''
                if items[component_name] not in vendor_instance.equipment_names_list:  # to avoid reloading same properties if present in csv file
                    vendor_instance.equipment_names_list.append(items[component_name])
                    new_equipment = Equipment()
                    #if items[component_name] == "ASR 1004":
                    #    print(items[component_name],items[subequipments_supported])

                    try:
                        supported_subequipments_list = new_equipment.identify_all_subequipments(items)
                        # for sub_eq in sub_equipment_list:
                        #    if sub_eq not in vendor_instance.subequipment_list:
                        #        vendor_instance.subequipment_list.append(sub_eq)
                    except:
                        print("no subequipments, only builtin components")
                        supported_subequipments_list=Default

                    vendor_instance.subeqpmnts_per_eqpmnts_dictionary[new_equipment] = supported_subequipments_list
                    new_equipment.equipment_properties(items)
                    vendor_instance.equipment_dictionary[items[component_name]] = new_equipment
                    new_dictionary={}
                    new_dictionary[subequipments_supported]=supported_subequipments_list
                    new_dictionary[protocol]=items[protocol]
                    new_dictionary[services]=items[services]
                    new_dictionary[ports]=items[ports]
                    new_dictionary[type] = items[type]
                    vendor_instance.all_eqpmnt_subeqpmnt_and_parts_dictionary[items[component_name]]=new_dictionary
                '''
                else:
                    # if items[component_name] not in vendor_instance.equipment_dictionary.keys():
                    new_equipment = SubEquipment()  # Equipment()
                    # vendor_instance.equipment_dictionary[items[card_name]]= new_equipment
                    new_equipment.equipment_properties(items)
                    vendor_instance.equipment_dictionary[items[component_name]] = new_equipment
                    # print(vendor_instance.equipment_dictionary .values())


                if flag_for_vendor == False:
                    print("vendor name not identified for ", items[component_name])
                '''

            elif items[subequipment_name] != "":
                if items[subequipment_name] not in vendor_instance.subequipment_list:
                    subequipment = SubEquipment()
                    vendor_instance.subequipment_list.append(items[subequipment_name])
                    vendor_instance.subequipment_dictionary[items[subequipment_name]] = subequipment
                    subequipment.subequipment_properties(items)

                    #
                    try:
                        subpart_dictionary=subequipment.identify_all_subparts(items)
                    except:
                        print("error in reading subparts on subequipments")
                        subpart_dictionary=Default
                    new_dictionary={}
                    new_dictionary[subeqpmnt_subpart]=subpart_dictionary
                    new_dictionary[protocol]=items[protocol]
                    new_dictionary[services]=items[services]
                    new_dictionary[ports]=items[ports]
                    new_dictionary[type] = items[type]
                    vendor_instance.all_eqpmnt_subeqpmnt_and_parts_dictionary[items[subequipment_name]]=new_dictionary


            elif items[subpart] != "":
                if items[subpart] not in vendor_instance.subpart_list:
                    subpart_instance = Subpart()
                    vendor_instance.subpart_list.append(items[subeqpmnt_subpart])
                    vendor_instance.subpart_dictionary[items[subeqpmnt_subpart]] = subpart_instance
                    subpart_instance.subpart_properties(items)
                    new_dictionary={}
                    new_dictionary[protocol]=items[protocol]
                    new_dictionary[services]=items[services]
                    new_dictionary[ports]=items[ports]
                    new_dictionary[type]=items[type]
                    vendor_instance.all_eqpmnt_subeqpmnt_and_parts_dictionary[items[subpart]]=new_dictionary


            else:
                print("Empty line")

    def calling_vendor_names(self):
        # forwarding json  file to app to gorward it to the web page
        return equipment_vendors

    def calling_equipment_names(self, vendor_name):
        return self.network_equipment_vendor_dictionary[vendor_name].returning_equipment_names()


###each time new instance created, vendor instance is added to network_equipment_vendor_dictionary dictionary of ne

class Vendor():
    # equipment_dictionary={}
    # component_property={}
    def __init__(self):
        self.equipment_series_list = []
        self.equipment_dictionary = {}
        self.component_list = {}
        self.component_properties_list = []
        self.equipment_names_list = []
        self.subequipment_list = []
        self.subpart_dictionary = {}
        self.subpart_list = []
        self.subequipment_dictionary = {}
        self.subeqpmnts_per_eqpmnts_dictionary = {}
        self.all_eqpmnt_subeqpmnt_and_parts_dictionary={}
        # use this sub equipment list to put the sub equipments to the equipment to be selected
        # print("equipment per vendor created")

    def returning_equipment_names(self):
        print("returning equipment names for specific vendor")
        return self.equipment_names_list


class Equipment_Series():
    def __init__(self):
        self.parts_list = []


class Equipment():
    # equipment_properties_dictionary={}
    def __init__(self):
        self.name = ""
        self.id = ""
        self.node_subequipment_dictionary = {}
        self.equipment_properties_dictionary = {}
        self.subequipment_list = []
        # self.card_list=[]

    def equipment_properties(self, items):

        for element in items:
            self.equipment_properties_dictionary[element] = items[element]
        try:
            if items[subequipment_name] == "":
                self.equipment_properties_dictionary[subequipment_name] = 'Default'
        except:
            print("include subequipment_name in csv file")

    def identify_all_ports(self):
        try:
            self.equipment_properties_dictionary[ports]
        except:
            print("Selected equipment has not mentioned number and types of ports in respective datasheet")

    def identify_all_subequipments(self,items):
        try:
            if items[subequipments_supported] != "":
                # self.subequipments_list_function(self.equipment_properties_dictionary[line_cards])
                print(subequipments_supported)
                self.identify_supported_subequipments_list_function(items[subequipments_supported])#self.equipment_properties_dictionary[subequipments_supported])
                return self.subequipment_list
            else:
                print("no data for cards")
                return Default

        except:
            print("error in reading equipment's subequipments")

    # on selecting sub equipment add this to equipment properties. on selection of cards from the gui
    def set_equipment_properties(self, items):
        pass



    def find_number_of_iteration(self,temp_string):
        regex_number_of_iterations=re.compile(r"^\s*[0-9]+\s*[X,x]\s*")
        temp = re.match(regex_number_of_iterations, temp_string)
        if temp is None:
            num_iteration = 1
        else:
            temp = temp.group()
            temp = re.match("[0-9]+", temp)
            temp = temp.group()
            num_iteration = int(temp)

        return num_iteration

    def identify_supported_subequipments_list_function(self, subequipments):
        subequipment_list = []
        subequipment_slot_regex=re.compile(r"\s*\$\s*|\s*\n\s*")
        subequipments_per_slot_regex=re.compile(r"\s*or\s+")

        print(subequipments)
        for subequipment_slot_option in re.split(subequipment_slot_regex,subequipments):#subequipments.split("\n"):#
            if subequipment_slot_option != "":
                temp_string = subequipment_slot_option

                num_iteration=self.find_number_of_iteration(temp_string)

                print(subequipment_slot_option)
                for subequipment_per_slot in re.split(subequipments_per_slot_regex,subequipment_slot_option):
                    #subequipment_per_slot=re.search(r"\w.*",subequipment_per_slot).group()
                    for num in range(num_iteration):
                        subequipment_list.append(subequipment_per_slot)

        ##### filling the subequipment_list for use while creating the device
        self.subequipment_list = subequipment_list


########################################################################################
########################################################################################



class Subpart():
    def __init__(self):
        self.name = ""
        self.id = ""
        self.port_instance_list = []
        self.subpart_properties_dictionary = {}

    def subpart_properties(self, items):
        for element in items:
            self.subpart_properties_dictionary[element] = items[element]


class SubEquipment(Equipment):
    def __init__(self):
        Equipment.__init__(self)
        self.name = ""
        self.id = ""
        self.port_instance_list = []
        self.subpart_instance_list = []
        self.subparts_list = []
        # self.subparts_dictionary={}
        self.subequipment_properties_dictionary = {}

    def subequipment_properties(self, items):
        for element in items:
            self.subequipment_properties_dictionary[element] = items[element]
            # try:
            #    if items[subequipment_name] == "":
            #        self.equipment_properties_dictionary[subequipment_name] = 'Default'
            # except:
            #    print("include interface name in csv file")

    def identify_all_ports(self):
        try:
            self.equipment_properties_dictionary[ports]
        except:
            print("Selected equipment has not mentioned number and types of ports in respective datasheet")

    def identify_all_subparts(self,items):
        try:


            if items[subeqpmnt_subpart] != "":
                # self.subequipments_list_function(self.equipment_properties_dictionary[line_cards])
                print("items[]",items[subeqpmnt_subpart])
                return self.subparts_list_function(items[subeqpmnt_subpart])#self.subequipment_properties_dictionary[subequipments_supported])
                # return self.subequipment_list
            else:
                return Default
                print("no data for subparts")

        except:
            print("error in reading subeqpmnt subparts")

    def subparts_list_function(self, subparts):
        subparts_list = []
        delimeter = [",", "+", "\t", "\n"]
        for words in subparts.split("\n"):
            subparts_list.append(words)
        # return subequipment_list
        ##### filling the subequipment_list for use while creating the device
        self.subparts_list = subparts_list
        # for eq in words.split(":"):
        # card=Card()
        # card_list.append(card)

    def set_subequipment(self, subequipment_items, topology, node_instance):
        # ubequipment_items[ports] to be used
        ports_size_dictionary = {}
        ports_size_dictionary[1] = 5
        ports_size_dictionary[10] = 5
        ports_size_dictionary[100] = 5
        self.initialize_subequipment_property(ports_size_dictionary, topology, node_instance)

    # initilialize this on selecting the module from the gui
    def initialize_subequipment_property(self, ports_size_dictionary, topology, node_instance):
        node_instance.subequipment_dictionary_of_port_lists[self] = []
        for port_size, number_of_ports in ports_size_dictionary.items():
            # create port
            for port in range(number_of_ports):
                port_instance = Port(topology.port_number, port_size, self, node_instance)
                self.port_instance_list.append(port_instance)
                node_instance.subequipment_dictionary_of_port_lists[self].append(port_instance)
                topology.port_number += 1



########################################
########################################
########################################
########################################
########################################
########################################
########################################
########################################
########################################
########################################
########################################
########################################
########################################
########################################
########################################
########################################

#from all_dependencies import *
#from topology import *
#from equipments import *

class Information_Frame():
    def __init__(self, canvas, le, simulation, topology):
        self.simulation = simulation
        self.ne = le.ne
        self.topology = topology
        self.current_node = ""
        self.current_vendor_name = ""
        self.network_equipments_on_nodes = {}
        self.canvas=canvas

        self.all_entries_list = []
        self.subpart_window_list = []
        self.selected_subequipment_index_list = []
        self.info_frame_flag=0

        self.frame = Frame(self.canvas, padx=2, pady=2)  # , bg="grey")
        self.create_info_frame_widgets()

        #self.create_info_frame()
        #self.create_info_frame_widgets()


    def create_info_frame(self):
        print("flag uis :",self.info_frame_flag)
        if self.info_frame_flag == 0:
            self.window_for_information_frame = self.canvas.create_window(125, 600, window=self.frame, width=250, height=500)
            self.show_info_frame_widgets()
            self.info_frame_flag=1

        #else:
        #    self.window_for_information_frame = self.canvas.create_window(125, 600, window=self.frame, width=250, height=500)
        #

    def show_info_frame_widgets(self):
        self.information_frame_label.grid(row=0, column=0, columnspan=2, sticky=N + E + S + W)
        row_span = 0
        self.node_name_label.grid(row=row_span + 1, column=0, sticky=N + E + S + W)
        self.node_name_entry.grid(row=row_span + 1, column=1, sticky=N + E + S + W)
        self.node_id_label.grid(row=row_span + 2, column=0, sticky=N + E + S + W)
        self.node_id_entry.grid(row=row_span + 2, column=1, sticky=N + E + S + W)
        self.mac_address_label.grid(row=row_span + 3, column=0, sticky=N + E + S + W)
        self.mac_address_entry.grid(row=row_span + 3, column=1, sticky=N + E + S + W)
        self.ip_address_label.grid(row=row_span + 4, column=0, sticky=N + E + S + W)
        self.ip_address_entry.grid(row=row_span + 4, column=1, sticky=N + E + S + W)
        row_span += 4  # 3
        self.latitude_label.grid(row=row_span + 1, column=0, sticky=N + E + S + W)
        self.latitude_entry.grid(row=row_span + 1, column=1, sticky=N + E + S + W)
        self.longitude_label.grid(row=row_span + 2, column=0, sticky=N + E + S + W)
        self.longitude_entry.grid(row=row_span + 2, column=1, sticky=N + E + S + W)
        self.first_node_label.grid(row=row_span + 3, column=0, sticky=N + E + S + W)
        self.node_A.grid(row=row_span + 3, column=1, sticky=N + E + S + W)
        self.second_node_label.grid(row=row_span + 4, column=0, sticky=N + E + S + W)
        self.node_B.grid(row=row_span + 4, column=1, sticky=N + E + S + W)
        self.node_entry_label.grid(row=row_span + 5, column=0, sticky=N + E + S + W)
        self.node_entry_box.grid(row=row_span + 5, column=1, sticky=N + E + S + W)

        self.network_prop_analysis_label.grid(row=row_span + 6, column=0, columnspan=2, sticky=N + E + S + W)
        self.shortest_path_button.grid(row=row_span + 7, column=0, sticky=N + E + S + W)
        self.shortest_path_box.grid(row=row_span + 7, column=1, sticky=N + E + S + W)
        self.two_node_simulation_button.grid(row=row_span + 8, column=0, columnspan=2, sticky=N + E + S + W)
        self.all_node_simulation_button.grid(row=row_span + 9, column=0, columnspan=2, sticky=N + E + S + W)

        row_span += 9

        self.display_subequipment_label.grid(row=row_span + 1, column=0, columnspan=2, sticky=N + E + S + W, pady=1)
        self.display_properties_subequipment_box.grid(row=row_span + 2, column=0, columnspan=2, rowspan=1,
                                                  sticky=N + E + S + W, pady=1)

    def create_info_frame_widgets(self):
        button_color = "sienna1"  # "thistle1"
        label_color = "khaki1"
        text_bg_color = "bisque2"
        info_label_color = "green2"
        # self.node_property_display = Text(self.frame,height=5,width=1 ,bg=text_bg_color)
        # self.node_property_display.grid(row=0, column=0, columnspan=2, sticky=N+S+E+W, padx=1, pady=1)
        # self.node_property_display.insert(1.0, "Node Attributes")
        self.two_node_simulation_button = Button(self.frame, bg=button_color,
                                                 text="Start traffic between nodes A and B",
                                                 command=lambda: self.simulation.start_ip_traffic_between_two_nodes(
                                                     self, self.topology))
        self.all_node_simulation_button = Button(self.frame, bg=button_color, text="Start traffic beteen all nodes",
                                                 command=lambda: self.simulation.start_all_nodes_ip_traffic(self,
                                                                                                            topology))
        self.information_frame_label = Label(self.frame, text="Node Info", bg=info_label_color)

        self.node_name_label = Label(self.frame, text="Node Name", bg=label_color)
        self.node_name_entry = Entry(self.frame, bg=text_bg_color)
        self.all_entries_list.append(self.node_name_entry)
        self.node_id_label = Label(self.frame, text="Node ID", bg=label_color)
        self.node_id_entry = Entry(self.frame, bg=text_bg_color)
        self.all_entries_list.append(self.node_id_entry)
        self.mac_address_label = Label(self.frame, text="Mac Address", bg=label_color)
        self.mac_address_entry = Entry(self.frame, bg=text_bg_color)
        self.all_entries_list.append(self.mac_address_entry)
        self.ip_address_label = Label(self.frame, text="IP Address", bg=label_color)
        self.ip_address_entry = Entry(self.frame, bg=text_bg_color)
        self.all_entries_list.append(self.ip_address_entry)
        self.latitude_label = Label(self.frame, text="Latitude", bg=label_color)
        self.longitude_label = Label(self.frame, text="Longitude", bg=label_color)
        self.latitude_entry = Entry(self.frame, bg=text_bg_color)
        self.longitude_entry = Entry(self.frame, bg=text_bg_color)
        self.all_entries_list.append(self.latitude_entry)
        self.all_entries_list.append(self.longitude_entry)
        # self.all_entries_list.append(self.node_name_entry)
        # self.all_entries_list.append(self.node_id_entry)

        self.first_node_label = Label(self.frame, text="Node A", bg=label_color)
        self.second_node_label = Label(self.frame, text="Node B", bg=label_color)
        self.node_A = Entry(self.frame, bg=text_bg_color)
        self.node_B = Entry(self.frame, bg=text_bg_color)
        self.shortest_path_box = Entry(self.frame, bg=text_bg_color)
        # self.all_entries_list.append(self.node_A)
        # self.all_entries_list.append(self.node_B)
        self.network_prop_analysis_label = Label(self.frame, text="Probes and Analysis", bg=info_label_color)
        self.shortest_path_button = Button(self.frame, bg=button_color, text="Shortest Path",
                                           command=self.shortest_path)
        # self.shortest_path_button.pack(side=TOP)
        # self.all_entries_list.append(self.shortest_path_box)
        # self.shortest_path_box.pack(side=TOP)
        # self.information_of_action.pack(side=TOP)

        self.node_entry_label = Label(self.frame, text="Node Attributes", bg=label_color)
        self.node_entry_box = Entry(self.frame, bg=text_bg_color)
        # self.all_entries_list.append(self.node_entry_box)
        # self.node_entry_box.pack(side=TOP)+
        self.display_equipment_label = Label(self.frame, text="Equipment Attributes")
        self.display_subequipment_label = Label(self.frame, text="Subequipment Attributes", bg=info_label_color)
        self.display_properties_equipment_box = Text(self.frame)
        self.display_properties_subequipment_box = Text(self.frame,height=100,width=25, bg=text_bg_color)
        # self.display_equipment_label.grid(row=row_span+9,column=0,columnspan=1,sticky=N+E+S+W,pady=1)
        # self.display_properties_equipment_box.grid(row=row_span+1,column=0,columnspan=1,rowspan=5,sticky=N+E+S+W,pady=1)

    def hide_info_frame(self):
        self.canvas.delete(self.window_for_information_frame)
        self.info_frame_flag=0

    def remove_info_frame(self):
        self.frame.destroy()
        self.info_frame_flag=0

    def set_node_property_from_input(self, node_property, current_node_instance):
        pass
        # "Enter node's\na)longitude, \nb)latitude, \nc)Ip_address, \nd)Number of ports \nseperated by spaces respectively"

        # self.label_entry = Label(self.frame, text=node_property)
        # window1 = self.canvas.create_window(100, canvas_height - 500, window=self.label_entry, height=200, width=200)
        # self.entry_window.append(window1)
        # node_property = StringVar()
        # self.node_entry = Entry(self.canvas, textvariable=node_property)
        # window2 = self.canvas.create_window(100, canvas_height - 300, window=self.node_entry, height=200, width=200)
        # self.entry_window.append(window2)
        # self.node_entry.bind('<Key-Return>',
        #                             lambda event: self.set_node_property_by_entry(event, current_node_instance, window1,
        #                                                                   window2))

    def create_canvas_window(self, x, y, canvas, node_instance):  # ,node_id,list_box):
        self.window_frame = Frame(canvas)
        self.window_box_id = canvas.create_window(x - 200, y + 50, window=self.window_frame, width=200, height=300)

    def remove_canvas_window_objects(self, list_box, label):
        list_box.destroy()
        label.destroy()

    def remove_canvas_window(self, canvas):  # ,node_instance):#,list_box):
        # self.remove_list_box(list_box)
        canvas.delete(self.window_box_id)
        self.window_frame.destroy()

    def reset_subequipment_property_box(self):
        self.display_properties_subequipment_box.delete(1.0, END)

    def reset_equipment_property_box(self):
        self.display_properties_equipment_box.delete(0, END)

    def create_vendor_list_box(self, event, node_label, canvas, node_instance):
        self.current_node_instance=node_instance
        self.create_canvas_window(event.x, event.y, canvas, node_instance)  # ,node_label,self.vendor_list_box)
        #self.vendor_yscrollbar = Scrollbar(self.window_frame, orient=VERTICAL)
        #self.vendor_xscrollbar = Scrollbar(self.window_frame, orient=HORIZONTAL)
        self.vendor_label = Label(self.window_frame, text="Vendor List")
        self.vendor_list_box = Listbox(self.window_frame, bd=5, cursor="hand2",exportselection=0, width=20, height=50, bg="skyblue1")
        #self.vendor_list_box.config(xscrollcommand=self.vendor_xscrollbar.set,yscrollcommand=self.vendor_yscrollbar.set)
        self.vendor_label.pack(side=TOP)
        self.vendor_list_box.pack(side=TOP)

        #self.vendor_xscrollbar.pack(side=BOTTOM, fill=X)
        #self.vendor_yscrollbar.pack(side=RIGHT,fill=Y)
        #self.vendor_xscrollbar.config(command=self.vendor_list_box.xview)
        #self.vendor_yscrollbar.config(command=self.vendor_list_box.yview)
        self.vendor_list_box.bind('<<ListboxSelect>>',
                                  lambda event: self.equipment_load(event, canvas, event.x, event.y, node_instance))

    def create_equipment_list_box(self, canvas, x, y, node_instance):  # ,node_label):
        print("equipment list  box ")
        # self.remove_canvas_window(canvas, self.vendor_list_box)
        self.remove_canvas_window_objects(self.vendor_list_box, self.vendor_label)
        # self.create_canvas_window(x,y,canvas)#, node_label, self.equipment_list_box)
        self.equipment_label = Label(self.window_frame, text="Equipment")
        #yscrollbar = Scrollbar(self.window_frame, orient=VERTICAL)
        #xscrollbar = Scrollbar(self.window_frame, orient=HORIZONTAL)
        self.equipment_list_box = Listbox(self.window_frame, bd=5,cursor="hand2" ,exportselection=0, width=20, height=50,
                                          bg="skyblue3")
        #self.equipment_list_box.config(xscrollcommand=xscrollbar.set,yscrollcommand=yscrollbar.set)

        self.equipment_label.pack(side=TOP)
        #xscrollbar.pack(side=BOTTOM, fill=X)
        #yscrollbar.pack(side=RIGHT,fill=Y)
        #xscrollbar.config(command=self.equipment_list_box.xview)
        #yscrollbar.config(command=self.equipment_list_box.yview)
        self.equipment_list_box.pack()
        #self.equipment_list_box.pack()
        self.equipment_list_box.bind("<<ListboxSelect>>",
                                     lambda event: self.equipment_property_load(event, canvas, x, y, node_instance))


    def create_subequipment_list_box(self, canvas, x, y, node_instance,equipment_name):  # ,node_label):
        # self.remove_canvas_window(canvas, self.equipment_list_box)
        self.remove_canvas_window_objects(self.equipment_list_box, self.equipment_label)
        #yscrollbar = Scrollbar(self.window_frame, orient=VERTICAL)
        #xscrollbar = Scrollbar(self.window_frame, orient=HORIZONTAL)
        # self.create_canvas_window(x,y,canvas)#,node_label,self.subequipment_list_box)
        self.subequipment_list_box = Listbox(self.window_frame, cursor="hand2",selectmode=MULTIPLE, bd=5, exportselection=0, width=20,
                                             height=15, bg="deepskyblue")
        #self.subequipment_list_box.config(xscrollcommand=xscrollbar.set,yscrollcommand=yscrollbar.set)
        self.subequipment_label = Label(self.window_frame, text="Subequipments")
        self.subequipment_label.pack()
        self.subequipment_list_box.pack()

        self.subequipment_select_button=Button(self.window_frame,text="Click",command= lambda: self.load_subeqpmnt_property_window_box(canvas,equipment_name))#,node_instance))

        self.subequipment_select_button.pack(side="bottom")
        self.subequipment_list_box.bind('<<ListboxSelect>>',lambda event: self.display_subparts_of_respective_subequipments(event, canvas, node_instance, x,y))

    def create_subpart_window(self, canvas, x, y, node_instance):
        subpart_frame=Frame(canvas)
        self.subpart_window=canvas.create_window(x-100,y-20,window=subpart_frame,width=x-90,height=y+50)
        self.subpart_list_box=Listbox(subpart_frame, selectmode=MULTIPLE, bd=5, exportselection=0, width=10,
                                             height=15, bg="deepskyblue")
        self.subpart_select_button=Button(subpart_frame,text="->",command=lambda : self.selecting_multiple_subparts(self.subpart_list_box,canvas,node_instance))
        self.subpart_list_box.pack()
        self.subpart_select_button.pack(side="bottom")

        #self.subpart_list_box.bind("<<ListboxSelect>>",self.add_subpart_to_equipment)
        #self.subpart_list_box.bind('<<ListboxSelect', lambda event: self.selecting_multiple_subparts(event,canvas,node_instance))

    def selecting_multiple_subparts(self,widget,canvas,node_instance):
        indices=widget.curselection()
        print("multiple subparts selected")

        for index in indices:
            subpart=widget.get(index)
            print(subpart)
            self.add_subpart_to_equipment(subpart)
        canvas.delete(self.subpart_window)

    def add_subpart_to_equipment(self,subpart):
        subpart_instance=Subpart()
        subpart_instance.name=subpart
        subpart_instance.subpart_properties_dictionary=self.current_vendor_instance.all_eqpmnt_subeqpmnt_and_parts_dictionary[subpart]
        ports = self.current_vendor_instance.all_eqpmnt_subeqpmnt_and_parts_dictionary[subpart][ports]
        subequipment = ""
        self.current_node_instance.update_ports(ports,subpart,subequipment,self.new_equipment)
        self.reset_subequipment_property_box()
        port=self.current_node_instance.port_list
        self.display_properties_subequipment_box.insert(END, "Ports" + " :-\n" + port + "\n")

    def remove_list_box(self, list_box):
        list_box.destroy()

    def shortest_path(self):
        print("shortest path ", self.node_A.get())
        for key, value in self.topology.node_instance_dictionary_by_node_id.items():
            print("key value is ", key, "\t", value)
        node_instance_1 = self.topology.node_instance_dictionary_by_node_id[int(self.node_A.get())]
        node_instance_2 = self.topology.node_instance_dictionary_by_node_id[int(self.node_B.get())]
        shortest_path = self.topology.find_shortest_path(node_instance_1, node_instance_2)
        self.set_shortest_path_box_window(shortest_path)

    def set_shortest_path_box_window(self, shortest_path):
        print("shortest path entry box cleared")
        self.shortest_path_box.delete(0, END)
        self.shortest_path_box.insert(END, str(shortest_path))

    def equipment_property_load(self, event, canvas, x, y, node_instance):
        # print("function traced")
        widget = event.widget
        index = int(widget.curselection()[0])
        equipment_name = widget.get(index)
        print("Equipment selected", equipment_name, "Equipment instance created for node", self.current_node)
        try:
            self.subequipment_list_box.delete(0, END)
        except:
            print("new subequipment list")
        self.new_equipment = Equipment()
        self.new_equipment.name=equipment_name
        # self.current_node.subequipment_list.append(new_equipment)
        self.network_equipments_on_nodes[self.current_node] = self.new_equipment
        self.new_equipment.equipment_properties_dictionary = \
            self.ne.network_equipment_vendor_dictionary[self.current_vendor_name].equipment_dictionary[
                equipment_name].equipment_properties_dictionary
        self.subequipment_window_load( canvas, x, y, node_instance,equipment_name)

    def subequipment_window_load(self,  canvas, x, y, node_instance,equipment_name):
        try:
            self.subequipment_list_box.delete(0, END)
        except:
            print("not new subequipment box")
        self.create_subequipment_list_box(canvas, x, y, node_instance,equipment_name)

        print("curent vendor is   ",self.current_vendor_instance)
        subequipment_supported=self.current_vendor_instance.all_eqpmnt_subeqpmnt_and_parts_dictionary[equipment_name][subequipments_supported]
        if subequipment_supported == Default:
            self.subequipment_list_box.insert(END,Default)

        else:
            for subeqpmnt_name in subequipment_supported:
                print(subeqpmnt_name)
                self.subequipment_list_box.insert(END,subeqpmnt_name)

            #    if self.current_vendor_instance.all_eqpmnt_subeqpmnt_and_parts_dictionary[subeqpmnt_name][subeqpmnt_subpart] != Default:
            #        self.subpart_window_list.append(self)
        # insert various cards names. default are the values
        '''
        if new_equipment.equipment_properties[subequipment_name] == "":
            for k, v in new_equipment.equipment_properties:
                self.subequipment_list_box.insert(k, v)
        else:
            self.subequipment_list_box.insert(END, self.new_equipment.equipment_properties[subequipment_name])
        '''


    def display_subparts_of_respective_subequipments(self,event,canvas,node_instance,x,y):
        new_subeqpmnt_option_list=event.widget.curselection()
        print("selected equipments weee", self.selected_subequipment_index_list)
        print("current scenario is ",new_subeqpmnt_option_list)
        new_subeqpmnt_option=[x for x in new_subeqpmnt_option_list if x not in self.selected_subequipment_index_list]
        print("alter add ", new_subeqpmnt_option)
        if new_subeqpmnt_option != "":
            for x in new_subeqpmnt_option:
                new_subequipment=event.widget.get(x)
                #print(self.current_vendor_instance.all_eqpmnt_subeqpmnt_and_parts_dictionary)
                if new_subequipment != Default :
                    #print(self.current_vendor_instance.all_eqpmnt_subeqpmnt_and_parts_dictionary[new_subequipment])
                    self.call_subpart_create_function(new_subequipment,canvas, node_instance, x, y)
                    self.selected_subequipment_index_list.append(x)
                else :
                    print("subequipment added")
                    self.create_sub_equipment(Default)

        else:
            print("subequipment is popped")

        print("currently",new_subeqpmnt_option_list)
        subequipment_unselected=[x for x in self.selected_subequipment_index_list if x not in new_subeqpmnt_option_list]
        print("node popped ",subequipment_unselected)
        for subeqpmnt in subequipment_unselected:
            self.selected_subequipment_index_list.remove(subeqpmnt)

        print(self.selected_subequipment_index_list)


    def create_sub_equipment(self,subequipment):
        self.add_ports_and_properties_to_equipment(self.current_vendor_instance.all_eqpmnt_subeqpmnt_and_parts_dictionary[self.new_equipment.name],self.new_equipment,subequipment)


    def add_ports_and_properties_to_equipment(self,equipment_dictionary,equipment,subequipment):
        #if subequipment == Default:
        port=self.current_vendor_instance.all_eqpmnt_subeqpmnt_and_parts_dictionary[self.new_equipment.name][ports]
        subpart = ""
        self.current_node_instance.update_ports(port,subpart,subequipment,equipment)
        self.reset_subequipment_property_box()
        port = self.current_node_instance.port_list
        self.display_properties_subequipment_box.insert(END, "Ports" + " :-\n" + port + "\n")

        #else:
        #    pass


    def call_subpart_create_function(self,new_subequipment,canvas,node_instance,x,y):
        print(self.current_vendor_instance)
        print(new_subequipment)
        subpart_dictionary = self.current_vendor_instance.all_eqpmnt_subeqpmnt_and_parts_dictionary[new_subequipment]#[subeqpmnt_subpart]
        print(self.current_vendor_instance.all_eqpmnt_subeqpmnt_and_parts_dictionary)
        #print(self.current_vendor_instance.all_eqpmnt_subeqpmnt_and_parts_dictionary[new_subequipment])
        self.create_subpart_window( canvas, x, y, node_instance)


    def load_subeqpmnt_property_window_box(self, canvas, equipment_name):#, node_instance):

        print("subequipments selected")
        try:
            self.reset_subequipment_property_box()

        except:
            print("First run, subequipment property box is empty")


        indices = self.subequipment_list_box.curselection()
        for index in indices:
            new_subequipment_name= self.subequipment_list_box.get(int(index))

            if new_subequipment_name == Default:
                #ports=self.current_node_instance.all_eqpmnt_subeqpmnt_and_parts_dictionary[ports]
                new_subequipment=Default
                #self.current_node_instance.update_ports(ports)

                subeqpmnt_property=self.current_vendor_instance.all_eqpmnt_subeqpmnt_and_parts_dictionary[equipment_name]
                for k,v in subeqpmnt_property.items():
                    print("equipment property ",k,"\t",v)
                port=subeqpmnt_property[ports]
                protocols=subeqpmnt_property[protocol]
                self.display_properties_subequipment_box.insert(END, "Ports" + " :-\n" + port+"\n")
                self.display_properties_subequipment_box.insert(END, "Protocols"+" :-\n"+protocols+"\n")

            else:
                new_equipment_property=self.current_vendor_instance.all_eqpmnt_subeqpmnt_and_parts_dictionary[new_subequipment_name]
            # self.subpart_window_list.append(self)

                for k, v in new_equipment_property.items():#.subequipment_properties_dictionary.items():
                    print("Sub equipment property ", k, v)
                port=new_equipment_property[ports]
                protocols=new_equipment_property[protocol]
                self.display_properties_subequipment_box.insert(END, "Ports"+ " :-\n"+port+"\n")
                self.display_properties_subequipment_box.insert(END, "Protocols" + " :-\n" + protocols + "\n")

            self.remove_canvas_window_objects(self.subequipment_list_box, self.subequipment_label)
            self.remove_canvas_window(canvas)  # ,node_instance)

            #for prop in new_subequipment.values():
            #    print(prop)

    def constraints_per_node(self, equipment, properties):
        pass

    def equipment_load(self, event, canvas, x, y, node_instance):
        widget = event.widget
        index = int(widget.curselection()[0])
        print("widget ", index)
        self.current_vendor_name = widget.get(index)
        self.current_vendor_instance = self.ne.network_equipment_vendor_dictionary[self.current_vendor_name]

        self.create_equipment_list_box(canvas, x, y, node_instance)
        try:
            self.equipment_list_box.delete(0, END)
        except:
            print("new equipment list")
        print("Vendor is ", self.current_vendor_name)
        self.equipment_options = self.ne.calling_equipment_names(self.current_vendor_name)
        for items in self.equipment_options:
            print(items)
            print("fbgVFgb")
            self.equipment_list_box.insert(END, items)

    '''
    def load_frame(self):
        self.vendor_options = []
        # test_option=[1,2,3,4,5]
        self.equipment_options = []
        self.cards_option = []
        # self.equipment_list_box = ""
        # self.subequipment_list_box = ""
        # self.vendor_list_box = Listbox(self.frame, bd=5, exportselection=0, height=300, bg="green")
        # self.equipment_list_box = Listbox(self.frame, bd=5, exportselection=0, height=300, bg="yellow")
        # self.subequipment_list_box = Listbox(self.frame, bd=5, exportselection=0, height=300)
        # self.vendor_list_box.pack(side=TOP)


        # self.vendor_list_box.bind('<<ListboxSelect>>', self.equipment_property_load)
        # self.equipment_list_box.bind('<<ListboxSelect>>', self.equipment_property_load)

        # self.vendor_list_box.pack(side=LEFT)
        # self.equipment_list_box.pack(side=LEFT)
        # self.subequipment_list_box.pack(side=LEFT)
        ''#'
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
        # '#''
    '''

    def vendor_name_selection(self, event, node_label, new_node_instance, canvas):
        self.vendor_options = self.ne.calling_vendor_names()
        self.current_node = new_node_instance
        try:
            self.vendor_list_box.delete(0, END)
        except:
            print("new object")
        self.create_vendor_list_box(event, node_label, canvas, new_node_instance)
        for ven in self.vendor_options:
            self.vendor_list_box.insert(END, ven)
            # print(self.vendor_options)

            ############
            # pass
##################3##################3##################3
##################3##################3##################3
##################3##################3##################3
##################3##################3##################3
##################3##################3##################3
##################3##################3##################3
##################3##################3##################3
##################3##################3##################3
##################3##################3##################3
##################3##################3##################3
##################3##################3##################3
##################3##################3##################3

#from all_dependencies import *
#from addresses import *
#import re


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



####################################################################
####################################################################
####################################################################
####################################################################
####################################################################
####################################################################
####################################################################
####################################################################
####################################################################
####################################################################
####################################################################
####################################################################

#from node import *
#from all_dependencies import *
#from addresses import  *
#from info_frame import *
#from onboarding_portal import *


class Network_Frame():
    def __init__(self, master, topology, simulation):
        self.simulation = simulation
        self.master = master
        #self.information_frame = information_frame
        self.canvas = Canvas(master, height=canvas_height, width=20, bg="azure")#""thistle1")
        self.canvas.pack(side=LEFT, expand=YES, fill=BOTH)
        self.frame = Frame(master, height=200, bg="orange")
        self.frame.pack(side=RIGHT)
        self.node_label_dictionary = {}
        self.text_label_dictionary = {}
        self.node_id_dictionary = {}
        self.current_label = ""
        self.topology = topology
        self.node_entry = ""
        self.entry_window = []
        self.network_node_instance_list = topology.network_node_instance_list

        self.network_edge_labels = {}

        self.edge_entry_point_label_list = []

        self.node_click_tally = 0
        # self.canvas_click_function()

        self.connecting_node_instance = ""
        self.network_node_instances_labels = {}

        #self.network_node_instance_by_node_id={}
        self.labels_generated_after_menu_node_type_selection = []

        # self.create_window_pane_for_network_node_labels()

        # print(self.node_numbers)
        # pass

    def delete_labels_generated_for_menu_node_type_selection(self):
        for label in self.labels_generated_after_menu_node_type_selection:
            try:
                self.canvas.delete(label)
            except:
                print("not deleted")
            try:
                self.node_label_dictionary.pop(label)
                self.text_label_dictionary.pop(label)
            except:
                print("text label")

    def canvas_click_function(self):
        # on clicking on canvas reset all the labels on canvas
        self.canvas.bind("<Button-1>", self.reset_entries_and_labels())

    def show_topology_on_frame(self):
        for node in self.network_node_instance_list:
            self.create_node_in_display_from_topology(node)
            # elf.network_node_instances_labels[]#
            ####need to create links

    def create_node_instance_label_on_canvas(self,node_instance):
        a,b,c,d=node_instance.canvas_coords
        # a and d are the required window
        label=Label(self.canvas,text=node_instance.node_id)
        node_instance.canvas_label_window_id=self.canvas.create_window(a+12,d+10,window=label,width=c-a,height=10)

    def remove_node_label_window(self,node_instance):
        self.canvas.delete(node_instance.canvas_label_window_id)

    def create_node_in_display_from_topology(self, node_instance):
        coords = node_instance.canvas_coords
        name = node_instance.name
        attributes = node_type[name]
        try:
            radius = attributes["radius"]
            new_node_label = self.canvas.create_oval(coords, fill=attributes["color"])
        except:
            length = attributes["length"]
            new_node_label = self.canvas.create_rectangle(coords, fill=attributes["color"])

        self.create_node_instance_label_on_canvas(node_instance)

        self.canvas.bind(new_node_label, "<Motion>", self.move_cursor_over_node)

        self.current_label = new_node_label
        self.node_label_dictionary[new_node_label] = name

        self.network_node_instances_labels[new_node_label] = node_instance

        # self.identify_nodes_on_position(node_instance,coords)


        # current_node_instance = self.network_node_instances_labels[self.current_label]

        self.canvas.tag_bind(new_node_label, "<Button-1>",
                             self.node_clicked_on_canvas)  # lambda event: self.node_clicked(event)#, new_node_label,text_at_previous_node_place,x,y))
        self.canvas.tag_bind(new_node_label, "<ButtonRelease-1>",
                             self.move_node)  # lambda event : self.move_node(event,new_node_label,text_at_previous_node_place,new_node_instance,attributes))
        self.canvas.bind(new_node_label, "<Double-1>",
                         lambda event: lambda event: self.create_equipment_selection_box(event,new_node_label, node_instance))
        self.canvas.tag_bind(new_node_label, "<Button-3>", lambda event: self.show_connecting_node_options(event,node_instance.canvas_coords,node_instance))
        self.canvas.update()

        #self.information_frame.vendor_name_selection(self.node_numbers, node_instance,self.canvas)


    def create_equipment_selection_box(self,event,new_node_label, node_instance):
        self.clear_all_boxes_on_canvas()
        #self.clear_all_information_frame_boxes()
        self.information_frame.vendor_name_selection(event, new_node_label, node_instance,self.canvas)

    def remove_edge_option_canvas_window(self):
        try:
            self.canvas.delete(self.window_for_edge_options)
        except:
            print("no edge option window present to be removed")

    def remove_equipment_canvas_window(self,node_instance):
        try:
            self.information_frame.remove_canvas_window(self.canvas)#,node_instance)
        except:
            print("no equipment window present to be removed")






    def remove_network_node_and_respective_components(self,node_instance):
        #self.topology.graph.remove_node(node_instance)
        self.delete_edge_entry_labels(node_instance)
        self.remove_node_label_window(node_instance)
        self.remove_equipment_canvas_window(node_instance)
        self.remove_edge_option_canvas_window()
        for connecting_node_instance in node_instance.connecting_node_instance_list:
            try:
                edge_label = self.network_edge_labels[(connecting_node_instance, node_instance)]
                self.network_edge_labels.pop((connecting_node_instance, node_instance))
            except:
                edge_label = self.network_edge_labels[(node_instance, connecting_node_instance)]
                self.network_edge_labels.pop((node_instance, connecting_node_instance))
            self.canvas.delete(edge_label)
        #for label,instance in self.network_node_instances_labels.items():
        for label in self.network_node_instances_labels.copy():
            instance=self.network_node_instances_labels[label]
            if node_instance == instance:
                try:
                    self.network_node_instances_labels.pop(label)
                except:
                    print("instance label is popped")
                self.canvas.delete(label)


    def show_connecting_node_options(self,event,present_coords,node_instance):
        button_color="gold"
        list_box_color="yellow"
        label_color="light goldenrod"
        frame_width=120
        frame_height=200
        literal_box_entry = "Node "
        x1,y1,x2,y2=present_coords
        self.node_connection_options_frame=Frame(self.canvas)
        delete_button=Button(self.node_connection_options_frame,bg=button_color,width=frame_width,text="Delete Node "+str(node_instance.node_id),command=lambda : self.remove_network_node_and_respective_components(node_instance))
        listbox=Listbox(self.node_connection_options_frame,selectmode=MULTIPLE,bg=list_box_color)
        connect_label=Label(self.node_connection_options_frame,bg=label_color,text="Connect to Nodes",width=frame_width)
        connect_button=Button(self.node_connection_options_frame,bg=button_color,text="Connect",width=frame_width)
        connect_button.configure(command=lambda: self.connect_edge_to_respective_node(listbox,node_instance,self.window_for_edge_options,literal_box_entry))
        delete_button.pack(side="top")
        connect_label.pack(side="top")
        connect_button.pack(side="bottom")
        listbox.pack()
        self.window_for_edge_options=self.canvas.create_window(x1+100,y2+100,window=self.node_connection_options_frame,width=frame_width,height=frame_height)
        #listbox.bind("<<ListboxSelect>>",lambda event: self.connect_edge_to_respective_node(event,node_instance,self.window_for_edge_options))
        for label, connecting_node_instance in self.network_node_instances_labels.items():
            if connecting_node_instance not in node_instance.connecting_node_instance_list and connecting_node_instance != node_instance:
                node_id=connecting_node_instance.node_id
                listbox.insert(END,literal_box_entry+str(node_id))
        #if len(self.network_node_instances_labels)==1 and


    #def connect_edge_to_respective_node(self,event,node_instance,window_label):
    def connect_edge_to_respective_node(self, widget, node_instance, window_label,literal_box_entry):
        #widget=event.widget

        #index=int(widget.curselection()[0])
        indices=widget.curselection()
        for index in indices:
            connecting_to_node=widget.get(int(index))
            connecting_node_id=int(connecting_to_node[len(literal_box_entry):])
            connecting_node_instance=self.topology.node_instance_dictionary_by_node_id[connecting_node_id]
            self.canvas.delete(window_label)
            self.create_edge_between_two_nodes(node_instance,connecting_node_instance)


    def create_edge_between_drop_and_positioned_nodes(self, new_node_instance):
        self.create_edge_between_two_nodes(new_node_instance,self.connecting_node_instance)
        self.connecting_node_instance = ""


    def create_line(self,coords1,coords2):
        x1, y1 = coords1[2], int(coords1[1] + (coords1[3] - coords1[1]) * 0.8)
        x2, y2 = coords2[0], int(coords2[1] + (coords2[3] - coords2[1]) * 0.2)
        edge_label = self.canvas.create_line(x1, y1, x2, y2)
        return edge_label

    def create_edge_between_two_nodes(self,new_node_instance,connecting_node_instance):
        print("new edge created between ", new_node_instance.node_id, " ", connecting_node_instance.node_id)
        coords1 = new_node_instance.canvas_coords
        coords2 = connecting_node_instance.canvas_coords
        edge_label=self.create_line(coords1,coords2)
        new_node_instance.connecting_node_instance_list.append(connecting_node_instance)
        connecting_node_instance.connecting_node_instance_list.append(new_node_instance)

        self.network_edge_labels[(new_node_instance, connecting_node_instance)] = edge_label
        new_node_instance.network_edge_labels_list.append(edge_label)
        connecting_node_instance.network_edge_labels_list.append(edge_label)


    def identify_new_position_to_place_node(self, node_instance, list_of_labels, coords, direction):
        label = list_of_labels[0]
        node_at_canvas_instance = self.network_node_instances_labels[label]
        print(node_at_canvas_instance)
        if direction == "left":
            coords = [(x - inter_node_distance) for x in coords]
            # direction="left"
        else:
            coords = [(x + inter_node_distance) for x in coords]
            # direction="right"

            x1, y1, x2, y2 = coords
        try:
            item = self.canvas.find_overlapping(x1, y1, x2, y2)
            coords = self.identify_new_position_to_place_node(node_at_canvas_instance, item, coords, direction)

        except:
            print("node is provided with coordinates")

        return coords

    def identify_nodes_on_position(self, node_instance, event, coords):  # coords,x,y):
        x, y = event.x, event.y
        x1, y1, x2, y2 = coords
        print("coordinates are", x, y)
        try:

            item = self.canvas.find_overlapping(x1, y1, x2, y2)
            if item != "":
                print("node super imposed on ")
                print("node", self.network_node_instances_labels[item[0]])

                self.connecting_node_instance = self.network_node_instances_labels[item[0]]
                for element in item:
                    print("element label is ", element)
                    # for k,v in self.node_label_dictionary.items():
                    #    print("new",k,v)
                    # for element in item:
                    print("node present here is ", self.node_label_dictionary[element])
            # return  item[0]

            coords = self.identify_new_position_to_place_node(node_instance, item, coords, "left")
            # for the newly created node in network by callback
        except:
            print("isolated node created on canvas")
        return coords
        # print("item is ",item[0])
        # self.current_label = item[0]
        # def move_node(self,event,node_label):
        # entry=Entry(self.canvas,text="node created",width=20)
        # print(event.widget)

    def create_network_node_instance(self, name, coords):

        if name == "Cl":
            node = Client_Node(self.topology.node_numbers)
            self.canvas_coords = coords
            # client
        elif name == "S":
            node = Server(self.topology.node_numbers)
            self.canvas_coords = coords
            # Server
        elif name == "Acc":
            node = Access_Node(self.topology.node_numbers, 0)
            self.canvas_coords = coords
            # Access_Network_Node
            # Access_Network_Node
        elif name == "M":
            node = Metro(self.topology.node_numbers, 0)
            self.canvas_coords = coords
            # Metro_Network_Node
        elif name == "CN":
            node = Core(self.topology.node_numbers, 0)
            self.canvas_coords = coords
            # Core_Network_Node
        elif name == "P":
            node = P_Node(self.topology.node_numbers, 0)
            self.canvas_coords = coords
            # P_Network_Node
        elif name == "CD":
            node = Core_Node(self.topology.node_numbers, 0)
            self.canvas_coords = coords
            # Core_DC_Node
        elif name == "Edg":
            node = Edge_Node(self.topology.node_numbers, 0, 0)
            self.canvas_coords = coords
            # Edge_DC_Node

        elif name == "Ag":
            node = Aggregation_Node(self.topology.node_numbers)
            self.canvas_coords = coords

        elif name == "Prb":
            node = Probe_Node(self.topology.node_numbers)
            self.canvas_coords = coords

        elif name == "Cntrlr":
            node = Controller(self.topology.node_numbers)
            node.start_controller(self.topology)
            self.canvas_coords = coords

        elif name == "WB":
            node = White_Box(self.topology.node_numbers)
            self.canvas_coords = coords
        elif name == "Sw":
            node = Switch(self.topology.node_numbers)
            self.canvas_coords = coords

        elif name == "R":
            node = Router(self.topology.node_numbers)
            self.canvas_coords = coords

        elif name == "F":
            node = Firewall(self.topology.node_numbers)
            self.canvas_coords = coords
        elif name == "Dci":
            node = DataCenter_Interconnect(self.topology.node_numbers)
            self.canvas_coords = coords
        elif name == "G":
            node = Gateway(self.topology.node_numbers)
            self.canvas_coords = coords
        elif name == "Agdc":
            node = Aggregation_DC_Node(self.topology.node_numbers)
            self.canvas_coords = coords

        else:
            print("node not identified")
            node = ""
            return ""
            # new node
        self.topology.node_instance_dictionary_by_node_id[self.topology.node_numbers] = node
        #self.network_node_instance_by_node_id[self.topology.node_numbers] = node
        self.topology.node_numbers += 1
        return node

    def create_node_in_graph(self, node, attributes, coords):
        node = self.create_network_node_instance(attributes["name"], coords)
        # self.topology.add_nodes_to_topology()
        # self.topology.graph.add_node(node)
        # self.topology.ip_address_graph.add_node(node.ip_address)
        return node
        # def move_node(self,event,node):#,circle_id,radius):
        # print(self.canvas.canvasx(event),self.canvas.canvasy(event))
        # self.canvas.coords(circle_id,event.x-radius,event.x+radius,event.y-radius,event.y+radius)
        # self.canvas.move(node,event.x,event.y)
        # circle_id.move()

    def move_cursor_over_node(self, event):
        # message_box=messagebox.showinfor("hi, cursor moved over the node")
        print("cursor moved")


        # nodemenubar.add_cascade(label="nodes")
        # elf.create_window_pane_for_generic_network_node_labels()

    def create_window_pane_for_data_center_node_labels(self):
        self.delete_labels_generated_for_menu_node_type_selection()
        self.create_node_label_image(data_center_node_type)

    def create_window_pane_for_client_server_node_labels(self):
        self.delete_labels_generated_for_menu_node_type_selection()
        self.create_node_label_image(client_server_node_type)

    def create_window_pane_for_general_nodes_label(self):
        self.delete_labels_generated_for_menu_node_type_selection()
        self.create_node_label_image(general_node_type)

    def create_window_pane_for_sdn_network_node_labels(self):
        self.delete_labels_generated_for_menu_node_type_selection()
        self.create_node_label_image(sdn_node_type)

    def create_window_pane_for_probe_network_node_labels(self):
        self.delete_labels_generated_for_menu_node_type_selection()
        self.create_node_label_image(probe_node_type)

    def create_window_pane_for_generic_network_node_labels(self):
        self.delete_labels_generated_for_menu_node_type_selection()
        self.create_node_label_image(network_node_type)


        # self.label_entry = Label(self.canvas, text=node_property)
        # window1 = self.canvas.create_window(100, canvas_height - 500, window=self.label_entry, height=200, width=200)

    def create_node_label_image(self, node_type_dictionary):
        a = b = 50
        label_color="DarkOliveGreen1"
        node_label_color="SandyBrown"
        print("creating the drag and drop part")
        x = 100
        y = 20
        width = 20
        label = Label(self.canvas, text="Drag and Drop the node", width=30,bg=label_color)
        window_label = self.canvas.create_window(x, y, window=label, height=width, width=200)
        # label.place(x=20,y=20)

        self.labels_generated_after_menu_node_type_selection.append(window_label)
        displacement = 150
        self.movement_objects = {}
        # c=d=50
        y = b + 10
        for node, attributes in node_type_dictionary.items():
            # print(node,attributes)
            try:
                radius = int(attributes["radius"])
                label = Label(self.canvas, text=node, width=width,bg=node_label_color)
                window_label = self.canvas.create_window(x, y, window=label, height=width, width=200)
                # label.place(x=a, y=b)
                coords = a + displacement, b, a + displacement + 20, b + 20
                # node_label=IntVar()
                node_label = self.canvas.create_oval(coords, fill=attributes["color"])

            except:
                length = int(attributes["length"])
                breadth = int(attributes["breadth"])
                label = Label(self.canvas, text=node, width=width,bg=node_label_color)
                window_label = self.canvas.create_window(x, y, window=label, height=width, width=200)
                # label.place(x=a, y=b)
                coords = a + displacement, b, a + displacement + 20, b + 20
                node_label = self.canvas.create_rectangle(coords, fill=attributes["color"])

            self.labels_generated_after_menu_node_type_selection.append(window_label)
            self.labels_generated_after_menu_node_type_selection.append(node_label)
            # node_label=Button(self.canvas,text=node,bd=2,bg="green")#
            self.canvas.bind(node_label, "<Motion>", self.move_cursor_over_node)

            self.node_label_dictionary[node_label] = node
            self.text_label_dictionary[node_label] = attributes["name"]
            # self.text_label_dictionary[node_label]=node
            # movements=Node_Movements()
            # movements.set_variables(self.canvas,self.node_label_dictionary,self.current_label,self.information_frame)
            self.canvas.tag_bind(node_label, "<Button-1>",
                                 self.node_clicked)  # partial(self.node_clicked,event,node))#laambda event : self.node_clicked(event,node))#attributes))
            # print(self.current_label)
            # DN=Display_Node(self)#.canvas,self.node_label_dictionary,self.current_label,self.information_frame)
            self.canvas.tag_bind(node_label, "<ButtonRelease-1>",
                                 self.create_node_in_display)  # lambda event: (event,self.current_label))#, attributes))

            self.canvas.update()
            # self.canvas.tag_bind(node_label,'<ButtonPress-1>',self.create_node)
            # ,command=partial(self.hold,node,attributes))
            # self.canvas.tag_bind(node_label,'<Motion>',lambda event: self.move_circle(event,node_label,attributes["radius"]))#,attributes.color))
            # node_label.pack(side=LEFT)
            # self.node_label_dictionary[node_label]=node
            # self.node_id_dictionary[node_label]=attributes
            b += 30
            y += 30

    def testing_function(self, events):
        print("yes function ois wojbnvj")

    def create_links(self):
        pass


    def clear_all_boxes_on_canvas(self):
        try:
            self.information_frame.remove_canvas_window(self.canvas)
        except:
            print("\n")


    def clear_all_information_frame_boxes(self):
        for entry in self.information_frame.all_entries_list:
            entry.delete(0,END)


    def node_clicked(self, event):

        self.reset_entries_and_labels()
        self.clear_all_boxes_on_canvas()
        self.clear_all_information_frame_boxes()
        self.remove_edge_option_canvas_window()
        x, y = event.x, event.y
        item = self.canvas.find_closest(x, y)
        # return  item[0]
        # print("item is ",item[0])
        try:
            self.current_label = item[0]
            # def move_node(self,event,node_label):
            # entry=Entry(self.canvas,text="node created",width=20)
            # print(event.widget)
            current_node_instance = self.network_node_instances_labels[self.current_label]
            self.delete_edge_entry_labels(current_node_instance)
            self.create_edge_entry_point(current_node_instance)
        except:
            print("new node is created")
        # self.information_frame.node_property_display.delete(1.0, END)
        # self.set_information_frame_text_box_for_node_information()
        # self.display_information_frame_text_box_for_node_information()
        self.canvas.update()

        # coords=500,500,530,530
        # self.canvas.create_oval(coords)

    def reset_entries_and_labels(self):

        # self.delete_edge_entry_labels()
        for window in self.entry_window:
            self.canvas.delete(window)
        self.entry_window = []
        # self.information_frame.node_property_display.delete(1.0,END)
        # self.canvas.delete(self.node_entry)

    def node_clicked_on_canvas(self, event):
        # self.delete_all_edge_entry_labels()
        self.reset_entries_and_labels()
        self.clear_all_boxes_on_canvas()
        self.clear_all_information_frame_boxes()
        self.remove_edge_option_canvas_window()
        x, y = event.x, event.y
        item = self.canvas.find_closest(x, y)
        # return  item[0]
        # print("item is ",item[0])
        current_node_instance = self.network_node_instances_labels[self.current_label]
        self.delete_edge_entry_labels(current_node_instance)
        # self.create_edge_entry_point(event,current_node_instance)
        self.current_label = item[0]
        # self.current_node_instance=current_node_instance
        # self.node_entry=Entry(self.canvas)
        # window=self.canvas.create_window(x-100,y,window=self.node_entry,height=70,width=150)
        # self.entry_window.append(window)
        # node_property="Longitude is "+ str(current_node_instance.longitude), "\nLatitude is "+str(current_node_instance.latitude)
        # self.node_entry.insert(0,node_property)
        # self.information_frame.node_property_display.insert(END,node_property)
        self.set_information_frame_text_box_for_node_information(current_node_instance)
        # print("node property is ")

        self.create_edge_entry_point(current_node_instance)
        #self.node_entry.update()
        # print(self.current_label)

        # def move_node(self,event,node_label):
        # entry=Entry(self.canvas,text="node created",width=20)
        # print(event.widget)

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

    def create_node_in_display(self, event):  # ,node_label):  # ,network_frame,event,node_label):#,node,attributes):
        # widget=event.GetEventObject()
        # print(widget)
        self.reset_entries_and_labels()
        time.sleep(0.25)
        print("erronous current label is ",self.current_label)
        node = self.node_label_dictionary[self.current_label]
        # text=self.text_label_dictionary[self.current_label]
        attributes = node_type[node]
        print("new node created on canvas ", node)
        x, y = event.x, event.y
        try:
            radius = int(attributes["radius"])

            coords = x - radius, y - radius, x + radius, y + radius
            new_node_instance = self.create_node_in_graph(node, attributes, coords)
            # print(new_node_instance)
            # identifying, if any node is present in the background. for drop  and add edge to work

            coords = self.identify_nodes_on_position(new_node_instance, event, coords)

            new_node_instance.canvas_coords = coords

            new_node_label = self.canvas.create_oval(coords, fill=attributes["color"])
        except:
            length = int(attributes["length"])
            breadth = int(attributes["breadth"])
            coords = x - length / 2, y - breadth / 2, x + length / 2, y + breadth / 2

            new_node_instance = self.create_node_in_graph(node, attributes, coords)

            coords = self.identify_nodes_on_position(new_node_instance, event, coords)
            new_node_instance.canvas_coords = coords
            new_node_label = self.canvas.create_rectangle(coords, fill=attributes["color"])
        # self.canvas.bind(new_node_label, "<Motion>", self.move_cursor_over_node)


        self.create_node_instance_label_on_canvas(new_node_instance)

        try:
            print("trace")
            print(coords, new_node_instance)
            print("tr", type(self.connecting_node_instance), self.connecting_node_instance, type(new_node_instance),
                  new_node_instance)
            if self.connecting_node_instance != "":
                connecting_node_instance=self.connecting_node_instance
                self.create_edge_between_drop_and_positioned_nodes(new_node_instance)
                self.topology.add_edge_to_topology(new_node_instance, connecting_node_instance)
            else:
                self.topology.add_nodes_to_topology(new_node_instance)
        except:
            print("no edge to add")

        self.create_edge_entry_point(new_node_instance)

        # node_text = self.canvas.create_text(x, y, text=attributes["name"])
        self.current_label = new_node_label
        self.node_label_dictionary[new_node_label] = node  # node is mapped to new node label in canvas
        # self.text_label_dictionary[new_node_label]=node_text


        self.network_node_instances_labels[new_node_label] = new_node_instance
        # text_at_previous_node_place=node_text



        current_node_instance = self.network_node_instances_labels[self.current_label]
        # print(self.current_label)

        self.set_node_information_window_box(current_node_instance)
        self.canvas.tag_bind(new_node_label, "<Button-1>",
                             self.node_clicked_on_canvas)  # lambda event: self.node_clicked(event)#, new_node_label,text_at_previous_node_place,x,y))
        self.canvas.tag_bind(new_node_label, "<ButtonRelease-1>",
                             self.move_node)  # lambda event : self.move_node(event,new_node_label,text_at_previous_node_place,new_node_instance,attributes))
        self.canvas.tag_bind(new_node_label,"<Double-1>",lambda event:self.create_equipment_selection_box(event,new_node_label, new_node_instance))
        self.canvas.tag_bind(new_node_label,"<Button-3>", lambda event:self.show_connecting_node_options(event,current_node_instance.canvas_coords,new_node_instance))
        self.canvas.update()
        # print("node jfnj")
        #self.information_frame.vendor_name_selection(self.node_numbers, new_node_instance,self.canvas)
        # elf.node_entry.insert(0,node_property)
        # elf.node_entry.update()

    def set_node_information_window_box(self, current_node_instance):
        self.set_information_frame_text_box_for_node_information(current_node_instance)
        node_property = "Enter node's\na)longitude, \nb)latitude, \nc)Ip_address, \nd)Number of ports \nseperated by spaces respectively"
        self.information_frame.set_node_property_from_input(node_property,current_node_instance)

    def set_information_frame_text_box_for_node_information(self, current_node_instance):
        self.reset_entries_and_labels()
        self.display_information_frame_text_box_for_node_information(current_node_instance)



    def display_information_frame_text_box_for_node_information(self, current_node_instance):
        self.clear_all_information_frame_boxes()
        #self.information_frame.node_name_entry.delete(1.0, END)
        #self.information_frame.node_id_entry.delete(1.0, END)
        #self.information_frame.mac_address_entry.delete(1.0, END)
        #self.information_frame.ip_address_entry.delete(1.0, END)
        #self.information_frame.longitude_entry.delete(1.0, END)
        #self.information_frame.latitude_entry.delete(1.0, END)
        #self.information_frame.node_name_entry.insert(END, "Node Name\t")
        self.information_frame.node_name_entry.insert(END, current_node_instance.type)
        #self.information_frame.node_property_display.insert(END, "\nNode ID\t")
        self.information_frame.node_id_entry.insert(END, current_node_instance.node_id)
        #self.information_frame.node_property_display.insert(END, "\nLatitude\t")
        self.information_frame.latitude_entry.insert(END, str(current_node_instance.latitude))
        #self.information_frame.node_property_display.insert(END, "\nLongitude\t")
        self.information_frame.longitude_entry.insert(END, str(current_node_instance.longitude))
        #self.information_frame.node_property_display.insert(END, "\nMAC Address\t")
        self.information_frame.mac_address_entry.insert(END, str(self.binary_to_hexa(current_node_instance.mac_address.mac_address)))
        #self.information_frame.node_property_display.insert(END, "\nIP Address\t")
        self.information_frame.ip_address_entry.insert(END, str(self.binary_to_ip_address(current_node_instance.ip_address.ip_address)))
        self.set_information_frame_node_entry_box_for_current_node_selection(current_node_instance)
        # self.information_frame.node_property_display.insert(END,)

    def binary_to_ip_address(self,binary_string):
        ip_address=""
        for i in range(0,len(binary_string),8):
            octet=0
            for j in range(8):
                octet=int(binary_string[i+j])*pow(2,7-j) + octet
                octet=int(octet)
            print(octet)
            ip_address += str(octet)
            if(i+8 < len(binary_string)):
                ip_address+="."
        return ip_address

    def binary_to_hexa(self,binary_string):
        dec_to_hex={10:'A',11:"B",12:"C",13:"D",14:"E",15:"F"}
        mac_address=""
        for i in range(0,len(binary_string),4):
            dec=0
            for j in range(4):
                dec=int(int(binary_string[i+j])*pow(2,j)+dec)
            if dec>10:
                dec=dec_to_hex[dec]
            else:
                dec=str(dec)
            mac_address+=dec
        return mac_address

    def set_information_frame_node_entry_box_for_current_node_selection(self, current_node_instance):
        if self.node_click_tally == 0:
            self.information_frame.node_A.insert(END, current_node_instance.node_id)
            self.node_click_tally += 1
        elif self.node_click_tally == 1:
            node_a = int(self.information_frame.node_A.get())
            if node_a == current_node_instance.node_id:
                self.node_click_tally = 1
            elif node_a != current_node_instance.node_id:
                self.information_frame.node_B.delete(0, END)
                self.information_frame.node_B.insert(END, current_node_instance.node_id)
                self.node_click_tally = 2

        else:
            node_b = int(self.information_frame.node_B.get())
            node_a = int(self.information_frame.node_A.get())
            if node_a == node_b:
                self.information_frame.node_B.delete(0, END)
                self.node_click_tally = 1
            else:
                self.information_frame.node_A.delete(0, END)
                self.information_frame.node_B.delete(0, END)
                self.information_frame.node_A.insert(0, node_b)
                self.information_frame.node_B.insert(0, current_node_instance.node_id)



    def set_node_property_by_entry(self, event, current_node_instance, window1, window2):
        node_property = self.node_entry.get()
        # white_space = [" ", ",", "\t", "\n"]
        node_property = node_property.split(" ")
        print(node_property)
        current_node_instance.longitude = node_property[0]
        current_node_instance.latitude = node_property[1]
        self.entry_window.remove(window1)
        self.entry_window.remove(window2)
        self.canvas.delete(window1)
        self.canvas.delete(window2)
        self.set_information_frame_text_box_for_node_information(current_node_instance)

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
        # movement = Node_Movements(self.canvas, self.node_label_dictionary, new_node_label, self.information_frame,self.network_frame)
        # movement.set_variables(self.canvas, self.node_label_dictionary, new_node_label, self.information_frame)
        # print("DN",new_node_label)
        # self.canvas.create_text(x, y, text=attributes["name"])

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

    def move_node(self, event):  # ,new_node_label,text,new_node_instance,attributes):
        self.reset_entries_and_labels()
        self.clear_all_information_frame_boxes()
        #self.clear_all_boxes_on_canvas()

        print("move node method")
        print("current label is ", self.current_label)
        node = self.node_label_dictionary[self.current_label]
        current_node_instance = self.network_node_instances_labels[self.current_label]

        self.remove_node_label_window(current_node_instance)
        self.network_node_instances_labels.pop(self.current_label)

        self.delete_edge_entry_labels(current_node_instance)

        # text=self.text_label_dictionary[self.current_label]
        attributes = node_type[node]
        self.canvas.delete(self.current_label)
        # self.canvas.delete(text)
        # self.text_label_dictionary.pop(self.current_label)
        self.node_label_dictionary.pop(self.current_label)
        x, y = event.x, event.y
        try:
            radius = int(attributes["radius"])
            coords = x - radius, y - radius, x + radius, y + radius

            # updating the coords for the moved node
            current_node_instance.canvas_coords = coords
            new_node_label = self.canvas.create_oval(coords, fill=attributes["color"])
        except:
            length = int(attributes["length"])
            breadth = int(attributes["breadth"])
            coords = x - length / 2, y - breadth / 2, x + length / 2, y + breadth / 2
            current_node_instance.canvas_coords = coords
            new_node_label = self.canvas.create_rectangle(coords, fill=attributes["color"])
        self.create_edge_entry_point(current_node_instance)

        self.create_node_instance_label_on_canvas(current_node_instance)

        self.set_node_information_window_box(current_node_instance)

        # self.canvas.bind(new_node_label, "<Motion>", lambda event:self.move_cursor_over_node(event))

        self.network_node_instances_labels[new_node_label] = current_node_instance
        self.node_label_dictionary[new_node_label] = node
        self.current_label = new_node_label
        # self.canvas.bind(new_node_label,"<Motion>",self.move_cursor_over_node)
        # text=self.canvas.create_text(x,y,text=attributes["name"])
        # self.text_label_dictionary[self.current_label]=text
        # print("ffdsf")
        # self.canvas.move(new_node_label,x,y)
        # self.canvas.move(text,x,y)
        # self.canvas.create_text(x,y,text=text)
        self.canvas.tag_bind(new_node_label, "<Button-1>",
                             lambda event: self.node_clicked(event))  # , self.current_label,text,x,y))
        # self.canvas.tag_bind(text, "<Button-1>", lambda event: self.node_tinkered(event, new_node_label,text,x,y))
        self.canvas.tag_bind(new_node_label, "<ButtonRelease-1>",
                             self.move_node)  # lambda event : self.move_node(event,self.current_label,text.text,new_node_instance,attributes))
        self.canvas.tag_bind(new_node_label,"<Double-1>",lambda event: self.create_equipment_selection_box(event,new_node_label, current_node_instance))

        self.canvas.tag_bind(new_node_label, "<Button-3>", lambda event: self.show_connecting_node_options(event,current_node_instance.canvas_coords,current_node_instance))
        self.move_edges(current_node_instance)
        self.canvas.update()
        # pass

    def create_edge_entry_point(self, current_node_instance):
        print("creating edge entry point")
        x1, y1, x2, y2 = current_node_instance.canvas_coords
        # self.delete_all_edge_entry_labels()
        current_node_instance.edge_entry_label = self.canvas.create_oval(x2 + 3, y2 + 3, x2 + 8, y2 + 8)
        self.canvas.tag_bind(current_node_instance.edge_entry_label, "<ButtonRelease-1>",
                             lambda event: self.create_new_edge_between_existing_nodes(event, current_node_instance))

    def create_new_edge_between_existing_nodes(self, event, current_node_instance):
        x, y = event.x, event.y
        item = self.canvas.find_closest(x, y)
        node_label = item[0]
        connecting_node_instance = self.network_node_instances_labels[node_label]
        print("edge created jere mnds", connecting_node_instance)
        self.create_edge_between_two_nodes(current_node_instance, connecting_node_instance)
        # self.delete_edge_entry_labels()

    def delete_edge_entry_labels(self, current_node_instance):
        try:
            self.canvas.delete(current_node_instance.edge_entry_label)
        except:
            print("no edge entry label existed")

    def find_coordinates_to_plot_edge(self, coords1, coords2):

        a1, b1, a2, b2 = coords1
        x1, y1, x2, y2 = coords2
        a = (a1 + a2) / 2
        b = (b1 + b2) / 2
        x = (x1 + x2) / 2
        y = (y1 + y2) / 2

        # try:
        if a <= x and b <= y:
            # m=(b-y)/(a-x)
            return a2, b2, x1, y1
        elif a <= x and b > y:
            return a2, b1, x1, y2

        elif a > x and b <= y:
            return x2, y1, a1, b2
        else:
            return x2, y2, a1, b1
            # print("we reached")

    def create_edge_between_two_nodes(self, current_node_instance, connecting_node_instance):

        try:
            print(current_node_instance, connecting_node_instance)
            print(current_node_instance.canvas_coords)
            print(connecting_node_instance.canvas_coords)
            x1, y1, x2, y2 = self.find_coordinates_to_plot_edge(current_node_instance.canvas_coords,
                                                                connecting_node_instance.canvas_coords)
            # x1, y1 = coords1[2], int(coords1[1] + (coords1[3] - coords1[1]) * 0.8)
            # x2, y2 = coords2[0], int(coords2[1] + (coords2[3] - coords2[1]) * 0.2)
            edge_label = self.canvas.create_line(x1, y1, x2, y2)
            self.network_edge_labels[(current_node_instance, connecting_node_instance)] = edge_label
            # current_node_instance.network_edge_labels_list.append(edge_label)
            # connecting_node_instance.network_edge_labels_list.append(edge_label)
            if connecting_node_instance not in current_node_instance.connecting_node_instance_list:
                current_node_instance.connecting_node_instance_list.append(connecting_node_instance)
            if current_node_instance not in connecting_node_instance.connecting_node_instance_list:
                connecting_node_instance.connecting_node_instance_list.append(current_node_instance)
        except:
            print("edge is not created between existing nodes")

    def move_edges(self, current_node_instance):
        for connecting_node_instance in current_node_instance.connecting_node_instance_list:
            try:
                edge_label = self.network_edge_labels[(connecting_node_instance, current_node_instance)]
                self.network_edge_labels.pop((connecting_node_instance, current_node_instance))
            except:
                edge_label = self.network_edge_labels[(current_node_instance, connecting_node_instance)]
                self.network_edge_labels.pop((current_node_instance, connecting_node_instance))
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
            self.create_edge_between_two_nodes(current_node_instance, connecting_node_instance)
        pass

    def node_tinkered(self, event, new_node_label, text, x, y):
        # print(event.widget)
        print("node ", new_node_label, " moved to new place ")
        # self.current_label=self.node_clicked()
        # self.canvas.delete(text_at_previous_node_place)
        # print(node)

    def refresh_canvas_windows(self):
        #self.information_frame.remove_canvas_window()
        #self.information_frame.remove_canvas_window_objects(self.subequipment_list_box, self.subequipment_label)
        self.information_frame.remove_canvas_window(self.canvas)


####################################################################
####################################################################
####################################################################
####################################################################
####################################################################
####################################################################
####################################################################
####################################################################




#from all_dependencies import *


class Onboarding_Portal():


    def __init__(self):
        #self.onboarding_portal_flag=0
        #self.onboarding = Tk()
        #self.onboarding_frame = Frame(self.onboarding)
        pass

    def checking_equipments_compatibility(self):
        #self.first_component
        #self.second_component
        pass# )


    def add_widgets_to_onboarding(self):
        self.first_equipment_label=Label(self.onboarding_frame,text="First Equipment")
        self.second_equipment_label=Label(self.onboarding_frame,text="Second Equipment")
        self.first_equipment_entry = Entry(self.onboarding_frame)
        self.second_equipment_entry=Entry(self.onboarding_frame)
        self.comment_section=Entry(self.onboarding_frame)
        self.first_equipment_label.grid(row=0,column=0)
        self.first_equipment_entry.grid(row=0,column=1)
        self.second_equipment_label.grid(row=1,column=0)
        self.second_equipment_entry.grid(row=1,column=1)
        self.comment_section.grid(row=2,column=0,rowspan=4,columnspan=2)


    def checking_services_possible_on_path(self):
        pass


    def checking_ports_compatibility(self):
        pass


    def checking_service_compatibility_on_port(self):
        pass


    def load_onboarding_rules(self):
        pass

    def create_onboarding_portal_window(self,master,node_frame):
        self.node_frame=node_frame
        #self.node_frame.onboarding_portal_button.destroy()
        #if self.onboarding_portal_flag == 0:
        self.onboarding_frame=Frame(self.node_frame.network_frame.canvas)
        self.onboarding_window=self.node_frame.network_frame.canvas.create_window(canvas_width,100,window=self.onboarding_frame,width=100,height=canvas_height)
        self.onboarding_portal_flag =1
        self.onboarding_frame.config(width=300,height=1000,bg='steelblue')
        self.onboarding_frame.pack(side="right")
        self.add_widgets_to_onboarding()

    def exit_onboarding_portal(self):
        self.onboarding_frame.destroy()
        self.node_frame.moving_back_to_verifier()

    def create_cell_on_portal(self,x,y,width,height):
        pass


'''
onboarding=Tk()
onboarding_portal=Onboarding_Portal()
onboarding_portal.create_onboarding_portal_window(onboarding)
onboarding.mainloop()
'''
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################

#from all_dependencies import *





class Probe():

    def __init__(self):
        pass


    def dynamic_probing(self):
        pass

    def generating_test_probes(self):
        pass


    def checking_edge_statistics(self):
        pass


###################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################

#from all_dependencies import *

class Topology():
    def __init__(self):
        self.graph = nx.Graph()
        self.network_node_instance_list = []
        self.node_numbers = 1
        self.node_instance_dictionary_by_node_id = {}
        self.port_graph = nx.Graph()
        self.ip_address_graph = nx.Graph()
        self.port_numbers = 1

    def draw_Network(self):
        pass

    def find_shortest_path(self, node_instance_1, node_instance_2):
        shortest_path = nx.shortest_path(self.graph, node_instance_1, node_instance_2)
        return shortest_path

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

##################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################

# from node import *
#from all_dependencies import *
#from info_frame import *
#from nw_frame import *
#from equipments import *

# from network_equipment import *


############################################################################
###############################################################################################
###############################################################################################


##################################################################################################################
##################################################################################################################


class Simulation():
    def __init__(self):
        self.environment = simpy.Environment()
        self.link_delay = 10  # micro second
        self.packet_id = 0
        self.max_time = 1000

    def create_ip_packets(self, number_of_packets):
        packets = []
        for i in range(number_of_packets):
            packet = Packet("IP", 1500, self.packet_id)
            packets.append(packet)
            self.packet_id += 1
        return packets

    def create_simulation(self):
        self.environment.process(self.simulation_of_packet())

    def start_ip_traffic_between_two_nodes(self, information_frame, topology):
        # self.information_frame
        print("starting ip traffic")
        node1 = topology.node_instance_dictionary_by_node_id[int(information_frame.node_A.get())]
        node2 = topology.node_instance_dictionary_by_node_id[int(information_frame.node_B.get())]
        packets = self.create_ip_packets(10)
        shortest_path = topology.find_shortest_path(node1, node2)
        information_frame.set_shortest_path_box_window(shortest_path)
        self.environment.process(self.start_ip_simulation(shortest_path, packets))
        self.max_time += self.environment.now
        self.environment.run(until=self.max_time)
        print("two nodes traffic completed suceessfully")

    def start_all_nodes_ip_traffic(self, information_frame, topology):

        node_instance_list = topology.node_instance_dictionary_by_node_id.values()
        nodes_pair = zip(node_instance_list, node_instance_list)
        for node1, node2 in nodes_pair:
            if node1 != node2:
                packets = self.create_ip_packets(10)
                shortest_path = topology.find_shortest_path(node1, node2)
                self.environment.process(self.start_ip_simulation(shortest_path, packets))
        self.max_time += self.environment.now
        self.environment.run(until=self.max_time)
        print("all node traffic completed successfully")

    def start_ip_simulation(self, shortest_path, packets):
        for packet in packets:
            print("packet ", str(packet.type), "\tpacket id ", str(packet.packet_id))
            for node in shortest_path:
                print("node ", node, "\t id ", str(node.node_id), str(self.environment.now))
                yield self.environment.timeout(self.link_delay)

    def simulation_of_packet(self):
        pass


class Packet():
    def __init__(self, type, size, packet_id):
        self.type = type
        self.size = size
        self.packet_id = packet_id


##################################################################################################
##################################################################################################




class Flow_Table():
    def __init__(self):
        pass


class Routing_Table():
    def __init__(self):
        self.routing_table_for_device = {}


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

        self.deployed_nodes = {}
        self.deployed_equipments = []

        # self.deployed_equipments_properties={}

        self.topology = ""
        try:
            self.create_minimal_topology()
        except:
            print("erorr in topology creation")
        try:
            self.load_current_deployed_topology()
        except:
            print("no initial topology")

    def create_minimal_topology(self):
        self.topology = Topology()
        print("topology created")

    def load_current_deployed_topology(self):
        try:
            if current_deployed_topology_file[-3:] == "csv":
                self.read_topology_from_csv()
                print("file is csv")
            elif current_deployed_topology_file[-3:] == "xml":
                self.read_topology_from_xml()
                print("xml file")
        except:
            print("no file selected ")  # type of elementi.e node, link
            # for node,2nd,3rd and 4th column are node_id, the latitude and longitude respectively
            # 5th column is equipment_id
            # 6th equipment_name
                # 7th column is sub_equipment_id
            # 8th is  sub_equipment_name
            # 9th column is interface type

            # line=csv.DictReader(current_deployed_topology_file,'r')

    def read_topology_from_csv(self):
        try:
            file = open(current_deployed_topology_file, 'r')
            data = csv.reader(file)
            data_list = list(data)  # 2-dimesnion list
            for data_record in data_list:
                self.load_data_record(data_record)
                self.current_deployed_equipments.append(data_record)
                # load current deployed topo;ogy

        except:
            print("no initial topology provided")

    def load_data_record(self, data_record):
        if data_record[0].lower() == "NODE".lower():
            # load te node attributes
            node_id = data_record[1]
            node_name = data_record[2]  ###### Core node, aggregation node, metro node,, etc name in node_type
            longitude = data_record[3]
            latitude = data_record[4]
            equipment_id = data_record[5]
            equipment_name = data_record[6]
            subequipment_id = data_record[7]
            subequipment_name = data_record[8]
            interface_type = data_record[9]
            self.create_node(node_id, node_name, longitude, latitude, equipment_id, equipment_name, subequipment_id,
                             subequipment_name, interface_type)


        elif data_record[1].lower() == "LINK".lower():
            # load the link attributes
            pass

    def create_node(self, node_id, node_name, longitude, latitude, equipment_id, equipment_name, subequipment_id,
                    subequipment_name, interface_type):
        if node_id not in self.deployed_nodes.values():
            width = canvas_width / (360 * 60 * 60)
            height = canvas_height / (180 * 60 * 60)
            l, m, s = longitude[:-1].split("-")
            node_width = (s + (m * 60 + l * 60 * 60)) * 360
            h, m, s = latitude[:-1].split("-")
            node_height = (s + (m * 60 + h * 60 + 60)) * 180
            if latitude[-1:] != "N":
                node_height = -1 * node_height
            if longitude[-1:] != "E":
                node_width = -1 * node_width
            node_height = node_height + height / 2
            node_width = node_width + width / 2
            attributes = node_type[node_name]
            radius = attributes["radius"]
            coords = node_width - radius, node_height - radius, node_width + radius, node_height + radius
            node_instance = self.create_node_instance(node_name, coords)
            node_instance.longitude = longitude
            node_instance.latitude = latitude
            # print("node added ")
            self.topology.graph.add_node(node_instance)
            self.deployed_nodes[node_id] = node_instance
            # self.deployed_equipments_properties[node_instance]

        self.create_equipments_on_nodes(node_id, equipment_id, equipment_name, subequipment_id, subequipment_name,
                                        interface_type)

    def create_equipments_on_nodes(self, node_id, equipment_id, equipment_name, subequipment_id, subequipment_name,
                                   interface_type):
        node_instance = self.deployed_nodes[node_id]
        if equipment_id not in node_instance.node_equipment_dictionary.values():
            equipment = Equipment()
            equipment.name = equipment_name
            equipment.id = equipment_id
            node_instance.node_equipment_dictionary[equipment_id] = equipment
            ###############
            ##
            ### add the equipment graph and respective edges
            ##
            ###############

        else:
            equipment = node_instance.node_equipment_dictionary[equipment_id]
        if subequipment_id not in equipment.node_subequipment_dictionary.values():
            subequipment = SubEquipment()
            subequipment.name = subequipment_name
            subequipment.id = subequipment_id
        else:
            subequipment = equipment.node_subequipment_dictionary[subequipment_id]
            ##########3
            ###3   add subequipment graph and edges and interface_type
            ##
            ############

    ############**********
    def create_node_instance(self, node_name,
                             coords):  # node_id,node_name,longitude,latitude,equipment_name,subequipment_name):
        # print("creating node instance on the canvas")
        attributes = node_type[node_name]
        name = attributes["name"]
        if name == "Cl":
            node = Client_Node(self.topology.node_numbers)
            node.canvas_coords = coords
            # client
        elif name == "S":
            node = Server(self.topology.node_numbers)
            node.canvas_coords = coords
            # Server
        elif name == "Acc":
            node = Access_Node(self.topology.node_numbers, 0)
            node.canvas_coords = coords
            # Access_Network_Node
            # Access_Network_Node
        elif name == "M":
            node = Metro(self.topology.node_numbers, 0)
            node.canvas_coords = coords
            # Metro_Network_Node
        elif name == "CN":
            node = Core(self.topology.node_numbers, 0)
            node.canvas_coords = coords
            # Core_Network_Node
        elif name == "P":
            node = P_Node(self.topology.node_numbers, 0)
            node.canvas_coords = coords
            # P_Network_Node
        elif name == "CD":
            node = Core_Node(self.topology.node_numbers, 0)
            node.canvas_coords = coords
            # Core_DC_Node
        elif name == "Edg":
            node = Edge_Node(self.topology.node_numbers, 0, 0)
            node.canvas_coords = coords
            # Edge_DC_Node
        elif name == "Prb":
            node = Probe_Node(self.topology.node_numbers)
            self.canvas_coords = coords

        elif name == "Cntrlr":
            node = Controller(self.topology.node_numbers)
            node.start_controller(self.topology)

            self.canvas_coords = coords

        elif name == "WB":
            node = White_Box(self.topology.node_numbers)
            self.canvas_coords = coords

        elif name == "Sw":
            node = Switch(self.topology.node_numbers)
            self.canvas_coords = coords

        elif name == "R":
            node = Router(self.topology.node_numbers)
            self.canvas_coords = coords

        elif name == "F":
            node = Firewall(self.topology.node_numbers)
            self.canvas_coords = coords
        elif name == "Dci":
            node = DataCenter_Interconnect(self.topology.node_numbers)
            self.canvas_coords = coords
        elif name == "G":
            node = Gateway(self.topology.node_numbers)
            self.canvas_coords = coords
        elif name == "Agdc":
            node = Aggregation_DC_Node(self.topology.node_numbers)
            self.canvas_coords = coords
        elif name == "Ag":
            node = Aggregation_Node(self.topology.node_numbers)
            self.canvas_coords = coords
        else:
            print("node not identified")
            node = ""
            # new node

        self.topology.node_instance_dictionary_by_node_id[self.topology.node_numbers] = node

        self.topology.node_numbers += 1
        return node

    def read_topology_from_xml(self):
        pass


##################################################################  Node Attributes
####################################################################################



####################################################################################### display
#######################################################################################

class Network():
    def __init__(self, topology, simulation):
        # self.topology=Three_Tier_Topology()
        self.node_list = ""
        self.topology = topology  # )
        self.simulation = simulation
        self.topology.draw_Network()

        # self.topology.create_network()
        # self.node_list=self.topology.nodes_list
        # self.edge_list=self.topology.edge_list
        # print(self.edge_list)
        # self.display_instance()

    def display_instance(self, master, le):
        # master=Tk()
        self.network_frame = Network_Frame(master, self.topology, self.simulation)
        self.information_frame = Information_Frame(self.network_frame.canvas, le, self.simulation, self.topology)
        self.network_frame.information_frame = self.information_frame
        self.information_frame.network_frame = self.network_frame
        self.node_frame = Node_Frame(master, self.network_frame, self.simulation)


        # self.information_frame.load_frame()
        self.network_frame.show_topology_on_frame()
        self.network_frame.node_numbers = self.topology.graph.number_of_nodes()
        self.node_frame.create_window_pane_for_network_node_labels()

        self.node_frame.create_onboarding_portal()


    def equipment_creation_handler(self, topology, node_instance):
        pass

    def subequipment_creation_handler(self, topology, node_instance, subequipment_instance):
        # noe_instance is equipment_instance
        # on clicking the sub equipment from cards list in information frame call this function
        # call subequipment method to put the data to the equipment and equipment
        pass


class Node_Frame():
    def __init__(self, master, network_frame, simulation):
        self.simulation = simulation
        self.master = master
        self.network_frame = network_frame



    def create_onboarding_portal(self):
        self.onboarding_portal_flag=0
        self.verifier_ballot = Frame(self.network_frame.canvas)
        self.verifier_window=self.network_frame.canvas.create_window(canvas_width/2,100,window=self.verifier_ballot,width=200,height=100)
        self.verifier_ballot.pack()
        self.verifier_label=Label(self.verifier_ballot,text="Verifier")
        self.verifier_label.pack()
        #self.onboarding_portal_button=Button(self.onboarding_button_frame,text="Onboarding Portal",command=self.add_onboarding)
        #self.hide_onboarding_button=Button(self.onboarding_button_frame,text="Hide Onboarding",command=self.remove_onboarding)
        #self.onboarding_portal_button.pack(side="top")
        #self.hide_onboarding_button.pack(side="top")



    def add_onboarding(self):
        if self.onboarding_portal_flag==0:
            self.onboarding_portal_flag=1
            self.onboarding_portal = Onboarding_Portal()
            self.onboarding_portal.create_onboarding_portal_window(self.master, self)


    def remove_onboarding(self):
        self.onboarding_portal.exit_onboarding_portal()
        self.onboarding_portal_flag=0

    def moving_back_to_verifier(self):
        #self.onboarding_portal_button = Button(self.master, text="Onboarding Portal",command=self.onboarding_portal.create_onboarding_portal_window(self.master, self.onboarding_portal_button, self))
        #self.onboarding_portal_button.pack(side="top")
        pass

    def create_window_pane_for_network_node_labels(self):
        # network_nodes_button=Button(self.canvas,"Network Nodes")
        nodemenubar = Menu(self.master)
        nodemenubar.add_command(label="Network Nodes",
                                command=self.network_frame.create_window_pane_for_generic_network_node_labels)
        nodemenubar.add_command(label="SDN Nodes",
                                command=self.network_frame.create_window_pane_for_sdn_network_node_labels)
        nodemenubar.add_command(label="Probe Nodes",
                                command=self.network_frame.create_window_pane_for_probe_network_node_labels)
        nodemenubar.add_command(label="Data Center Nodes",
                                command=self.network_frame.create_window_pane_for_data_center_node_labels)
        nodemenubar.add_command(label="Client Server Nodes",
                                command=self.network_frame.create_window_pane_for_client_server_node_labels)
        nodemenubar.add_command(label="General Nodes",
                                command=self.network_frame.create_window_pane_for_general_nodes_label)
        nodemenubar.add_command(label="Onboarding Portal",command=self.add_onboarding)
        nodemenubar.add_command(label="Hide Onboarding Portal", command=self.remove_onboarding)
        nodemenubar.add_command(label="Show Information",
                                command=self.network_frame.information_frame.create_info_frame)
        nodemenubar.add_command(label="Hide Information",command=self.network_frame.information_frame.hide_info_frame)
        self.master.config(menu=nodemenubar)


le = Load_Network_Information()
simulation = Simulation()
# simulation.start_ip_simulation()
print("network graph ", le.topology.graph)
network = Network(le.topology, simulation)
master = Tk()
master.title("Verifier")
master.minsize(500, 500)
network.display_instance(master, le)
# simulation.environment.run(until=100)
master.mainloop()

# network.


