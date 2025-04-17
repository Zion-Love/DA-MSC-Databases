from datetime import datetime
from dataclasses import dataclass
from FlightManagementSoftware.db.sqlite import dbConnectionInstance
from FlightManagementSoftware.Entities.EntityBase import EntityBase
from FlightManagementSoftware.Entities.QueryResult import QueryResult
from FlightManagementSoftware.DataTransferObjects.Mappable import Mappable

@dataclass
class Pilot(EntityBase, Mappable):
    Id : int = None
    Name : str = None
    AirlineId : int = None
    CreatedDate : datetime = None
    DeletedDate : datetime = None

    @classmethod
    def QueryByAirline(cls, airlineId : int):
        qry = r'''
            SELECT * FROM Pilot p WHERE p.AirlineId = ?
        '''
        return cls.Map(QueryResult(qry, airlineId))

    def Create(self):
        Pilot._Create(self)


    def Update(self):
        Pilot._Update(self)


    def Delete(self, pilotId = None):
        with dbConnectionInstance.Get_Transaction() as transaction:
            deleteAssignedUncompleteFlightsQuery = '''
                DELETE FROM PilotFlight WHERE PilotId = ? AND FlightId in (
                    SELECT f.Id from Flight f 
                    WHERE (f.DepartureTimeUTC > date('now') OR f.DepartureTimeUTC IS NULL)
                      AND f.ArrivalTimeUTC IS NULL
                );
            '''
            transaction.execute(deleteAssignedUncompleteFlightsQuery, (pilotId if pilotId != None else self.Id,))
            Pilot._Delete(self, transaction)