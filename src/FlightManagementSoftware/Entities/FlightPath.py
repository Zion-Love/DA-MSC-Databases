from dataclasses import dataclass
from datetime import datetime
from FlightManagementSoftware.DataTransferObjects.Mappable import Mappable
from FlightManagementSoftware.Entities.EntityBase import EntityBase


@dataclass
class FlightPath(EntityBase, Mappable):
    Id : int
    FromDestinationId : int
    ToDestinationId : int
    DistanceKm : int
    Active : bool
    CreatedDate : datetime
    DeletedDate : datetime

    # flight dependant FK are handled through the db constraints so we dont need to validate that in creation...
    def Create(self):
        self._Create(self)

    def Update(self):
        self._Update(self)

    def Delete(self):
        self._Delete(self)