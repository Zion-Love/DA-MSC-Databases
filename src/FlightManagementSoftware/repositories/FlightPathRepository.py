from FlightManagementSoftware.repositories.RepositoryBase import RepositoryBase
from FlightManagementSoftware.DataTransferObjects.FlightHistory import FlightPathVerbose
from FlightManagementSoftware.DataTransferObjects.DataFrame import DataFrame
from FlightManagementSoftware.Entities.QueryResult import QueryResult

flightPathBaseQuery = r'''
    SELECT fp.Id as FlightPathId, fromDestination.Name as FromDestination,
           toDestination.Name as ToDestination, fp.DistanceKm, fp.Active, fp.DeletedDate 
    FROM FlightPath fp

    JOIN Destination fromDestination
        on fromDestination.Id = fp.fromDestinationId

    JOIN Destination toDestination
        on toDestination.Id = fp.toDestinationId

    {MainQueryFilter}

    ORDER BY fp.CreatedDate DESC
'''

class FlightPathRepository(RepositoryBase):

    def QueryAll(self, includeDeleted : bool = True, includeInactive : bool = True):
        qry = flightPathBaseQuery
        mainQueryFilter = ""

        if(not includeDeleted):
            mainQueryFilter += "WHERE fp.DeletedDate is NULL "

        if(not includeInactive):
            mainQueryFilter += "WHERE fp.Active = 1" if mainQueryFilter == "" else "AND fp.Active = 1"

        qry = qry.replace("{MainQueryFilter}", mainQueryFilter)
        
        return DataFrame(FlightPathVerbose.Map(QueryResult(qry)), FlightPathVerbose)


flightPathRepository : FlightPathRepository = FlightPathRepository()