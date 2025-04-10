from dataclasses import dataclass
from datetime import datetime
from FlightManagementSoftware.DataTransferObjects.Mappable import Mappable
from FlightManagementSoftware.Entities.QueryResult import QueryResult
from FlightManagementSoftware.Entities.EntityBase import EntityBase


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


    def Create(self):
        Country._Create(self)  


    def Update(self):
        Country._Update(self)


    def Delete(self):
        Country._Delete(self)