from FlightManagementSoftware.repositories.RepositoryBase import RepositoryBase

airlineBaseQuery = r'''
    SELECT a.Id as AirlineId, a.Name, ActivePilots.cnt as ActivePilots, InactivePilots.cnt as InactivePilots
    FROM Airline a

    LEFT JOIN (
        SELECT COUNT(p.Id) as cnt, p.AirlineId FROM Pilot p
        WHERE p.DeletedDate IS NULL
        GROUP BY p.AirlineId
    ) ActivePilots
    on a.Id = ActivePilots.AirlinesId

    LEFT JOIN (
        SELECT COUNT(p.Id) as cnt, p.AirlineId FROM Pilot p
        WHERE p.DeletedDate is NOT NULL
        GROUP BY p.Airline
    ) InactivePilots
    on a.Id = InactivePilots.AirlinesId


    {MainQueryFilter}

    ORDER BY a.CreatedDate DESC
'''


class AirlineRepository(RepositoryBase):

    def QuerySummary(self, airlineId : int | list[int] = None):
        qry = airlineBaseQuery

        paramaters = []
        mainQueryFilter = ""
        # TODO this and command for it

airlineRepository : AirlineRepository = AirlineRepository()