# -*- coding: utf-8 -*-
"""
Created on Sun Jun  3 22:18:38 2018

@author: markus
"""

from bus_departure_provider import BusDepartureProvider
from config import BUS_STOP_CODES
import httplib
import json


class HSLProvider():
    _HOST = "api.digitransit.fi"
    
    def __apiCall(self, code):
        h = httplib.HTTPConnection(self._HOST)
        params = """{
             stop(id: "HSL:1434180") {
        		 name
                code
                stoptimesWithoutPatterns{
                  scheduledDeparture
                  realtimeDeparture
                  trip {
                    route {
                      shortName
                    }
                  }
                }
              }
            }"""
        headers = {"User-Agent": "Raspberry-Pi joukkoliikenne", "Content-Type": "application/graphql", "Accept": "application/json"}
        h.request("POST", "/routing/v1/routers/hsl/index/graphql", params, headers=headers)
        r = h.getresponse()
        print r.status, r.reason
        data = r.read()
        h.close()
        return json.loads(data)
        
    def getDepartures(self, busStops):
        return map(lambda busStop: self.__apiCall(busStop[0])["data"]["stop"]["stoptimesWithoutPatterns"], busStops)
        
    def __filterDepartures(self, departures, lineNumbers):
        return filter(lambda d: d["trip"]["route"]["shortName"] in lineNumbers, departures)
    
    def filterDepartures(self, departures, busStops):
        deps = []
        for i in range(len(departures)):
            deps = deps + self.__filterDepartures(departures[i], busStops[i][2])
        return deps
        
    def formatDepartures(self, departures):
        return map(lambda d: { "hours": int(d["scheduledDeparture"] / 60 / 60), "minutes": (d["scheduledDeparture"] / 60) % 60, "line": d["trip"]["route"]["shortName"], "time": d["scheduledDeparture"] }, departures)
        
    
BusDepartureProvider.register(HSLProvider)

def main():
    hsl = HSLProvider()
    departures = hsl.getDepartures(BUS_STOP_CODES)
    departures = hsl.filterDepartures(departures, BUS_STOP_CODES)
    departures = hsl.formatDepartures(departures)
    for i in departures:
        print i

if __name__ == "__main__":
    main()