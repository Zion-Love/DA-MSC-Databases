from datetime import datetime
from Entities.EntityBase import EntityBase
from DataTransferObjects.Mappable import Mappable
from db.sqlite import dbConnectionInstance
from dataclasses import dataclass

@dataclass
class Pilot(EntityBase, Mappable):
    Id : int
    Name : str
    AirlineId : int
    CreatedDate : datetime
    DeletedDate : datetime

    def Create(self):
        self._Create(self)


    def Update(self):
        self._Update(self)


    # for Pilot if we are softdeleting we still need to clean up
    # PilotFlight to unassign this pilot from all their current flights
    # having a wrapped call to _Delete lets me do this easily
    def Delete(self, pilotId = None):
        with dbConnectionInstance.Get_Transaction() as transaction:
            # Uncompleted flights are either not departed (departureTime = null) OR departureTime is set in the future
            # deleted flights should also be ignored here since we may need a record of the pilots at time of deletion
            deleteAssignedUncompleteFlightsQuery = '''
                DELETE FROM PilotFlight WHERE PilotId = ? AND FlightId in (
                    SELECT f.Id from Flight f 
                    WHERE (f.DepartureTimeUTC > date('now') OR f.DepartureTimeUTC IS NULL)
                      AND f.ArrivalTimeUTC IS NULL
                );
            '''
            transaction.execute(deleteAssignedUncompleteFlightsQuery, (pilotId if pilotId != None else self.Id,))
            self._Delete(self, transaction)