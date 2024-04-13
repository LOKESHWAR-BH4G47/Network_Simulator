import time
from devices import MacAddress, Hub, Device, Switch

class ReservationProtocol:
    def __init__(self, num_slots):
        self.num_slots = num_slots
        # Initialize all slots as available, but reserve odd slots
        self.slots_available = [True if i % 2 == 0 else False for i in range(num_slots)]

    def reserve_slot(self, slot):
        if 0 <= slot < self.num_slots:
            if self.slots_available[slot]:
                self.slots_available[slot] = False
                return True  # Slot reserved successfully
            else:
                print("Slot already reserved.")
                return False  # Slot already reserved
        else:
            print("Invalid slot number.")
            return False  # Invalid slot number

    def release_slot(self, slot):
        if 0 <= slot < self.num_slots and not self.slots_available[slot]:
            self.slots_available[slot] = True
            print(f"Slot {slot} released.")
        else:
            print("Invalid slot number or slot not reserved.")

def chunk_data(data, chunk_size):
    return [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]

class SelectiveRepeat:
    def __init__(self, window_size):
        self.window_size = window_size
        self.sent_frames = {}
        self.next_sequence_number = 0

    def send_frame(self, frame):
        self.sent_frames[self.next_sequence_number] = frame
        self.next_sequence_number += 1

    def receive_ack(self, seq_num):
        if seq_num in self.sent_frames:
            print(f"Acknowledgment received for frame {seq_num}")
            del self.sent_frames[seq_num]
            return True
        else:
            print(f"Acknowledgment for frame {seq_num} not found")
            return False

def main():
    num_slots = 10  # Number of time slots in the reservation protocol
    reservation_protocol = ReservationProtocol(num_slots)

    hub_mac_manager = MacAddress()
    switch_mac_manager = MacAddress()
    device_mac_manager = MacAddress()

    switch = Switch("MainSwitch", switch_mac_manager)

    hub1 = Hub("Hub1", hub_mac_manager)
    hub2 = Hub("Hub2", hub_mac_manager)

    devices_hub1 = [Device(f"Device{i}", device_mac_manager) for i in range(1, 6)]
    devices_hub2 = [Device(f"Device{i+5}", device_mac_manager) for i in range(1, 6)]

    for device in devices_hub1:
        hub1.connect(device)
    for device in devices_hub2:
        hub2.connect(device)

    switch.connect(hub1, 1)
    switch.connect(hub2, 2)

    s = int(input("Enter the device number who wants to send: "))
    r = int(input("Enter the device number you want to send to: "))

    if 1 <= s <= 10 and 1 <= r <= 10:
        data = input("Enter the data to send: ")
        # Convert data to binary format
        binary_data = bin(int.from_bytes(data.encode(), 'big'))[2:]
        print("Binary representation:", binary_data)

        # Chunk the binary data into frames of 16 bits each
        frames = chunk_data(binary_data, 16)

        slot = int(input("Enter the time slot to reserve: "))
        if reservation_protocol.reserve_slot(slot):
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

            window_size = 3  # Adjust the window size as needed
            selective_repeat = SelectiveRepeat(window_size)
            for frame in frames:
                sender_device.send_data(frame, sender_hub, receiver_hub, switch, receiver_device)
                print(f"Sending frame: {frame}")
                time.sleep(1)  # Add a delay of 1 second between sending each frame

            # Wait for acknowledgments for each frame
            for seq_num in range(selective_repeat.next_sequence_number):
                while not selective_repeat.receive_ack(seq_num):
                    pass
        else:
            print("Failed to reserve time slot. Aborting transmission.")
    else:
        print("Device numbers are out of range.")

if __name__ == "__main__":
    main()
