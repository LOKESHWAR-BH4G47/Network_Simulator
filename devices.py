class Device:
    def __init__(self, name):
        self.name = name
        self.connected_devices = []

    def connect(self, other_device):
        self.connected_devices.append(other_device)
        other_device.connected_devices.append(self)

class Hub:
    def __init__(self, name):
        self.name = name
        self.connected_devices = []

    def connect(self, device):
        self.connected_devices.append(device)
        device.connected_devices.append(self)
        for device in self.connected_devices:
            print(f"Hub connection established with {device.name}")


def main():
    hub = Hub("CentralHub")  # Instantiate a Hub object
    device1 = Device("Device1")  # Instantiate a Device object
    hub.connect(device1)  # Connect device1 to the hub

if __name__ == "__main__":
    main()
