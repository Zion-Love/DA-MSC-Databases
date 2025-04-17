from dataclasses import dataclass
from datetime import datetime
from FlightManagementSoftware.DataTransferObjects.Mappable import Mappable
from FlightManagementSoftware.db.sqlite import dbConnectionInstance
from FlightManagementSoftware.Entities.EntityBase import EntityBase
from FlightManagementSoftware.Entities.QueryResult import QueryResult

@dataclass
class Destination(EntityBase, Mappable):
    Id : int
    CountryId : int
    Name: str
    AirportCode: str
    Active: bool
    CreatedDate: datetime
    DeletedDate: datetime

    @classmethod
    def QueryByAirportCode(cls, airportCode : str):
        qry = r'''
            SELECT * from Destination d WHERE d.AirportCode = ?
        '''
        return cls.Map(QueryResult(qry, airportCode).AssertSingleOrNull())
    
    @classmethod
    def QueryByCountry(cls, countryId : int):
        qry = r'''
            SELECT * FROM Destination d WHERE d.CountryId = ?
        '''
        return cls.Map(QueryResult(qry, countryId))


    def Create(self):
        self._Create(self)


    def Update(self):
        self._Update(self)


    # To delete a destination we need to first find all the flight paths that use it
    # Then delete those flight paths pending flights , the flight paths and finall the destination itself
    # I could use my entity setup to find those entites and call the corresponding .Delete methods
    # but for many flights to a destination this would result in many more db calls than doing it in 
    # 2 hard coded querys here
    def Delete(self):
        # cannot use table alias for these update statements
        pendingFlightsQry = r'''
            -- delete the pending flights
            UPDATE Flight SET DeletedDate = DATETIME('now') WHERE FlightPathId in (
                SELECT fp.Id from FlightPath fp 
                WHERE (fp.FromDestinationId = ? OR fp.ToDestinationId = ? )
            )
            AND ArrivalTimeUTC IS NULL
            AND DepartureTimeUTC > DATETIME('now')
        '''
        flightPathsQry = r'''
            -- delete the flight paths
            UPDATE FlightPath SET DeletedDate = DATETIME('now') 
            WHERE (FromDestinationId = ? OR ToDestinationId = ? )
        '''
        with dbConnectionInstance.Get_Transaction() as transaction:
            transaction.execute(pendingFlightsQry, (self.Id, self.Id))
            transaction.execute(flightPathsQry, (self.Id, self.Id))
            self._Delete(self, transaction)