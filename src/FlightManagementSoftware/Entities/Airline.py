from dataclasses import dataclass
from datetime import datetime
from FlightManagementSoftware.DataTransferObjects.Mappable import Mappable
from FlightManagementSoftware.Entities.EntityBase import EntityBase


@dataclass
class Airline(EntityBase, Mappable):
    Id : int
    Name : str
    CreatedDate : datetime
    DeletedDate : datetime

    # flight dependant FK are handled through the db constraints so we dont need to validate that in creation...
    def Create(self):
        self._Create(self)

    def Update(self):
        self._Update(self)

    def Delete(self):
        self._Delete(self)