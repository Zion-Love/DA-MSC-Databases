from dataclasses import dataclass
from datetime import datetime
from FlightManagementSoftware.DataTransferObjects.Mappable import Mappable

'''
    This module contains more verbose mapping objects to convert query results to
    used in cases where queries dont return a 1:1 mapping to the entity columns
'''

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
    AirplaneId : int
    DepartureDestination : str
    ArrivalDestination : str
    DepartureTimeUTC : datetime
    ArrivalTimeUTC : datetime
    Pilots : str # an aggregated list of pilotIds
    FlightDeletionDate : datetime


@dataclass
class FlightPathVerbose(Mappable):
    FlightPathId : int
    FromDestination : str
    ToDestination : str
    DistanceKm : int
    Active : bool
    DeletedDate : datetime
