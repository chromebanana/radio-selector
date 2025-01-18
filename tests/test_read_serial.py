import pytest

from radio_activator import read_serial


def test_parse_input():
    serial_data = b"2\r\n"

    assert read_serial.parse_input(serial_data) == 2


STATIONS = {
    1: "https://groovy-radio-url.com",
    2: "https://guff-and-trollop.com",
}


def test_get_station_url():
    assert read_serial.get_station_url(1, STATIONS) == "https://groovy-radio-url.com"


def test_get_station_url_no_station_configured():
    with pytest.raises(read_serial.NoStationConfigured):
        read_serial.get_station_url(3, STATIONS)
