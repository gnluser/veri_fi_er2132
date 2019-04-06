
try:
    import networkx as nx
    import simpy
    import csv
    import time
    from functools import partial
    import random
    import numpy as np
except ValueError as error:
    print("import error", error.args)
    exit(1)
#
try:
    from tkinter import *
except ImportError:
    from Tkinter import *



data_file = "/home/gnl/Desktop/mankul/verifier/verifier/csv_files/network_equipments_10_3_2019 - Sheet1.csv"#Network Equipments (Updated) - Sheet1.csv"#network_equipments_2_Sheet1.csv"#equipments.csv"
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
                     "DCI": {"color": "skyblue3", "radius": "14", "name": "Dci", "distance": 0}}
network_node_type = {
    "Provider": {"color": "pink", "radius": "14", "name": "P", "distance": 170}, \
    "Core": {"color": "blue", "radius": "14", "name": "CN", "distance": 0}, \
    "Metro": {"color": "brown", "radius": "13", "name": "M", "distance": 100}, \
    "Access": {"color": "orange", "radius": "12", "name": "Acc", "distance": 350}, \
    "Aggregation": {"color": "lightgreen", "radius": "12", "name": "Ag", "distance": 0}}

data_center_node_type = {"Aggregation": {"color": "coral", "radius": "13", "name": "Agdc", "distance": 290, }, \
                         "Edge": {"color": "orangered", "radius": "13", "name": "Edg", "distance": 250}, \
                         "Core": {"color": "cyan", "radius": "14", "name": "CD", "distance": 200}}

sdn_node_type = {"White Box": {"color": "grey", "radius": "12", "name": "WB", "distance": 0}, \
                 "Controller": {"color": "lightblue", "length": "50", "breadth": "20", "name": "Cntrlr", "distance": 0}}
client_server_node_type = {"Server": {"color": "salmon", "length": "15","breadth":"15", "name": "S", "distance": 300}, \
                           "Client": {"color": "green", "length": "12","breadth":"12", "name": "Cl", "distance": 380}}

probe_node_type = {"Probe": {"color": "yellow", "length": "10", "breadth": "10", "name": "Prb", "distance": 0}}

service_color="gold"
button_color="yellow"
label_color="cyan"
entry_color="lightblue"
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

number_of_packets=1000

service_options_list=["ECMP"]

canvas_color="azure"
outer_frame_color="red"

node_option_frame_color="lemon chiffon"#"lightyellow"
background_canvas_color = node_option_frame_color  # label_color
background_label_color = "gainsboro"#"whitesmoke"

window_background_color="white"


