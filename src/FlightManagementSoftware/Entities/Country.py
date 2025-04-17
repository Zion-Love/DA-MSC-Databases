from dataclasses import dataclass
from datetime import datetime
from FlightManagementSoftware.DataTransferObjects.DataFrame import DataFrame
from FlightManagementSoftware.Entities.EntityBase import EntityBase
from FlightManagementSoftware.DataTransferObjects.Mappable import Mappable
from FlightManagementSoftware.Entities.QueryResult import QueryResult
from FlightManagementSoftware.db.sqlite import dbConnectionInstance


@dataclass
class Country(EntityBase, Mappable):
    Id : int
    Name : str 
    IsoCode :str
    AllowingFlights : bool
    CreatedDate : datetime
    DeletedDate : datetime


    @classmethod
    def QueryByIsoCode(cls, isoCode: str):
        qry = '''
            SELECT * FROM Country c WHERE c.IsoCode = ?
        '''
        return QueryResult(qry, isoCode).AssertSingle().result[0]
    
    
    # since this returns the mapped entity base class I have included it here instead of a repository
    @classmethod
    def Query(cls, includeDeleted : bool = False, includeInactive : bool = False) -> DataFrame:
        qry = r'''
            SELECT * FROM Country c

            {Filter}
        '''
        filter = ""
        if not includeDeleted:
            filter += " WHERE c.DeletedDate IS NULL"
        if not includeInactive:
            filter += " WHERE c.AllowingFlights = 1" if filter == "" else " AND c.AllowingFlights = 1"

        qry = qry.replace("{Filter}" , filter)
        return DataFrame(cls.Map(QueryResult(qry)), cls)


    def Create(self):
        Country._Create(self)  


    def Update(self):
        Country._Update(self)


    # When Deleting a country we need to delete all of the corresponding 
    # - Destinations
    # - FlightPaths
    # - Flights
    # This would be much better done with an ORM with proper relationship navigation
    # but we dont have the luxury....
    # also I realise this shares deletion logic with its inversly dependant entities
    # BUT doing it at each level bespoke is technically more performant since we arent having to loop 
    # each layer individually nor are wel pulling any data into memory to push Ids through to each layer
    def Delete(self):
        flightsQry = r'''
            UPDATE Flight SET DeletedDate = DATETIME('now') 
            FROM Flight f
            JOIN FlightPath fp
                ON fp.Id = f.FlightPathId
            
            JOIN Destination fromDestination
                on fromDestination.Id = fp.FromDestinationId

            JOIN Destination toDestination 
                on toDestination.Id = fp.ToDestinationId

            WHERE toDestination.CountryId = ? OR fromDestination.CountryId = ?
        '''
        flightPathsQry = r'''
            UPDATE FlightPath SET DeletedDate = DATETIME('now')
            FROM FlightPath fp
            JOIN Destination fromDestination
                on fromDestination.Id = fp.FromDestinationId

            JOIN Destination toDestination 
                on toDestination.Id = fp.ToDestinationId

            WHERE toDestination.CountryId = ? OR fromDestination.CountryId = ?
        '''
        destinationsQry = r'''
            UPDATE Destination SET DeletedDate = DATETIME('now') WHERE Destination.CountryId = ?
        '''
        with dbConnectionInstance.Get_Transaction() as transaction:
            transaction.execute(flightsQry, (self.Id, self.Id))
            transaction.execute(flightPathsQry, (self.Id, self.Id))
            transaction.execute(destinationsQry, (self.Id,))
            Country._Delete(self, transaction)