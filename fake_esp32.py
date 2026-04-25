import numpy as np
import time
import socket
import json
import random

UDP_IP = "127.0.0.1" 
UDP_PORT = 5005      
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def generate_fake_csi(is_anomaly=False, num_subcarriers=30):
    if is_anomaly:
        # Generate a massive spike in the data!
       return (np.random.rand(num_subcarriers) * 10.0).tolist()
    else:
        # Normal baseline data
        return np.random.rand(num_subcarriers).tolist()

print(f"Starting Fake ESP32 with Anomaly Injection...")

packet_count = 0
try:
    while True:
        packet_count += 1
        
        # Every 10th packet, we simulate a sudden anomaly (like a fall)
        if packet_count % 10 == 0:
            print(">>> INJECTING ANOMALY (Simulated Fall/Movement) <<<")
            fake_data = generate_fake_csi(is_anomaly=True)
        else:
            fake_data = generate_fake_csi(is_anomaly=False)
            print("Sending normal data...")
            
        payload = json.dumps({"device": "ESP32_Node_1", "csi": fake_data}).encode('utf-8')
        sock.sendto(payload, (UDP_IP, UDP_PORT))
        
        time.sleep(1) 
        
except KeyboardInterrupt:
    print("\nSimulation stopped.")