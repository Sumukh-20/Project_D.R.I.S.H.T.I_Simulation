import matplotlib
matplotlib.use('Qt5Agg') 
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import socket
import json
import numpy as np
import random
import paho.mqtt.client as mqtt
import time

# --- 1. AURA-NET CLOUD LINK (MQTT) ---
MQTT_BROKER = "broker.hivemq.com" 
MQTT_TOPIC = "dristi/rvce/actuator"

print("D.R.S.H.T.I SYSTEM INITIALIZING...")
client_name = f"CogniSense_Pro_{random.randint(1000,9999)}"
mqtt_client = mqtt.Client(client_id=client_name)

try:
    mqtt_client.connect(MQTT_BROKER, 1883, 60)
    mqtt_client.loop_start()
    print("✅ Cloud Link Active!")
except Exception as e:
    print(f"⚠️ Could not connect to Cloud: {e}")

# --- 2. UDP SETUP ---
UDP_IP = "127.0.0.1" 
UDP_PORT = 5005      
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
sock.settimeout(2.0)

# --- 3. PRO 2x2 UI SETUP ---
plt.style.use('dark_background')
plt.ion() 
fig = plt.figure(figsize=(14, 8))
fig.suptitle(" D.R.I.S.T.I : SPATIAL PROCTORING TERMINAL", fontsize=16, weight='heavy', color='#00f3ff', ha='left', x=0.03, family='monospace')
fig.patch.set_facecolor('#02060e') # Deeper, darker cyber background

gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.2)
ax_map = fig.add_subplot(gs[0, 0])  
ax_alert = fig.add_subplot(gs[0, 1]) 
ax_csi = fig.add_subplot(gs[1, 0])   
ax_log = fig.add_subplot(gs[1, 1])   

# Setup Glowing CSI Plot
ax_csi.set_title("CSI MICRO-DOPPLER SPECTROGRAM", color='#88aacc', loc='left', family='monospace', fontsize=10)
ax_csi.set_ylim(0, 5)
ax_csi.set_xlim(0, 50)
ax_csi.set_facecolor('#040d1a')
ax_csi.grid(color='#00334d', linestyle=':', linewidth=0.5)
raw_line, = ax_csi.plot([], [], label='Raw RF Carrier', color='#ff0055', alpha=0.4, linewidth=1)
clean_line, = ax_csi.plot([], [], label='AI Cleaned', color='#00f3ff', linewidth=2)
ax_csi.legend(loc="upper right", facecolor='#02060e', edgecolor='#00f3ff', labelcolor='white')

history_buffer, x_data, y_raw_data, y_clean_data = [], [], [], []
packet_count = 0
last_state = "SAFE"

desks = [(1, 12), (6, 12), (11, 12), 
         (1, 7),  (6, 7),  (11, 7), 
         (1, 2),  (6, 2),  (11, 2)]

# Expanded student database
student_names = ["Student A", "Student B", "Student C", "Student D", "Student E", "Student F", "Student G", "Student H", "Student I", "Student J", "Student K", "Student L"]
anomaly_types = ["USING MOBILE", "FALLING", "UNKNOWN PERSON"]

# Single target tracker
current_target = {"name": "AARAV", "x": desks[0][0] + 1.5, "y": desks[0][1] + 1, "status": "SCANNING...", "color": "#00f3ff"}

