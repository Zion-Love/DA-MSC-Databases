from FlightManagementSoftware.repositories.RepositoryBase import RepositoryBase
from FlightManagementSoftware.DataTransferObjects.DataFrame import DataFrame
from FlightManagementSoftware.DataTransferObjects.Airline import AirlinePilotSummary
from FlightManagementSoftware.Entities.QueryResult import QueryResult

airlineBaseQuery = r'''
    SELECT a.Id as AirlineId, a.Name, COALESCE(ActivePilots.cnt, 0) as ActivePilots, COALESCE(InactivePilots.cnt, 0) as InactivePilots,
        a.CreatedDate, a.DeletedDate
    FROM Airline a

    LEFT JOIN (
        SELECT COUNT(p.Id) as cnt, p.AirlineId FROM Pilot p
        WHERE p.DeletedDate IS NULL
        GROUP BY p.AirlineId
    ) ActivePilots
    on a.Id = ActivePilots.AirlineId

    LEFT JOIN (
        SELECT COUNT(p.Id) as cnt, p.AirlineId FROM Pilot p
        WHERE p.DeletedDate is NOT NULL
        GROUP BY p.AirlineId
    ) InactivePilots
    on a.Id = InactivePilots.AirlineId

    {MainQueryFilter}

    ORDER BY a.CreatedDate DESC
'''


class AirlineRepository(RepositoryBase):

    # query the summary of airlines and their pilot counts
    def QuerySummary(self, airlineId : int | list[int] = None, includeDeleted: bool = False) -> DataFrame:
        qry = airlineBaseQuery

        paramaters = []
        mainQueryFilter = ""
        
        if isinstance(airlineId, int):
            mainQueryFilter += " WHERE a.Id = ?"
            paramaters.append(airlineId)
        elif isinstance(airlineId, list):
            mainQueryFilter += f" WHERE a.Id IN ({','.join(['?'] * len(airlineId))})"
            paramaters.extend(airlineId)

        if not includeDeleted:
            mainQueryFilter += " WHERE a.DeletedDate IS NULL" if mainQueryFilter == ""  else " AND a.DeletedDate IS NULL"
            
        qry = qry.replace("{MainQueryFilter}", mainQueryFilter) 
        return DataFrame(AirlinePilotSummary.Map(QueryResult(qry, *paramaters)), AirlinePilotSummary)


airlineRepository : AirlineRepository = AirlineRepository()