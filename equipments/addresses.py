from all_dependencies import *


class IP_Domain():
    def __init__(self):
        self.ip_domain_range = ""
        self.ip_addresses_for_hosts = []
        self.ip_address_host_map = {}
        self.subnet_domain_pool = []
        # self.create_ip_host_range(ip_address_of_network,number_of_hosts)

    def create_ip_host_range(self, ip_address_of_network, number_of_hosts):
        host_bits = int(log(number_of_hosts, 2)) + 1
        add_to_host_bits = "".join([str(1) for bits in range(host_bits)])
        # for bits in host_bits:
        #    add_to_host_bits += str(1)
        # add_to_host_bits=
        for ip_no in range(pow(2, host_bits)):
            ip_addr = Ip_Address()
            ip_addr.subnet_mask = (ip_address_of_network.subnet_mask.split('1', 1)[0] + add_to_host_bits).ljust(32, '0')
            # ip_addr.host_id=
            # +str(int(ip_no,2))
            mask = "".join([ord(a) and ord(b) for a, b in
                            zip(ip_address_of_network.ip_address, ip_address_of_network.subnet_mask)])
            ip_addr.ip_address = (mask + bin(ip_no)[2:]).ljust(32, "0")
            self.subnet_domain_pool.append(ip_addr)
            ip_address_of_network.subnet_addresses_pool = []


class Ip_Address():
    def __init__(self, parent_ip_address):
        self.type = ""
        self.parent_ip_address = parent_ip_address
        self.ip_address = ""
        self.host_id = ""
        self.subnet_mask = ""
        self.gateway_id = ""
        self.domain_id = ""
        self.subnet_addresses_pool = []
        self.subnet_distributed_addresses = []
        self.ip_domain = IP_Domain()

    def dafault_ip_address(self):
        if self.parent_ip_address == "":
            self.create_ip_address()
        else:
            try:
                self.ip_address = self.parent_ip_address.subnet_addresses_pool.pop(0)
            except:
                self.create_ip_address()



    def convert_str_to_ipv4(self,address):
        f=""
        for i in range(1,5):
            m=0
            for j in range(1,9):
                r=int(address[i*8-j])
                m+=int(pow(2,j-1)*r)
            f+=str(m)
            if i < 4:
                f+="."
        return f



    def create_ip_address(self):
        i = 0
        while (i < 100000):
            b1 = bin(random.randint(0, 15))[2:]
            b1 = b1.rjust(24, "0")
            address = ("1010" + b1).rjust(32, "0")
            if address not in ip_addresses_allotted:
                ip_addresses_allotted.append(address)

                self.ip_address =address
                print("ip address created ",  self.convert_str_to_ipv4(address))
                break
            i += 1
            # self.ip_address="".join(['0' for i in range(32)])


###############################################################################################
###############################################################################################



class Traffic():
    def __init__(self):
        pass


############################################################################################
############################################################################################


class MAC_Address():
    def __init__(self):
        self.mac_address = ""
        # self.mac_address_alotted=[]
        # self.create_mac_address_id()

    def create_mac_address_id(self):
        # for i in range(48)
        while (True):
            address = ""
            for i in range(6):
                # b1=b2=""
                b1 = bin(random.randint(0, 15))[2:]
                b2 = bin(random.randint(0, 15))[2:]
                b1 = b1.ljust(4, "0")
                b2 = b2.ljust(4, "0")
                # string=""
                # for i in range(4-len(b1)):
                #    string+=str(0)
                # b1+=string
                # string = ""
                # for i in range(4 - len(b2)):
                #    string += str(0)
                # b2+=string
                slot = b1 + b2  # +":"
                address += slot

            if address not in mac_addresses_allotted:
                mac_addresses_allotted.append(address)
                self.mac_address = address
                break

