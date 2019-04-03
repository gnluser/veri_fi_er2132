from node import *
from all_dependencies import *
from addresses import  *
from info_frame import *
from onboarding_portal import *


class Network_Frame():
    def __init__(self, master, topology, simulation):
        self.simulation = simulation
        self.master = master
        rel_frame_width=0.99
        rel_frame_height=0.99
        canvas_x=0
        canvas_y=0
        rel_canvas_width=0.99*rel_frame_width#frame_width-canvas_x
        rel_canvas_height=0.99*rel_frame_height#frame_height
        #self.information_frame = information_frame
        self.project_frame=Frame(master,bg=outer_frame_color)#,height=frame_height,width=frame_width,bd=5,bg="blue")
        self.project_frame.place(relx=0.01,rely=0.01,relwidth=rel_frame_width,relheight=rel_frame_height)
        self.canvas = Canvas(self.project_frame,  bg=canvas_color)#""thistle1")width=20,
        #self.canvas.pack(side=LEFT, expand=YES, fill=BOTH)
        self.canvas.place(relx=0.01,rely=0.01,relheight=rel_canvas_height,relwidth=rel_canvas_width)
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

        self.node_option_frame = Frame(self.canvas, background=node_option_frame_color, bd=2, pady=1)#, bg=node_option_frame_color)
        self.background_strip_canvas = Canvas(self.node_option_frame, highlightthickness=0,
                                              bg=background_canvas_color)  # self.canvas.create_polygon(background_strip_coords,fill=label_color)
        self.background_labels=[]
        self.background_frame_labels=[]
        self.background_node_label_dictionary={}
        self.service_counter=0
        self.node_dict_for_service={}


    def allow_node_selection_for_service(self,service_nodes):
        self.service_counter=1
        service_nodes.dictionary_right_nodes={}
        service_nodes.dictionary_left_nodes={}
        #print("allowignbdn jbn ")



    def close_node_selection_for_service(self,service_nodes):
        self.service_counter=0
        #for label,node in self.dictionary_left_nodes.items():
        #    self.canvas.itemconfig(label,fill=node.color)
        print("close node")
        for label,node in service_nodes.dictionary_right_nodes.items():
            self.canvas.itemconfig(label,fill=node.color)


        for label,node in service_nodes.dictionary_left_nodes.items():
            self.reset_node_on_canvas(label,node)

        for label,node in service_nodes.dictionary_right_nodes.items():
            self.reset_node_on_canvas(label,node)



    def reset_node_on_canvas(self,label,node):
        print("service is hidden")
        node_name=self.node_label_dictionary[label]
        self.canvas.delete(label)
        self.node_label_dictionary.pop(label)
        label = self.create_polygon_node(node.canvas_coords, node.color)
        self.node_label_dictionary[label]=node_name
        self.network_node_instances_labels[label] = node

        self.canvas.tag_bind(label, "<Button-1>",
                             lambda event: self.node_clicked(event))  # , self.current_label,text,x,y))
        # self.canvas.tag_bind(text, "<Button-1>", lambda event: self.node_tinkered(event, new_node_label,text,x,y))
        self.canvas.tag_bind(label, "<ButtonRelease-1>",
                             self.move_node)  # lambda event : self.move_node(event,self.current_label,text.text,new_node_instance,attributes))
        self.canvas.tag_bind(label, "<Double-1>",
                             lambda event: self.create_equipment_selection_box(event, label,
                                                                               node))
        self.canvas.tag_bind(label, "<Button-3>",
                             lambda event: self.show_connecting_node_options(event, node.canvas_coords,node))
        self.move_edges(node)
        self.canvas.update()

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


    def create_polygon_node(self,coords,color):
        a1,b1,a2,b2=coords
        node_height=int((b2-b1)/2)
        node_width=(a2-a1)
        slack=node_height
        #self.canvas.create_line(a1,a2,b1,b2)
        #print("coords are ",a1,a2,b1,b2)
        a2, b2 = a1, b1 + node_height
        a3,b3 = a2 + node_width, b2
        a4,b4 = a3 + slack, b3 - slack
        a5,b5 = a4, b4 - node_height
        #self.canvas.create_line(d1,d2,e1,e2)
        a6,b6 = a5 - node_width, b5
        label = self.canvas.create_polygon(a1, b1, a2,b2,a3,b3,a4,b4,a5,b5,a6,b6, fill=color)

        #label=self.canvas.create_oval(coords, fill=color)

        return label



    def move_polygon_node(self,coords,color):
        a1, b1, a2, b2 = coords
        node_height = int((b2 - b1) / 2)
        node_width = (a2 - a1)
        slack = node_height
        # self.canvas.create_line(a1,a2,b1,b2)
        # print("coords are ",a1,a2,b1,b2)
        a2, b2 = a1, b1 + node_height
        a3, b3 = a2 + node_width, b2
        a4, b4 = a3 + slack, b3 - slack
        a5, b5 = a4, b4 - node_height
        # self.canvas.create_line(d1,d2,e1,e2)
        a6, b6 = a5 - node_width, b5
        label = self.canvas.create_polygon(a1, b1, a2, b2, a3, b3, a4, b4, a5, b5, a6, b6, fill=color)


        return label

    def create_node_instance_label_on_canvas(self,node_instance):
        a,b,c,d=node_instance.canvas_coords
        # a and d are the required window
        label=Label(self.canvas,text=node_instance.node_id)
        node_instance.canvas_label_window_id=self.canvas.create_window(a+12,d+10,window=label,width=c-a,height=10)

    def remove_node_label_window(self,node_instance):
        self.canvas.delete(node_instance.canvas_label_window_id)

    def create_node_in_display_from_topology(self, node_instance):
        # canvas_coords are coords for rectangle of node
        coords = node_instance.canvas_coords
        name = node_instance.name
        attributes = node_type[name]
        node_instance.color=attributes["color"]
        try:
            radius = attributes["radius"]
            new_node_label = self.create_polygon_node(coords,fill=node_instance.color)#self.canvas.create_oval(coords, fill=attributes["color"])
        except:
            length = attributes["length"]
            new_node_label = self.canvas.create_rectangle(coords, fill=node_instance.color)

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
        box_entry_literal = "Node "
        x1,y1,x2,y2=present_coords
        self.node_connection_options_frame=Frame(self.canvas)
        delete_button=Button(self.node_connection_options_frame,width=frame_width,bg=button_color,text="Delete Node "+str(node_instance.node_id),command=lambda : self.remove_network_node_and_respective_components(node_instance))
        listbox=Listbox(self.node_connection_options_frame,selectmode=MULTIPLE,bg=list_box_color)
        show_ports_option_button=Button(self.node_connection_options_frame,bg=button_color,text="Show Ports",width=int(frame_width/2))
        connect_label=Label(self.node_connection_options_frame,bg=label_color,text="Connect to Nodes",width=frame_width)
        connect_button=Button(self.node_connection_options_frame,bg=button_color,text="Connect",width=int(frame_width/2))
        connect_button.configure(command=lambda: self.connect_edge_to_respective_node(listbox,node_instance,self.window_for_edge_options,box_entry_literal))
        show_ports_option_button.configure(command=lambda: self.show_ports_options_between_node1_node2(x1,y2,listbox,node_instance,box_entry_literal))

        delete_button.pack(side="top")
        connect_label.pack(side="top")

        connect_button.pack(side="bottom")
        show_ports_option_button.pack(side="bottom")
        listbox.pack()
        #delete_button.grid(row=0,column=0,columnspan=2)
        #connect_label.grid(row=1,column=0,columnspan=2)
        #listbox.grid(row=2,column=0,rowspan=3,columnspan=2)
        #show_ports_option_button.grid(row=6,column=1)
        #connect_button.grid(row=6, column=0)
        #listbox.bind('<<ListboxSelect>>',lambda event: self.show_ports_options_between_node1_node2(event,node_instance))
        self.window_for_edge_options=self.canvas.create_window(x1+100,y2+100,window=self.node_connection_options_frame,width=frame_width,height=frame_height)
        #listbox.bind("<<ListboxSelect>>",lambda event: self.connect_edge_to_respective_node(event,node_instance,self.window_for_edge_options))
        for label, connecting_node_instance in self.network_node_instances_labels.items():
            if connecting_node_instance not in node_instance.connecting_node_instance_list and connecting_node_instance != node_instance:
                node_id=connecting_node_instance.node_id
                listbox.insert(END,box_entry_literal+str(node_id))
        #if len(self.network_node_instances_labels)==1 and



    def show_ports_options_between_node1_node2(self,x1,y2,listbox,node_instance,box_entry_literal):

        self.current_ports_label_instance_dictionary={}
        self.connecting_ports_label_instance_dictionary={}
        self.label_index_ordered_pair_dictionary={}
        height = width = 100

        indices=listbox.curselection()
        print("indices are ",indices)
        port_option_frame = Frame(self.canvas,background="orange")
        frame_1 = Frame(port_option_frame, background="gold", bd=2)
        frame_2 = Frame(port_option_frame, background="silver", bd=2)

        self.connecting_node_port_list_box = Listbox(frame_1,exportselection=0)
        self.current_node_list_box=Listbox(frame_2,exportselection=0)
        label = Label(frame_2, text="Current Node", bg="gold")
        label.pack(side="top")
        connected_label=Label(frame_1,text="Connected Nodes",bg="silver")
        connected_label.pack(side="top")

        connecting_node_instances=[]
        rowspan=0

        print(indices)
        '''
        for index in indices:
            print(listbox.get(index))
            node_2=listbox.get(index)
            print(node_2)
            node_2_id=int(node_2[len(box_entry_literal):])
            connecting_node_instance=self.topology.node_instance_dictionary_by_node_id[node_2_id]
            connecting_node_instances.append(connecting_node_instance)

            for port in connecting_node_instance.port_list:
                print("port is ",str(port.port_id))
                connecting_node_port_list_box.insert()
                current_node_list_box.insert(END,"port "+str(port.port_id))

                rowspan+=1

            current_node_list_box.pack(side="top")
            rowspan+=1
        right_labels_list=[]
        '''
        pre_node_string= "node "
        post_node_string=": port "
        for connected_node in node_instance.connecting_node_instance_list:
            connected_node_label=pre_node_string+str(connected_node.node_id)
            for port in connected_node.port_list:
                print("port is ",str(port.port_id))
                label=connected_node_label+post_node_string+str(port.port_id)
                self.connecting_node_port_list_box.insert(END,label)
                self.connecting_ports_label_instance_dictionary[label]=port

                rowspan += 1
        self.connecting_node_port_list_box.pack(side="top")
        rowspan=0
        #right_list_box=Listbox(frame_2)

        for port in node_instance.port_list:
            print(port)
            #label=Label(frame_2,text=str(port.port_id),bg="cyan")
            #current_node_list_box.append(label)
            label="port "+str(port.port_id)
            self.current_node_list_box.insert(END,label)
            self.current_ports_label_instance_dictionary[label]=port
            rowspan+=1
        self.current_node_list_box.pack(side="top")
        #right_list_box.pack(side="top")
        frame_3=Frame(port_option_frame,background="yellow",bd=2)
        label=Label(frame_3,text="Ports Connections")
        self.port_selection_box=Listbox(frame_3,selectmode=MULTIPLE)
        connect_button=Button(frame_3,text="Connect")
        remove_button=Button(frame_3,text="Remove Entry")
        label.place(x=0,y=0,width=3*width-4,height=10)#pack()
        self.port_selection_box.place(x=0,y=11,width=3*width-4,height=160)#pack()#side="top")
        connect_button.place(x=0,y=175,width=int(1.5*width)-2,height=20)#ack()#side="top")
        remove_button.place(x=int(1.5*width),y=175,width=int(1.5*width)-2,height=20)#ack()#side="top")
        self.current_port_flag=0
        self.connected_port_flag=0
        self.current_node_list_box.bind("<<ListboxSelect>>",lambda event: self.matching_current_port_to_connected_port(event,self.connecting_node_port_list_box))
        self.connecting_node_port_list_box.bind("<<ListboxSelect>>",lambda event: self.matching_connecting_port_to_current_port(event,self.current_node_list_box))

        #self.port_selection_box.bind("<<ListboxSelect",self.add_back_ports_to_listboxes)
        remove_button.configure(command=lambda : self.add_back_ports_to_listboxes())
        connect_button.configure(command=lambda: self.create_port_links(node_instance,pre_node_string,post_node_string))

        frame_1.place(x=0,y=0, anchor="nw", width=int(1.5 * width), height=height)
        frame_2.place(x=int(1.5 * width),y=0, anchor="nw", width=int(1.5 * width), height=height)
        frame_3.place(x=0,y=height+1, anchor="nw",width=3 * width,height=2 * height)

        self.port_option_window=self.canvas.create_window(x1+100,y2+150,window=port_option_frame,width=3 * width,height=3*height)

    def create_port_links(self,node_instance,pre_node_string,post_node_string):
        indices=self.port_selection_box.curselection()
        node_id_start_place=len(pre_node_string)
        for index in indices:
            label=self.port_selection_box.get(index)
            label_set=self.label_index_ordered_pair_dictionary[label]
            current_port_label=label_set[0]
            connected_port_label=label_set[1]
            current_port=self.current_ports_label_instance_dictionary[current_port_label]
            connected_port=self.connecting_ports_label_instance_dictionary[connected_port_label]

            matching_post_id_label_place=connected_port_label.find(post_node_string)
            connected_port_id=connected_port_label[node_id_start_place:matching_post_id_label_place]
            connected_port_id=int(connected_port_id)
            connected_node_instance=self.topology.node_instance_dictionary_by_node_id[connected_port_id]

            self.add_ports_to_topology_graph(current_port,connected_port)
            port_link=Port_Link(current_port,connected_port)
            node_instance.port_links_list.append(port_link)
            print("ports links created")
            self.remove_port_from_node_list(current_port,node_instance)
            self.remove_port_from_node_list(connected_port,connected_node_instance)
        self.canvas.delete(self.port_option_window)
        self.canvas.delete(self.window_for_edge_options)
        #self.clear_all_boxes_on_canvas()


    def remove_port_from_node_list(self,port,node_instance):
        node_instance.port_list.remove(port)

    def add_ports_to_topology_graph(self,port1,port2):
        self.topology.port_graph.add_edge(port1,port2)

    def add_back_ports_to_listboxes(self):
        print("remove button clicked")
        indices=self.port_selection_box.curselection()
        for index in indices:
            print(index)
            label=self.port_selection_box.get(index)
            label_set=self.label_index_ordered_pair_dictionary[label]
            current_port_label=label_set[0]
            connected_port_label=label_set[1]
            self.current_node_list_box.insert(END,current_port_label)
            self.connecting_node_port_list_box.insert(END,connected_port_label)
            self.port_selection_box.delete(index)

    def matching_current_port_to_connected_port(self,event,connecting_node_part_list_box):
        current_listbox=event.widget
        current_index=current_listbox.curselection()[0]
        current_port=current_listbox.get(current_index)
        self.current_port_flag=1
        if self.connected_port_flag == 1:
        #if connecting_node_part_list_box.curselection() != "":
            connected_index = connecting_node_part_list_box.curselection()
            self.insert_port_entries(current_listbox,current_index,connecting_node_part_list_box,connected_index)
            current_listbox.delete(current_index)
            connecting_node_part_list_box.delete(connected_index)
            self.current_port_flag=self.connected_port_flag=0




    def insert_port_entries(self,current_listbox,current_index,connected_listbox,connected_index):
        label_1=current_listbox.get(current_index)
        label_2=connected_listbox.get(connected_index)
        label=label_1+" -- "+label_2
        self.label_index_ordered_pair_dictionary[label]=(label_1,label_2)
        self.port_selection_box.insert(END,label)

    def matching_connecting_port_to_current_port(self,event,current_node_list_box):
        connected_listbox=event.widget
        connected_index=connected_listbox.curselection()[0]
        connected_port=connected_listbox.get(connected_index)
        self.connected_port_flag=1
        if self.current_port_flag == 1:
            current_index = current_node_list_box.curselection()
            self.insert_port_entries(current_node_list_box,current_index,connected_listbox,connected_index)
            connected_listbox.delete(connected_index)
            current_node_list_box.delete(current_index)
            self.current_port_flag=self.connected_port_flag=0




    def select_ports_for_port_connection(self):
        pass

    def dedicate_ports_for_ports_connection(self):
        pass

    def add_back_ports_to_node(self):
        pass

    #def connect_edge_to_respective_node(self,event,node_instance,window_label):
    def connect_edge_to_respective_node(self, widget, node_instance, window_label,box_entry_literal):
        #widget=event.widget
        self.canvas.delete(window_label)
        #index=int(widget.curselection()[0])
        indices=widget.curselection()
        for index in indices:
            print("code works here")
            connecting_to_node=widget.get(int(index))
            connecting_node_id=int(connecting_to_node[len(box_entry_literal):])
            print("code works here")

            connecting_node_instance=self.topology.node_instance_dictionary_by_node_id[connecting_node_id]
            #self.canvas.delete(window_label)
            print("code works here")
            print(connecting_node_instance)
            print(node_instance)
            self.create_edge_between_two_nodes(node_instance,connecting_node_instance)
            print("code works here")


    def create_edge_between_drop_and_positioned_nodes(self, new_node_instance):
        self.create_edge_between_two_nodes(new_node_instance,self.connecting_node_instance)
        self.connecting_node_instance = ""


    def create_line(self,coords1,coords2):
        #x1, y1 = coords1[2], int(coords1[1] + (coords1[3] - coords1[1]) * 0.8)
        #x2, y2 = coords2[0], int(coords2[1] + (coords2[3] - coords2[1]) * 0.2)
        x1,y1=int((coords1[0]+coords1[2])/2),int((coords1[1]+coords1[3])/2)
        x2,y2=int((coords2[0]+coords2[2])/2),int((coords2[1]+coords2[3])/2)
        edge_label = self.canvas.create_line(x1, y1, x2, y2)
        return edge_label

    def create_edge_between_two_nodes(self,new_node_instance,connecting_node_instance):
        print("new edge created between ", new_node_instance.node_id, " ", connecting_node_instance.node_id)

        coords1 = new_node_instance.canvas_coords
        coords2 = connecting_node_instance.canvas_coords
        edge_label=self.create_line(coords1,coords2)
        print(edge_label)
        new_node_instance.connecting_node_instance_list.append(connecting_node_instance)
        connecting_node_instance.connecting_node_instance_list.append(new_node_instance)
        self.topology.graph.add_edge(new_node_instance,connecting_node_instance)
        ####nx.add_edge(self.topology.graph
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
            node = Edge_Node(0,self.topology.node_numbers,  0)
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

    def create_node_in_graph(self,attributes, coords):
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
        self.create_node_option_image(data_center_node_type)

    def create_window_pane_for_client_server_node_labels(self):
        self.delete_labels_generated_for_menu_node_type_selection()
        self.create_node_option_image(client_server_node_type)

    def create_window_pane_for_general_nodes_label(self):
        self.delete_labels_generated_for_menu_node_type_selection()
        self.create_node_option_image(general_node_type)

    def create_window_pane_for_sdn_network_node_labels(self):
        self.delete_labels_generated_for_menu_node_type_selection()
        self.create_node_option_image(sdn_node_type)

    def create_window_pane_for_probe_network_node_labels(self):
        self.delete_labels_generated_for_menu_node_type_selection()
        self.create_node_option_image(probe_node_type)

    def create_window_pane_for_generic_network_node_labels(self):
        self.delete_labels_generated_for_menu_node_type_selection()
        self.create_node_option_image(network_node_type)

        # self.label_entry = Label(self.canvas, text=node_property)
        # window1 = self.canvas.create_window(100, canvas_height - 500, window=self.label_entry, height=200, width=200)



    def clear_background_canvas_and_frame(self):
        for items in self.background_labels:
            self.background_strip_canvas.delete(items)
        for items in self.background_frame_labels:
            #self.node_option_frame.delete(items)
            items.destroy()

    def create_node_option_image(self, node_type_dictionary):

        self.clear_background_canvas_and_frame()
        node_label_color=background_canvas_color#"lightyellow"#SandyBrown"


        #self.node_option_frame=Frame(self.canvas,background=node_option_frame_color,bd=2,pady=1,bg="lightgrey")
        pos_x = 0
        pos_y = 0#20
        label_gap=30
        oval_gap=18
        width=300
        height=20
        print("creating the drag and drop part")
        window_x = 100
        window_y = 100
        window_width=int(width/2)-4
        window_height=window_width
        displacement_x = window_width
        exit_button_side=height
        exit_button_color="red"
        #background_strip_coords=pos_x+displacement_x,0,pos_x+displacement_x,window_height,pos_x+displacement_x+oval_gap,window_height,pos_x+displacement_x+oval_gap,0

        #self.background_strip_canvas=Canvas(self.node_option_frame,highlightthickness=0,bg=background_canvas_color)#self.canvas.create_polygon(background_strip_coords,fill=label_color)
        self.node_option_window_label = self.canvas.create_window(window_x, window_y, window=self.node_option_frame, width=window_width, height=window_height)

        main_label = Label(self.node_option_frame, text="Drag and Drop",bg=background_label_color)
        self.background_frame_labels.append(main_label)

        exit_button = Button (self.node_option_frame,text="X",bg=exit_button_color)
        self.background_frame_labels.append(exit_button)

        main_label.place(x=pos_x,y=pos_y,width=window_width-exit_button_side,height=height)
        exit_button.place(x=window_width-exit_button_side,y=pos_y,width=exit_button_side,height=exit_button_side)
        self.background_strip_canvas.place(x=window_width-exit_button_side,y=pos_y+exit_button_side,width=oval_gap,height=window_height-exit_button_side)

        displacement_y=10
        pos_y+=height+ displacement_y

        self.movement_objects = {}
        # c=d=50
        x=2
        y=1+displacement_y#exit_button_side
        for node, attributes in node_type_dictionary.items():
            # print(node,attributes)
            try:
                radius = int(attributes["radius"])
                label = Label(self.node_option_frame, text=node, bg=node_label_color)

                #self.node_option_window_label = self.canvas.create_window(x, y, window=label, height=width, width=200)
                coords = x,y,x+oval_gap-3,y+oval_gap-3#pos_x + displacement_x, pos_y, pos_x + displacement_x + oval_gap, pos_y+oval_gap
                #node_label = self.canvas.create_oval(coords, fill=attributes["color"])
                node_label = self.background_strip_canvas.create_oval(coords, fill=attributes["color"])
                print(node_label,"#")
            except:
                length = int(attributes["length"])
                breadth = int(attributes["breadth"])
                label = Label(self.node_option_frame, text=node, bg=node_label_color)
                coords = x,y,x+oval_gap-3,y+oval_gap-3#pos_x + displacement_x, pos_y, pos_x + displacement_x + oval_gap, pos_y+oval_gap


                #self.node_option_window_label = self.canvas.create_window(x, y, window=label, height=width, width=200)
                #node_label = self.canvas.create_rectangle(coords, fill=attributes["color"])
                node_label = self.background_strip_canvas.create_rectangle(coords, fill=attributes["color"])
                print(node_label,"#")
            self.background_labels.append(node_label)
            label.place(x=pos_x,y=pos_y,width=window_width-oval_gap,height=height)
            self.background_frame_labels.append(label)

            #self.labels_generated_after_menu_node_type_selection.append(node_label)

            #self.canvas.bind(node_label, "<Motion>", self.move_cursor_over_node)

            self.background_node_label_dictionary[node_label] = node
            self.text_label_dictionary[node_label] = attributes["name"]

            self.background_strip_canvas.tag_bind(node_label, "<Button-1>",
                                self.sub_canvas_node_clicked)  # partial(self.node_clicked,event,node))#laambda event : self.node_clicked(event,node))#attributes))

            self.background_strip_canvas.tag_bind(node_label, "<ButtonRelease-1>",
                               lambda event: self.create_node_from_sub_canvas(event,window_width,window_height-window_y))  # lambda event: (event,self.current_label))#, attributes))

            self.canvas.update()
            pos_y += label_gap
            y+= label_gap

        self.labels_generated_after_menu_node_type_selection.append(self.node_option_window_label)


    def sub_canvas_node_clicked(self,event):
        self.current_attributes = ""
        print("node clicked")
        if self.service_counter == 1:
            self.node_property_alter(event.x,event.y)

        else:
            self.reset_entries_and_labels()
            self.clear_all_boxes_on_canvas()
            self.clear_all_information_frame_boxes()
            self.remove_edge_option_canvas_window()
            x, y = event.x, event.y
            item = self.background_strip_canvas.find_closest(x, y)
            self.current_node_name=self.background_node_label_dictionary[item[0]]
            print("dictionary is ",self.background_node_label_dictionary)
            print(item)


            print(self.current_node_name)
            try:
                self.current_attributes=node_type[self.current_node_name]
                self.current_label = item[0]
                #current_node_instance = self.network_node_instances_labels[self.current_label]
                #self.delete_edge_entry_labels(current_node_instance)
                #self.create_edge_entry_point(current_node_instance)
            except:
                print("error in sub canvas")
            self.canvas.update()


    def create_node_from_sub_canvas(self,event,window_width,window_height):
        print(event.x,event.y)
        self.reset_entries_and_labels()
        time.sleep(0.25)
        attributes = self.current_attributes#node_type[node]
        node=self.current_node_name
        print(attributes)
        print("node is",node)
        x, y = event.x+ window_width, event.y+window_height
        try:
            radius = int(attributes["radius"])
            coords = x - radius, y - radius, x + radius, y + radius
            # coords=x,y,x+20,y+10
            new_node_instance = self.create_node_in_graph( attributes, coords)
            coords = self.identify_nodes_on_position(new_node_instance, event, coords)

            new_node_instance.canvas_coords = coords
            new_node_instance.color = attributes["color"]
            new_node_label = self.create_polygon_node(coords,
                                                      new_node_instance.color)  # canvas.create_oval(coords, fill=attributes["color"])
        except:
            length = int(attributes["length"])
            breadth = int(attributes["breadth"])
            coords = x - length / 2, y - breadth / 2, x + length / 2, y + breadth / 2

            new_node_instance = self.create_node_in_graph( attributes, coords)

            coords = self.identify_nodes_on_position(new_node_instance, event, coords)
            new_node_instance.canvas_coords = coords
            new_node_instance.color = attributes["color"]
            new_node_label = self.canvas.create_rectangle(coords, fill=new_node_instance.color)



        self.create_node_instance_label_on_canvas(new_node_instance)

        try:
            if self.connecting_node_instance != "":
                connecting_node_instance = self.connecting_node_instance
                self.create_edge_between_drop_and_positioned_nodes(new_node_instance)
                self.topology.add_edge_to_topology(new_node_instance, connecting_node_instance)
            else:
                self.topology.add_nodes_to_topology(new_node_instance)
        except:
            print("no edge to add")

        self.create_edge_entry_point(new_node_instance)

        self.current_label = new_node_label
        self.node_label_dictionary[new_node_label] = node  # node is mapped to new node label in canvas

        self.network_node_instances_labels[new_node_label] = new_node_instance
        # text_at_previous_node_place=node_text



        current_node_instance = self.network_node_instances_labels[self.current_label]
        # print(self.current_label)

        self.set_node_information_window_box(current_node_instance)
        self.canvas.tag_bind(new_node_label, "<Button-1>",
                             self.node_clicked_on_canvas)  # lambda event: self.node_clicked(event)#, new_node_label,text_at_previous_node_place,x,y))
        self.canvas.tag_bind(new_node_label, "<ButtonRelease-1>",
                             self.move_node)  # lambda event : self.move_node(event,new_node_label,text_at_previous_node_place,new_node_instance,attributes))
        self.canvas.tag_bind(new_node_label, "<Double-1>",
                             lambda event: self.create_equipment_selection_box(event, new_node_label,
                                                                               new_node_instance))
        self.canvas.tag_bind(new_node_label, "<Button-3>",
                             lambda event: self.show_connecting_node_options(event, current_node_instance.canvas_coords,
                                                                             new_node_instance))
        self.canvas.update()
        # print("node jfnj")
        # self.information_frame.vendor_name_selection(self.node_numbers, new_node_instance,self.canvas)
        # elf.node_entry.insert(0,node_property)
        # elf.node_entry.update()

    def testing_function(self, events):
        print("yes function ois wojbnvj")

    def create_links(self):
        pass


    def clear_all_boxes_on_canvas(self):
        try:
            self.information_frame.remove_canvas_window(self.canvas)
            self.canvas.delete(self.port_option_window)
        except:
            print("\n")


    def clear_all_information_frame_boxes(self):
        for entry in self.information_frame.all_entries_list:
            entry.delete(0,END)


    def node_clicked(self, event):
        if self.service_counter == 1:
            self.node_property_alter(event.x,event.y)

        else:
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
        try:
            self.canvas.delete(self.port_option_window)
        except:
            print("port connection window not there on canvas")
        # self.information_frame.node_property_display.delete(1.0,END)
        # self.canvas.delete(self.node_entry)

    def node_property_alter(self,x,y):
        item = self.canvas.find_closest(x, y)
        self.current_label = item[0]
        current_node_instance = self.network_node_instances_labels[self.current_label]
        self.canvas.itemconfig(self.current_label, fill=service_color)
        self.node_dict_for_service[self.current_label] = current_node_instance




    def node_clicked_on_canvas(self, event):
        #self.delete_all_edge_entry_labels()
        if self.service_counter == 1:
            self.node_property_alter(event.x,event.y)
        else:

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
            #coords=x,y,x+20,y+10
            new_node_instance = self.create_node_in_graph( attributes, coords)
            # print(new_node_instance)
            # identifying, if any node is present in the background. for drop  and add edge to work

            coords = self.identify_nodes_on_position(new_node_instance, event, coords)

            new_node_instance.canvas_coords = coords
            new_node_instance.color=attributes["color"]
            new_node_label = self.create_polygon_node(coords,new_node_instance.color)#canvas.create_oval(coords, fill=attributes["color"])
        except:
            length = int(attributes["length"])
            breadth = int(attributes["breadth"])
            coords = x - length / 2, y - breadth / 2, x + length / 2, y + breadth / 2

            new_node_instance = self.create_node_in_graph( attributes, coords)

            coords = self.identify_nodes_on_position(new_node_instance, event, coords)
            new_node_instance.canvas_coords = coords
            new_node_instance.color=attributes["color"]
            new_node_label = self.canvas.create_rectangle(coords, fill=new_node_instance.color)
        # self.canvas.bind(new_node_label, "<Motion>", self.move_cursor_over_node)


        self.create_node_instance_label_on_canvas(new_node_instance)

        try:
            #print("trace")
            #print(coords, new_node_instance)
            #print("tr", type(self.connecting_node_instance), self.connecting_node_instance, type(new_node_instance),new_node_instance)
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
        #self.information_frame.node_id_entry.delete(1.0, END)aa
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
            #print(octet)
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
        #print(node_property)
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

        if self.service_counter ==1 :
            self.node_property_alter(event.x,event.y)

        else:
            self.reset_entries_and_labels()
            self.clear_all_information_frame_boxes()
            #self.clear_all_boxes_on_canvas()

            #print("move node method")
            #print("current label is ", self.current_label)
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
                #coords=x,y,x+20,y+10

                # updating the coords for the moved node
                current_node_instance.canvas_coords = coords
                current_node_instance.color=attributes["color"]
                new_node_label = self.move_polygon_node(coords,current_node_instance.color)#canvas.create_oval(coords, fill=attributes["color"])
            except:

                length = int(attributes["length"])
                breadth = int(attributes["breadth"])
                coords = x - length / 2, y - breadth / 2, x + length / 2, y + breadth / 2
                current_node_instance.canvas_coords = coords
                current_node_instance.color=attributes["color"]
                new_node_label = self.canvas.create_rectangle(coords, fill=current_node_instance.color)
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
        #print("edge created jere mnds", connecting_node_instance)
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

    def create_edges_between_two_nodes(self, current_node_instance, connecting_node_instance):

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
            self.create_edges_between_two_nodes(current_node_instance, connecting_node_instance)

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


