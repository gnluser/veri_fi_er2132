import networkx as nx
# import numpy as np
#from topology import Topology

try:
    from tkinter import *
except ImportError:
    from Tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
# from variables import *
import math
#from network_equipment import *
import csv

class Network():
    def __init__(self,topology):
        self.topology = topology
        self.node_list = self.topology.nodes_list
        self.edge_list = self.topology.edge_list
        print(self.edge_list)


class Network_frame():
    network_size_x, network_size_y = 50, 50
    r = 40

    def __init__(self, master, network, iframe):
        self.iframe = iframe
        # pass
        self.inter_node_gap_x = 50
        self.inter_node_gap_y = 20
        self.node_start_x = 40
        self.node_radius = 20
        self.network_frame_width = 700
        self.network_frame_height = 1000
        self.frame = Frame(master, width=self.network_frame_width, height=self.network_frame_height)
        self.frame.pack(side=RIGHT)
        canvas = Canvas(self.frame, width=self.network_frame_width, height=self.network_frame_height, bd=20)
        canvas.pack(side=BOTTOM)
        self.creating_network_systems(master, canvas, network)
        self.equipment_node = {}

    def next_node_coordinates(self):
        # following an elliptical curve trace for node display.
        #
        a, b = self.network_frame_width, self.network_frame_height

        if self.direction == "NE":
            if self.x + self.inter_node_gap_x > self.network_frame_width:
                self.direction = "NW"
                self.x -= self.inter_node_gap_x
                # self.y=math.sqrt(((a*a-self.x*self.x)*b*b)/a*a)
                self.y -= self.inter_node_gap_y
            else:
                self.x += self.inter_node_gap_x
                # self.y=math.sqrt(((a*a-self.x*self.x)*b*b)/a*a)
                self.y -= self.inter_node_gap_y

        if self.direction == "NW":
            if self.y - self.inter_node_gap_y < 0:
                self.direction = "SW"
                self.x -= self.inter_node_gap_x
                # self.y=math.sqrt(((a*a-self.x*self.x)*b*b)/a*a)
                self.y += self.inter_node_gap_y
            else:
                self.x -= self.inter_node_gap_x
                # self.y=math.sqrt(((a*a-self.x*self.x)*b*b)/a*a)
                self.y -= self.inter_node_gap_y

        if self.direction == "SW":
            if self.x - self.inter_node_gap_x < 0:
                self.direction = "SE"
                self.x -= self.inter_node_gap_x
                # self.y=math.sqrt(((a*a-self.x*self.x)*b*b)/a*a)
                self.y += self.inter_node_gap_y
            else:
                self.x -= self.inter_node_gap_x
                # self.y=math.sqrt(((a*a-self.x*self.x)*b*b)/a*a)
                self.y += self.inter_node_gap_y
        if self.direction == "SE":
            if self.y + self.inter_node_gap_y > self.network_frame_height:
                self.direction = "NE"
                self.x += self.inter_node_gap_x
                # self.y=math.sqrt(((a*a-self.x*self.x)*b*b)/a*a)
                self.y -= self.inter_node_gap_y
            else:
                self.x += self.inter_node_gap_x
                # self.y=math.sqrt(((a*a-self.x*self.x)*b*b)/a*a)
                self.y += self.inter_node_gap_y

    def creating_network_systems(self, master, canvas, network):
        self.x = self.node_start_x
        self.y = self.network_frame_height / 2
        self.direction = "NE"
        self.nodes_id = {}
        self.nodes_covered = {}
        self.coordinates_occupied = []
        self.node_names_dictionary = {}

        for line in nx.generate_adjlist(network.topology.graph, delimiter=","):
            node_list = line.split(",")
            node0 = node_list[0]

            if node0 not in self.nodes_covered.keys():
                node0_id = self.create_node(canvas)
                self.nodes_covered[node0] = node0_id
                self.node_names_dictionary[node0_id] = node0
                # self.x,self.y=
                # self.next_node_coordinates()

            else:
                node0_id = self.nodes_covered[node0]
            for node1 in node_list[1:]:

                if node1 not in self.nodes_covered.keys():
                    node1_id = self.create_node(canvas)
                    self.nodes_covered[node1] = node1_id
                    self.node_names_dictionary[node1_id] = node1
                    # self.x,self.y=\
                    # self.next_node_coordinates()

                else:
                    node1_id = self.nodes_covered[node1]
                self.create_edge(canvas, node0_id, node1_id)

        '''
        #node_radius
        for edge in network.edge_list:
            node0=edge[0]
            node1=edge[1]

        for nodes in network.node_list:
            node_id=self.create_node(canvas,x,y,node_radius)#mention only center of node
            self.nodes_id[nodes]=node_id
            if x+50 > network_frame_width:
                x= 50
                y+=50
            else:
                x+=50
        for edge in network.edge_list:
            self.create_edge(canvas,edge)
        #canvas.create_oval(100,100,150,150,fill="cyan")
        #canvas.create_oval(200,100,250,150,fill="cyan")
        #canvas.create_line()
        '''

    def create_node(self, canvas):
        self.next_node_coordinates()
        # coords=xr-r,yr-r,xr+r,yr+r

        coords = self.x - self.node_radius, self.y - self.node_radius, self.x + self.node_radius, self.y + self.node_radius
        node_id = canvas.create_oval(coords, fill="red")
        # node_id.bind("<Button-1",self.node_click)
        canvas.tag_bind(node_id, "<Button-1>", lambda event: self.node_click(event, node_id))
        print(node_id, self.direction, self.x, self.y, "\n", )
        return node_id

    def node_click(self, event, node_id):
        print("node clicked", event.x, event.widget)
        '''
        if(self.iframe.vendor_list_box.count>0):
            self.iframe.vendor_list_box.delete(0,END)
            self.iframe.equipment_list_box.delete(0,END)
            self.iframe.cards_list_box.delete(0,END)
        '''
        print(self.node_names_dictionary[node_id])
        # self.equipment_node[node_id]=
        self.iframe.property_selection(node_id)
        # print([node,tnode_id for node,tnode_id in self.nodes_covered.items()][node_id])# in self.nodes_covered.items() if tnode_id == node_id)
        # print(self.nodes_covered.keys()[list(self.nodes_covered.values()).index(node_id)])

    def create_edge(self, canvas, node0_id, node1_id):

        x1, y1, x2, y2 = canvas.coords(node0_id)
        a1, b1, a2, b2 = canvas.coords(node1_id)
        if x1 < a1:
            coords = x2, (y1 + y2) / 2, a1, (b1 + b2) / 2
            canvas.create_line(coords)
        elif x1 >= a1:
            coords = x1, (y1 + y2) / 2, a2, (b1 + b2) / 2
            canvas.create_line(coords)

            # for node in edge:
            #   #print(canvas.coords(self.nodes_id[node]))
            #    #self.nodes_id[node]


