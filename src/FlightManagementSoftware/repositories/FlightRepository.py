from datetime import datetime
from FlightManagementSoftware.repositories.RepositoryBase import RepositoryBase
from FlightManagementSoftware.Entities.QueryResult import QueryResult
from FlightManagementSoftware.Entities.PilotFlight import PilotFlight
from FlightManagementSoftware.DataTransferObjects.DataFrame import DataFrame
from FlightManagementSoftware.DataTransferObjects.FlightHistory import FlightScheduleDto

flightScheduleBaseQuery = r'''
    SELECT f.Id as FlightId,f.DepartureTimeUTC , f.ArrivalTimeUTC,
        DepartureDestination.Name as DepartureDestination, ArrivalDestination.Name as ArrivalDestination,
        AssignedPilots.AssignedPilots, f.DeletedDate FlightDeletionDate
    FROM Flight f

    JOIN FlightPath fp 
        ON f.FlightPathId = fp.Id 
        
    JOIN Destination DepartureDestination
        ON fp.FromDestinationId = DepartureDestination .Id 
        
    JOIN Destination ArrivalDestination 
        ON fp.ToDestinationId = ArrivalDestination.Id 

    LEFT JOIN (
        SELECT pf.FlightId, GROUP_CONCAT(format('%s (Id : %s)' , p.Name, p.Id), ', ') AS AssignedPilots 
        FROM PilotFlight pf
            JOIN Pilot p
                ON p.Id = pf.PilotId
            {PilotIdFilter}    
            GROUP BY pf.FlightId
    ) AssignedPilots
    ON AssignedPilots.FlightId = f.Id

    {FlightIdFilter}
    {IncludeDeletedFilter}

    ORDER BY f.DepartureDateUTC ASC
'''

class FlightRepository(RepositoryBase):

    def QueryByPilotFlight(
            self, 
            pilotId : list[int] | int = None, 
            flightId : list[int] | int = None,
            includeDeleted : bool = True):
        parameters = []
        qry = flightScheduleBaseQuery

        # Append our pilot id filter if it is present
        if pilotId == None:
            qry = qry.replace("{PilotIdFilter}" , "")
        else:
            if isinstance(pilotId, list) and len(pilotId) > 1:
                qry = qry.replace("{PilotIdFilter}", "WHERE p.Id in ?")
                parameters.append(f"({','.join(pilotId)})")
            elif (isinstance(pilotId, list) and len(pilotId) == 1):
                qry = qry.replace("{PiilotIdFilter}", "WHERE p.Id = ?")
                parameters.append(pilotId[0])
            elif isinstance(pilotId, int):
                qry = qry.replace("{PiilotIdFilter}", "WHERE p.Id = ?")
                parameters.append(pilotId)

        # Append our flight id filter if it is present
        if flightId == None:
            qry = qry.replace("{FlightIdFilter}" , "")
        else:
            if isinstance(flightId, list) and len(flightId) > 1:
                qry = qry.replace("{FlightIdFilter}", "WHERE f.Id in ?")
                parameters.append(f"({','.join(flightId)})")
            elif (isinstance(flightId, list) and len(flightId) == 1):
                qry = qry.replace("{FlightIdFilter}", "WHERE f.Id = ?")
                parameters.append(flightId[0])
            elif isinstance(flightId, int):
                qry = qry.replace("{FlightIdFilter}", "WHERE f.Id = ?")
                parameters.append(flightId)

        if includeDeleted == True:
            qry = qry.replace("{IncludeDeletedFilter}", "")
        else:
            if flightId != None:
                qry = qry.replace("{IncludeDeletedFilter}", " AND f.DeletedDate IS NULL")
            else:
                qry = qry.replace("{IncludeDeletedFilter}", " WHERE f.DeletedDate IS NULL")

        return DataFrame(PilotFlight.Map(QueryResult(qry, tuple(parameters))), PilotFlight)
    

    def QueryAll(self, includeDeleted : bool = False):
        qry = flightScheduleBaseQuery
        qry = qry.replace("{PilotIdFilter}" , "")
        qry = qry.replace("{FlightIdFilter}" , "")
        return DataFrame(FlightScheduleDto.Map(QueryResult(qry)), FlightScheduleDto)
    

flightRepository : FlightRepository = FlightRepository()