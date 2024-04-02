from cryptography.fernet import Fernet



key = Fernet.generate_key()
fernet = Fernet(key)


class Device:
    def __init__(self, name):
        self.name = name
        self.connected_devices = []

    def connect(self, other_device):
        self.connected_devices.append(other_device)
        other_device.connected_devices.append(self)

    def send_data(self, data, hub, receiver):
        print(f"{self.name} is sending data to {receiver.name}: {data}")
        encMessage = fernet.encrypt(data.encode())
        hub.receive_from_device(encMessage, self.name, receiver.name) # Fixed to use hub's method

    def receive_data(self, encMessage, sender, receiver):
        if self.name == receiver: # Corrected the logic to compare names
            decMessage = fernet.decrypt(encMessage).decode()
            print(f"{self.name} received data from {sender}: {decMessage}")
        else:
            print(f"{self.name} rejected data {encMessage} from {sender}")
    
class Hub:
    def __init__(self, name):
        self.name = name
        self.connected_devices = []

    def connect(self, device):
        self.connected_devices.append(device)
        device.connected_devices.append(self)
        print(f"Hub connection established with {device.name}")

    def receive_from_device(self, encMessage, sender, receiver):
        print(f"{self.name} received data from {sender} and is forwarding it.")
        self.send_from_hub(encMessage, sender, receiver) # Corrected call

    def send_from_hub(self, encMessage, sender, receiver):
        for device in self.connected_devices: # Corrected attribute name
            if device.name != sender: # Corrected logic to compare names
                device.receive_data(encMessage, sender, receiver)

def main():
    n_devices = int(input("enter no of devices : "))

    hub = Hub("CentralHub")
    devices = [Device(f"Device{i}") for i in range(1, n_devices + 1 )]
 
    for device in devices:
        hub.connect(device)

    s = int(input("enter the device number who want to send:  "))
    r = int(input("enter the device number you want to send:  "))
 


    devices[s-1].send_data("10101", hub, devices[r-1]) # Corrected data to  stringg

if __name__ == "__main__":
    main()
