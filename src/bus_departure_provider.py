# -*- coding: utf-8 -*-
"""
Created on Sun Jun  3 19:55:56 2018

@author: markus
"""

from abc import ABCMeta, abstractmethod

class BusDepartureProvider():
    __metaclass__ = ABCMeta

    """Returns a list of departures from some external source"""
    @abstractmethod
    def getDepartures(busStops):
        pass

    """ Returns a list of departures. Filters out buses that are not included in busStops. """
    @abstractmethod
    def filterDepartures(departures, busStops):
        pass

    """ Returns a list of formatted departures. The format is { "hours": 16, "minutes": 12, "line": "3A", "time": 16 * 60 + 12 } """
    @abstractmethod
    def formatDepartures(departures):
        pass
