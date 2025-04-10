import argparse
from FlightManagementSoftware.cli.Commands.AssignPilotFlight import AssignPilotFlightCommandParser
from FlightManagementSoftware.cli.Commands.CreatePilot import CreatePilotCommandParser
from FlightManagementSoftware.cli.Commands.RebuildDatabase import RebuildDatabaseCommandParser
from FlightManagementSoftware.cli.Commands.UpdateFlight import UpdateFlightCommandParser
from FlightManagementSoftware.cli.Commands.ViewPilots import ViewPilotsCommandParser
from FlightManagementSoftware.cli.Commands.ViewPilotFlightSchedule import ViewPilotFlightScheduleCommandParser
from FlightManagementSoftware.cli.Commands.ViewFlightSchedule import ViewFlightScheduleCommandParser
from FlightManagementSoftware.cli.Commands.DeletePilot import DeletePilotCommandParser
from FlightManagementSoftware.cli.Commands.CreateFlightPath import CreateFlightPathCommandParser

# A map that builds our cli commands with key as the primary argument to execute the command
# each parser will build the commands specific arguments
commandMap = {
    "AssignPilotFlight" : {
        "parser": AssignPilotFlightCommandParser,
        "help": "Assign a pilot to a flight"
    },
    "CreatePilot" : { 
       "parser": CreatePilotCommandParser,
       "help": "Create a new Pilot"
    },
    "RebuildDatabase" : {
        "parser": RebuildDatabaseCommandParser,
        "help": "Teardown the database and rebuild it using the CreateTestData.sql file"
    },
    "ViewPilots" : { 
        "parser": ViewPilotsCommandParser,
        "help": "View pilots matching criteria"
    },
    "ViewPilotFlightSchedule" : {
        "parser": ViewPilotFlightScheduleCommandParser,
        "help": "View a specific pilot's flight schedule"
    },
    "ViewFlightSchedule" : {
        "parser": ViewFlightScheduleCommandParser,
        "help": "View flight schedule matching criteria, aggregates assigned pilotIds into a list"
    },
    "UpdateFlight" : {
        "parser" : UpdateFlightCommandParser,
        "help": "Update information surrounding a specific flight"
    },
    "DeletePilot" : {
        "parser" : DeletePilotCommandParser,
        "help" : "Delete a pilot by their unique Id"
    },
    "CreateFlightPath": {
        "parser" : CreateFlightPathCommandParser,
        "help" : "Create a flight path"
    }
}

# the entry point for out cli application, after installing when entering FlightManagementSoftware into the cmd
# it will call this method and build all of our commands, then using argparse it will execute the desired command
def main():
    '''
        This will build all of our sub parsers for each command using the above map

        this tells our python module what arguments it expects to parse from console input
        meaning we can build a library of cli commands with allowed arguments to pass to our handlers
    '''
    programParser = argparse.ArgumentParser(prog="FlightManagementSoftware")
    subparsers = programParser.add_subparsers(help='sub-command help')
    commandParsers = {k : v['parser']().BuildCommandArgs(subparsers.add_parser(k, help=v['help'])) for k, v in commandMap.items()}
    try:
        args = vars(programParser.parse_args())
        args['command'](**args)
    except Exception as e:
        print(e)
