import uuid
import random

# Physical Layer
class Device:
    def __init__(self, device_id, device_type):
        self.device_id = device_id
        self.device_type = device_type

    def send_data(self, data, connection):
        print(f"Device {self.device_id} sending data: {data}")
        connection.transmit_data(data, self)

    def receive_data(self, data):
        print(f"Device {self.device_id} received data: {data}")

class Hub(Device):
    def __init__(self, device_id):
        super().__init__(device_id, "hub")
        self.connected_devices = []

    def add_device(self, device):
        self.connected_devices.append(device)

    def broadcast_data(self, data, sender):
        for device in self.connected_devices:
            if device != sender:
                device.receive_data(data)

class Connection:
    def __init__(self, device1, device2):
        self.connection_id = str(uuid.uuid4())
        self.device1 = device1
        self.device2 = device2

    def transmit_data(self, data, sender):
        receiver = self.device2 if sender == self.device1 else self.device1
        receiver.receive_data(data)

class NetworkSimulator:
    def __init__(self):
        self.devices = []
        self.connections = []

    def create_device(self, device_type):
        device_id = str(uuid.uuid4())
        device = Hub(device_id) if device_type == "hub" else Device(device_id, device_type)
        self.devices.append(device)
        return device

    def create_connection(self, device1, device2):
        connection = Connection(device1, device2)
        self.connections.append(connection)
        return connection

    def send_data(self, sender, data, connection):
        sender.send_data(data, connection)

# Data Link Layer: Sliding Window Protocol: Go-Back-N ARQ
class SlidingWindow:
    def __init__(self, window_size):
        self.window_size = window_size
        self.send_base = 0
        self.next_seq_num = 0
        self.buffer = []

    def send(self, data, send_func):
        if self.next_seq_num < self.send_base + self.window_size:
            self.buffer.append(data)
            send_func(data, self.next_seq_num)
            self.next_seq_num += 1
        else:
            print("Window is full. Waiting for acknowledgment...")

    def receive_ack(self, ack_num):
        if self.send_base <= ack_num < self.next_seq_num:
            self.send_base = ack_num + 1
            self.buffer = self.buffer[ack_num - self.send_base + 1:]

# Network Layer
class Router(Device):
    def __init__(self, device_id):
        super().__init__(device_id, "router")
        self.routing_table = {}
        self.arp_table = {}

    def add_route(self, destination_network, subnet_mask, next_hop):
        self.routing_table[(destination_network, subnet_mask)] = next_hop

    def arp_request(self, ip_address):
        if ip_address not in self.arp_table:
            mac_address = str(uuid.uuid4())
            self.arp_table[ip_address] = mac_address
        return self.arp_table[ip_address]

    def forward_packet(self, packet):
        dest_ip = packet.destination_ip
        for (network, mask), next_hop in sorted(self.routing_table.items(), key=lambda x: -self._mask_to_bin(x[1]).count('1')):
            if self._ip_in_subnet(dest_ip, network, mask):
                next_hop_mac = self.arp_request(next_hop)
                print(f"Forwarding packet to next hop {next_hop} with MAC {next_hop_mac}")
                break

    def _ip_in_subnet(self, ip, network, mask):
        ip_bin = self._ip_to_bin(ip)
        network_bin = self._ip_to_bin(network)
        mask_bin = self._ip_to_bin(mask)
        return ip_bin & mask_bin == network_bin & mask_bin

    def _ip_to_bin(self, ip):
        return int(''.join(f'{int(octet):08b}' for octet in ip.split('.')), 2)

class ARPEntry:
    def __init__(self, ip_address, mac_address):
        self.ip_address = ip_address
        self.mac_address = mac_address

# Transport Layer Protocols
class TransportLayer:
    def __init__(self):
        self.port_table = {}

    def assign_port(self, process_name, port_type='well-known'):
        port = random.randint(0, 1023) if port_type == 'well-known' else random.randint(1024, 65535)
        self.port_table[port] = process_name
        return port

    def get_process_by_port(self, port):
        return self.port_table.get(port)

class TCP:
    def __init__(self, window_size):
        self.window = SlidingWindow(window_size)

    def send(self, data, send_func):
        self.window.send(data, send_func)

    def receive_ack(self, ack_num):
        self.window.receive_ack(ack_num)

class UDP:
    def send(self, data, send_func):
        send_func(data)

# Application Layer Services
class Telnet:
    def __init__(self, transport_layer):
        self.transport_layer = transport_layer
        self.port = self.transport_layer.assign_port('Telnet', 'well-known')

    def connect(self, destination_port):
        print(f"Connecting to Telnet service on port {destination_port}")

    def send_data(self, data, tcp_connection):
        tcp_connection.send(data, self._send_func)

    def _send_func(self, data, seq_num):
        print(f"Telnet sending data: {data} with sequence number: {seq_num}")

class FTP:
    def __init__(self, transport_layer):
        self.transport_layer = transport_layer
        self.port = self.transport_layer.assign_port('FTP', 'well-known')

    def connect(self, destination_port):
        print(f"Connecting to FTP service on port {destination_port}")

    def send_data(self, data, tcp_connection):
        tcp_connection.send(data, self._send_func)

    def _send_func(self, data, seq_num):
        print(f"FTP sending data: {data} with sequence number: {seq_num}")

# Testing the Full Protocol Stack
if __name__ == "__main__":
    simulator = NetworkSimulator()
    transport_layer = TransportLayer()

    devices = [simulator.create_device("end_device") for _ in range(5)]
    router = Router(str(uuid.uuid4()))

    for device in devices:
        simulator.create_connection(router, device)

    for i, device in enumerate(devices):
        ip_address = f"192.168.0.{i + 1}"
        device.ip_address = ip_address
        arp_entry = ARPEntry(ip_address, device.device_id)
        router.arp_table[device.device_id] = arp_entry.mac_address
        router.routing_table[ip_address] = arp_entry.mac_address

    print(f"ARP Entry: IP Address: {arp_entry.ip_address}, MAC Address: {arp_entry.mac_address}")

    simulator.send_data(devices[0], "Test data for routing", simulator.connections[0])

    tcp = TCP(window_size=4)
    udp = UDP()

    telnet_service = Telnet(transport_layer)
    ftp_service = FTP(transport_layer)

    telnet_service.connect(telnet_service.port)
    ftp_service.connect(ftp_service.port)

    telnet_service.send_data("Telnet Test Data", tcp)
    ftp_service.send_data("FTP Test Data", tcp)

    for i in range(5):
        tcp.receive_ack(i)
