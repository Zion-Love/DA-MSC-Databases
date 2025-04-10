from dataclasses import dataclass
from datetime import datetime
from FlightManagementSoftware.DataTransferObjects.Mappable import Mappable

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


@dataclass
class PilotFlightScheduleDto(Mappable):
    PilotId : int
    PilotName : str
    FromDestination : str
    ToDestination : str
    DepartureTime : datetime
    ArrivalTime : datetime
    DeletedDate : datetime


# instead of showing the user the basic Flight entity records
# this includes more verbose columns such as the destination names etc
@dataclass
class FlightScheduleDto(Mappable):
    FlightId : int
    DepartureDestination : str
    ArrivalDestination : str
    DepartureTimeUTC : datetime
    ArrivalTimeUTC : datetime
    Pilots : str # an aggregated list of pilotIds
    FlightDeletionDate : datetime