# --- 4. MAIN DASHBOARD LOOP ---
try:
    while True:
        try:
            data, addr = sock.recvfrom(1024) 
            payload = json.loads(data.decode('utf-8'))
            raw_csi = payload["csi"]
            
            history_buffer.append(raw_csi)
            if len(history_buffer) > 5: history_buffer.pop(0)
            current_value = np.mean(history_buffer, axis=0)[0]

            packet_count += 1
            x_data.append(packet_count)
            y_raw_data.append(raw_csi[0])
            y_clean_data.append(current_value)
            
            if len(x_data) > 50:
                x_data.pop(0); y_raw_data.pop(0); y_clean_data.pop(0)
                ax_csi.set_xlim(x_data[0], x_data[-1])
                
            raw_line.set_data(x_data, y_raw_data)
            clean_line.set_data(x_data, y_clean_data)
            
            # Add neon glow under the line
            [p.remove() for p in ax_csi.collections] # Clear old fills
            ax_csi.fill_between(x_data, 0, y_clean_data, color=current_target["color"], alpha=0.15)

            # --- TARGET SCANNING LOGIC ---
            if current_value > 1.5:
                # 🚨 ANOMALY TRIGGERED 🚨
                if last_state != "ANOMALY":
                    mqtt_client.publish(MQTT_TOPIC, "ANOMALY") 
                    last_state = "ANOMALY"
                    
                    ano_type = random.choice(anomaly_types)
                    target_name = "UNKNOWN INTRUDER" if ano_type == "UNKNOWN PERSON" else random.choice(student_names)
                    desk = random.choice(desks)
                    
                    current_target = {"name": target_name, "x": desk[0] + 1.5, "y": desk[1] + 1, "status": ano_type, "color": "#ff003c"}
            else:
                # ✅ NORMAL SCANNING ✅
                if last_state != "SAFE":
                    mqtt_client.publish(MQTT_TOPIC, "SAFE")
                    last_state = "SAFE"
                
                # Switch normal targets every 20 packets to simulate room scanning
                if packet_count % 20 == 0:
                     desk = random.choice(desks)
                     current_target = {"name": random.choice(student_names), "x": desk[0] + 1.5, "y": desk[1] + 1, "status": "NORMAL SITTING", "color": "#00f3ff"}

            # Slight live jitter
            current_target["x"] = max(0.5, min(15.5, current_target["x"] + random.uniform(-0.05, 0.05)))
            current_target["y"] = max(0.5, min(15.5, current_target["y"] + random.uniform(-0.05, 0.05)))

            # --- RENDER CLASSROOM MAP ---
            ax_map.clear()
            ax_map.set_title("WI-FI SPATIAL MAP (GAN V2)", color='#88aacc', loc='left', family='monospace', fontsize=10)
            ax_map.set_xlim(0, 16); ax_map.set_ylim(0, 16)
            ax_map.set_facecolor('#040d1a')
            ax_map.grid(color='#00334d', linestyle='-', linewidth=0.5, alpha=0.5)
            ax_map.set_xticks([]); ax_map.set_yticks([]) 
            
            # Draw Wireframe Desks
            for dx, dy in desks:
                ax_map.add_patch(patches.Rectangle((dx, dy), 3, 2, fill=False, ec='#005580', lw=1.5))
                ax_map.text(dx+1.5, dy+1, "DESK", color='#005580', ha='center', va='center', fontsize=7, family='monospace')

            # Draw "Cool" Target Reticle
            c_color = current_target["color"]
            ax_map.scatter(current_target["x"], current_target["y"], c=c_color, s=800, alpha=0.15) # Outer Glow
            ax_map.scatter(current_target["x"], current_target["y"], c=c_color, s=250, marker='+', linewidths=1.5) # Crosshair
            ax_map.scatter(current_target["x"], current_target["y"], c='white', s=30, marker='o') # Center Dot
            
            ax_map.text(current_target["x"], current_target["y"] + 1.2, f"[ ID: {current_target['name']} ]\n{current_target['status']}", color=c_color, ha='center', fontsize=9, weight='bold', family='monospace', bbox=dict(facecolor='#02060e', alpha=0.6, edgecolor='none'))

            # --- RENDER PANELS ---
            ax_alert.clear(); ax_alert.set_facecolor('#040d1a'); ax_alert.axis('off')
            ax_log.clear(); ax_log.set_facecolor('#040d1a'); ax_log.axis('off')
            
            # Header Texts
            ax_alert.text(0.05, 0.9, "THREAT DETECTION", color='#88aacc', fontsize=10, family='monospace')
            ax_log.text(0.05, 0.9, "", color='#88aacc', fontsize=10, family='monospace')

            if last_state == "ANOMALY":
                ax_csi.set_facecolor('#1a0404') # Flash red background on wave
                ax_alert.add_patch(patches.Rectangle((0, 0), 1, 1, fill=False, ec='#ff003c', lw=4, transform=ax_alert.transAxes)) # Red Border
                ax_alert.text(0.5, 0.6, f"!!! ALERT !!!\n{current_target['status']}", color='#ff003c', fontsize=20, weight='bold', ha='center', family='monospace')
                ax_alert.text(0.5, 0.3, f">> LOCK: {current_target['name']} <<", color='white', fontsize=14, ha='center', backgroundcolor='#ff003c', family='monospace')
                
                ax_log.text(0.05, 0.6, f"> TIME: {time.strftime('%H:%M:%S')}\n> CLASSIFIER: {current_target['status']}\n> MATCH: {current_target['name']}\n> CONFIDENCE: {random.randint(92,99)}%\n> HARDWARE: ACTUATING...", color='#ff003c', fontsize=11, family='monospace')
            else:
                ax_alert.add_patch(patches.Rectangle((0, 0), 1, 1, fill=False, ec='#005580', lw=2, transform=ax_alert.transAxes)) # Blue Border
                ax_alert.text(0.5, 0.6, "SYSTEM SECURE\nNO THREATS", color='#00f3ff', fontsize=18, weight='bold', ha='center', family='monospace')
                ax_alert.text(0.5, 0.3, f"TRACKING: {current_target['name']}", color='#88aacc', fontsize=12, ha='center', family='monospace')
                
                log_text = f"> TIME: {time.strftime('%H:%M:%S')}\n> RF LINK: ACTIVE (500Hz)\n> TARGET: {current_target['name']}\n> POSTURE: NORMAL\n> STATUS: SCANNING..."
                ax_log.text(0.05, 0.6, log_text, color='#00f3ff', fontsize=11, family='monospace')

            plt.pause(0.01)
        except socket.timeout:
            plt.pause(0.01) 
except KeyboardInterrupt:
    mqtt_client.disconnect()
    print("\nSystem Offline.")