from devices import MacAddress, Hub, Device, Switch

def main():
    hub_mac_manager = MacAddress()  # Separate MAC address manager for the hubs
    switch_mac_manager = MacAddress()  # Separate MAC address manager for the switch
    device_mac_manager = MacAddress()  # Separate MAC address manager for the devices

    switch = Switch("MainSwitch", switch_mac_manager)  # Pass the MAC address manager to the Switch constructor

    hub1 = Hub("Hub1", hub_mac_manager)
    hub2 = Hub("Hub2", hub_mac_manager)

    devices_hub1 = [Device(f"Device{i}", device_mac_manager) for i in range(1, 6)]
    devices_hub2 = [Device(f"Device{i+5}", device_mac_manager) for i in range(1, 6)]

    # Connecting devices to hubs
    for device in devices_hub1:
        hub1.connect(device)
    for device in devices_hub2:
        hub2.connect(device)

    # Connecting hubs to switch
    switch.connect(hub1, 1)
    switch.connect(hub2, 2)

    s = int(input("Enter the device number who wants to send: "))
    r = int(input("Enter the device number you want to send to: "))

    if 1 <= s <= 10 and 1 <= r <= 10:
        if s <= 5:
            sender_hub = hub1
            sender_device = devices_hub1[s-1]
        else:
            sender_hub = hub2
            sender_device = devices_hub2[s-6]
        if r <= 5:
            receiver_hub = hub1
            receiver_device = devices_hub1[r-1]
        else:
            receiver_hub = hub2
            receiver_device = devices_hub2[r-6]
        sender_device.send_data("10101", sender_hub, switch, receiver_device)
    else:
        print("Device numbers are out of range.")

    print("\nMAC Addresses of Devices:")
    for device_name, mac_address in device_mac_manager.mac_addresses.items():
        print(f"{device_name}: {mac_address}")

    print("\nMAC Addresses of Hubs:")
    for hub_name, mac_address in hub_mac_manager.mac_addresses.items():
        print(f"{hub_name}: {mac_address}")

    print("\nMAC Addresses of Switch:")
    for switch_name, mac_address in switch_mac_manager.mac_addresses.items():
        print(f"{switch_name}: {mac_address}")


if __name__ == "__main__":
    main()
    
