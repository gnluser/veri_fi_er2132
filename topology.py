import networkx as nx
import math
from network_graph import *



class Three_Tier_Topology():

    def __init__(self):
        #self.edge_list = []
        #self.metro_nodes=50#per core_node
        self.nodes=100#per metro node number of access nodes
        self.node_count=0
        #self.nodes=500
        #nodes interfaces by roadms
        #self.nodes_list=range(1,self.nodes+1)
        self.metro_rings={}
        self.core_rings={}
        self.core_ring_id=0
        self.metro_id=0
        self.graph=nx.Graph()
        self.port_graph=nx.Graph()
        self.fat_tree_k_index = 4
        self.nodes_in_core=3
        self.nodes_in_metro=2 # per core
        self.nodes_in_access=3 # per metro
        self.data_center_dict={}
        self.core_nodes_dict={}
        self.provider_node_dict={}
        self.metro_nodes_dict={}
        self.access_node_dict={}
        self.core_links={}
        self.provider_links={}
        #self.provider_link={}
        self.node_display_attributes={}
        self.port_display_attributes={}
        self.node_objects={}
        self.number_of_clients_per_access=4
        #port_mapping ?? for port mapping with in node


    def create_network(self):
        self.three_tier_topology()
        self.data_center_topology()

    def data_center_topology(self):
        for core_node, p_node_instance in self.provider_node_dict.items():
            #print("direction is ",p_node_instance.direction)
            self.create_data_center_per_core_node(core_node,p_node_instance)

    def create_data_center_per_core_node(self,core_node,p_node_instance):  # data center instance created for every p node per core node
        data_center = Data_Center(self.graph, self.port_graph,self.node_objects,p_node_instance)
        self.data_center_dict[p_node_instance]=data_center
        #data_center.direction=self.update_direction()
        degree=0
        degree_diff=10
        for dc_core_node,dc_core_node_instance in data_center.core_node_dict.items():
            self.graph.add_edge(p_node_instance,dc_core_node_instance)
            dc_core_node_instance.direction=self.update_direction(p_node_instance.distance,p_node_instance.direction,\
                                                                 dc_core_node_instance.distance,degree)
            degree+=degree_diff
            self.node_objects[str(p_node_instance)]=p_node_instance
            self.node_objects[str(dc_core_node_instance)]=dc_core_node_instance
            core_node_port_instance=dc_core_node_instance.north_ports_dict[0]
            p_node_port=p_node_instance.unused_ports.pop(0)
            p_node_port_instance=p_node_instance.port_dict[p_node_port]
            self.port_graph.add_edge(core_node_port_instance,p_node_port_instance)
            #pass#dc_core_node_instance.port_dict

    ############ creating three tier topology ###############################
    #########################################################################
    #########################################################################
    #####1 create core nodes ring

    def three_tier_topology(self):
        self.create_core_nodes_ring()
        #for core_node in range(self.nodes_in_core):
        for provider_node in self.provider_node_dict.values():
            self.create_metro_ring(provider_node)



    def add_ports_edges(self,node_1_instance,node_2_instance):
        port1=node_1_instance.unused_ports.pop(0)
        port2=node_2_instance.unused_ports.pop(0)
        port1_instance=node_1_instance.port_dict[port1]
        port2_instance=node_2_instance.port_dict[port2]
        self.port_graph.add_edge(port1_instance,port2_instance)

    def update_direction(self,distance,direction,distance2,degree):
        radius=distance2-distance
        theta=math.degrees(math.atan((distance*math.sin(math.radians(direction))+radius*math.sin(math.radians(direction+degree)))\
            /(distance*math.cos(math.radians(direction))+radius*math.cos(math.radians(direction+degree+1)))))
        return theta


    def create_core_nodes_ring(self):
        self.core_ring_id+=1
        ring=[]
        core_node_ports=3
        p_node_ports=1+pow(int(self.fat_tree_k_index/2),2)
        degree=0
        core_degree_diff=int(360/self.nodes_in_core)
        for core_node in range(self.nodes_in_core):
            self.core_nodes_dict[core_node]=Core(core_node,core_node_ports)
            self.provider_node_dict[core_node]=P_Node(core_node,p_node_ports)
            self.core_nodes_dict[core_node].direction = degree
            self.provider_node_dict[core_node].direction=degree
            degree+=core_degree_diff

        for core_node in range(self.nodes_in_core):
            provider_node=self.provider_node_dict[core_node]
            core_node_1=self.core_nodes_dict[core_node]
            core_node_2 = self.core_nodes_dict[(core_node+1)%self.nodes_in_core]
            self.graph.add_edge(core_node_1,core_node_2)
            self.node_objects[str(core_node_1)]=core_node_1
            self.node_objects[str(core_node_2)]=core_node_2
            edge=(core_node_1,core_node_2)
            ring.append(edge)
            self.graph.add_edge(core_node_1,provider_node)
            self.node_objects[str(provider_node)]=provider_node
            self.core_links[core_node_1]=provider_node
            self.add_ports_edges(core_node_1,core_node_2)
            ######## this provider node has to be attached with data center
        self.core_rings[self.core_ring_id]=ring




    def create_p_node_metro_linking(self):
        for core_node,provider_node_instance in self.provider_node_dict.items():
            self.create_metro_ring(provider_node_instance)


    def create_metro_ring(self,provider_node_instance):
        metro_nodes_port=10
        self.metro_id+=1
        ring=[]
        degree=0
        #math.degrees(math.atan())
        metro_degree_diff=int(360/self.nodes_in_metro)
        for metro_node in range(self.nodes_in_metro):
            metro_node_instance=Metro(metro_node,metro_nodes_port)
            self.metro_nodes_dict[metro_node]=metro_node_instance
            metro_node_instance.direction=self.update_direction(provider_node_instance.distance,provider_node_instance.direction,\
                                                                metro_node_instance.distance,degree)
            degree+=metro_degree_diff
        self.graph.add_edge(provider_node_instance,self.metro_nodes_dict[0])
        self.provider_links[provider_node_instance]=self.metro_nodes_dict[0]
        for metro_node in range(self.nodes_in_metro):
            metro_node_1=self.metro_nodes_dict[metro_node]
            metro_node_2=self.metro_nodes_dict[(metro_node+1)%self.nodes_in_metro]
            self.graph.add_edge(metro_node_1,metro_node_2)
            self.node_objects[str(metro_node_1)]=metro_node_1
            self.node_objects[str(metro_node_2)]=metro_node_2
            edge=(metro_node_1,metro_node_2)
            ring.append(edge)
            self.add_ports_edges(metro_node_1,metro_node_2)
            self.create_access_network(metro_node_1)
        self.metro_rings[provider_node_instance]=ring



    def create_access_network(self,metro_node): # per moetro node, one access network is created
        access_nodes_port=10
        degree=0
        access_degree_diff=int(360/self.nodes_in_access)
        for access_node in range(self.nodes_in_access):
            access_node_instance=Access_Node(access_node,access_nodes_port)
            self.graph.add_edge(access_node_instance,metro_node)
            self.access_node_dict[access_node] = access_node_instance
            access_node_instance.direction=self.update_direction(metro_node.distance,metro_node.direction,\
                                                                 access_node_instance.distance,degree)
            degree+=access_degree_diff
        for access_node in range(self.nodes_in_access):
            access_node_1=self.access_node_dict[access_node]
            access_node_2=self.access_node_dict[(access_node+1)%self.nodes_in_access]
            self.graph.add_edge(access_node_1, access_node_2)
            self.create_customers(access_node_1)
            self.node_objects[str(access_node_1)]=access_node_1
            self.node_objects[str(access_node_2)]=access_node_2
            self.add_ports_edges(access_node_1, access_node_2)
            self.create_customers(access_node_1)

    def create_customers(self,access_node):
        degree=0
        degree_difference=int(120/self.number_of_clients_per_access)
        for nod_number in range(self.number_of_clients_per_access):
            client_node=Client_Node(nod_number)
            client_node.direction=self.update_direction(access_node.distance,access_node.direction,\
                                                        client_node.distance,degree)
            degree+=degree_difference
            self.graph.add_edge(access_node,client_node)
            self.node_objects[str(client_node)]=client_node

    ########## methods for three tier topology ends here ########################
    #############################################################################
    #############################################################################


    def network_graph(self):
        pass

    def create_network_topology(self):
        # create topology
        for node in self.nodes_list:
            if node % self.nodes > 0:
                self.edge_list.append([node, node + 1])



    ###### creating data center topology as fat tree topology with k value defined in fat_tree_k_index######
    ########################################################################################################################
    ########################################################################################################################


