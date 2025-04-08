from dataclasses import dataclass
from datetime import datetime
from DataTransferObjects.Mappable import Mappable

'''
    This module contains all of my Data Transfer objects (DTO) related to flight history views

    Ideally you would use pydantic here to apply validation logic to our data classes
    since python uses dynamica types the annotation here is more of a guide than enforced.
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
    Pilots : str
    

@dataclass
class PilotFlightHistoryDto(Mappable):
    PilotId : int
    FlightId : int
    DepartureDestination : str
    DepartureDestinationCountry: str
    ArrivalDestination : str
    ArrivalDestinationCountry: str
    DepartureTimeUTC : datetime
    ArrivalTimeUTC : datetime


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