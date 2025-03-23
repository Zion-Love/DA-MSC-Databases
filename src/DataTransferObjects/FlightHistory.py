from dataclasses import dataclass
from datetime import datetime
from db.MappingObjects import Mappable

'''
    This module contains all of my Data Transfer objects (DTO) related to flight history views


    TODO : Create our query layer to fetch this data from database
'''

@dataclass
class FlightHistoryDto(Mappable):
    DepartureDate : datetime
    ArrivalTime : datetime
    DepartureLocation : str
    ArrivalLocation : str
    Destination : str
    CreatedDate : datetime
    DeletedDate : datetime


@dataclass
class PilotFlightHistorySummaryDto(Mappable):
    PilotId : int
    PilotName : str
    StartDate : datetime
    EndDate : datetime
    FlightsUndertaken : int
    FlightsCancelled : int  # understood as the number of flights assigned to this Pilot that have a deletedDate
    TotalAirMilesTravelled : int


@dataclass 
class AirplaneFlightHistoryDto(Mappable):
    AirplaneId : int
    StartDate : datetime
    EndDate : datetime
    FlightsUndertaken : int
    FlightsCancelled : int
    TotalAirMilesTravelled : int