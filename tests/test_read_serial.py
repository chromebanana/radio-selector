from radio_activator import read_serial

def test_parse_input():
    serial_data = b'2\r\n'

    assert read_serial.parse_input(serial_data) == 2
