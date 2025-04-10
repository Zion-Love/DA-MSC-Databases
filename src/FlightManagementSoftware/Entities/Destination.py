from dataclasses import dataclass
from datetime import datetime
from FlightManagementSoftware.DataTransferObjects.Mappable import Mappable
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
        qry = '''
            SELECT * from Destination d WHERE d.AirportCode = ?
        '''
        destination =  cls.Map(QueryResult(qry, airportCode).AssertSingleOrNull())
        return None if destination == None else destination[0]


    def Create(self):
        self._Create(self)


    def Update(self):
        self._Update(self)


    def Delete(self):
        self._Delete(self)