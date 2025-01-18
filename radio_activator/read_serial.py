import os
import subprocess
import threading

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


def play_radio(station_url: str, stop_playing: threading.Event):
    process = subprocess.Popen(["mpv", station_url])
    stop_playing.wait()
    process.terminate()


def main():
    radio_thread: threading.Thread | None = None
    stop_playing_event = threading.Event()

    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
        print("Waiting for serial data...")
        while True:
            line = ser.readline()
            if line:
                dialed_number = parse_input(line)
                print(f"Received: {dialed_number}")
                try:
                    station_url = get_station_url(dialed_number, STATIONS)
                except NoStationConfigured:
                    print(f"No station configured for {dialed_number}.")

                if radio_thread and radio_thread.is_alive():
                    stop_playing_event.set()
                    radio_thread.join()  # Wait for the thread to finish
                    stop_playing_event.clear()

                radio_thread = threading.Thread(
                    target=play_radio, args=(station_url, stop_playing_event)
                )
                radio_thread.start()
                print(f"Playing: {station_url}")


if __name__ == "__main__":
    main()
