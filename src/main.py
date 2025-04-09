from FlightManagementSoftware.db.sqlite import dbConnectionInstance
from FlightManagementSoftware.cli.Commands.ViewPilots import ViewPilotsCommand
from FlightManagementSoftware.cli.Commands.CreatePilot import CreatePilotCommandParser
from FlightManagementSoftware.cli.clientry import main




def __main__():
    dbConnectionInstance.Init_db(refresh=True)
    command = ViewPilotsCommand(IncludeDeleted=True, SearchName="The forces")
    main()
    input()

if __name__ == "__main__" :
    __main__()
