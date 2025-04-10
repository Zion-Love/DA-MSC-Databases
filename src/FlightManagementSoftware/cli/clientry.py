import argparse
from FlightManagementSoftware.cli.Commands.AssignPilotFlight import AssignPilotFlightCommandParser
from FlightManagementSoftware.cli.Commands.CreatePilot import CreatePilotCommandParser
from FlightManagementSoftware.cli.Commands.RebuildDatabase import RebuildDatabaseCommandParser
#from FlightManagementSoftware.cli.Commands.UpdateFlight import UpdateFlightCommandParser
from FlightManagementSoftware.cli.Commands.ViewPilots import ViewPilotsCommandParser
from FlightManagementSoftware.cli.Commands.ViewPilotFlightSchedule import ViewPilotFlightScheduleCommandParser
from FlightManagementSoftware.cli.Commands.ViewFlightSchedule import ViewFlightScheduleCommandParser

# A map that builds our cli commands with key as the primary argument to execute the command
# each parser will build the commands specific arguments
commandMap = {
    "AssignPilotFlight" : AssignPilotFlightCommandParser,
    "CreatePilot" : CreatePilotCommandParser,
    "RebuildDatabase" : RebuildDatabaseCommandParser,
    "ViewPilots" : ViewPilotsCommandParser,
    "ViewPilotFlightSchedule" : ViewPilotFlightScheduleCommandParser,
    "ViewFlightSchedule" : ViewFlightScheduleCommandParser,
}


def main():
    '''
        This will build all of our sub parsers for each command using the above map

        this tells our python module what arguments it expects to parse from console input
        meaning we can build a library of cli commands with allowed arguments to pass to our handlers
    '''
    programParser = argparse.ArgumentParser(prog="PROG")
    subparsers = programParser.add_subparsers(help='sub-command help')
    commandParsers = {k : v().BuildCommandArgs(subparsers.add_parser(k, help=f"{k} Help")) for k, v in commandMap.items()}
    try:
        args = vars(programParser.parse_args())
        args['command'](**args)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
