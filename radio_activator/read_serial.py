import os

import serial
from dotenv import load_dotenv

load_dotenv()

BAUD_RATE = 9600
SERIAL_PORT = os.getenv("SERIAL_PORT")


def main():
    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
        print("Waiting for serial data...")
        while True:
            line = ser.readline()
            if line:
                print(f"{line}")


if __name__ == "__main__":
    main()
