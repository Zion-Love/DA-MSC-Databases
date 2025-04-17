import argparse
from FlightManagementSoftware.cli.Commands.AssignPilotFlight import AssignPilotFlightCommandParser
from FlightManagementSoftware.cli.Commands.CreateAirline import CreateAirlineCommandParser
from FlightManagementSoftware.cli.Commands.CreateAirplane import CreateAirplaneCommandParser
from FlightManagementSoftware.cli.Commands.CreateCountry import CreateCountryCommandParser
from FlightManagementSoftware.cli.Commands.CreateDestination import CreateDestinationCommandParser
from FlightManagementSoftware.cli.Commands.CreateFlight import CreateFlightCommandParser
from FlightManagementSoftware.cli.Commands.CreateFlightPath import CreateFlightPathCommandParser
from FlightManagementSoftware.cli.Commands.CreatePilot import CreatePilotCommandParser

from FlightManagementSoftware.cli.Commands.DeleteAirline import DeleteAirlineCommandParser
from FlightManagementSoftware.cli.Commands.DeleteAirplane import DeleteAirplaneCommandParser
from FlightManagementSoftware.cli.Commands.DeleteCountry import DeleteCountryCommandParser
from FlightManagementSoftware.cli.Commands.DeleteDestination import DeleteDestinationCommandParser
from FlightManagementSoftware.cli.Commands.DeletePilot import DeletePilotCommandParser
from FlightManagementSoftware.cli.Commands.DeleteFlight import DeleteFlightCommandParser
from FlightManagementSoftware.cli.Commands.DeleteFlightPath import DeleteFlightPathCommandParser

from FlightManagementSoftware.cli.Commands.RebuildDatabase import RebuildDatabaseCommandParser

from FlightManagementSoftware.cli.Commands.UpdateAirplane import UpdateAirplaneCommandParser
from FlightManagementSoftware.cli.Commands.UpdateAirline import UpdateAirlineCommandParser
from FlightManagementSoftware.cli.Commands.UpdateCountry import UpdateCountryCommandParser
from FlightManagementSoftware.cli.Commands.UpdateFlight import UpdateFlightCommandParser
from FlightManagementSoftware.cli.Commands.UpdateFlightPath import UpdateFlightPathCommandParser
from FlightManagementSoftware.cli.Commands.UpdateDestination import UpdateDestinationCommandParser

from FlightManagementSoftware.cli.Commands.ViewAirlines import ViewAirlinesCommandParser
from FlightManagementSoftware.cli.Commands.ViewAirlinePilotSummary import ViewAirlinePilotSummaryCommandParser
from FlightManagementSoftware.cli.Commands.ViewAirplanes import ViewAirplanesCommandParser
from FlightManagementSoftware.cli.Commands.ViewCountries import ViewCountriesCommandParser
from FlightManagementSoftware.cli.Commands.ViewDestinations import ViewDestinationsCommandParser
from FlightManagementSoftware.cli.Commands.ViewPilots import ViewPilotsCommandParser
from FlightManagementSoftware.cli.Commands.ViewPilotFlightSchedule import ViewPilotFlightScheduleCommandParser
from FlightManagementSoftware.cli.Commands.ViewFlightSchedule import ViewFlightScheduleCommandParser
from FlightManagementSoftware.cli.Commands.ViewFlightPaths import ViewFlightPathsCommandParser


