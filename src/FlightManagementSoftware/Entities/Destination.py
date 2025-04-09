from dataclasses import dataclass
from datetime import datetime
from FlightManagementSoftware.Entities import EntityBase
from FlightManagementSoftware.DataTransferObjects.Mappable import Mappable

@dataclass
class Destination(EntityBase, Mappable):
    Id : int
    CountryId : int
    Name: str
    AirportCode: str
    Active: bool
    CreatedDate: datetime
    DeletedDate: datetime

    def Create(self):
        self._Create(self)

    def Update(self):
        self._Update(self)

    def Delete(self):
        self._Delete(self)