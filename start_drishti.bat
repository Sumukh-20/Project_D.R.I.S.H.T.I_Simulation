@echo off
echo Starting D.R.I.S.T.I Simulation Pipeline...

echo 1. Launching Fake ESP32 Sensor Data...
start cmd /k "python fake_esp32.py"

echo 2. Launching Raspberry Pi Gateway UI...
start cmd /k "python pi_gateway.py"

echo Both scripts are running in the background! 
echo You can now go to your browser and hit "Play" on the Wokwi simulation.
pause