class Data_Center():
    def __init__(self,graph,port_graph,node_objects,p_node):
        self.core_node_list = []
        self.core_node_dict = {}
        self.fat_tree_k_index = 4
        self.node_count=0
        self.core_nodes = pow(int(self.fat_tree_k_index / 2), 2)
        self.number_of_pods = self.fat_tree_k_index
        self.pod_dict = {}
        self.node_objects = node_objects
        self.graph = graph
        self.port_graph = port_graph
        self.create_pods(p_node)
        self.create_core_nodes(p_node)
        self.data_center_topology()




    def data_center_topology(self):
        self.create_core_to_pod_topology()
        self.create_pod_internal_topology()

    def create_pods(self,p_node):
        for pod_count in range(self.number_of_pods):
            pod_name = "Pod_" + str(pod_count)
            self.pod_dict[pod_name] = Pod(pod_name, self.fat_tree_k_index,p_node)  # creating aggregation and edge switches

    def create_core_nodes(self,p_node):
        degree=0
        core_degree_diff=int(120/self.core_nodes)
        for node in range(self.core_nodes):
            self.node_count += 1
            node_name = "Core_" + str(node)
            core_node = Core_Node(node_name, self.fat_tree_k_index)
            core_node.direction=self.update_direction(p_node.distance,p_node.direction,\
                                                                core_node.distance,degree)
            degree+=core_degree_diff
            self.core_node_list.append(node_name)
            self.core_node_dict[node_name] = core_node
            self.graph.add_node(core_node)
            self.graph.add_edge(core_node,p_node)
            self.node_objects[str(core_node)]=core_node


    def update_direction(self,distance,direction,distance2,degree):
        radius=distance2-distance
        theta=math.atan((distance*math.sin(direction)+radius*math.sin(direction+degree))\
            /(distance*math.cos(direction)+radius*math.cos(direction+degree)))
        return theta


    def create_pod_internal_topology(self):
        for pod_name, pod_instance in self.pod_dict.items():
            self.create_pod_topology(pod_instance)# aggregation and edge nodes

    def create_core_to_pod_topology(self):
        core_node_count=0
        for core_node_name,core_node_instance in self.core_node_dict.items():
            port_count=0
            core_node_count=0
            for e_port,e_port_instance in self.core_node_dict[core_node_name].south_ports_dict.items():
                pod_name="Pod_"+str(port_count)
                aggr_node_instance=self.pod_dict[pod_name].aggregation_node_dict[core_node_count/(int(self.fat_tree_k_index/2))]
                if not self.graph.has_node(aggr_node_instance):
                    self.graph.add_node(aggr_node_instance)
                    self.node_objects[str(aggr_node_instance)]=aggr_node_instance

                if not self.graph.has_edge(core_node_instance, aggr_node_instance):
                    self.graph.add_edge(core_node_instance,aggr_node_instance)
                    self.node_objects[str(core_node_instance)]=core_node_instance
                    self.node_objects[str(aggr_node_instance)]=aggr_node_instance
                i_port_instance=aggr_node_instance.north_ports_dict[core_node_count%(int(self.fat_tree_k_index/2))]
                aggr_node_instance.north_port[i_port_instance]=e_port_instance
                core_node_instance.south_port[e_port_instance]=i_port_instance
                self.port_graph.add_edge(e_port_instance,i_port_instance)
                port_count+=1
            core_node_count+=1


    def create_pod_topology(self,pod_instance):
        self.create_aggr_edge_topology(pod_instance)
        self.create_servers_per_pod(pod_instance)

    def create_aggr_edge_topology(self,pod_instance):
        degree=0
        degree_diff=int(60/pod_instance.k)
        for node_name, aggr_node_instance in pod_instance.aggregation_node_dict.items():
            for port_name, aggr_port_instance in aggr_node_instance.south_ports_dict.items():
                edge_node_instance=pod_instance.edge_node_dict[port_name]
                edge_port_instance=edge_node_instance.north_ports_dict[node_name]
                if not self.graph.has_node(aggr_node_instance):
                    self.graph.add_node(aggr_node_instance)
                    self.node_objects[str(aggr_node_instance)]=aggr_node_instance

                if not self.graph.has_node(edge_node_instance):
                    self.graph.add_node(edge_node_instance)
                    self.node_objects[str(edge_node_instance)]=edge_node_instance
                    edge_node_instance.direction=aggr_node_instance.direction
                if not self.graph.has_edge(aggr_node_instance,edge_node_instance):
                    self.graph.add_edge(aggr_node_instance,edge_node_instance)
                    self.node_objects[str(aggr_node_instance)]=aggr_node_instance
                    self.node_objects[str(edge_node_instance)] = edge_node_instance
                    aggr_node_instance.direction = self.update_direction(pod_instance.p_node.distance,pod_instance.p_node.direction \
                                                                         , aggr_node_instance.distance, degree)
                    edge_node_instance.direction = self.update_direction(pod_instance.p_node.distance,pod_instance.p_node.direction \
                                                                         , edge_node_instance.distance, degree)
                    degree += degree_diff
                self.port_graph.add_node(aggr_port_instance)
                self.port_graph.add_node(edge_port_instance)
                self.port_graph.add_edge(aggr_port_instance,edge_port_instance)
                aggr_node_instance.south_port[aggr_port_instance]=edge_port_instance
                edge_node_instance.north_port[edge_port_instance]=aggr_port_instance



    def create_servers_per_pod(self,pod_instance):#,num_servers):
        edge_count=0

        for edge_node, edge_node_instance in pod_instance.edge_node_dict.items():
            degree = 0
            degree_diff = int(120 / pod_instance.k)
            for port_name , port_instance in edge_node_instance.south_ports_dict.items():#pod_instance.edge_node_dict.south_ports_dict.items():
                server_instance=pod_instance.server_dict[edge_count*int(self.fat_tree_k_index/2)+port_name]
                edge_node_instance.south_port[port_instance]=server_instance
                self.port_graph.add_edge(port_instance,server_instance.port)
                self.graph.add_edge(edge_node_instance, server_instance)
                server_instance.direction=self.update_direction(edge_node_instance.distance,edge_node_instance.direction,\
                                                                server_instance.distance,degree)
                degree+=degree_diff
                self.node_objects[str(edge_node_instance)]=edge_node_instance
                self.node_objects[str(server_instance)]=server_instance
            edge_count+=1


    ################################### ending functions for data center topology creating######################
    ############################################################################################################
    ############################################################################################################


