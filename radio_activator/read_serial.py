import os

import serial
from dotenv import load_dotenv

load_dotenv()

BAUD_RATE = 9600
SERIAL_PORT = os.getenv("SERIAL_PORT")

def parse_input(serial_data: bytes) -> int:
    """
    Given a string of serial data, parse the integer value from it.
    """
    return int(serial_data.decode("utf-8").strip())

def main():
    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
        print("Waiting for serial data...")
        while True:
            line = ser.readline()
            if line:
                dialed_number = parse_input(line)
                print(f"Received: {dialed_number}")


if __name__ == "__main__":
    main()
