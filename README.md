# D.R.I.S.T.I Simulation Pipeline

This repository contains the software simulation for the D.R.I.S.T.I project. It simulates a network where an ESP32 sensor node sends data to a Raspberry Pi gateway, which processes the information and displays a UI.

### ⚠️ Important Note
**Currently, this repository only contains the software simulation files. The actual hardware model implementation and the code for the physical devices will be uploaded to this repository soon!**

### Files Included:
* `fake_esp32.py`: Simulates an ESP32 generating and sending fake CSI (Channel State Information) data over UDP, including simulated anomaly injections (like fall detection).
* `pi_gateway.py`: Acts as the Raspberry Pi gateway. It receives the UDP data, visualizes the data using a real-time UI, and links to an MQTT cloud broker.
* `start_dristi.bat`: A simple Windows batch script to launch both the sensor simulation and the gateway UI simultaneously.

### How to Run:
Simply double-click the `start_dristi.bat` file to launch the simulation pipeline.
