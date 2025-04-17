from datetime import datetime
from FlightManagementSoftware.repositories.RepositoryBase import RepositoryBase
from FlightManagementSoftware.Entities.QueryResult import QueryResult
from FlightManagementSoftware.DataTransferObjects.DataFrame import DataFrame
from FlightManagementSoftware.Entities.Destination import Destination

destinationBaseQuery = r'''
    SELECT d.* FROM Destination d

    JOIN Country c
        ON c.Id = d.CountryId

    {MainQueryFilter}

    ORDER BY d.CreatedDate ASC
'''

class DestinationRepository(RepositoryBase):

    # Adding in ability to query by a country c
    def QueryDestinations(
            self,
            destinationId : int | list[int] = None,
            countryCode : str | list[str] = None,
            includeInactive : bool = False,
            includeDeleted : bool = False
            ) -> DataFrame:
        qry = destinationBaseQuery

        parameters = []

        mainQueryFilter = ""

        # Apply DestinationId filter
        if destinationId != None:
            mainQueryFilter += " WHERE "
            if isinstance(destinationId, int):
                mainQueryFilter += "d.Id = ?"
                if isinstance(destinationId, int):
                    parameters.append(destinationId)
                else:
                    parameters.append(destinationId[0])
            else:
                mainQueryFilter += f"d.Id in ({','.join(['?'] * len(destinationId))})"
                parameters.extend(destinationId)

        # Apply CountryCode filter
        if countryCode != None:
            mainQueryFilter += " WHERE " if mainQueryFilter == "" else " AND "
            if isinstance(countryCode, str):
                mainQueryFilter += "c.IsoCode = ?"
                if isinstance(countryCode, int):
                    parameters.append(countryCode)
                else:
                    parameters.append(countryCode[0])
            else:
                mainQueryFilter += f"c.IsoCode in ({','.join([['?'] * len(countryCode)])})"
                parameters.extend(countryCode)

        if not includeDeleted:
            mainQueryFilter += " WHERE " if mainQueryFilter == "" else " AND "
            mainQueryFilter += " d.DeletedDate IS NULL " 

        if not includeInactive:
            mainQueryFilter += " WHERE " if mainQueryFilter == "" else " AND "
            mainQueryFilter += " d.Active = 1 " 

        qry = qry.replace("{MainQueryFilter}", mainQueryFilter)

        return DataFrame(Destination.Map(QueryResult(qry, *parameters)), Destination)



destinationRepository : DestinationRepository = DestinationRepository()
