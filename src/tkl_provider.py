# -*- coding: utf-8 -*-
"""
Created on Sun Jun  3 19:58:50 2018

@author: markus
"""

from bus_departure_provider import BusDepartureProvider
from config import TKL_USER, TKL_PASS, BUS_STOP_CODES
import httplib
import json

class TKLProvider():
    _HOST = "api.publictransport.tampere.fi"
    
    def __apiCall(self, code):
        h = httplib.HTTPConnection(self._HOST)
        headers = {"User-Agent": "Raspberry-Pi joukkoliikenne", "Accept": "application/json"}
        h.request("GET", "/prod/?request=stop&code=" + code + "&user=" + TKL_USER + "&pass=" + TKL_PASS, headers=headers)
        r = h.getresponse()
        print r.status, r.reason
        data = r.read()
        h.close()
        return json.loads(data)
        
    def getDepartures(self, busStops):
        return map(lambda busStop: self.__apiCall(busStop[0])[0]["departures"], busStops)
        
    def __filterDepartures(self, departures, lineNumbers):
        return filter(lambda d: d["code"] in lineNumbers, departures)
    
    def filterDepartures(self, departures, busStops):
        deps = []
        for i in range(len(departures)):
            deps = deps + self.__filterDepartures(departures[i], busStops[i][2])
        return deps
                    
    def formatDepartures(self, departures):
        return map(lambda d: { "hours": d["time"][:2], "minutes": d["time"][2:4], "line": d["code"], "time": int(d["time"][:2]) * 60 + int(d["time"][2:4]) }, departures)
        
    
BusDepartureProvider.register(TKLProvider)

def main():
    tkl = TKLProvider()
    departures = tkl.getDepartures(BUS_STOP_CODES)
    departures = tkl.filterDepartures(departures, BUS_STOP_CODES)
    departures = tkl.formatDepartures(departures)
    for i in departures:
        print i

if __name__ == "__main__":
    main()