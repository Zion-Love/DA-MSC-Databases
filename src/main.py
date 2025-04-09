from FlightManagementSoftware.db.sqlite import dbConnectionInstance
from FlightManagementSoftware.cli.Commands.ViewPilots import ViewPilotsCommandParser
from FlightManagementSoftware.cli.Commands.CreatePilot import CreatePilotCommand
from FlightManagementSoftware.cli.Commands.RebuildDatabase import RebuildDatabaseCommandParser
from FlightManagementSoftware.cli.clientry import main


def __main__():
    command1 = ViewPilotsCommandParser().run()
    command = CreatePilotCommand(name="name", airlineId=1)

    input()

if __name__ == "__main__" :
    __main__()
