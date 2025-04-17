from datetime import datetime
from FlightManagementSoftware.cli.Commands.AssignPilotFlight import AssignPilotFlightCommand
from FlightManagementSoftware.cli.Commands.RebuildDatabase import RebuildDatabaseCommand
from FlightManagementSoftware.cli.Commands.UpdateFlight import UpdateFlightCommand
from FlightManagementSoftware.cli.Commands.ViewFlightSchedule import ViewFlightScheduleCommand
from FlightManagementSoftware.cli.Commands.ViewFlightPaths import ViewFlightPathsCommand
from FlightManagementSoftware.cli.Commands.ViewDestinations import ViewDestinationsCommand
from FlightManagementSoftware.cli.Commands.ViewPilots import ViewPilotsCommand
from FlightManagementSoftware.cli.Commands.ViewPilotFlightSchedule import ViewPilotFlightScheduleCommand
from FlightManagementSoftware.cli.Commands.ViewAirlinePilotSummary import ViewAirlinePilotSummaryCommand


from FlightManagementSoftware.cli.Commands.UpdateFlightPath import UpdateFlightPathCommand


from FlightManagementSoftware.cli.UserInputHelpers import AbortCommandException
from FlightManagementSoftware.cli.Commands.DeleteAirplane import DeleteAirplaneCommand



def __main__():

    try:
        RebuildDatabaseCommand()

        # Assigning Pilots to flights
        #command = AssignPilotFlightCommand(pilotId=5, flightId=5)
        #command = AssignPilotFlightCommand(pilotId=5, flightId=5, remove=True)

        # Applying multiple filter criteria through a single command
        #command = ViewFlightScheduleCommand(flightId=[3,5], includeCompleted=True)
        #command = ViewPilotFlightScheduleCommand(pilotId=[1,2])
        #command = ViewFlightPathsCommand(includeDeleted=False,includeInactive=False)
        #command = DeleteAirplaneCommand(airplaneId=2)
        command = ViewAirlinePilotSummaryCommand()
    except AbortCommandException as e:
        print(e)

if __name__ == "__main__" :
    __main__()
6