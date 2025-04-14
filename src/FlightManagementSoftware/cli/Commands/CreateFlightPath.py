from dataclasses import dataclass
from datetime import datetime
from FlightManagementSoftware.cli.CommandParser import CommandParser
from FlightManagementSoftware.Entities.FlightPath import FlightPath
from FlightManagementSoftware.Entities.Destination import Destination
from FlightManagementSoftware.cli.CommandHandler import CommandHandler
from FlightManagementSoftware.cli.UserInputHelpers import AbortCommandException



@dataclass
class CreateFlightPathCommand(CommandHandler):
    fromDestinationId : int = None
    fromDestinationAirportCode : str = None
    toDestinationAirportCode : str = None
    toDestinationId : int = None
    active : bool = True
    distanceKm : int = None
    alsoCreateInverse : bool = False


    def Validate(self):
        if (not ((self.fromDestinationId != None) != (self.fromDestinationAirportCode != None)) or
            not ((self.toDestinationId != None) != (self.toDestinationAirportCode != None))):
           raise AbortCommandException(f"You must supply both a from and to destination either as Ids or airportCodes") 

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
        
        self.existingFlightPath : FlightPath = FlightPath.QueryByDestinationId(self.fromDestination.Id, self.toDestination.Id)
        if self.existingFlightPath != None:
            raise AbortCommandException(f"Flight path from {self.fromDestination.Name} to {self.toDestination.Name} already exists")
        
        self.existingInverseFlightPath : FlightPath = FlightPath.QueryByDestinationId(self.toDestination.Id, self.fromDestination.Id)

        if self.existingInverseFlightPath != None and self.existingInverseFlightPath.DistanceKm != self.distanceKm:
            raise AbortCommandException(f"An existing inverse flight path was found with a different distance metric to that supplied")


    def Handle(self):
        flightPath = FlightPath(
            Id=None,
            FromDestinationId=self.fromDestination.Id,
            ToDestinationId=self.toDestination.Id,
            DistanceKm=self.distanceKm,
            Active=self.active,
            CreatedDate=datetime.now(),
            DeletedDate=None
        )
        # infer distance from reverse route if found
        if self.existingFlightPath != None and self.distanceKm == None:
            flightPath.DistanceKm = self.existingFlightPath.DistanceKm

        flightPath.Create()

        if self.alsoCreateInverse == True:
            if self.existingInverseFlightPath != None:
                print(f"The inverse flight path from {self.toDestination.Name} to {self.fromDestination.Name} already exists , skipping")
            else:
                inverseFlightPath = FlightPath(
                    Id=None,
                    FromDestinationId=self.toDestination.Id,
                    ToDestinationId=self.fromDestination.Id,
                    DistanceKm=self.distanceKm,
                    Active=self.active,
                    CreatedDate=datetime.now(),
                    DeletedDate=None
                )
                inverseFlightPath.Create()
                print(f"Created Inverse flight path from {self.toDestination.Name} to {self.fromDestination.Name} with Id : {inverseFlightPath.Id}")
        print(f"Flight path sucessfully created from {self.fromDestination.Name} to {self.toDestination.Name} with Id {flightPath.Id}")


class CreateFlightPathCommandParser(CommandParser):
    def __init__(self):
        super().__init__(CreateFlightPathCommand)


    def BuildCommandArgs(self, parser):
        parser.add_argument('-fId','-fromId',"--fromDestinationId", nargs=None, type=int, help="The Departure destination Id", required=True)
        parser.add_argument('-tId','-toId',"--toDestinationId", nargs=None, type=int, help="The Arrival destination Id", required=True)
        parser.add_argument('-d','-dist','-distance',"--distanceKm", nargs=None, type=int, help="The Distance in Km between thw two destinations", required=True)
        parser.add_argument('-ia','--active', default=True, action='store_false', help="If included will mark the flight path as inactive")
        parser.add_argument('-i','-inv','--alsoCreateInverse', action='store_true', help="If included will create both the desired flight path and its inverse direction")
        parser.set_defaults(command=self.run)
