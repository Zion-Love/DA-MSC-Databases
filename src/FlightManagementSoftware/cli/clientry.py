import argparse
from FlightManagementSoftware.cli.Commands.CreatePilot import CreatePilotCommandParser
from FlightManagementSoftware.cli.Commands.ViewPilots import ViewPilotsCommandParser
from FlightManagementSoftware.cli.Commands.ViewPilotFlightSchedule import ViewPilotFlightScheduleCommand


commandMap = {
    "ViewPilots" : ViewPilotsCommandParser,
    "CreatePilot" : CreatePilotCommandParser,
    #"ViewPilotFlightSchedule" : ViewPilotFlightScheduleCommand
}


def main():
    '''
        This will build all of our sub parsers for each command using the above map
    '''
    programParser = argparse.ArgumentParser(prog="PROG")
    subparsers = programParser.add_subparsers(help='sub-command help')
    commandParsers = {k : v().BuildCommandArgs(subparsers.add_parser(k, help=f"{k} Help")) for k, v in commandMap.items()}
    try:
        args = vars(programParser.parse_args())
        print(args)
        args['command'](**args)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()
