from dataclasses import dataclass
from FlightManagementSoftware.cli.InputValidator import (
    AssertDateTimeString,
    AssertDateAIsBeforeDateB,
    AssertIsPositiveInteger
)
from FlightManagementSoftware.cli.CommandParser import CommandParser
from FlightManagementSoftware.cli.CommandHandler import CommandHandler
from FlightManagementSoftware.Entities.FlightPath import FlightPath
from FlightManagementSoftware.cli.UserInputHelpers import AbortCommandException
from FlightManagementSoftware.cli.UserInputHelpers import ContinueYN
from FlightManagementSoftware.Entities.Destination import Destination

'''
    This command provides a way to update information about a specific flight path

    Intentionally not allowing the editing of the CreatedDate column as this is representative
    of the insertion time of record
'''
@dataclass
class UpdateFlightPathCommand(CommandHandler):
    flightPathId : int
    fromDestinationId : int = None
    fromDestinationAirportCode : str = None
    toDestinationId : int = None
    toDestinationAirportCode : str = None
    distanceKm : int = None
    active : bool = None


    def Validate(self):
        if (not (self.fromDestinationId != None ^ self.fromDestinationAirportCode != None) or
           not (self.toDestinationId != None ^ self.toDestinationAirportCode != None)):
           raise AbortCommandException(f"You must supply both a from and to destination either as Ids or airportCodes") 

        self.existingFlightPath : FlightPath = FlightPath.QueryById(self.flightPathId)

        if self.existingFlightPath == None:
            raise AbortCommandException(f"Flight path with Id {self.fligtPathId} not found")
        
        self.fromDestination : Destination = (
            Destination.QueryById(self.fromDestinationId) if self.fromDestinationId != None 
            else Destination.QueryByAirportCode(self.fromDestinationAirportCode)
        )

        if self.fromDestination == None:
            raise AbortCommandException("Could not find From Destination")

        self.toDestination : Destination = (
            Destination.QueryById(self.toDestinationId) if self.toDestinationId != None 
            else Destination.QueryByAirportCode(self.toDestinationAirportCode)
        )

        if self.toDestination == None:
            raise AbortCommandException("Could not find To Destination")


    def Handle(self):
        pass


class UpdateFlightPathCommandParser(CommandParser):
    def __init__(self):
        super().__init__(UpdateFlightPathCommand)


    # TODO :
    def BuildCommandArgs(self, parser):
        parser.add_argument('-fp',"--flightPathId", type=lambda x: AssertIsPositiveInteger(x), nargs=None, help="The Flight Path Id to update date for", required=True)

        parser.set_defaults(command=self.run)
