# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 21:17:11 2017

@author: markus
"""


from nokia_lcd import NokiaLCD
from config import API_CALL_INTERVAL_SECONDS, BUS_STOP_CODES, PROVIDER
from tkl_provider import TKLProvider
from hsl_provider import HSLProvider
import time

lcd = NokiaLCD()
provider = HSLProvider()

if (PROVIDER == "TKL"):
    provider = TKLProvider()

def sortDeparturesAscendingByTime(departures):
    return sorted(departures, key=lambda d: int(d["time"]))
    
def updateDepartures():
    lcd.clear(x1=40, y1=48)
    try:
        departures = provider.getDepartures(BUS_STOP_CODES)
    except Exception:
        return False
    departures = provider.filterDepartures(departures, BUS_STOP_CODES)
    departures = provider.formatDepartures(departures)
    departures = sortDeparturesAscendingByTime(departures)
    for i,d in enumerate(departures[:7]):
        lcd.setText(d["line"] + " " + str(d["hours"]) + ":" + str(d["minutes"]), x=0, y= i*7)
    return departures

def main():
    while not updateDepartures():
        print "No internet connection... waiting a bit"
        time.sleep(1)
    i = 1
    while True:
        lcd.drawTime()
        if (i % API_CALL_INTERVAL_SECONDS == 0):
            updateDepartures()
        i+=1
        time.sleep(1)

if __name__ == "__main__":
    main()