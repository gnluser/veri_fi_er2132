from all_dependencies import *
import re

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
                        supported_subequipments_list=[Default]

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
                pass
                #print("Empty line")

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
                #print(subequipments_supported)
                self.identify_supported_subequipments_list_function(items[subequipments_supported])#self.equipment_properties_dictionary[subequipments_supported])

            else:
                #print("no data for cards")
                self.subequipment_list.append(Default)

            return self.subequipment_list

        except:
            print("error in reading equipment's subequipments")

    # on selecting sub equipment add this to equipment properties. on selection of cards from the gui
    def set_equipment_properties(self, items):
        pass



    def find_number_of_iteration(self,temp_string):
        regex_number_of_iterations=re.compile(r"^\s*[0-9]+\s*[X,x]\s*[$]")
        temp = re.match(regex_number_of_iterations, temp_string)
        if temp is None:
            num_iteration = 1
            string_index=temp_string.find("$")
            if string_index != -1:
                temp_string=temp_string[string_index+1:].lstrip()

        else:
            temp = temp.group()
            temp = re.match("[0-9]+", temp)
            temp = temp.group()
            num_iteration = int(temp)
            string_index=temp_string.find("$")
            temp_string=temp_string[string_index+1:].lstrip()
        return num_iteration,temp_string

    def identify_supported_subequipments_list_function(self, subequipments):
        subequipment_list = []
        subequipment_slot_regex=re.compile(r"\s*\n\s*")#\s*\$\s*
        subequipments_per_slot_regex=re.compile(r"\s*or\s+")

        #print(subequipments)
        for subequipment_slot_option in re.split(subequipment_slot_regex,subequipments):#subequipments.split("\n"):#
            if subequipment_slot_option != "":
                temp_string = subequipment_slot_option

                num_iteration,subequipment_option=self.find_number_of_iteration(temp_string)

                print("num iterations are ",num_iteration)
                #print(subequipment_slot_option)
                for subequipment_per_slot in re.split(subequipments_per_slot_regex,subequipment_option):
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
                #print("items[]",items[subeqpmnt_subpart])
                return self.subparts_list_function(items[subeqpmnt_subpart])#self.subequipment_properties_dictionary[subequipments_supported])
                # return self.subequipment_list
            else:
                return Default
                #print("no data for subparts")

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

