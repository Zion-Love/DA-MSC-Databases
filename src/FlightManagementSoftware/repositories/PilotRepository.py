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


    def QueryById(self, pilotId : int | list[int]) -> DataFrame:
        if(pilotId == None):
            raise Exception("PilotRepository.QueryById requires at least 1 Id")
        params = []
        query = f"""
            SELECT * from Pilot p
        """
        if(isinstance(pilotId, int)):
            query += " WHERE p.Id = ?"
            return DataFrame(Pilot.Map(QueryResult(query, pilotId), type(Pilot)))
        elif(len(pilotId) > 1):
            query += ' WHERE p.Id IN ?'
            params = fr"({str.join(', ', pilotId)})"
            return DataFrame(Pilot.Map(QueryResult(query, *params), type(Pilot)))


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

            {PilotIdFilter}
            {CreatedDateFilter}
            {IncludeDeletedFlightsFilter}

            ORDER BY p.Name , f.DepartureTimeUTC ASC
        '''
        params = []

        # Apply our pilotId filter(s) if one exitsts
        if pilotId == None:
            qry = qry.replace("{PilotIdFilter}", "")
        else:
            if isinstance(pilotId, int):
                qry = qry.replace("{PilotIdFilter}", " WHERE p.Id = ?")
                params.append(pilotId)
            elif isinstance(pilotId, list) and len(pilotId) == 1:
                qry = qry.replace("{PilotIdFilter}", " WHERE p.Id = ?")
                params.append(pilotId[0])
            elif isinstance(pilotId, list) and len(pilotId) > 1:
                qry = qry.replace("{PilotIdFilter}", " WHERE p.Id in ?")
                params.append(f"({','.join(pilotId)})")

        # Apply our CreatedDate filter if one exsits
        # using a prefix keyword if we have also got a pilot filter
        createdDateFilterKeyword = " WHERE" if pilotId == None else " AND"
        if startDate == None and endDate == None:
            qry = qry.replace("{CreatedDateFilter}", "")
        else:
            if startDate != None:
                if endDate != None:
                    qry = qry.replace(r"{CreatedDateFilter}", f"{createdDateFilterKeyword} f.CreatedDate >= ? AND f.CreatedDate <= ?")
                    params.append(startDate)
                    params.append(endDate)
                else:
                    qry = qry.replace(r"{CreatedDateFilter}", f"{createdDateFilterKeyword} f.CreatedDate >= ?")
                    params.append(startDate)
            elif endDate != None and startDate == None:
                qry = qry.replace(r"{CreatedDateFilter}", f"{createdDateFilterKeyword} f.CreatedDate <= ?")
                params.append(endDate)

        # Apply our deletion filter
        if not includeDeletedFlights:
            if pilotId != None or startDate != None or endDate != None:
                qry = qry.replace(r"{IncludeDeletedFlightsFilter}" , " AND f.DeletedDate IS NULL")
            else:
                qry = qry.replace(r"{IncludeDeletedFlightsFilter}" , " WHERE f.DeletedDate IS NULL")
        else:
            qry = qry.replace(r"{IncludeDeletedFlightsFilter}", "")
                
        
        return DataFrame(PilotFlightScheduleDto.Map(QueryResult(qry, *params)), PilotFlightScheduleDto)


pilotRepository : PilotRepository = PilotRepository()