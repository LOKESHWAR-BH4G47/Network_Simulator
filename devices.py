from cryptography.fernet import Fernet

key = Fernet.generate_key()
fernet = Fernet(key)

class Encrpyt_data:
    @staticmethod
    def encMessage(data):
        return fernet.encrypt(data.encode())

class Decrpyt_data:
    @staticmethod
    def decMessage(encMessage):
        return fernet.decrypt(encMessage).decode()

class Device:
    def __init__(self, name):
        self.name = name
        self.connected_devices = []

    def connect(self, other_device):
        self.connected_devices.append(other_device)
        other_device.connected_devices.append(self)

    def send_data(self, data, hub, receiver):
        print(f"{self.name} is sending data to {receiver.name}: {data}")
        Message = Encrpyt_data.encMessage(data)
        hub.receive_from_device(Message, self.name, receiver.name) # Fixed to use hub's method

    def receive_data(self, encMessage, sender, receiver):
        if self.name == receiver:
            Message = Decrpyt_data.decMessage(encMessage)
            print(f"{self.name} received data from {sender}: {Message}")
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
        self.send_from_hub(encMessage, sender, receiver)

    def send_from_hub(self, encMessage, sender, receiver):
        for device in self.connected_devices:
            if device.name != sender:
                device.receive_data(encMessage, sender, receiver)


