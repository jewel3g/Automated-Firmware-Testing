# Automated Firmware Testing with Python

This project automates firmware testing using **Python + PySerial**.  
It connects to an embedded device via serial port, sends commands, and verifies responses automatically.

## Features
- Sends predefined test commands
- Validates responses (PASS/FAIL)
- Logs results to `logs/firmware_test.log`
- Works on **Windows, Linux, Mac**

## Requirements
- Python 3.x
- [PySerial](https://pypi.org/project/pyserial/)

## Install dependencies:
```bash
pip install -r requirements.txt
Usage

Connect your embedded device via USB/Serial.

Update the serial port in firmware_test.py:

SERIAL_PORT = "COM3"  # or "/dev/ttyUSB0"


Run the script:

python firmware_test.py


Logs will be saved in logs/firmware_test.log.

## Example Output
✅ Test 1 PASSED: b'OK'
✅ Test 2 PASSED: b'LED:ON'
❌ Test 3 FAILED: Expected b'LED:OFF' but got b'ERROR'
