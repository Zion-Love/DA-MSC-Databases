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

    def Create(self):
        Airline._Create(self)


    def Update(self):
        Airline._Update(self)


    def Delete(self):
        Airline._Delete(self)