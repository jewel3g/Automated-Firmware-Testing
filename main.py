import serial
import time
import logging
import sys

# Optional Linux-only libraries
try:
    import smbus2   # For I2C
    import spidev   # For SPI
except ImportError:
    smbus2 = None
    spidev = None

# ------------------------------
# Configurations
# ------------------------------
LOG_FILE = "logs/firmware_test.log"

# Serial / UART
SERIAL_PORT = "COM3"  # Linux: "/dev/ttyUSB0"
BAUD_RATE = 115200

# I2C Example (Raspberry Pi)
I2C_BUS = 1
I2C_ADDR = 0x48  # Example address for sensor

# SPI Example (Raspberry Pi)
SPI_BUS = 0
SPI_DEVICE = 0

# Define Test Cases
TEST_CASES = [
    {"interface": "UART", "command": b"AT\r\n", "expected": b"OK"},
    {"interface": "UART", "command": b"LED_ON\r\n", "expected": b"LED:ON"},
    {"interface": "UART", "command": b"LED_OFF\r\n", "expected": b"LED:OFF"},
    {"interface": "I2C", "register": 0x00, "expected_range": (20, 30)},  # e.g., Temp Sensor
    {"interface": "SPI", "data": [0x9F], "expected_len": 3}  # Read JEDEC ID from flash
]

# ------------------------------
# Setup Logging
# ------------------------------
logging.basicConfig(filename=LOG_FILE,
                    level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

def run_uart_tests(ser, test, i):
    ser.write(test["command"])
    time.sleep(0.5)
    response = ser.read(100).strip()

    if test["expected"] in response:
        logging.info(f"✅ UART Test {i} PASSED: Received {response}")
        print(f"✅ UART Test {i} PASSED: {response}")
    else:
        logging.error(f"❌ UART Test {i} FAILED: Expected {test['expected']} but got {response}")
        print(f"❌ UART Test {i} FAILED: got {response}")


def run_i2c_tests(bus, test, i):
    try:
        value = bus.read_byte_data(I2C_ADDR, test["register"])
        if test["expected_range"][0] <= value <= test["expected_range"][1]:
            logging.info(f"✅ I2C Test {i} PASSED: Register {hex(test['register'])} = {value}")
            print(f"✅ I2C Test {i} PASSED: Value = {value}")
        else:
            logging.error(f"❌ I2C Test {i} FAILED: {value} out of range {test['expected_range']}")
            print(f"❌ I2C Test {i} FAILED: Value = {value}")
    except Exception as e:
        logging.error(f"❌ I2C Test {i} ERROR: {e}")
        print(f"❌ I2C Test {i} ERROR: {e}")


def run_spi_tests(spi, test, i):
    try:
        response = spi.xfer2(test["data"])
        if len(response) >= test["expected_len"]:
            logging.info(f"✅ SPI Test {i} PASSED: Response {response}")
            print(f"✅ SPI Test {i} PASSED: {response}")
        else:
            logging.error(f"❌ SPI Test {i} FAILED: Expected {test['expected_len']} bytes, got {response}")
            print(f"❌ SPI Test {i} FAILED: got {response}")
    except Exception as e:
        logging.error(f"❌ SPI Test {i} ERROR: {e}")
        print(f"❌ SPI Test {i} ERROR: {e}")


def run_tests():
    try:
        # Initialize UART
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2)
        time.sleep(2)

        # Initialize I2C
        bus = smbus2.SMBus(I2C_BUS) if smbus2 else None

        # Initialize SPI
        spi = spidev.SpiDev() if spidev else None
        if spi:
            spi.open(SPI_BUS, SPI_DEVICE)
            spi.max_speed_hz = 50000

        logging.info("Starting automated firmware tests...")
        print("🚀 Running Automated Firmware Tests...")

        for i, test in enumerate(TEST_CASES, start=1):
            if test["interface"] == "UART":
                run_uart_tests(ser, test, i)
            elif test["interface"] == "I2C" and bus:
                run_i2c_tests(bus, test, i)
            elif test["interface"] == "SPI" and spi:
                run_spi_tests(spi, test, i)
            else:
                logging.warning(f"⚠️ Test {i} skipped: Interface {test['interface']} not available")
                print(f"⚠️ Test {i} skipped: Interface {test['interface']} not available")

        ser.close()
        if bus: bus.close()
        if spi: spi.close()
        logging.info("All tests completed.")
        print("✅ All tests completed. Logs saved.")

    except Exception as e:
        logging.error(f"Fatal error running tests: {e}")
        print(f"❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run_tests()
