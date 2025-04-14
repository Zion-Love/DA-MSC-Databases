from dataclasses import dataclass
from datetime import datetime
from FlightManagementSoftware.DataTransferObjects.Mappable import Mappable
from FlightManagementSoftware.Entities.EntityBase import EntityBase
from FlightManagementSoftware.Entities.QueryResult import QueryResult


@dataclass
class FlightPath(EntityBase, Mappable):
    Id : int
    FromDestinationId : int
    ToDestinationId : int
    DistanceKm : int
    Active : bool
    CreatedDate : datetime
    DeletedDate : datetime

    @classmethod
    def QueryByDestinationId(cls, fromDestinationId : int, toDestinationId : int):
        qry = '''
            SELECT * FROM FlightPath fp WHERE fp.FromDestinationId = ? AND fp.ToDestinationId = ?
        '''
        return cls.Map(QueryResult(qry, fromDestinationId, toDestinationId).AssertSingleOrNull())


    def Create(self):
        FlightPath._Create(self)


    def Update(self):
        FlightPath._Update(self)


    def Delete(self):
        FlightPath._Delete(self)