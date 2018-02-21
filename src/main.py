# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 21:17:11 2017

@author: markus
"""

import httplib
import json
from nokia_lcd import NokiaLCD
from config import HOST, PASS, USER, API_CALL_INTERVAL_SECONDS, BUS_STOP_CODES
import time

lcd = NokiaLCD()

def apiCall(code):
    h = httplib.HTTPConnection(HOST)
    headers = {"User-Agent": "Raspberry-Pi joukkoliikenne", "Accept": "application/json"}
    h.request("GET", "/prod/?request=stop&code=" + code + "&user=" + USER + "&pass=" + PASS, headers=headers)
    r = h.getresponse()
    print r.status, r.reason
    data = r.read()
    h.close()
    return json.loads(data)

def getDepartures(stopCodes):
    return reduce(list.__add__, map(lambda stopCode: filterDepartures(apiCall(stopCode[0])[0]["departures"], stopCode[2]), stopCodes))

def filterDepartures(departures, lineNumbers):
    return filter(lambda d: d["code"] in lineNumbers, departures)

def formatDepartures(departures):
    return map(lambda d: { "hours": d["time"][:2], "minutes": d["time"][2:4], "line": d["code"], "time": int(d["time"][:2]) * 60 + int(d["time"][2:4]) }, departures)

def sortDeparturesAscendingByTime(departures):
    return sorted(departures, key=lambda d: int(d["time"]))

def updateDepartures():
    lcd.clear(x1=40, y1=48)
    try:
        departures = getDepartures(BUS_STOP_CODES)
    except Exception:
        return False
    departures = formatDepartures(departures)
    departures = sortDeparturesAscendingByTime(departures)
    print departures
    for i,d in enumerate(departures[:7]):
        lcd.setText(d["line"] + " " + d["hours"] + ":" + d["minutes"], x=0, y= i*7)
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