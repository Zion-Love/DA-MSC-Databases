from dataclasses import dataclass
from datetime import datetime
from DataTransferObjects.Mappable import Mappable
from Entities.EntityBase import EntityBase


@dataclass
class Flight(EntityBase, Mappable):
    Id : int
    DepartureAirportId : int
    ArrivalAirportId : int
    AirplaneId : int
    AirMiles : int
    DepartureTimeUTC : datetime
    ArrivalTimeUTC : datetime
    CreatedDate : datetime
    DeletedDate : datetime

    def Create(self):
        self._Create(self)

    def Update(self):
        self._Update(self)

    def Delete(self):
        self._Delete(self)