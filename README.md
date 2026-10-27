# AegisVault

Autonomous Dual-Tier Threat Mitigation and Active Asset Concealment IoT Security System for CSE402 (Internet of Things Lab), Department of CSE, University of Information Technology and Sciences (UITS).

## Team Members
* Elham Rafat Mahmud (ID: 1056)
* Rudro Antony Mrong (ID: 1059)
* Md. Masud Rahman (ID: 1064)

Supervisor: S. M. Zafrul Islam, Lecturer, Department of CSE, UITS

## Project Overview
AegisVault is an embedded IoT security system built on an ESP32 microcontroller with active physical countermeasures:
* Optical & Thermal Fusion: LDR laser break-beam receiver (GPIO 34) and PIR motion sensor (GPIO 27) prevent false alarms.
* Mechanical Concealment: Servo 1 (GPIO 18) locks the deadbolt, Servo 2 (GPIO 13) drops the asset into a hidden chamber.
* Tamper Limit Switch: GPIO 14 detects physical tampering of the sub-chamber.
* Real-time MQTT Telemetry: Publishes status to `aegisvault/telemetry` and accepts commands on `aegisvault/commands` over HiveMQ.
* Dual-Mode Retro Dashboard: Web terminal with manual PC disarm and smartphone WebAuthn biometric (fingerprint/Face ID) clearance.

## Hardware & Pin Assignments
* LDR Laser Receiver: GPIO 34 (Analog)
* PIR Motion Sensor: GPIO 27 (Digital Input)
* Tamper Limit Switch: GPIO 14 (Internal Pull-Up)
* Door Deadbolt Servo: GPIO 18 (PWM)
* Asset Drop Servo: GPIO 13 (PWM)
* Buzzer (Tier 1 Alert): GPIO 25
* Siren (Tier 2 Breach): GPIO 26
* Red Alert LED: GPIO 32
* White Strobe LED: GPIO 33

## How to Run

### 1. Run the ESP32 Simulation (Wokwi)
1. Open the project in Wokwi using `diagram.json` and `sketch.ino`.
2. Click Start Simulation.
3. The ESP32 connects to WiFi (`Wokwi-GUEST`), links to HiveMQ broker (`broker.hivemq.com`), calibrates sensors, and enters `IDLE_ARMED` state.

### 2. Open the Dashboard

#### Option A: GitHub Pages (Direct & Mobile Biometric)
Enable GitHub Pages in repository settings pointing to the `main` branch root. Open:
`https://<username>.github.io/AegisVault/dashboard.html`

#### Option B: Local PC Browser
Open `dashboard.html` directly in any web browser. Use the `[ DISARM / RESET SYSTEM ]` button to disarm.

#### Option C: Local Tunnel for Mobile Fingerprint Testing
To test mobile fingerprint authentication over your phone without certificate errors:
1. Run the gateway script:
```bash
python3 run_tunnel.py
```
2. Open the printed `https://...trycloudflare.com/dashboard.html` link on your phone.
3. Tap `[ ⌘ SCAN FINGERPRINT TO DISARM ]` to trigger your phone's native fingerprint/biometric sensor. Upon verification, the vault unlocks and alarms silence.
