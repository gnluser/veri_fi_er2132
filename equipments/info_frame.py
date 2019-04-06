from all_dependencies import *
from topology import *
from equipments import *

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

        self.frame_width=200
        self.frame_height=300

        self.window_frame = Frame(canvas,highlightbackground="white",  highlightthickness=2, width=self.frame_width, height=self.frame_height, bd= 5)

        #self.create_info_frame()
        #self.create_info_frame_widgets()


    def create_info_frame(self):
        #print("flag uis :",self.info_frame_flag)
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

        #self.display_subequipment_label.grid(row=row_span + 1, column=0, columnspan=2, sticky=N + E + S + W, pady=1)
        #self.display_properties_subequipment_box.grid(row=row_span + 2, column=0, columnspan=2, rowspan=1,sticky=N + E + S + W, pady=1)
        self.port_option_label.grid(row=row_span+1,column=0,columnspan=2,sticky=N +E+W+S,pady=1)
        self.port_option_list_box.grid(row=row_span+2, column=0, columnspan=2, rowspan=1,sticky=N + E + S + W, pady=1)


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

        #self.subequipment_option_label=Label(self.frame,text="Subequipments",bg=label_color)
        self.port_option_label=Label(self.frame,text="Ports and Protocols",bg=label_color)
        #self.subequipment_option_list_box=Listbox(self.frame,bg=text_bg_color)
        self.port_option_list_box=Listbox(self.frame,bg=text_bg_color)
        #self.subequipment_option_list_box.bind("<<ListboxSelect>>",lambda event: self.load_port_information(event))
        # self.display_equipment_label.grid(row=row_span+9,column=0,columnspan=1,sticky=N+E+S+W,pady=1)
        # self.display_properties_equipment_box.grid(row=row_span+1,column=0,columnspan=1,rowspan=5,sticky=N+E+S+W,pady=1)

    def load_port_information(self,node_instance):
        self.port_option_list_box.delete(0,END)
        for port in node_instance.ports_list:
            self.port_option_list_box.insert(END,port.id,"\t",port.name)


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

        self.window_box_id = canvas.create_window(x - 200, y + 50, window=self.window_frame, width=self.frame_width, height=self.frame_height)

    def remove_canvas_window_objects(self, list_box, label):
        list_box.destroy()
        label.destroy()

    def remove_canvas_window(self, canvas):  # ,node_instance):#,list_box):
        # self.remove_list_box(list_box)
        canvas.delete(self.window_box_id)
        #self.window_frame.destroy()
        pass

    def reset_subequipment_property_box(self):
        self.display_properties_subequipment_box.delete(1.0, END)

    def reset_equipment_property_box(self):
        self.display_properties_equipment_box.delete(0, END)

    def create_vendor_list_box(self, event, node_label, canvas, node_instance):
        self.current_node_instance=node_instance
        self.create_canvas_window(event.x, event.y, canvas, node_instance)  # ,node_label,self.vendor_list_box)
        #self.vendor_yscrollbar = Scrollbar(self.window_frame, orient=VERTICAL)
        #self.vendor_xscrollbar = Scrollbar(self.window_frame, orient=HORIZONTAL)
        self.exit_button=Button(self.window_frame,text="x")
        self.vendor_label = Label(self.window_frame, text="Vendor List")
        self.vendor_list_box = Listbox(self.window_frame, bd=5, cursor="hand2",exportselection=0, bg=window_background_color)#, width=20, height=50
        #self.vendor_list_box.config(xscrollcommand=self.vendor_xscrollbar.set,yscrollcommand=self.vendor_yscrollbar.set)

        self.exit_button.place(x=0.85*self.frame_width,y=0,width=0.1 * self.frame_width,height=0.1 * self.frame_height)

        self.vendor_label.place(x=0.1*self.frame_width,y=0,width=0.7*self.frame_width,height=0.1 * self.frame_height)#pack(side=TOP)
        #self.vendor_list_box.
        self.vendor_list_box.place(x=0.01*self.frame_width,y=30,width=0.88*self.frame_width,height=0.8*self.frame_height)
        #self.vendor_xscrollbar.pack(side=BOTTOM, fill=X)
        #self.vendor_yscrollbar.pack(side=RIGHT,fill=Y)
        #self.vendor_xscrollbar.config(command=self.vendor_list_box.xview)
        #self.vendor_yscrollbar.config(command=self.vendor_list_box.yview)
        print("vendor names are present")
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
                                          bg=window_background_color)
        #self.equipment_list_box.config(xscrollcommand=xscrollbar.set,yscrollcommand=yscrollbar.set)

        self.equipment_label.place(x=0.1*self.frame_width,y=0,width=0.7*self.frame_width,height=0.1 * self.frame_height)#pack(side=TOP)#.pack(side=TOP)
        #xscrollbar.pack(side=BOTTOM, fill=X)
        #yscrollbar.pack(side=RIGHT,fill=Y)
        #xscrollbar.config(command=self.equipment_list_box.xview)
        #yscrollbar.config(command=self.equipment_list_box.yview)

        #self.exit_button.place(x=0.85*self.frame_width,y=0,width=0.1 * self.frame_width,height=0.1 * self.frame_height)

        #self.vendor_label.place(x=0.1*self.frame_width,y=0,width=0.7*self.frame_width,height=0.1 * self.frame_height)#pack(side=TOP)
        #self.vendor_list_box.
        #self.vendor_list_box.place(x=0.01*self.frame_width,y=30,width=0.88*self.frame_width,height=0.8*self.frame_height)
        self.equipment_list_box.place(x=0.01*self.frame_width,y=30,width=0.88*self.frame_width,height=0.8*self.frame_height)#.pack()
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
                                             height=15, bg=window_background_color)
        #self.subequipment_list_box.config(xscrollcommand=xscrollbar.set,yscrollcommand=yscrollbar.set)
        self.subequipment_label = Label(self.window_frame, text="Subequipments")

        self.subequipment_label.place(x=0.1*self.frame_width,y=0,width=0.7*self.frame_width,height=0.1 * self.frame_height)#pack(side=TOP)#.pack()
        self.subequipment_list_box.place(x=0.01*self.frame_width,y=30,width=0.88*self.frame_width,height=0.8*self.frame_height)#.pack()

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
            #print(subpart)
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
                #print(subeqpmnt_name)
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
        print("selected equipments : ", self.selected_subequipment_index_list)
        #print("current scenario is ",new_subeqpmnt_option_list)
        new_subeqpmnt_option=[x for x in new_subeqpmnt_option_list if x not in self.selected_subequipment_index_list]
        #print("alter add ", new_subeqpmnt_option)
        if new_subeqpmnt_option != "":
            for x in new_subeqpmnt_option:
                new_subequipment=event.widget.get(x)
                #print(self.current_vendor_instance.all_eqpmnt_subeqpmnt_and_parts_dictionary)
                subequipment=self.create_sub_equipment(new_subequipment)
                if new_subequipment != Default :
                    #print(self.current_vendor_instance.all_eqpmnt_subeqpmnt_and_parts_dictionary[new_subequipment])

                    self.call_subpart_create_function(subequipment,canvas, node_instance, x, y)
                    self.selected_subequipment_index_list.append(x)
                else :
                    print("subequipment added")

        else:
            print("subequipment is popped")

        ####print("currently",new_subeqpmnt_option_list)
        subequipment_unselected=[x for x in self.selected_subequipment_index_list if x not in new_subeqpmnt_option_list]
        #print("node popped ",subequipment_unselected)
        for subeqpmnt in subequipment_unselected:
            print("node popped ", subeqpmnt)
            self.selected_subequipment_index_list.remove(subeqpmnt)
        print(self.selected_subequipment_index_list)


    def create_sub_equipment(self,subequipment_name):
        equipment_dictionary=self.current_vendor_instance.all_eqpmnt_subeqpmnt_and_parts_dictionary[self.new_equipment.name]
        if subequipment_name == Default:
            subequipment_dictionary=self.new_equipment.equipment_properties_dictionary
        else:
            subequipment_dictionary=self.current_vendor_instance.all_eqpmnt_subeqpmnt_and_parts_dictionary[subequipment_name]
        subequipment=SubEquipment()
        subequipment.name=subequipment_name
        subequipment.subequipment_properties_dictionary=subequipment_dictionary
        if subequipment_dictionary[subeqpmnt_subpart] == "":
            #self.current_vendor_instance.all_eqpmnt_subeqpmnt_and_parts_dictionary[sesubeqpmnt_subpart]
            self.add_ports_and_properties_to_equipment(equipment_dictionary,self.new_equipment,subequipment)
        return subequipment



    def add_ports_and_properties_to_equipment(self,equipment_dictionary,equipment,subequipment):
        #if subequipment == Default:
        port=self.current_vendor_instance.all_eqpmnt_subeqpmnt_and_parts_dictionary[self.new_equipment.name][ports]
        subpart = ""
        self.current_node_instance.update_ports(port,subpart,subequipment,equipment)
        self.reset_subequipment_property_box()
        for port in self.current_node_instance.port_list:
            self.display_properties_subequipment_box.insert(END, str(port.port_id) + "\n")

        #else:
        #    pass


    def call_subpart_create_function(self,new_subequipment,canvas,node_instance,x,y):
        #print(self.current_vendor_instance)
        #print(new_subequipment)
        if new_subequipment.name != "":
            subpart_dictionary = self.current_vendor_instance.all_eqpmnt_subeqpmnt_and_parts_dictionary[new_subequipment.name]#[subeqpmnt_subpart]
            #print(self.current_vendor_instance.all_eqpmnt_subeqpmnt_and_parts_dictionary)
            #print(self.current_vendor_instance.all_eqpmnt_subeqpmnt_and_parts_dictionary[new_subequipment])
            self.create_subpart_window( canvas, x, y, node_instance)


    def load_subeqpmnt_property_window_box(self, canvas, equipment_name):#, node_instance):

        try:
            self.reset_subequipment_property_box()

        except:
            print("First run, subequipment property box is empty")

        indices = self.subequipment_list_box.curselection()
        for index in indices:
            subpart = ""
            #print("index value is ",index)
            new_subequipment_name= self.subequipment_list_box.get(index)
            print("Subequipment selected is ",new_subequipment_name)
            subequipment = SubEquipment()
            subequipment.name = new_subequipment_name
            if new_subequipment_name == Default:
                #ports=self.current_node_instance.all_eqpmnt_subeqpmnt_and_parts_dictionary[ports]
                new_subequipment=Default
                #self.current_node_instance.update_ports(ports)

                subeqpmnt_property=self.current_vendor_instance.all_eqpmnt_subeqpmnt_and_parts_dictionary[equipment_name]
                subequipment.subequipment_properties_dictionary = subeqpmnt_property
                #for k,v in subeqpmnt_property.items():
                #    print("equipment property ",k,"\t",v)

                port=subeqpmnt_property[ports]
                protocols=subeqpmnt_property[protocol]
                #self.display_properties_subequipment_box.insert(END, "Ports" + " :-\n" + port+"\n")
                #self.display_properties_subequipment_box.insert(END, "Protocols"+" :-\n"+protocols+"\n")

            else:
                new_equipment_property=self.current_vendor_instance.all_eqpmnt_subeqpmnt_and_parts_dictionary[new_subequipment_name]
                # self.subpart_window_list.append(self)
                subequipment.subequipment_properties_dictionary = new_equipment_property
                #for k, v in new_equipment_property.items():#.subequipment_properties_dictionary.items():
                #   print("Sub equipment property ", k, v)
                port=new_equipment_property[ports]
                protocols=new_equipment_property[protocol]
                #self.current_node_instance.update_ports(port, subpart, subequipment, self.new_equipment)
                #self.display_properties_subequipment_box.insert(END, "Ports"+ " :-\n"+port+"\n")
                #self.display_properties_subequipmnt_box.insert(END, "Protocols" + " :-\n" + protocols + "\n")

            #self.current_node_instance.update_ports(port,subpart,subequipment,self.new_equipment)
            print("Subequipment ", new_subequipment_name, " ports are ::")
            for item in port.split("\n"):
                print(item)
            for item in self.current_node_instance.port_list:
                print(item.port_id)

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
            #print(items)
            #print("fbgVFgb")
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