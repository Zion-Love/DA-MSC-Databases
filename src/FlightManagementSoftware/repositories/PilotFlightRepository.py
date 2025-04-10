from datetime import datetime
from FlightManagementSoftware.repositories.RepositoryBase import RepositoryBase
from FlightManagementSoftware.Entities.QueryResult import QueryResult
from FlightManagementSoftware.Entities.PilotFlight import PilotFlight
from FlightManagementSoftware.DataTransferObjects.DataFrame import DataFrame

pilotFlightsBaseQuery : str = '''
    SELECT f.Id as FlightId, AsignedPilots.AssignedPilots,
        f.DepartureTimeUTC, f.ArrivalTimeUTC, f.DeletedDate
    FROM Flight f

    LEFT JOIN (
        SELECT pf.FlightId, GROUP_CONCAT(p.Name + '(' + CAST(p.Id AS NVARCHAR) + ')'), ', ') AS AssignedPilots FROM PilotFlight pf
        JOIN Pilot p
            ON p.Id = pf.PilotId
        GROUP BY pf.FlightId
    ) AssignedPilots
    ON AssignedPilots.FlightId = f.Id
'''

# not using Entity base for mapping here since PilotFlight is just a join table
# between Flight and Pilot
class PilotFlightRepository(RepositoryBase):


    def QueryByPilotFlight(self, pilotId : list[int] | int = None, flightId : list[int] | int = None) -> DataFrame:
        
        if(pilotId == None and flightId == None):
            raise Exception("No filteres supplied to QueryByPilotFlight")
        
        
        qry = pilotFlightsBaseQuery


        return DataFrame(PilotFlight.Map(QueryResult(qry)), PilotFlight)
    
    def QueryFlightSchedule(self,) -> DataFrame:
        pass


pilotFlightRepository = PilotFlightRepository()