class network_nms_frame():
    def __init__(self, master):
        pass


class Information_frame():
    def __init__(self, master, network, ne):
        self.ne = ne
        self.information_frame_height = 1000
        self.information_frame_width = 200
        self.inf_frame = Frame(master, height=self.information_frame_height, width=self.information_frame_width, bd=4)
        self.inf_frame.grid()
        self.inf_frame.pack(side=LEFT)
        vendor_label = Label(self.inf_frame, text="Select vendor")
        vendor_label.pack()
        self.load_frame()
        self.current_node = ""
        self.current_vendor_name = ""
        self.network_equipments_on_nodes = {}
        # self.test_text="rttt"
        # self.property_selection()

    def equipment_property_load(self, event):
        index = int(event.widget.curselection()[0])
        equipment_name = event.widget.get(index)
        new_equipment = Equipment()
        self.network_equipments_on_nodes[self.current_node] = new_equipment
        new_equipment.equipment_properties_dict = \
        self.ne.network_equipment_vendor_dict[self.current_vendor_name].equipment_dict[
            equipment_name].equipment_properties_dict
        self.cards_list_box.delete(0, END)
        for prop in new_equipment.equipment_properties_dict.values():
            self.equipment_list_box.insert(END, prop)

    def equipment_load(self, event):
        # print("venjgbnbfdjnlgkdmnlbfkn")
        index = int(event.widget.curselection()[0])

        self.current_vendor_name = event.widget.get(index)
        print("current vendor", self.current_vendor_name)
        # self.equipment_options = self.ne.calling_equipment_names(vendor_name)
        # self.equipment_list_box.delete(0,END)
        # for eq in self.equipment_options:
        #    self.equipment_list_box.insert(END,eq)

    def load_frame(self):
        self.vendor_options = []
        # test_option=[1,2,3,4,5]
        self.equipment_options = []
        self.cards_option = []
        self.vendor_list_box = Listbox(self.inf_frame, bd=5, exportselection=0)
        self.vendor_list_box.pack(side=TOP)
        self.vendor_list_box.bind('<<ListboxSelect>>', self.equipment_load)
        self.equipment_list_box = Listbox(self.inf_frame, bd=5, exportselection=0)
        self.vendor_list_box.bind('<<ListboxSelect>>', self.equipment_property_load)
        self.cards_list_box = Listbox(self.inf_frame, bd=5, exportselection=0)
        self.vendor_list_box.pack()
        self.equipment_list_box.pack()
        self.cards_list_box.pack()
        '''
        vendor_default_name=StringVar()
        equipment_default_name=StringVar()
        cards_default_name=StringVar()
        equipment_default_name.set("equipment_name")
        cards_default_name.set("cards")
        vendor_default_name.set("vendor_name")
        self.equipment_option = OptionMenu(self.inf_frame, equipment_default_name, self.equipment_options)
        self.cards_option = OptionMenu(self.inf_frame, cards_default_name, self.cards_option)
        OptionMenu(self.inf_frame,"num",test_option).pack()
        self.vendor_option = OptionMenu(self.inf_frame, vendor_default_name, self.vendor_options)
        self.vendor_option.pack()

        self.equipment_option.pack()
        self.cards_option.pack()
        '''

    def property_selection(self, node_id):
        self.vendor_options = self.ne.calling_vendor_names()
        self.current_node = node_id
        self.vendor_list_box.delete(0, END)
        for ven in self.vendor_options:
            self.vendor_list_box.insert(END, ven)
        print(self.vendor_options)
        '''
        self.vendor_list_box.curselection()
        vendor_name=self.vendor_list_box.get(ACTIVE)
        self.equipment_options=self.ne.calling_equipment_names(vendor_name)
        #print(self.vendor_list_box.get(ACTIVE))
        print(self.equipment_options)
        for eq in self.equipment_options:
            self.equipment_list_box.insert(END,eq)
        self.equipment_list_box.curselection()
        equipment_name=self.equipment_list_box.get(ACTIVE)
        new_equipment=Equipment()
        new_equipment.equipment_properties_dict=self.ne.network_equipment_vendor_dict[vendor_name].equipment_dict[equipment_name].equipment_properties_dict
        for prop in new_equipment.equipment_properties_dict.values():
            self.equipment_list_box.insert(END,prop)
            print(vendor_name,equipment_name,prop)

        return new_equipment

        #print(self.test_text)
        #self.test_text+="t"
        pass
        '''

