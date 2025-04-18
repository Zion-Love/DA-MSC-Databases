from datetime import datetime
from FlightManagementSoftware.repositories.RepositoryBase import RepositoryBase
from FlightManagementSoftware.Entities.QueryResult import QueryResult
from FlightManagementSoftware.Entities.Pilot import Pilot
from FlightManagementSoftware.DataTransferObjects.DataFrame import DataFrame
from FlightManagementSoftware.DataTransferObjects.FlightHistory import PilotFlightScheduleDto

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
        qry = r'''
            SELECT p.Id as PilotId, p.Name as PilotName, 
                fromD.Name as FromDestination ,toD.Name as ToDestination, f.DepartureTimeUTC as DepartureTime, 
                f.ArrivalTimeUTC as ArrivalTime, f.DeletedDate
            FROM Pilot p

            JOIN PilotFlight pf
                on pf.PilotId = p.Id

            JOIN Flight f
                on f.Id = pf.FlightId
                
            JOIN FlightPath fp 
                on fp.Id = f.FlightPathId
                
            JOIN Destination toD 
                on toD.Id  = fp.ToDestinationId
                
            JOIN Destination fromD
                on fromD.Id = fp.FromDestinationId

            {MainQueryFilter}

            ORDER BY p.Name , f.DepartureTimeUTC ASC
        '''
        params = []
        mainQueryFilter = ""

        # Apply our pilotId filter(s) if one exitsts
        if isinstance(pilotId, int):
            mainQueryFilter += " WHERE p.Id = ?"
            params.append(pilotId)
        elif isinstance(pilotId, list):
            mainQueryFilter += f" WHERE p.Id in ({','.join(['?'] * len(pilotId))})"
            params.extend(pilotId)

        # Apply our date range filters
        if startDate != None:
            mainQueryFilter += " WHERE f.DepartureTimeUTC >= ? " if mainQueryFilter == "" else " AND f.DepartureTimeUTC >= ?"
            params.append(startDate)
        if endDate != None:
            mainQueryFilter += " WHERE f.DepartureTimeUTC <= ? " if mainQueryFilter == "" else " AND f.DepartureTimeUTC <= ?"
            params.append(endDate)

        # Apply deleted filter if needed
        if not includeDeletedFlights:
            mainQueryFilter += " WHERE f.DeletedDate IS NULL" if mainQueryFilter == "" else " AND f.DeletedDate IS NULL"
 
        qry = qry.replace("{MainQueryFilter}", mainQueryFilter)
        
        return DataFrame(PilotFlightScheduleDto.Map(QueryResult(qry, *params)), PilotFlightScheduleDto)


pilotRepository : PilotRepository = PilotRepository()