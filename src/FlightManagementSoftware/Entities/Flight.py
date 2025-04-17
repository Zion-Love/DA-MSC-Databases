from dataclasses import dataclass
from datetime import datetime
from FlightManagementSoftware.DataTransferObjects.Mappable import Mappable
from FlightManagementSoftware.Entities.EntityBase import EntityBase
from FlightManagementSoftware.Entities.QueryResult import QueryResult


@dataclass
class Flight(EntityBase, Mappable):
    Id : int
    FlightPathId : int
    AirplaneId : int
    DepartureTimeUTC : datetime
    ArrivalTimeUTC : datetime
    CreatedDate : datetime
    DeletedDate : datetime

    @classmethod
    def QueryByFlightPath(cls, flightPathId : int | list[int]):
        qry = r'''
            SELECT * FROM Flight f
        '''
        parameters = []
        if isinstance(flightPathId, int):
            qry += " WHERE f.FlightPathId = ?"
            parameters.append(flightPathId)
        elif isinstance(flightPathId, list):
            qry += f" WHERE f.FlightPathId IN ({','.join(['?'] * len(flightPathId))})"
            parameters.extend(flightPathId)
        return cls.Map(QueryResult(qry, *parameters))
    

    @classmethod
    def QueryPendingByCountry(cls, countryId : int):
        qry = r'''
            SELECT f.* FROM Flight f

            JOIN FlightPath fp
                on fp.Id = f.FlightPathId

            JOIN Destination fromDestination
                on fromDestination.Id = fp.FromDestinationId

            JOIN Destination toDestination
                on toDestination.Id = fp.ToDestinationId

            WHERE (fromDestination.CountryId = ? OR toDestination.CountryId = ?)
                AND f.ArrivalTimeUTC IS NULL
                AND f.DepartureTimeUTC > DATETIME('now')
        '''
        return cls.Map(QueryResult(qry, countryId, countryId))
    

    def Create(self):
        Flight._Create(self)


    def Update(self):
        Flight._Update(self)


    def Delete(self):
        Flight._Delete(self)