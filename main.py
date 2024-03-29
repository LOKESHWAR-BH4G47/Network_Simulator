import networkx as nx
import matplotlib.pyplot as plt

class Device:
    def __init__(self, name):
        self.name = name
        self.connections = []

    def connect(self, other_device):
        self.connections.append(other_device)
        other_device.connections.append(self)
        # Add edge to the graph for visualization
        topology_graph.add_edge(self.name, other_device.name)

    def send_data(self, data, recipient):
        print(f"{self.name} is sending data to {recipient.name}: {data}")
        for connection in self.connections:
            if connection == recipient:
                connection.receive_data(data, self)

    def receive_data(self, data, sender):
        print(f"{self.name} received data from {sender.name}: {data}")

class Hub:
    def __init__(self, name):
        self.name = name
        self.connections = []

    def connect(self, device):
        self.connections.append(device)
        device.connections.append(self)
        # Add edge to the graph for visualization
        topology_graph.add_edge(self.name, device.name)

    def receive_data(self, data, sender):
        print(f"{self.name} received data from {sender.name} and is forwarding it.")
        for device in self.connections:
            if device != sender:
                device.receive_data(data, sender)

# Initialize a NetworkX graph
topology_graph = nx.Graph()

def create_star_topology(num_devices):
    hub = Hub("CentralHub")
    devices = [Device(f"Device{i}") for i in range(1, num_devices + 1)]

    for device in devices:
        hub.connect(device)

    return hub, devices

def visualize_topology():
    plt.figure(figsize=(10, 8))
    nx.draw(topology_graph, with_labels=True, node_size=1500, node_color="lightblue", font_size=10, font_weight="bold")
    plt.title("Network Topology")
    plt.show()

def main():
    # Example usage and visualization
    hub, devices = create_star_topology(6)
    visualize_topology()

if __name__ == "__main__":
    main()
