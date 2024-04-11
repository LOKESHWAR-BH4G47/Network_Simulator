from cryptography.fernet import Fernet
from generate_mac import generate_mac

key = Fernet.generate_key()
fernet = Fernet(key)

class EncryptData:
    @staticmethod
    def encMessage(data):
        return fernet.encrypt(data.encode())

class DecryptData:
    @staticmethod
    def decMessage(encMessage):
        return fernet.decrypt(encMessage).decode()


class MacAddress:
    def __init__(self):
        self.mac_addresses = {}

    def assign_mac(self, device_name):
        mac = generate_mac.total_random()
        self.mac_addresses[device_name] = mac
        return mac

    def get_mac(self, device_name):
        return self.mac_addresses.get(device_name, None)


class Device:
    def __init__(self, name, Mac):
        self.name = name
        self.connected_devices = []
        self.mac_address = Mac.assign_mac(name)

    def connect(self, other_device):
        self.connected_devices.append(other_device)
        other_device.connected_devices.append(self)

    def send_data(self, data, hub,switch, receiver):
        print(f"{self.name} is sending data to {receiver.name}: {data}")
        Message = EncryptData.encMessage(data)
        hub.receive_from_hdevice(Message,hub,switch ,self.mac_address, receiver.mac_address, self.name, receiver)

    def receive_data(self, encMessage,hub,switch, sender_mac, receiver_mac, sender_name,receiver_name):
        if self.mac_address == receiver_mac:
            Message = DecryptData.decMessage(encMessage)
            print(f"{self.name} received data from {sender_name}: {Message}")
        else:
            print(f"{self.name} rejected data {encMessage} from {sender_name}")
 

class Hub(Device):
    def __init__(self, name, Mac):
        super().__init__(name, Mac) 
        self.mac_manager = MacAddress()  # Separate MAC address manager for the hub
        self.name = name
        self.connected_devices = []

    def connect(self, device):
        self.connected_devices.append(device)
        device.connected_devices.append(self)
        print(f"{self.name} connected to {device.name}")

    def receive_from_hdevice(self, encMessage,hub,switch, sender_mac, receiver_mac,sender_name,receiver_name):
        print(f"{self.name} received data from {sender_name} and is forwarding it.")
        self.send_from_hub(encMessage,hub,switch, sender_mac, receiver_mac,sender_name,receiver_name)

    def send_from_hub(self, encMessage,hub,switch, sender_mac, receiver_mac,sender_name,receiver_name):
        for device in self.connected_devices:
            if device.mac_address != sender_mac:
                device.receive_data(encMessage,hub,switch, sender_mac, receiver_mac,sender_name,receiver_name)
                
        switch.recieve_from_sdevice(encMessage, hub,switch, sender_mac, receiver_mac,sender_name,receiver_name)



class Switch(Device):
    def __init__(self, name, Mac):
        super().__init__(name, Mac)  # Call the constructor of the parent class
        self.mac_table = {}  # Maps MAC addresses to ports
        self.connected_devices = {}  # Maps ports to devices


    def learn_mac(self, mac_address, port):
        """
        Learns a MAC address associated with a port.
        """
        if mac_address not in self.mac_table:
            self.mac_table[mac_address] = port
            print(f"Learned MAC address {mac_address} on port {port}.")
        else:
            print(f"MAC address {mac_address} already exists on port {self.mac_table[mac_address]}.")

    def connect(self, device, port):
        """
        Connects a device to a specified port on the switch.
        """
        self.connected_devices[port] = device.mac_address 
        print(f"{device.name} connected on port {port}.")

    
    def find_port_by_mac(self, mac_address):
        """
        Finds the port associated with a MAC address.
        """
        print("Searching for MAC address:", mac_address)
        print("MAC Table:", self.mac_table)
        for mac,port in self.mac_table.items():
            print("Comparing with MAC in table:", mac)
            if mac == mac_address:
                print("MAC address found:", mac_address)
                return port
        print("MAC address not found:", mac_address)
        return None


    def recieve_from_sdevice(self,encMessage,hub, switch, sender_mac,receiver_mac,sender_name,receiver_name):
        print(f"{self.name} received data from {sender_name} and is forwarding it to {receiver_name.name}.")


        self.send_from_switch(encMessage,hub,switch,sender_mac,receiver_mac,sender_name,receiver_name)


    def send_from_switch(self, encMessage, hub, switch, sender_mac, receiver_mac, sender_name, receiver_name):
        sender_length = len(sender_name) 
        sender_number = int(sender_name[sender_length-1])
        if sender_number <= 5:
            self.learn_mac(sender_mac, 1)
        else:
            self.learn_mac(sender_mac, 2)
        # reciever_length = len(receiver_name.name)  
        # reciever_number = int(receiver_name.name[reciever_length-1])
        receiver_number = int(receiver_name.name.replace('Device', ''))
        if receiver_number <= 5:
            self.learn_mac(receiver_mac, 1)  # Learn receiver's MAC address 
        else:
            self.learn_mac(receiver_mac, 2)
        
        print(sender_mac)
        sender_port = self.find_port_by_mac(sender_mac)
        print(receiver_mac)
        receiver_port = self.find_port_by_mac(receiver_mac)

        if sender_port is None:
            print(f"{self.name} doesn't have MAC address {sender_mac} in its table.")
            return
        print(receiver_port)
        if receiver_port is not None:
            if receiver_port != sender_port:
                print(self.connected_devices)
                if receiver_port in self.connected_devices:
                    print(f"{self.name} received data from {sender_name} and is forwarding it to {receiver_name.name}.")
                    self.receive_data(encMessage, hub, switch, sender_mac, receiver_mac, sender_name, receiver_name)
                else:
                    print(f"{self.name} received data from {sender_name} and forwarding it to Hub {hub.name}.") 
                    hub.receive_from_hdevice(encMessage, hub, switch, sender_mac, receiver_mac, sender_name, receiver_name)
        else:
            print(f"{self.name} doesn't have MAC address {receiver_mac} in its table. Flooding the frame to all ports except the sender's port.")
            self.flood_frame(encMessage, hub, switch, sender_mac, receiver_mac, sender_name, receiver_name, sender_port)

    def flood_frame(self, encMessage, hub, switch, sender_mac, receiver_mac, sender_name, receiver_name, sender_port):
        """
        Floods the frame to all ports except the sender's port.
        """
        
        for port, device in self.connected_devices.items():
            if port != sender_port and port != "Port 1" and port != "Port 2":  # Exclude sender's port and switch ports
                if isinstance(device, Hub):
                    print(f"Flooding frame to Hub {device.name}.")
                    device.receive_from_hdevice(encMessage, hub, switch, sender_mac, receiver_mac, sender_name, receiver_name)
                else:
                    print(f"Flooding frame to Device {device.name}.")
                    device.receive_data(encMessage, hub, switch, sender_mac, receiver_mac, sender_name, receiver_name)
