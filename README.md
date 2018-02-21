# Tampere public transportation screen

This is a minimalist python software to display departing buses on given bus stops with raspberry pi connected to Nokia 5510 LCD.

[Public transportation LCD display](doc/img1.jpg)

## Installation

1. Clone this repository
2. Copy & paste into `src/config.py`:
```python
HOST = "api.publictransport.tampere.fi"
USER = "YOUR-API-USERNAME"
PASS = "YOUR-API-PASSWORD"

API_CALL_INTERVAL_SECONDS = 20 * 60
BUS_STOP_CODES = [
    ("3607", "Nayt.katu", ["3A"]), # Use whatever bus stop codes & bus line numbers here,
    ("3601", "Arkk.katu", ["3B"]), # consult public transport API documentation for all codes
]
```
3. Install dependencies
4. [Optional] For automatic startup add to `/etc/crontab`:
```
@reboot root python /home/{USER}/{LOCATION}/joukkoliikenne-rpi/src/main.py >> /home/{USER}/joukkoliikenne.log 2>&1
```

## Dependencies

[Adafruit Nokia LCD library](https://github.com/adafruit/Adafruit_Nokia_LCD)

## Hardware

- Raspberry PI
- Female-Female Jumper Wires, [like these](http://www.dx.com/p/diy-female-to-female-dupont-breadboard-jumper-wires-black-multi-color-40-pcs-10cm-343484)
- Nokia 5110 LCD, [like this](https://www.adafruit.com/product/338)

## Pin setup

[Pin setup 1](doc/img2.jpg)
[Pin setup 2](doc/img3.jpg)

