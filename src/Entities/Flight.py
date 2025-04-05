from dataclasses import dataclass
from datetime import datetime
from DataTransferObjects.Mappable import Mappable
from Entities.EntityBase import EntityBase
from db.sqlite import dbConnectionInstance


@dataclass
class Flight(EntityBase, Mappable):
    Id : int
    DepartureDestinationId : int
    ArrivalDestinationId : int
    AirplaneId : int
    AirMiles : int
    DepartureTimeUTC : datetime
    ArrivalTimeUTC : datetime
    CreatedDate : datetime
    DeletedDate : datetime

    # flight dependant FK are handled through the db constraints so we dont need to validate that in creation...
    def Create(self):
        self._Create(self)

    def Update(self):
        self._Update(self)

    def Delete(self):
        self._Delete(self)