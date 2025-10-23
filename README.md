# Telephone Radio Selector
An IoT project that uses the rotary dial of an old telephone to select and play radio stations.

## Overview
This project upcycles an old rotary phone dial to tune into internet radio stations.
An Arduino Nano reads the dialed number and sends it to a Raspberry Pi over serial. The Raspberry Pi maps the number to a specific radio station and plays it using a media player.

## Setup
### Hardware
* Rotary dial (this one generated pulses when the dial was rotated)
* Arduino Nano (actuator)
* Raspberry Pi (controller)

### Software
* Arduino code to count the pulses and send the number over serial
* Python code to read the serial data and play the radio station using MPV
* MPV media player (`sudo apt install mpv`)

## Getting Started
### Setting up radio player
Install mpv media player:
```
sudo apt install mpv
```
Configure environment variables:
```
cp .env-example .env
```
Note: you'll need to update the serial port to match where your Arudiuno is connected. You can check this with `ls /dev/ttyUSB*` (linux) or `ls /dev/tty.*` (mac).

Set up python env and dependencies:
```
python -m venv pi-radio
source pi-radio/bin/activate
pip install -r requirements.txt
```
Run the ting...
```
python radio_activator/read_serial.py
```
