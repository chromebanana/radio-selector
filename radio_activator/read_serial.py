import os

import serial
from dotenv import load_dotenv

load_dotenv()

STATIONS = {
    1: "https://stream-relay-geo.ntslive.net/stream",
    2: "https://stream-relay-geo.ntslive.net/stream2",
    3: "https://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_radio_three/bbc_radio_three.isml/bbc_radio_three-audio%3d96000.norewind.m3u8",
    4: "https://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_radio_fourfm/bbc_radio_fourfm.isml/bbc_radio_fourfm-audio%3d96000.norewind.m3u8",
}


BAUD_RATE = 9600
SERIAL_PORT = os.getenv("SERIAL_PORT")


def parse_input(serial_data: bytes) -> int:
    """
    Given a string of serial data, parse the integer value from it.
    """
    return int(serial_data.decode("utf-8").strip())


class NoStationConfigured(Exception):
    pass


def get_station_url(station_number: int, stations: dict[int, str]) -> str:
    """
    Given a station number, return the URL of the station.
    """
    station_url = stations.get(station_number)
    if station_url is None:
        raise NoStationConfigured
    return station_url


def main():
    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
        print("Waiting for serial data...")
        while True:
            line = ser.readline()
            if line:
                dialed_number = parse_input(line)
                print(f"Received: {dialed_number}")
                try:
                    station_url = get_station_url(dialed_number, STATIONS)
                    print(f"Playing: {station_url}")
                except NoStationConfigured:
                    print(f"No station configured for {dialed_number}.")


if __name__ == "__main__":
    main()