'''


    def __init__(self):
        self.g= nx.Graph()
        self.topology= Topology()
        self.g.add_nodes_from(self.topology.nodes_list)
        self.g.add_edges_from(self.topology.edge_list)
        self.window_root=Tk()
        self.window_root.wm_title("Network topology")
        print("network topology created")



    def display_information_window(self):
        #topology_frame=Frame(window_root)
        #topology_frame.pack()
        equipment_frame=Frame(self.window_root)
        equipment_frame.pack(side=BOTTOM)
        vendor_button=Button(equipment_frame,text="Vendor Name",fg="green")
        equipment_button = Button(equipment_frame, text="Equipment Name", fg="green")
        property_button = Button(equipment_frame, text="Equipment Properties", fg="green")
        vendor_button.pack(side=LEFT)
        equipment_button.pack(side=LEFT)
        property_button.pack(side=LEFT)

        #label=Label(window_root,text="first label")
        #
        # label.pack()
        #window_root.mainloop()



    def node_click_event(self):
        print("node clicked")



    def topology_information_window(self):
        network_graph_frame = Frame(self.window_root)
        network_graph_frame.pack()
        canvas=Canvas(network_graph_frame,bg="red",height=200,width=200)
        line_coordinate = 10, 10, 100, 100
        #initial_node_center_coordinate=20,20
        x,y=20,20
        self.distance=30
        canvas.create_arc(line_coordinate, start=0, extent=150, fill="blue")
        canvas.pack()
        self.node_radius=20
        self.network_nodes={}
        xr,yr=x,y
        for node in self.topology.nodes_list:
            node_coordinate=xr-self.node_radius,yr-self.node_radius,xr+self.node_radius,yr+self.node_radius
            self.network_nodes[node]=canvas.create_oval(node_coordinate,fill="cyan")
            canvas.tag_bind(self.network_nodes[node],"<Button-1>",self.node_click_event())
            xr+=self.distance
            yr+=self.distance


        #self.window_root.mainloop()





################################
################################
def display_network_with_mtplb(network):
    #nx.draw(network.g)
    fig = Figure()
    nx.draw(network.g,ax=fig.add_subplot(111))
    #fig.add_subplot(nx.draw(network.g))
    topology_frame = Frame(network.window_root)
    canvas=Canvas(network.window_root,bg="red",height=100,width=200)
    #canvas = FigureCanvasTkAgg(fig, master=topology_frame)
    ##canvas.show()
    #canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
    topology_frame.pack()

    ##graph_frame=Frame(window_root)
    ##window_root.frame.pack()
    ##plt.draw()
    ##plt.show()



def tkinter_function():
    window=Tk()
    frame=Frame(window)
    frame.pack(side=BOTTOM)
    frame2=Frame(window)
    frame2.pack()
    canvas=Canvas(frame,bg="blue",height=400,width=400)
    coordinate=1,1,80,80
    #canvas.create_arc(coordinate,fill="red")
    button=Button(frame2,text="button")
    button.pack()
    canvas.create_oval(80,80,100,100,fill="white")
    canvas.create_oval(120, 120, 140, 140, fill="white")
    canvas.create_line(100,100,120,120,fill="yellow")
    canvas.pack()
    window.mainloop()

#tkinter_function()

############################################################
############################################################


network=Network()
network.display_information_window()
network.topology_information_window()
network.window_root.mainloop()
#print("exit")
#network.display_window()
#display_network_with_mtplb(network)
#network.display_network()
'''

