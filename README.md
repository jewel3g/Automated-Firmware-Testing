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

Install dependencies:
```bash
pip install -r requirements.txt
