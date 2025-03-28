from datetime import datetime
from repositories.RepositoryBase import RepositoryBase
from DataTransferObjects.FlightHistory import PilotFlightHistory
from Entities.QueryResult import QueryResult
from Entities.Pilot import Pilot
from DataFrame import DataFrame

'''
    Repositories for this project are a way of creating more complex queries requiring multiple tables,

    these will REQUIRE a dto and will not have CRUD operations , instead they will be built using bespoke method signatures

    any of these methods should therefore be abstracted for example 

    PilotRepository.QueryPilotFlightHistory(pilotId int, DateRange) will need an accompanying PilotFlightHistoryDto

    that we can then map to a DataFrame due to the inheritance of Mappable

'''
class PilotRepository(RepositoryBase):
    def __init__(self):
        super().__init__()
        pass

    def QueryById(self, pilotId : int) -> DataFrame:
        query = f'''
            SELECT * from Pilot p WHERE p.Id = ?;
        '''
        return DataFrame(Pilot.Map(QueryResult(query, (pilotId)).AssertSingleOrNull()))

    def QueryByName(self, name : str) -> DataFrame:
        query = f'''
            SELECT * from Pilot p WHERE p.\"Name\" = ?;
        '''
        return DataFrame(Pilot.Map(QueryResult(query, (name)).AssertSingleOrNull()))
    

    def QueryActivePilots(self, active : bool = True) -> DataFrame: 
        query = f'''
            SELECT * from Pilot p WHERE p.DeletedDate is ?
        '''
        return DataFrame(Pilot.Map(QueryResult(query, (active)).AssertSingleOrNull()))
    

    def QueryPilotFlightHistory(self, 
            pilotId : int, 
            startDate : datetime = None, 
            endDate : datetime = None) -> DataFrame:
        qry = '''
            SELECT p.Id as PilotId, p.Name as PilotName
             
            FROM Pilot p

            JOIN PilotFlight pf
                on pf.PilotId = p.Id

            JOIN Flight f
                on f.Id = pf.FlightId

            WHERE p.Id = ?
        '''
        params = [pilotId]
        if startDate: 
            qry += ' AND p.CreatedDate >= ?'
            params.append(startDate)
        if endDate: 
            qry += ' AND p.CreatedDate <= ?'
            params.append(endDate)
        
        return DataFrame(PilotFlightHistory.Map(QueryResult(qry, tuple(params))))



pilotRepository : PilotRepository = PilotRepository()