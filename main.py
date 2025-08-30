import serial
import time
import logging

# ------------------------------
# Configurations
# ------------------------------
SERIAL_PORT = "COM3"  # Change for Linux: "/dev/ttyUSB0"
BAUD_RATE = 115200
TEST_CASES = [
    {"command": b"AT\r\n", "expected": b"OK"},
    {"command": b"LED_ON\r\n", "expected": b"LED:ON"},
    {"command": b"LED_OFF\r\n", "expected": b"LED:OFF"}
]
LOG_FILE = "firmware_test.log"

# ------------------------------
# Setup Logging
# ------------------------------
logging.basicConfig(filename=LOG_FILE,
                    level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")


def run_tests():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2)
        time.sleep(2)  # Allow device reset

        logging.info("Starting automated firmware tests...")

        for i, test in enumerate(TEST_CASES, start=1):
            logging.info(f"Running Test {i}: {test['command'].decode().strip()}")

            ser.write(test["command"])
            time.sleep(0.5)
            response = ser.read(100).strip()

            if test["expected"] in response:
                logging.info(f"✅ Test {i} PASSED: Received {response}")
                print(f"✅ Test {i} PASSED: {response}")
            else:
                logging.error(f"❌ Test {i} FAILED: Expected {test['expected']} but got {response}")
                print(f"❌ Test {i} FAILED: got {response}")

        ser.close()
        logging.info("All tests completed.")

    except Exception as e:
        logging.error(f"Error running tests: {e}")
        print(f"Error: {e}")


if __name__ == "__main__":
    run_tests()
