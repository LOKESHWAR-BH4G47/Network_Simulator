class Device:
    def __init__(self, name):
        self.name = name
        self.connected_devices = []

    def connect(self, other_device):
        self.connected_devices.append(other_device)
        other_device.connected_devices.append(self)

    def send_data(self,data,hub,receiver):
        print(f"{self.name} is sending data to {recipient.name}: {data}")
        for connection in self.connections:
            if connection == recipient:
                connection.recieve_from_device(data,self.name,receiver)
        






    def receive_data(self, data, sender,reciever):
        if device == reciever:
            print(f"{self.name} received data from {sender.name}: {data}")
        else:
            print(f"{self.name} rejected data from {sender.name}: {data}")



class Hub:
    def __init__(self, name):
        self.name = name
        self.connected_devices = []

    def connect(self, device):
        self.connected_devices.append(device)
        device.connected_devices.append(self)
        print(f"Hub connection established with {device.name}")

    def recieve_from_device(self,data,sender,receiver):
        print(f"{self.name} received data from {sender.name} and is forwarding it.")
        self.send_from_hub(self,data,sender,receiver)

   def send_from_hub(self):
       for device in self.connections:
           if device != sender:
               device.receive_data(data, sender,reciever)




def main():
    n_devices = int(input("enter no of devices : "))

    hub = Hub("CentralHub")  # Instantiate a Hub object
    devices = [Device(f"Device{i}") for i in range(1, n_devices + 1)]

    for device in devices:
        hub.connect(device)

    devices[0].send_data(10101,hub,devices[2])


    

if __name__ == "__main__":
    main()