class Network_frame():
    network_size_x, network_size_y = 50, 50
    r = 40

    def __init__(self, master, network, iframe):
        self.iframe = iframe
        # pass
        self.angle = 0
        self.inter_node_gap_x = 50
        self.inter_node_gap_y = 10
        self.node_radius = 10
        self.network_frame_width = 1400
        self.network_frame_height = 1000
        self.frame_width_gap = 100
        self.frame_height_gap = 100
        self.node_start_x = self.network_frame_width / 2  #
        self.node_start_y = self.network_frame_height / 2
        self.node_direction = {}
        self.node_coordinates = {}
        # self.frame=Frame(master,width=self.network_frame_width-self.frame_width_gap,height=self.network_frame_height-self.frame_height_gap,bg='blue',bd=30)
        # self.frame.pack(side=LEFT)
        sbarV = Scrollbar(master, orient=VERTICAL)
        sbarH = Scrollbar(master, orient=HORIZONTAL)

        self.num_node_click = 0
        self.first_node = ""
        self.second_node = ""

        self.network = network
        canvas = Canvas(master, width=self.network_frame_width - self.frame_width_gap,
                        height=self.network_frame_height - self.frame_height_gap, bd=20, bg='pink')
        sbarV.config(command=canvas.yview)
        sbarH.config(command=canvas.xview)
        sbarV.pack(side=RIGHT, fill=Y)
        sbarH.pack(side=BOTTOM, fill=X)
        canvas.config(yscrollcommand=sbarV.set)
        canvas.config(xscrollcommand=sbarH.set)
        canvas.pack(side=BOTTOM, expand=YES, fill=BOTH)
        # self.creating_network_systems(master,canvas,network)
        # self.equipment_node={}
        self.display_network_system(master, canvas, network)

    # ef create_nodes_on_canvas(self,master,canva#
    def display_network_system(self, master, canvas, network):
        self.x = 200  # self.node_start_x
        self.y = self.network_frame_height / 2
        # self.direction = "NE"
        self.nodes_id = {}
        self.nodes_covered = {}
        self.coordinates_occupied = []
        self.node_names_dictionary = {}
        # self.create_nodes_on_canvas(master,canvas,network)
        # self.display_rings(network, canvas)
        for line in nx.generate_adjlist(network.topology.graph, delimiter=","):
            node_list = line.split(",")
            print(node_list)
            node0 = node_list[0]  ##### node0 is node object in the string form
            print("here new node is ", node0)
            if node0 not in self.nodes_covered.keys():
                direction = 0
                node0_id = self.create_new_node(canvas,
                                                network.topology.node_objects[node0])  # , direction)  # ,radius=0)
                self.nodes_covered[node0] = node0_id  # node_id is the node id returned create_oval function of canvas
                self.node_names_dictionary[node0_id] = node0
                # self.x,self.y=
                # self.next_node_coordinates()

            else:
                node0_id = self.nodes_covered[node0]
            for node1 in node_list[1:]:
                if node1 not in self.nodes_covered.keys():
                    direction = network.topology.node_objects[node0].direction  # self.node_direction[node0]
                    node1_id = self.create_new_node(canvas,
                                                    network.topology.node_objects[node1])  # , direction)  # ,radius=0)
                    self.nodes_covered[node1] = node1_id
                    self.node_names_dictionary[node1_id] = node1
                    # self.x,self.y=\
                    # self.next_node_coordinates()

                else:
                    node1_id = self.nodes_covered[node1]
                self.create_edge(canvas, node0_id, node1_id)

    def create_new_node(self, canvas, node):

        color, radius, text, distance = self.node_attributes(node)
        direction = node.direction
        distance = node.distance
        x = self.x + distance * cos(radians(direction))
        y = self.y + distance * sin(radians(direction))
        coords = x - radius, y - radius, x + radius, y + radius
        self.node_coordinates[node] = x, y
        node_id = canvas.create_oval(coords, fill=color)
        canvas.create_text(x, y, text=text)
        # node_id.bind("<Button-1",self.node_click)
        canvas.tag_bind(node_id, "<Button-1>", lambda event: self.node_click(event, node_id))
        # canvas.tag_bind(node_id,"<ButtonRelease-1>",lambda  event: self.nodes_move(event,node_id))
        canvas.update()
        print(node_id, self.x, self.y, "\n", )
        # self.node_direction[node] = direction
        return node_id

        # pass

    '''
    def next_node_coordinates(self):
        #following an elliptical curve trace for node display.
        #
        a,b=self.network_frame_width,self.network_frame_height
        frame_width_gap=100
        frame_height_gap=100
        ''
        if self.direction == "NE":
            if self.x + self.inter_node_gap_x > self.network_frame_width-frame_width_gap :
                #
                self.direction = "NW"
                self.x-=self.inter_node_gap_x
                #self.y=math.sqrt(((a*a-self.x*self.x)*b*b)/a*a)
                self.y-=self.inter_node_gap_y
            else:
                self.x+=self.inter_node_gap_x
                #self.y=math.sqrt(((a*a-self.x*self.x)*b*b)/a*a)
                self.y-=self.inter_node_gap_y
                self.direction = "SE"

        if self.direction == "NW":
            if self.y - self.inter_node_gap_y < frame_height_gap :
                self.direction = "SW"
                self.x-=self.inter_node_gap_x
                #self.y=math.sqrt(((a*a-self.x*self.x)*b*b)/a*a)
                self.y+=self.inter_node_gap_y
            else:
                self.x-=self.inter_node_gap_x
                #self.y=math.sqrt(((a*a-self.x*self.x)*b*b)/a*a)
                self.y-=self.inter_node_gap_y
                self.direction = "SW"

        if self.direction =="SW":
            if self.x-self.inter_node_gap_x < frame_width_gap:
                self.direction = "SE"
                self.x-=self.inter_node_gap_x
                #self.y=math.sqrt(((a*a-self.x*self.x)*b*b)/a*a)
                self.y+=self.inter_node_gap_y
            else:
                self.x-=self.inter_node_gap_x
                #self.y=math.sqrt(((a*a-self.x*self.x)*b*b)/a*a)
                self.y+=self.inter_node_gap_y
                self.direction = "NW"
        if self.direction == "SE":
            if self.y+ self.inter_node_gap_y>self.network_frame_height-frame_height_gap:
                self.direction="NE"
                self.x+=self.inter_node_gap_x
                #self.y=math.sqrt(((a*a-self.x*self.x)*b*b)/a*a)
                self.y-=self.inter_node_gap_y
            else:
                self.x+=self.inter_node_gap_x
                #self.y=math.sqrt(((a*a-self.x*self.x)*b*b)/a*a)
                self.y+=self.inter_node_gap_y
                self.direction = "NE"
        ''


    def coordinates_check(self):
        if (self.x, self.y) not in self.coordinates_occupied:
            self.coordinates_occupied.append((self.x, self.y))
        else:
            self.x+=self.inter_node_gap_x
            self.y+=self.inter_node_gap_y
            self.coordinates_check()



    def display_rings(self,network,canvas):

        for ring_id,edge_list in network.topology.core_rings.items():
            self.angle=0
            core_inter_node_degree = int(360/len(edge_list))

            print("degree is ",core_inter_node_degree)
            degree=0#core_inter_node_degree
            print(edge_list)
            for edge in edge_list:
                for node in edge:
                    print(node,",")
                    if node not in self.nodes_covered.keys():

                        node_id=self.create_ring_node(canvas,node,core_ring_radius,node.direction,degree)
                        node.direction=degree
                        self.node_direction[node]=degree
                        #self.node_direction[node] = degree
                        degree+=core_inter_node_degree%360
                        print(degree)
                        self.nodes_covered[str(node)]=node_id
            #self.update_coordinates()

        for core_node,provider_node in network.topology.core_links.items():#provider_node_dict.items():
            if core_node not in self.nodes_covered.keys():
                print(core_node)
                direction=core_node.direction#self.node_direction[core_node]
                #coordinates=self.coordinates_check()#####
                node_id =self.create_node(canvas,core_node,direction)#,radius=0)

                self.nodes_covered[str(core_node)]=node_id
            if provider_node not in self.nodes_covered.keys():
                direction=core_node.direction#self.node_direction[core_node]
                node_id = self.create_node(canvas,provider_node,direction)#,radius=0)
                self.nodes_covered[str(provider_node)]=node_id
                provider_node.direction=direction
                self.node_direction[provider_node]=direction
        for provider_node,edge_list in network.topology.metro_rings.items():
            self.angle=0
            metro_inter_node_degree= int(360/len(edge_list))
            degree=0#metro_inter_node_degree
            for edge in edge_list:
                for node in edge:
                    print(node, ",")
                    if node not in self.nodes_covered.keys():
                        direction=provider_node.direction#self.node_direction[provider_node]
                        node_id = self.create_ring_node(canvas, node,metro_ring_radius,direction,degree)
                        self.node_direction[node]=degree
                        node.direction= direction+ degree
                        degree+=metro_inter_node_degree
                        self.nodes_covered[str(node)] = node_id
            #self.update_coordinates()
    def update_coordinates(self):
        self.y+=20
        #self.y+=50

    def creating_network_systems(self,master,canvas,network):
        self.x = self.node_start_x
        self.y = self.network_frame_height / 2
        self.direction = "NE"
        self.nodes_id = {}
        self.nodes_covered = {}
        self.coordinates_occupied = []
        self.node_names_dictionary={}

        self.display_rings(network,canvas)
        for line in nx.generate_adjlist(network.topology.graph,delimiter=","):
            node_list = line.split(",")
            print(node_list)
            node0=node_list[0]##### node0 is node object in the string form
            print("here new node is ",node0)
            if node0 not in self.nodes_covered.keys():
                direction=0
                node0_id = self.create_node(canvas,network.topology.node_objects[node0],direction)#,radius=0)
                self.nodes_covered[node0] = node0_id # node_id is the node id returned create_oval function of canvas
                self.node_names_dictionary[node0_id]=node0
                # self.x,self.y=
                # self.next_node_coordinates()

            else:
                node0_id = self.nodes_covered[node0]
            for node1 in node_list[1:]:
                if node1 not in self.nodes_covered.keys():
                    direction=network.topology.node_objects[node0].direction#self.node_direction[node0]
                    node1_id = self.create_node(canvas,network.topology.node_objects[node1],direction)#,radius=0)
                    self.nodes_covered[node1] = node1_id
                    self.node_names_dictionary[node1_id]=node1
                    # self.x,self.y=\
                    # self.next_node_coordinates()

                else:
                    node1_id = self.nodes_covered[node1]
                self.create_edge(canvas, node0_id, node1_id)

        ''
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
        ''
        '''

    def node_attributes(self, node):
        print(node, "p")
        print("node is ", node)
        # print("node tyoe is :",node.type)
        if type(node) != str:
            attributes = node_type[node.type]
            return attributes["color"], int(attributes["radius"]), attributes["name"], attributes["distance"]
        else:
            print("node as stringmm")
            return "black", 0, 0

    '''
    def create_ring_node(self,canvas,node,ring_radius,direction,inter_node_degree):
        #self.next_node_coordinates()
        #self.coordinates_check()
        # coords=xr-r,yr-r,xr+r,yr+r
        color, radius, text,distance = self.node_attributes(node)
        x=self.node_start_x + distance*cos(radians(direction))+ring_radius*cos(radians(inter_node_degree+direction))
        y=self.node_start_y + distance*cos(radians(direction))+ring_radius*sin(radians(inter_node_degree+direction))
        coords = x - radius, y - radius, x + radius, y + radius
        self.node_coordinates[node]=x,y

        node_id = canvas.create_oval(coords, fill=color)
        canvas.create_text(x, y, text=text)
        # node_id.bind("<Button-1",self.node_click)
        canvas.tag_bind(node_id, "<Button-1>", lambda event: self.node_click(event, node_id))
        # canvas.tag_bind(node_id,"<ButtonRelease-1>",lambda  event: self.nodes_move(event,node_id))
        canvas.update()
        #print(node_id, self.direction,x, y, "\n", )
        self.node_direction[node]=inter_node_degree+direction
        return node_id

    def create_node(self,canvas,node,direction):#,radius):
        #self.next_node_coordinates()
        #self.coordinates_check()
        #coords=xr-r,yr-r,xr+r,yr+r
        color,radius,text,distance=self.node_attributes(node)
        x=distance*cos(radians(direction))
        y=distance*cos(radians(direction))
        coords=x-radius,y-radius,x+radius,y+radius
        self.node_coordinates[node]=x,y
        node_id = canvas.create_oval(coords,fill=color)
        canvas.create_text(x,y,text=text)
        #node_id.bind("<Button-1",self.node_click)
        canvas.tag_bind(node_id,"<Button-1>",lambda event: self.node_click (event,node_id))
        #canvas.tag_bind(node_id,"<ButtonRelease-1>",lambda  event: self.nodes_move(event,node_id))
        canvas.update()
        #print(node_id,self.direction,self.x, self.y, "\n", )
        self.node_direction[node]=direction
        return node_id
    '''

    def nodes_move(self, event, node_id):
        pass

    def calculate_shortest_path(self, first_node, second_node):
        # pass
        shortest_path = nx.shortest_path(self.network.topology.graph,
                                         source=self.network.topology.node_objects[first_node], \
                                         target=self.network.topology.node_objects[second_node])
        print("shortest path is ", shortest_path)
        # pass
        print(shortest_path.split(","))
        self.iframe.shortest_path_box.delete(0, END)
        self.iframe.shortest_path_box.insert(0, str(shortest_path))
        # self.network.graph.

    def node_click(self, event, node_id):
        print("node clicked", event.x, event.widget)
        node = self.node_names_dictionary[node_id]
        '''
        if(self.iframe.vendor_list_box.count>0):
            self.iframe.vendor_list_box.delete(0,END)
            self.iframe.equipment_list_box.delete(0,END)
            self.iframe.cards_list_box.delete(0,END)
        '''
        if self.num_node_click == 0 or node == self.first_node:
            self.first_node = node
            self.num_node_click = 1
            print("first node clicked")
        elif self.num_node_click == 1 and node != self.first_node:
            self.second_node = node
            self.num_node_click = 0
            print("Second node clicked and ")
            self.calculate_shortest_path(self.first_node, self.second_node)
        else:
            print("no option for node click")
            self.num_node_click = 0
            self.first_node = ""
            self.second_node = ""

        print("testing for node is ", self.node_names_dictionary[node_id])
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
        self.inf_frame = Frame(master, height=self.information_frame_height, width=self.information_frame_width, bd=4,
                               bg='orange')
        # self.inf_frame.grid()
        self.inf_frame.pack()
        self.inf_frame.pack(side=LEFT)
        self.shortest_path_label = Label(self.inf_frame, text="Shortest path")
        self.shortest_path_label.pack(side=TOP)
        self.shortest_path_box = Entry(self.inf_frame)
        self.shortest_path_box.pack(side=TOP)
        # self.shortest_path_label.bind(<<)
        vendor_label = Label(self.inf_frame, text="Select Equipment for each node")
        vendor_label.pack()
        self.load_frame()
        self.current_node = ""
        self.current_vendor_name = ""
        self.network_equipments_on_nodes = {}  # dictionary of network equipment loaded per node

        # self.test_text="rttt"
        # self.property_selection()

    def shortest_path(self, node):
        pass

    def equipment_property_load(self, event):
        # print("function traced")
        index = int(event.widget.curselection()[0])
        equipment_name = event.widget.get(index)
        print("Equipment selected", equipment_name, "Equipment instance created for node", self.current_node)
        new_equipment = Equipment()
        self.network_equipments_on_nodes[self.current_node] = new_equipment
        new_equipment.equipment_properties_dict = \
        self.ne.network_equipment_vendor_dict[self.current_vendor_name].equipment_dict[
            equipment_name].equipment_properties_dict

        if self.cards_list_box != "":
            self.cards_list_box.forget()

        self.cards_list_box = Listbox(self.inf_frame, bd=5, exportselection=0, height=300)
        for k, v in new_equipment.equipment_properties_dict.items():
            print("equipment ", k, v)
            self.cards_list_box.insert(END, v)

        self.cards_list_box.pack(side=LEFT)

        # self.cards_list_box.delete(0,END)
        for prop in new_equipment.equipment_properties_dict.values():
            print(prop)
            #    self.equipment_list_box.insert(END, prop)

    def constraints_per_node(self, equipment, properties):
        pass

    def equipment_load(self, event):
        # print("venjgbnbfdjnlgkdmnlbfkn")
        index = int(event.widget.curselection()[0])

        self.current_vendor_name = event.widget.get(index)
        print("current vendor", self.current_vendor_name)
        if self.equipment_list_box != "":
            self.equipment_list_box.forget()
        self.equipment_list_box = Listbox(self.inf_frame, bd=5, exportselection=0, height=300, bg="yellow")
        self.equipment_options = self.ne.calling_equipment_names(self.current_vendor_name)
        for items in self.equipment_options:
            print(items)
            self.equipment_list_box.insert(END, items)
        self.equipment_list_box.bind('<<ListboxSelect>>', self.equipment_property_load)
        self.equipment_list_box.pack(side=LEFT)
        # self.equipment_options = self.ne.calling_equipment_names(vendor_name)
        # self.equipment_list_box.delete(0,END)
        # for eq in self.equipment_options:
        #    self.equipment_list_box.insert(END,eq)

    def load_frame(self):
        self.vendor_options = []
        # test_option=[1,2,3,4,5]
        self.equipment_options = []
        self.cards_option = []
        self.equipment_list_box = ""
        self.cards_list_box = ""
        self.vendor_list_box = Listbox(self.inf_frame, bd=5, exportselection=0, height=300, bg="green")
        # self.equipment_list_box = Listbox(self.inf_frame, bd=5, exportselection=0, height=300, bg="yellow")
        # self.cards_list_box = Listbox(self.inf_frame, bd=5, exportselection=0, height=300)
        # self.vendor_list_box.pack(side=TOP)
        self.vendor_list_box.bind('<<ListboxSelect>>', self.equipment_load)

        # self.vendor_list_box.bind('<<ListboxSelect>>', self.equipment_property_load)
        # self.equipment_list_box.bind('<<ListboxSelect>>', self.equipment_property_load)

        self.vendor_list_box.pack(side=LEFT)
        # self.equipment_list_box.pack(side=LEFT)
        # self.cards_list_box.pack(side=LEFT)
        # '''
        # vendor_default_name=StringVar()
        # equipment_default_name=StringVar()
        # cards_default_name=StringVar()
        # equipment_default_name.set("equipment_name")
        # cards_default_name.set("cards")
        # vendor_default_name.set("vendor_name")
        # self.equipment_option = OptionMenu(self.inf_frame, equipment_default_name, self.equipment_options)
        # self.cards_option = OptionMenu(self.inf_frame, cards_default_name, self.cards_option)
        # OptionMenu(self.inf_frame,"num",test_option).pack()
        # self.vendor_option = OptionMenu(self.inf_frame, vendor_default_name, self.vendor_options)
        # self.vendor_option.pack()

        # self.equipment_option.pack()
        # self.cards_option.pack()
        # '''

    def property_selection(self, node_id):
        self.vendor_options = self.ne.calling_vendor_names()
        self.current_node = node_id
        self.vendor_list_box.delete(0, END)
        for ven in self.vendor_options:
            self.vendor_list_box.insert(END, ven)
        # print(self.vendor_options)
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


network = Network()
root = Tk()
ne = Network_Equipments()
ne.loading_equipments_list()
iframe = Information_frame(root, network, ne)
nframe = Network_frame(root, network, iframe)

root.mainloop()

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







topology=Three_Tier_Topology()
topology.create_network()
print(topology.port_graph.node)
print(topology.graph.node)