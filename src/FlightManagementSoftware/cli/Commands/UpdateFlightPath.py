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
        self.existingFlightPath : FlightPath = FlightPath.QueryById(self.flightPathId)
        self.fromDestination = None
        self.toDestination = None

        if self.existingFlightPath == None:
            raise AbortCommandException(f"Flight path with Id {self.fligtPathId} not found")
        
        if self.fromDestinationAirportCode != None or self.fromDestinationId != None:
            self.fromDestination : Destination = (
                Destination.QueryById(self.fromDestinationId) if self.fromDestinationId != None 
                else Destination.QueryByAirportCode(self.fromDestinationAirportCode)
            )

            if self.fromDestination == None:
                raise AbortCommandException("Could not find From Destination")
            
        if self.toDestinationAirportCode == None or self.toDestinationId == None:
            self.toDestination : Destination = (
                Destination.QueryById(self.toDestinationId) if self.toDestinationId != None 
                else Destination.QueryByAirportCode(self.toDestinationAirportCode)
            )

            if self.toDestination == None:
                raise AbortCommandException("Could not find To Destination")


    def Handle(self):
        if self.fromDestination != None:
            self.existingFlightPath.FromDestinationId = self.fromDestination.Id

        if self.toDestination!= None:
            self.existingFlightPath.ToDestinationId = self.toDestination.Id

        if self.distanceKm != None:
            self.existingFlightPath.DistanceKm = self.distanceKm

        if self.active != None:
            self.existingFlightPath.Active = self.active

        self.existingFlightPath.Update()
        print(f"Succesfully updated flight path : {self.existingFlightPath}")
        


class UpdateFlightPathCommandParser(CommandParser):
    def __init__(self):
        super().__init__(UpdateFlightPathCommand)


    # TODO :
    def BuildCommandArgs(self, parser):
        parser.add_argument('-fp',"--flightPathId", type=lambda x: AssertIsPositiveInteger(x), nargs=None, help="The Flight Path Id to update date for", required=True)

        parser.set_defaults(command=self.run)
