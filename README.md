# D.R.I.S.T.I Simulation Pipeline

This repository contains the software simulation for the D.R.I.S.T.I project. It simulates a network where an ESP32 sensor node sends data to a Raspberry Pi gateway, which processes the information and displays a UI.

### ⚠️ Important Note
**Currently, this repository only contains the software simulation files. The actual hardware model implementation and the code for the physical devices will be uploaded to this repository soon!**

### Files Included:
* `fake_esp32.py`: Simulates an ESP32 generating and sending fake CSI (Channel State Information) data over UDP, including simulated anomaly injections (like fall detection).
* `pi_gateway.py`: Acts as the Raspberry Pi gateway. It receives the UDP data, visualizes the data using a real-time UI, and links to an MQTT cloud broker.
* `start_dristi.bat`: A simple Windows batch script to launch both the sensor simulation and the gateway UI simultaneously.

### How to Run:

**Method 1: Using the Batch File (Windows Only)**
Simply double-click the `start_dristi.bat` file. This will automatically open the necessary command windows and launch the entire simulation pipeline.

**Method 2: Manual Execution (Command Line/Terminal)**
If you prefer to run the scripts manually or are not using Windows:
1. Open two separate terminal or command prompt windows.
2. In the first window, start the sensor simulation by running:
   ```bash
   python fake_esp32.py
3. In the second window, start the gateway UI by running
   ```bash
   python pi_gateway.py 
