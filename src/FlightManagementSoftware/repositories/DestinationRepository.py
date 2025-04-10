from datetime import datetime
from FlightManagementSoftware.repositories.RepositoryBase import RepositoryBase
from FlightManagementSoftware.Entities.QueryResult import QueryResult
from FlightManagementSoftware.DataTransferObjects.DataFrame import DataFrame

destinationBaseQuery = r'''
    SELECT * FROM Destination d

    JOIN Country c
        ON c.Id = d.CountryId

    {MainQueryFilter}

    ORDER BY d.CreatedDate ASC
'''


class DestinationRepository(RepositoryBase):

    def QueryDestination(
            self,
            destinationId : int | list[int] = None,
            countryCode : str | list[str] = None,
            ) -> DataFrame:
        qry = destinationBaseQuery

        mainQueryFilter = ""
        if destinationId != None:
            pass



destinationRepository : DestinationRepository = DestinationRepository()
