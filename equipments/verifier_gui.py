# from node import *
from all_dependencies import *
from info_frame import *
from nw_frame import *
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
