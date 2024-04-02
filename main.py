from devices import *

def main():
    n_devices = int(input("enter no of devices : "))

    hub = Hub("CentralHub")
    devices = [Device(f"Device{i}") for i in range(1, n_devices + 1)]
 
    for device in devices:
        hub.connect(device)

    s = int(input("enter the device number who want to send:  "))
    r = int(input("enter the device number you want to send:  "))
 
    devices[s-1].send_data("10101", hub, devices[r-1])

if __name__ == "__main__":
    main()
# ed