import argparse
from Commands.CreatePilot import CreatePilotCommandParser
from Commands.ViewPilots import ViewPilotsCommandParser
from Commands.ViewPilotFlightSchedule import ViewPilotFlightScheduleCommand


commandMap = {
    "ViewPilots" : ViewPilotsCommandParser,
    "CreatePilot" : CreatePilotCommandParser,
    "ViewPilotFlightSchedule" : ViewPilotFlightScheduleCommand
}


def main():
    '''
        This will build all of our sub parsers for each command using the above map
    '''
    programParser = argparse.ArgumentParser(prog="PROG")
    subparsers = programParser.add_subparsers(help='sub-command help')
    commandParsers = {k : v(subparsers.add_parser(k, help=f"{k} Help")) for k, v in commandMap}
    args = vars(programParser.parse_args())
    args.command(args)