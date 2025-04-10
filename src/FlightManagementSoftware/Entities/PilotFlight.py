from dataclasses import dataclass
from FlightManagementSoftware.Entities.EntityBase import EntityBase
from FlightManagementSoftware.db.sqlite import dbConnectionInstance
from FlightManagementSoftware.DataTransferObjects.Mappable import Mappable
from FlightManagementSoftware.Entities.QueryResult import QueryResult


@dataclass
class PilotFlight(EntityBase, Mappable):
    PilotId : int
    FlightId : int

    # overwriting default behavour since this entity does not use Id as PK
    def Create(self):
        qry = '''
            INSERT INTO PilotFlight (PilotId, FlightId) VALUES (?,?)
        '''
        with (dbConnectionInstance.Get_Transaction() as transaction):
            transaction.execute(qry, tuple([self.PilotId, self.FlightId]))


    # Pilot flight assignment should only be either this record exists = assigned to flight or no record = not assigned
    def Update(self):
        pass

    # special case pass to the cls method for single implementation either as instance.Delete or cls.Delete
    def Delete(self):
        type(self).Delete(self.PilotId,self.FlightId)


    @classmethod
    def Delete(cls, pilotId : int, flightId : int):
        # weirdly I tried doing this with a table alias pf but it threw an error?
        qry = '''
            DELETE FROM PilotFlight WHERE PilotId = ? AND FlightId = ?
        '''
        with(dbConnectionInstance.Get_Transaction() as transaction):
            transaction.execute(qry, tuple([pilotId, flightId]))


    @classmethod
    def QueryPilotFlight(cls, pilotId : int, flightId : int):
        qry = '''
            SELECT * from PilotFlight pf
            WHERE pf.PilotId = ? AND pf.FlightId = ?
        '''
        result = PilotFlight.Map(QueryResult(qry, pilotId, flightId).AssertSingleOrNull())
        if len(result) == 0: return None
        return result[0]
