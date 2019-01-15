

#import networkx as nx
import csv

data_file="/home/gnl/Desktop/mankul/flask_project/sdnProject0.2/equipments.csv"
component_name='component name'
ports_per_cards='ports on cards/equipment'
throughput='Throughput'
line_rate='Mpps'
line_cards='line cards'
protocol='Feature and protocols'
layer_2="Layer 2 features"
layer_3='Layer 3 features'
usage='usage'
equipment_vendors=['cisco','juniper','nokia','ciena','huawei','fujitsu']#'arista',
equipment_properties=[component_name,ports_per_cards,throughput,line_rate,line_cards,protocol,layer_2,layer_3,usage]


class Load_Network_Information():
    def __init__(self):
        ne = Network_Equipments()
        ne.loading_equipments_list()
        self.ne=ne
        self.vendor_name=""
        self.network_deployed_equipment_dict={}
        self.network_equipment_dict={}
        
        


class Network_Equipments:
    def __init__(self):
        self.network_equipment_vendor_dict={}
        self.per_vendors_equipments_list=[]

        #for items in equipment_properties:
        #    print items



    def loading_equipments_list(self):#equipment list is loaded in vendor_instance's variable component_list dictionary with all names in list equipment_properties
        self.dictionary_list=[]
        dictionary_equipments=[]
        data=csv.DictReader(open(data_file,'r'))
        for row in data:
            self.dictionary_list.append(row)# row is an open dictionary object

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
                    flag_for_vendor=True
                    if vendor_name not in self.network_equipment_vendor_dict:
                        ####
                        ####Creating new vendor instance for new vendor in list....... vendor instances are in nw_eq_vndr_lst
                        ####
                        vendor_instance=Equipments_per_Vendor()
                        self.network_equipment_vendor_dict[vendor_name] = vendor_instance
                        self.per_vendors_equipments_list.append(vendor_instance)
               
                    else:
                        ####
                        ####adding new equipment in list information to vendor instance
                        ####
                        vendor_instance=self.network_equipment_vendor_dict[vendor_name]
                    #print(vendor_instance.func())
                    if items[component_name] not in vendor_instance.equipment_names_list:#to avoid reloading same properties if present in csv file
                        vendor_instance.equipment_names_list.append(items[component_name])
                    if items[component_name] not in vendor_instance.equipment_dict.keys():
                        new_equipment=Equipment()
                        new_equipment.equipment_properties(items)
                        vendor_instance.equipment_dict[items[component_name]]=new_equipment
                        #print(vendor_instance.equipment_dict.values())
                        '''
                            vendor_instance.equipment_dict[items[component_name]]=new_equipment
                        for element in equipment_properties:
                            vendor_instance.equipment_dict[items[component_name]].equipment_properties_dict[element]=items[element]
                            vendor_instance.component_list[element]=items[element]
                        '''




                    #if self.vendor_instance.eqipment_list is N
                    #if items[component_name].lower in equipment_vendors:
                    #print(items[component_name])
                #else:
                #   print("vendor name not identified for ",items[component_name])
            if flag_for_vendor==False:
                print("vendor name not identified for ", items[component_name])

    def calling_vendor_names(self):
        # forwarding json  file to app to gorward it to the web page
        return equipment_vendors

    def calling_equipment_names(self,vendor_name):
        return self.network_equipment_vendor_dict[vendor_name].returning_equipment_names()

###each time new instance created, vendor instance is added to network_equipment_vendor_dict dictionary of ne

class Equipments_per_Vendor:
    #equipment_dict={}
    #component_property={}
    def __init__(self):
        self.equipment_dict={}
        self.component_list={}
        self.component_properties_list=[]
        self.equipment_names_list=[]
        #print("equipment per vendor created")

    def returning_equipment_names(self):
        print("returning equipment names for specific vendor")
        return self.equipment_names_list


class Equipment:
    #equipment_properties_dict={}
    def __init__(self):
        self.name=""
        self.equipment_properties_dict={}


    def equipment_properties(self,items):
        for element in items:
            self.equipment_properties_dict[element]=items[element]

#ne= Network_Equipments()
#ne.loading_equipments_list()

'''
with open(data_file,'r') as data_csv:
    data=csv.reader(data_csv,delimiter=",", quotechar='|')
    for row in data:
        print row[0]
''
d=open(data_file)
print d.read()
'''

