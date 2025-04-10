from dataclasses import dataclass
from datetime import datetime
from FlightManagementSoftware.DataTransferObjects.Mappable import Mappable
from FlightManagementSoftware.Entities.EntityBase import EntityBase


@dataclass
class Airplane(EntityBase, Mappable):
    Id : int
    ModelNumeber : str
    ManufacturedDate : datetime
    LastServiceDate : datetime
    PassengerCapacity : int
    CurrentDestinationId : int
    CreatedDate : datetime
    DeletedDate : datetime

    def Create(self):
        self._Create(self)

    def Update(self):
        self._Update(self)

    def Delete(self):
        self._Delete(self)