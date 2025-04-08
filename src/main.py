from db.sqlite import dbConnectionInstance
import sys
from FlightManagementSoftware.cli.Commands.ViewPilots import ViewPilotsCommand


def __main__():
    print(sys.path)
    dbConnectionInstance.Init_db(refresh=True)
    command = ViewPilotsCommand(IncludeDeleted=True, SearchName="The forces")

    input()

if __name__ == "__main__" :
    __main__()