# import networkx as nx


data_file = "/home/gnl/Desktop/mankul/flask_project/sdnProject0.2/equipments.csv"
component_name = 'component name'
ports_per_cards = 'ports on cards/equipment'
throughput = 'Throughput'
line_rate = 'Mpps'
line_cards = 'line cards'
protocol = 'Feature and protocols'
layer_2 = "Layer 2 features"
layer_3 = 'Layer 3 features'
usage = 'usage'
equipment_vendors = ['cisco', 'juniper', 'nokia', 'arista', 'ciena', 'huawei', 'fujitsu']
equipment_properties = [component_name, ports_per_cards, throughput, line_rate, line_cards, protocol, layer_2, layer_3,
                        usage]


class Load_Network_Information():
    def __init__(self):
        ne = Network_Equipments()
        ne.loading_equipments_list()
        self.ne = ne
        self.vendor_name = ""
        self.network_deployed_equipment_dict = {}
        self.network_equipment_dict = {}


class Network_Equipments:
    def __init__(self):
        self.network_equipment_vendor_dict = {}
        self.per_vendors_equipments_list = []

        # for items in equipment_properties:
        #    print items

    def loading_equipments_list(
            self):  # equipment list is loaded in vendor_instance's variable component_list dictionary with all names in list equipment_properties
        self.dictionary_list = []
        dictionary_equipments = []
        data = csv.DictReader(open(data_file, 'r'))
        for row in data:
            self.dictionary_list.append(row)  # row is an open dictionary object

        '''
        for row  in data:
            self.dictionary_list.append(row)
            print(row)
        print(self.dictionary_list[3])
        print(self.dictionary_list[3][component_name])
        print(self.dictionary_list[3][ports_per_cards])
        print(self.dictionary_list[3][throughput])
        print(self.dictionary_list[3][line_rate])
        print(self.dictionary_list[3][line_cards])
        print(self.dictionary_list[3][protocol])
        print(self.dictionary_list[3][layer_2])
        print(self.dictionary_list[3][layer_3])
        print(self.dictionary_list[3][usage])
        '''

        for items in self.dictionary_list:
            flag_for_vendor = False
            # loading equipments for all known vendors.
            for vendor_name in equipment_vendors:
                if vendor_name.lower() in (items[component_name]).lower():
                    flag_for_vendor = True
                    if vendor_name not in self.network_equipment_vendor_dict:
                        ####
                        ####Creating new vendor instance for new vendor in list....... vendor instances are in nw_eq_vndr_lst
                        ####
                        vendor_instance = Equipments_per_Vendor()
                        self.network_equipment_vendor_dict[vendor_name] = vendor_instance
                        self.per_vendors_equipments_list.append(vendor_instance)

                    else:
                        ####
                        ####adding new equipment in list information to vendor instance
                        ####
                        vendor_instance = self.network_equipment_vendor_dict[vendor_name]
                    # print(vendor_instance.func())
                    if items[
                        component_name] not in vendor_instance.equipment_names_list:  # to avoid reloading same properties if present in csv file
                        vendor_instance.equipment_names_list.append(items[component_name])
                    if items[component_name] not in vendor_instance.equipment_dict.keys():
                        new_equipment = Equipment()
                        new_equipment.equipment_properties(items)
                        vendor_instance.equipment_dict[items[component_name]] = new_equipment
                        # print(vendor_instance.equipment_dict.values())
                        '''
                            vendor_instance.equipment_dict[items[component_name]]=new_equipment
                        for element in equipment_properties:
                            vendor_instance.equipment_dict[items[component_name]].equipment_properties_dict[element]=items[element]
                            vendor_instance.component_list[element]=items[element]
                        '''




                        # if self.vendor_instance.eqipment_list is N
                        # if items[component_name].lower in equipment_vendors:
                        # print(items[component_name])
                        # else:
                        #   print("vendor name not identified for ",items[component_name])
            if flag_for_vendor == False:
                print("vendor name not identified for ", items[component_name])

    def calling_vendor_names(self):
        # forwarding json  file to app to gorward it to the web page
        return equipment_vendors

    def calling_equipment_names(self, vendor_name):
        return self.network_equipment_vendor_dict[vendor_name].returning_equipment_names()


