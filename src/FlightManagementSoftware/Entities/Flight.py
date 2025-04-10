from dataclasses import dataclass
from datetime import datetime
from FlightManagementSoftware.DataTransferObjects.Mappable import Mappable
from FlightManagementSoftware.Entities.EntityBase import EntityBase


@dataclass
class Flight(EntityBase, Mappable):
    Id : int
    FlightPathId : int
    AirplaneId : int
    DepartureTimeUTC : datetime
    ArrivalTimeUTC : datetime
    CreatedDate : datetime
    DeletedDate : datetime

    def Create(self):
        Flight._Create(self)


    def Update(self):
        Flight._Update(self)


    def Delete(self):
        Flight._Delete(self)