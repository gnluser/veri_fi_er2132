# from node import *
from all_dependencies import *
from info_frame import *
from nw_frame import *
from service_module import *
from simulation import *

#from equipments import *

# from network_equipment import *


############################################################################
###############################################################################################
###############################################################################################556



##################################################################################################################
##################################################################################################################


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
            print("error in topology creation")
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
    def __init__(self, topology, simulation,services_and_operations):
        # self.topology=Three_Tier_Topology()
        self.node_list = ""
        self.topology = topology  # )
        self.simulation = simulation
        self.topology.draw_Network()
        self.services_and_operations=services_and_operations

        # self.topology.create_network()
        # self.node_list=self.topology.nodes_list
        # self.edge_list=self.topology.edge_list
        # print(self.edge_list)
        # self.start_project()

    def start_project(self, master, le):
        # master=Tk()
        self.network_frame = Network_Frame(master, self.topology, self.simulation)
        self.information_frame = Information_Frame(self.network_frame.canvas, le, self.simulation, self.topology)
        self.network_frame.information_frame = self.information_frame
        self.information_frame.network_frame = self.network_frame
        self.node_frame = Node_Frame(master, self.network_frame, self.simulation,self.topology,self.services_and_operations)
        self.name_of_project()

        # self.information_frame.load_frame()
        self.network_frame.show_topology_on_frame()
        self.network_frame.node_numbers = self.topology.graph.number_of_nodes()
        self.node_frame.create_window_pane_for_network_node_labels()

        self.node_frame.create_service_box()

        self.node_frame.create_onboarding_portal()



    def name_of_project(self):
        self.verifier_ballot = Frame(self.network_frame.canvas)
        self.verifier_label=Label(self.verifier_ballot,text="Verifier")
        self.verifier_window = self.network_frame.canvas.create_window(canvas_width/2,100, window=self.verifier_ballot, width=100,height=50)
        self.verifier_label.pack()
        self.verifier_ballot.pack()

    def equipment_creation_handler(self, topology, node_instance):
        pass

    def subequipment_creation_handler(self, topology, node_instance, subequipment_instance):
        # noe_instance is equipment_instance
        # on clicking the sub equipment from cards list in information frame call this function
        # call subequipment method to put the data to the equipment and equipment
        pass


class Node_Frame():
    def __init__(self, master, network_frame, simulation,topology,services_and_operations):
        self.simulation = simulation
        self.master = master
        self.network_frame = network_frame
        self.topology=topology
        self.services_and_operations=services_and_operations



    def delete_service_frame(self):
        self.network_frame.canvas.delete(self.service_window)
        self.rollback_nodes_canvas_attributes()

    def add_service_frame(self):
        self.service_window=self.network_frame.canvas.create_window(canvas_width-350,200,window=self.service_frame,width=200,height=400)
        self.firstbutton.configure(command=lambda: self.selecting_left_nodes_for_service())
        self.scndbutton.configure(command=lambda: self.selecting_right_nodes_for_service())
        self.node_selection_button.configure(command=lambda: self.network_frame.allow_node_selection_for_service(self.service_nodes))
        #self.service_frame.pack()
        #self.node_selection_button.pack(side="top")
        self.node_selection_button.grid(row=0,sticky=N+E+W+S)
        self.firstbutton.grid(row=1,sticky=N+E+W+S)#.pack(side="top")
        self.scndbutton.grid(row=2,sticky=N+E+W+S)#.pack(side="top")
        self.service_list_box.grid(row=3,rowspan=5,sticky=N+E+W+S)#.pack(side="top")
        self.identify_service_compatibility_button.grid(row=8,sticky=N+E+W+S)#.pack(side="top")
        self.select_services_button.grid(row=9,sticky=N+E+W+S)#.pack(side="top")
        self.identify_service_compatibility_button.configure(command=lambda:self.identify_service_compatibility(self.service_list_box))
        self.select_services_button.configure(command=lambda: self.start_service(self.service_list_box))


    def identify_service_compatibility(self,listbox):
        for service_name in listbox:
            for left_node,right_node in self.service_nodes.nodes_pair.keys():
                s=self.topology.graph.all_shortest_path(left_node,right_node)
                print("For nodes ",left_node,"\t",right_node," shortest paths are ",s)



    def start_service(self,listbox):
        indices = listbox.curselection()
        nodes_pairs = [(x, y) for x in self.service_nodes.dictionary_left_nodes.values() for y in self.service_nodes.dictionary_right_nodes.values()]
        for nodepair in nodes_pairs:
            node_pair = Node_Pair(nodepair)
            self.service_nodes.nodes_pair[nodepair]=node_pair

        for index in indices:
            service_name=listbox.get(index)
            service=Service(service_name,self.service_nodes,self.topology,self.services_and_operations)
            service.allocate_service(self.topology)

        for nodepair in nodes_pairs:
            node_pair=self.service_nodes.nodes_pair[nodepair]
            self.services_and_operations.service_and_op_dictionary[node_pair] = node_pair.allocated_services




    def create_service_box(self):
        self.service_nodes=Service_Nodes()
        self.service_frame=Frame(self.network_frame.canvas)
        self.node_selection_button=Button(self.service_frame,text="Select nodes for Service",bg=button_color)
        self.firstbutton=Button(self.service_frame,text="Click for Ist set",bg=button_color)
        self.scndbutton=Button(self.service_frame,text="Click for 2nd set",bg=button_color)
        self.service_option_label=Label(self.service_frame,text="Service Options",bg=button_color)
        self.service_list_box=Listbox(self.service_frame,selectmode=MULTIPLE,bg=entry_color)
        for item in service_options_list:
            self.service_list_box.insert(END,item)
        self.select_services_button=Button(self.service_frame,text="Start Services",bg=button_color)
        self.identify_service_compatibility_button=Button(self.service_frame,text="Identify Service Comaptibilty",bg=button_color)

        #self.service_list_box.bind("<<ListboxSelect>>")

    def selecting_right_nodes_for_service(self):
        print("second button pressed and nodes are ")
        self.service_nodes.dictionary_right_nodes=self.network_frame.node_dict_for_service
        self.service_nodes.node_dict_for_service={}
        print("set 2 nodes are ",self.service_nodes.dictionary_right_nodes)
        #self.rollback_nodes_canvas_attributes()

    def selecting_left_nodes_for_service(self):
        print("ist node button pressed and nodes selected are ")
        self.service_nodes.dictionary_left_nodes=self.network_frame.node_dict_for_service
        self.network_frame.node_dict_for_service={}
        print("set 1 is ", self.service_nodes.dictionary_left_nodes)

    def rollback_nodes_canvas_attributes(self):
        self.network_frame.close_node_selection_for_service(self.service_nodes)


    def create_onboarding_portal(self):
        self.onboarding_portal_flag=0

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
        nodemenubar.add_command(label="Service",command=self.add_service_frame)
        nodemenubar.add_command(label="Service Frame Hide",command=self.delete_service_frame)
        nodemenubar.add_command(label="Start random traffic",command=self.simulation.resume_traffic(self.topology,self.services_and_operations))
        self.master.config(menu=nodemenubar)


le = Load_Network_Information()
simulation = Simulation()
# simulation.start_ip_simulation()
print("network graph ", le.topology.graph)
services_and_operations=Services_and_Operations()
network = Network(le.topology, simulation,services_and_operations)
master = Tk()
master.title("Verifier")
master.minsize(500, 500)
network.start_project(master, le)

# simulation.environment.run(until=100)
master.mainloop()

# network.
