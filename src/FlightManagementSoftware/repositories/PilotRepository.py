from datetime import datetime
from FlightManagementSoftware.repositories.RepositoryBase import RepositoryBase
from FlightManagementSoftware.Entities.QueryResult import QueryResult
from FlightManagementSoftware.Entities.Pilot import Pilot
from FlightManagementSoftware.DataTransferObjects.DataFrame import DataFrame

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


    def QueryById(self, pilotId : int | list[int]) -> DataFrame:
        if(pilotId == None):
            raise Exception("PilotRepository.QueryById requires at least 1 Id")
        params = []
        query = f"""
            SELECT * from Pilot p
        """
        if(isinstance(pilotId, int)):
            query += " WHERE p.Id = ?"
            return DataFrame(Pilot.Map(QueryResult(query, (pilotId)), type(Pilot)))
        elif(len(pilotId) > 1):
            query += ' WHERE p.Id IN ?'
            params = fr"({str.join(', ', pilotId)})"
            return DataFrame(Pilot.Map(QueryResult(query, params), type(Pilot)))


    def QueryByName(self, name : str) -> DataFrame:
        query = r"""
            SELECT * FROM Pilot p WHERE p.'Name' = ?
        """
        return DataFrame(Pilot.Map(QueryResult(query, (name), Pilot)))
    

    def QueryPilots(self, showDeleted : bool = True, partialSearchKey: str = None) -> DataFrame: 
        params = []
        query = f'''
            SELECT * FROM Pilot p
        '''
        if not showDeleted:
            query += 'WHERE p.DeletedDate IS NULL'
        if partialSearchKey != None:
            if not showDeleted:
                query += ' AND '
            else:
                query += ' WHERE '
            query += " p.Name LIKE ?"
            params.append(f"%{partialSearchKey}%")
        return DataFrame(Pilot.Map(QueryResult(query, *params)), Pilot)
    

    def QueryPilotFlightSchedule(self, 
            pilotId : int, 
            includeDeletedFlights: bool = False,
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
        if not includeDeletedFlights:
            qry += ' AND f.DeletedDate IS NULL'
        
        return DataFrame(PilotFlightHistory.Map(QueryResult(qry, tuple(params), PilotFlightHistory)))



pilotRepository : PilotRepository = PilotRepository()