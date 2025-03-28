from datetime import datetime
from Entities.EntityBase import EntityBase
from DataTransferObjects.Mappable import Mappable
from dataclasses import dataclass

@dataclass
class Pilot(EntityBase, Mappable):
    Id : int
    Name : str
    CreatedDate : datetime
    DeletedDate : datetime

    def Create(self):
        self._Create(self)

    def Update(self):
        self._Update(self)

    def Delete(self):
        self._Delete(self)