###each time new instance created, vendor instance is added to network_equipment_vendor_dict dictionary of ne

class Equipments_per_Vendor:
    # equipment_dict={}
    # component_property={}
    def __init__(self):
        self.equipment_dict = {}
        self.component_list = {}
        self.component_properties_list = []
        self.equipment_names_list = []
        # print("equipment per vendor created")

    def returning_equipment_names(self):
        print("returning equipment names for specific vendor")
        return self.equipment_names_list


class Equipment:
    # equipment_properties_dict={}
    def __init__(self):
        self.name = ""
        self.equipment_properties_dict = {}

    def equipment_properties(self, items):
        for element in items:
            self.equipment_properties_dict[element] = items[element]


# ne= Network_Equipments()
# ne.loading_equipments_list()

'''
with open(data_file,'r') as data_csv:
    data=csv.reader(data_csv,delimiter=",", quotechar='|')
    for row in data:
        print row[0]
''
d=open(data_file)
print d.read()
'''



class Topology():

    def __init__(self):
        self.edge_list = []
        self.nodes=20
        self.nodes_list=range(1,self.nodes+1)
        self.graph=nx.Graph()
        self.graph.add_nodes_from(self.nodes_list)
        self.create_network_topology()
        self.graph.add_edges_from(self.edge_list)
        print(self.edge_list)
        print(self.nodes_list)


    def network_graph(self):
        pass

    def create_network_topology(self):
        #create topology
        for node in self.nodes_list:
            if node%self.nodes>0:
                self.edge_list.append([node,node+1])




topology=Topology()
network = Network(topology)
root = Tk()

ne = Network_Equipments()
ne.loading_equipments_list()
iframe = Information_frame(root, network, ne)
nframe = Network_frame(root, network, iframe)

root.mainloop()
