from dataclasses import dataclass
from datetime import datetime
from FlightManagementSoftware.DataTransferObjects.Mappable import Mappable
from FlightManagementSoftware.db.sqlite import dbConnectionInstance
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
    def QueryByDestinations(cls, fromDestinationId : int, toDestinationId : int):
        qry = r'''
            SELECT * FROM FlightPath fp WHERE fp.FromDestinationId = ? AND fp.ToDestinationId = ?
        '''
        return cls.Map(QueryResult(qry, fromDestinationId, toDestinationId).AssertSingleOrNull())
    
    @classmethod
    def QueryByDestinationId(cls, destinationId : int):
        qry = r'''
            SELECT * FROM FlightPath fp WHERE fp.FromDestinationId = ? OR fp.ToDestinationId = ?
        '''
        return cls.Map(QueryResult(qry, destinationId, destinationId))
    
    @classmethod 
    def QueryByCountry(cls, countryId : int):
        qry = r'''
            SELECT fp.* FROM FlightPath fp

            JOIN Destination fromDestination
                on fromDestination.Id = fp.FromDestinationId
            JOIN Destination toDestination
                on toDestination.Id = fp.ToDestinationId

            WHERE fromDestination.CountryId = ? OR toDestination.CountryId = ?
        '''
        return cls.Map(QueryResult(qry, countryId, countryId))


    def Create(self):
        FlightPath._Create(self)


    def Update(self):
        FlightPath._Update(self)


    # To Delete a flight Path we need to first delete any pending flights for that path
    def Delete(self):
        qry = r'''
            UPDATE Flight f SET f.DeletedDate = DATETIME('now') WHERE f.FlighPathId = ?
        '''
        with dbConnectionInstance.Get_Transaction() as transaction:
            transaction.execute(qry, self.Id)
            FlightPath._Delete(self, transaction)