# A map that builds our cli commands with key as the primary argument to execute the command
# each parser will build the commands specific arguments
commandMap = {
    "AssignPilotFlight": {
        "parser": AssignPilotFlightCommandParser,
        "help": "Assign a pilot to a flight"
    },
    "CreateAirline": {
        "parser": CreateAirlineCommandParser,
        "help": "Creates a new Airline"
    },
    "CreateAirplane": {
        "parser": CreateAirplaneCommandParser,
        "help": "Create a new Airplane"
    },
    "CreateDestination": {
        "parser": CreateDestinationCommandParser,
        "help": "Create a Destination"
    },
    "CreatePilot": { 
       "parser": CreatePilotCommandParser,
       "help": "Create a new Pilot"
    },
    "CreateCountry": {
        "parser": CreateCountryCommandParser,
        "help": "Create a new Country record"
    },
    "CreateFlight": {
        "parser": CreateFlightCommandParser,
        "help": "Create a Flight"
    },
    "CreateFlightPath": {
        "parser": CreateFlightPathCommandParser,
        "help": "Create a FlightPath"
    },
    "DeleteAirline": {
        "parser": DeleteAirlineCommandParser,
        "help": "Deletes an Airline and unassigns any of their pilots" 
    },
    "DeleteAirplane": {
        "parser": DeleteAirplaneCommandParser,
        "help": "Delete an airplane along with any of its pending flights"
    },
    "DeleteCountry": {
        "parser": DeleteCountryCommandParser,
        "help": "Delete a Country along with any of its destination, flight paths and pending flights"
    },
    "DeleteDestination": {
        "parser": DeleteDestinationCommandParser,
        "help": "Delete a Destination and its assocaited FlightPaths / pending flights"
    },
    "DeleteFlight": {
        "parser": DeleteFlightCommandParser,
        "help": "Delete a Flight"
    },
    "DeletePilot": {
        "parser": DeletePilotCommandParser,
        "help": "Delete a Pilot by their unique Id"
    },
    "DeleteFlightPath": {
        "parser": DeleteFlightPathCommandParser,
        "help": "Deletes a FlightPath"
     },
    "ViewAirlines": {
        "parser": ViewAirlinesCommandParser,
        "help": "View Airlines"
     },
    "ViewAirlinePilotSummary": {
        "parser": ViewAirlinePilotSummaryCommandParser,
        "help": "Views a summary of the Airlines and their Pilot Counts"
     },
    "ViewAirplanes": {
       "parser": ViewAirplanesCommandParser,
       "help": "View Airplanes"  
     },
    "ViewCountries": {
        "parser": ViewCountriesCommandParser,
        "help": "View Countries"
     },
    "ViewPilots": { 
        "parser": ViewPilotsCommandParser,
        "help": "View pilots matching criteria"
    },
    "ViewPilotFlightSchedule": {
        "parser": ViewPilotFlightScheduleCommandParser,
        "help": "View a specific pilot's flight schedule"
    },
    "ViewFlightSchedule": {
        "parser": ViewFlightScheduleCommandParser,
        "help": "View flight schedule matching criteria, aggregates assigned pilotIds into a list"
    },
    "ViewDestinations": {
        "parser": ViewDestinationsCommandParser,
        "help": "View Destinations matching criteria"
    },
    "ViewFlightPaths": {
        "parser": ViewFlightPathsCommandParser,
        "help": "View FlightPaths matching criteria"
    },
    "UpdateCountry": {
        "parser": UpdateCountryCommandParser,
        "help" : "Update a Country"
    },
    "UpdateAirplane": {
        "parser": UpdateAirplaneCommandParser,
        "help": "Update an Airplanes Information"
    },
    "UpdateAirline": {
        "parser": UpdateAirlineCommandParser,
        "help": "Update an Airlines Information"
    },
    "UpdateFlight": {
        "parser": UpdateFlightCommandParser,
        "help": "Update information surrounding a specific Flight"
    },
    "UpdateFlightPath": {
        "parser": UpdateFlightPathCommandParser,
        "help": "Update FlightPath Information"
    },
    "UpdateDestination": {
        "parser": UpdateDestinationCommandParser,
        "help": "Update Information for an existing destination"
    },
    "RebuildDatabase": {
        "parser": RebuildDatabaseCommandParser,
        "help": "Teardown the database and rebuild it using the CreateTestData.sql file"
    },
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


if __name__ == "__main__":
    main()