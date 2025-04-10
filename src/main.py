from datetime import datetime
from FlightManagementSoftware.cli.Commands.ViewPilotFlightSchedule import ViewPilotFlightScheduleCommand
from FlightManagementSoftware.cli.Commands.AssignPilotFlight import AssignPilotFlightCommand
from FlightManagementSoftware.cli.Commands.RebuildDatabase import RebuildDatabaseCommand
from FlightManagementSoftware.cli.Commands.ViewPilots import ViewPilotsCommandParser
from FlightManagementSoftware.cli.Commands.ViewFlightSchedule import ViewFlightScheduleCommand
from FlightManagementSoftware.cli.Commands.UpdateFlight import UpdateFlightCommand


def __main__():
    RebuildDatabaseCommand()
    #command = AssignPilotFlightCommand(pilotId=5, flightId=5)
    #command = AssignPilotFlightCommand(pilotId=5, flightId=5, remove=True)

    #command = ViewPilotFlightScheduleCommand(pilotId=1, startDate='1000-01-01 00:00:00')
    # hold the console open
    input()

if __name__ == "__main__" :
    __main__()
