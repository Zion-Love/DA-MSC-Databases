from datetime import datetime
from FlightManagementSoftware.repositories.RepositoryBase import RepositoryBase
from FlightManagementSoftware.Entities.QueryResult import QueryResult
from FlightManagementSoftware.DataTransferObjects.DataFrame import DataFrame
from FlightManagementSoftware.DataTransferObjects.FlightHistory import FlightScheduleDto

flightScheduleBaseQuery = r'''
    SELECT f.Id AS FlightId, f.AirplaneId,f.DepartureTimeUTC , f.ArrivalTimeUTC,
        DepartureDestination.Name AS DepartureDestination, ArrivalDestination.Name AS ArrivalDestination,
        f.DeletedDate AS FlightDeletionDate,
        GROUP_CONCAT(p.Id, ', ') AS Pilots
    FROM Flight f

    JOIN FlightPath fp 
        ON f.FlightPathId = fp.Id 
        
    JOIN Destination DepartureDestination
        ON fp.FromDestinationId = DepartureDestination .Id 
        
    JOIN Destination ArrivalDestination 
        ON fp.ToDestinationId = ArrivalDestination.Id 

    LEFT JOIN PilotFlight pf
        on pf.FlightId = f.Id
    LEFT JOIN Pilot p
        on p.Id = pf.PilotId

    {MainQueryFilter}

    GROUP BY f.Id, f.DepartureTimeUTC, f.ArrivalTimeUTC,
        DepartureDestination.Name, ArrivalDestination.Name, f.DeletedDate

    ORDER BY f.DepartureTimeUTC ASC
'''

class FlightRepository(RepositoryBase):

    def QueryFlightSchedule(
            self, 
            pilotId : list[int] | int = None, 
            flightId : list[int] | int = None,
            destinationId : list[int] | int = None,
            startDate : datetime = None,
            endDate : datetime = None,
            includeCompleted : bool = True,
            includeDeleted : bool = False):
        parameters = []
        qry = flightScheduleBaseQuery

        # build our filters
        mainQueryFilter = ""
        if pilotId != None:
            if isinstance(pilotId, list) and len(pilotId) > 1:
                mainQueryFilter += f" WHERE p.Id in ({','.join(['?'] * len(pilotId))})"
                parameters.extend(pilotId)
            elif (isinstance(pilotId, list) and len(pilotId) == 1):
                mainQueryFilter += " WHERE p.Id = ?"
                parameters.append(pilotId[0])
            elif isinstance(pilotId, int):
                mainQueryFilter += " WHERE p.Id = ?"
                parameters.append(pilotId)

        # Append our flight id filter if it is present
        if flightId != None:
            if mainQueryFilter == "":
                mainQueryFilter += "WHERE "
            else:
                mainQueryFilter += " AND "
            if isinstance(flightId, int) or isinstance(flightId, list) and len(flightId) == 1:
                mainQueryFilter += "f.Id = ?"
                parameters.append(flightId) if isinstance(flightId, int) else parameters.append(flightId[0])
            elif (isinstance(flightId, list) and len(flightId) >= 1):
                mainQueryFilter += f"f.Id in ({','.join(['?'] * len(flightId))})"
                parameters.extend(flightId)

        # Apply our destination Id filter to both departure and arrival destinations
        if destinationId != None:
            if mainQueryFilter == "":
                mainQueryFilter += "WHERE "
            else:
                mainQueryFilter += " AND "
            if isinstance(destinationId, int) or (isinstance(destinationId, list) and len(destinationId) == 1):
                mainQueryFilter += "(DepartureDestination.Id = ? OR ArrivalDestination.Id = ?)"
                # adding this value once for each destination
                if isinstance(destinationId, list):
                    parameters.append(destinationId[0])
                    parameters.append(destinationId[0])
                else:
                    parameters.append(destinationId)
                    parameters.append(destinationId)
            elif isinstance(destinationId, list) and len(destinationId) > 1:
                mainQueryFilter += f"""
                  ( DepartureDestination.Id in ({','.join(['?'] * len(destinationId))})
                    OR ArrivalDestination.Id in ({','.join(['?'] * len(destinationId))}) )"""
                parameters.extend(destinationId)
                parameters.extend(destinationId)


        if startDate != None:
            if mainQueryFilter == "":
                mainQueryFilter += "WHERE "
            else:
                mainQueryFilter += " AND "
            mainQueryFilter += "f.DepartureTimeUTC >= ?"
            parameters.append(startDate)

        if endDate != None:
            if mainQueryFilter == "":
                mainQueryFilter += "WHERE "
            else:
                mainQueryFilter += " AND "
            mainQueryFilter += "f.DepartureTimeUTC <= ?"
            parameters.append(startDate)

        if includeDeleted != True:
            if mainQueryFilter != "":
                mainQueryFilter += " AND f.DeletedDate IS NULL"
            else:
                mainQueryFilter += " WHERE f.DeletedDate IS NULL"

        if includeCompleted != True:
            if mainQueryFilter != "":
                mainQueryFilter += " AND f.ArrivalTimeUTC IS NULL"
            else:
                mainQueryFilter += " WHERE f.ArrivalTimeUTC IS NULL"

        qry = qry.replace("{MainQueryFilter}", mainQueryFilter)

        return DataFrame(FlightScheduleDto.Map(QueryResult(qry, *parameters)), FlightScheduleDto)
    

    def QueryAll(self):
        qry = flightScheduleBaseQuery
        qry = qry.replace("{MainQueryFilter}" , "")
        return DataFrame(FlightScheduleDto.Map(QueryResult(qry)), FlightScheduleDto)
    

    def QueryScheduleByFlightPath(self, flightPathId : int | list[int], includeDeleted : bool = False):
        qry = flightScheduleBaseQuery

        parameters = []

        mainQueryFilter = ""
        if isinstance(flightPathId,int):
            mainQueryFilter += "WHERE fp.Id = ?"
            parameters.append(flightPathId)
        elif isinstance(flightPathId, list) and all([isinstance(Id,int) for Id in flightPathId]):
            mainQueryFilter += f"WHERE fp.Id IN ({','.join(['?' * len(flightPathId)])})"
            parameters.extend(flightPathId)

        if not includeDeleted:
            mainQueryFilter += " AND f.DeletionDate IS NULL"

        qry = qry.replace("{MainQueryFilter}", mainQueryFilter)

        return DataFrame(QueryResult(FlightScheduleDto.Map(qry,*parameters)), FlightScheduleDto)


    def QueryByAirplane(self, 
            airplaneId : int | list[int], 
            includeDeleted : bool = False, 
            pendingOnly : bool = False):
        qry = flightScheduleBaseQuery

        parameters = []
        mainQueryFilter = ""

        if isinstance(airplaneId, int):
            mainQueryFilter += " WHERE "

flightRepository : FlightRepository = FlightRepository()