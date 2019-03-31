from  all_dependencies import *




class Simulation():
    def __init__(self):
        self.environment = simpy.Environment()
        self.link_delay = 10  # micro second
        self.packet_id = 0
        self.max_time = 1000

    def create_ip_packets(self, number_of_packets,source,sink):
        source_ip=source.ip_address
        sink_ip=sink.ip_address

        packets = []
        for i in range(number_of_packets):
            packet = Packet("IP", 1500, self.packet_id,source_ip,sink_ip)
            packets.append(packet)
            self.packet_id += 1
        return packets

    def create_simulation(self):
        self.environment.process(self.simulation_of_packet())


    def create_simulation_on_processes(self,process_list):
        for process in process_list:
            self.environment.process(process)

    def run_simulation(self,simulation_time_limit):
        now=self.environment.now
        self.environment.run(now+simulation_time_limit)



    def resume_traffic(self,topology,services_and_operations):
        # start ip traffic
        nodes=topology.graph.nodes
        nodes_pairs=[(node1,node2) for node1 in nodes for node2 in nodes]
        for node_pair in nodes_pairs:
            if node_pair[0] != node_pair[1]:
                self.start_ip_traffic(node_pair[0],node_pair[1],topology,services_and_operations)
        self.resume_simulation()


    def resume_simulation(self):
        pass


    def start_ip_traffic(self,source,sink,topology,services_and_operations):

        #for service in services_and_operations.service_dict[(source,sink)]:
        #    service.
        packets=self.create_ip_packets(number_of_packets,source,sink)
        shortest_paths=topology.find_all_shortest_paths(source,sink)
        for shortest_path in shortest_paths:
            for node in shortest_path:
                yield self.environment.timeout(node.processing_time)



    def start_ip_traffic_between_two_nodes(self, information_frame, topology):
        # self.information_frame
        print("starting ip traffic")
        node1 = topology.node_instance_dictionary_by_node_id[int(information_frame.node_A.get())]
        node2 = topology.node_instance_dictionary_by_node_id[int(information_frame.node_B.get())]
        packets = self.create_ip_packets(10,node1,node2)
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
                packets = self.create_ip_packets(10,node1,node2)
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




##################################################################################################
##################################################################################################



class Packet():
    def __init__(self, type, size, packet_id,source_ip,sink_ip):
        self.type = type
        self.size = size
        self.packet_id = packet_id
        self.source_ip=""
        self.destination_ip=""
        self.source_port=""
        self.destination_port=""
        self.source_ip=source_ip
        self.sink_ip=sink_ip


##################################################################################################
##################################################################################################




class Flow_Table():
    def __init__(self):
        pass


##################################################################################################
##################################################################################################


class Routing_Table():
    def __init__(self):
        self.routing_table_for_device = {}
