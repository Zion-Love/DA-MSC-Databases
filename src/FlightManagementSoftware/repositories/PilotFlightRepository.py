from datetime import datetime
from FlightManagementSoftware.repositories.RepositoryBase import RepositoryBase
from FlightManagementSoftware.Entities.QueryResult import QueryResult
from FlightManagementSoftware.Entities.PilotFlight import PilotFlight
from FlightManagementSoftware.DataTransferObjects.DataFrame import DataFrame


# not using Entity base for mapping here since PilotFlight is just a join table
# between Flight and Pilot
class PilotFlightRepository(RepositoryBase):

    def QueryByPilotId(self, pilotId : list[int] | int ) -> DataFrame:
        qry = '''

        '''
        return DataFrame(PilotFlight.Map(QueryResult(qry)), PilotFlight)
    
    def QueryByFlightId(self, flightId : list[int] | int):
        qry = '''

        '''
        return DataFrame(PilotFlight.Map(QueryResult(qry)), PilotFlight)