from dataclasses import dataclass
from FlightManagementSoftware.cli.CommandParser import CommandParser
from FlightManagementSoftware.cli.CommandHandler import CommandHandler
from FlightManagementSoftware.Entities.FlightPath import FlightPath
from FlightManagementSoftware.cli.UserInputHelpers import AbortCommandException
from FlightManagementSoftware.Entities.Destination import Destination

'''
    This command provides a way to update information about a specific flight path
'''

@dataclass
class UpdateFlightPathCommand(CommandHandler):
    flightPathId : int
    fromDestinationId : int = None
    fromDestinationAirportCode : str = None
    toDestinationId : int = None
    toDestinationAirportCode : str = None
    distanceKm : int = None
    setInactive : bool = None
    setActive : bool = None


    def Validate(self):
        if self.setInactive == self.setActive:
            raise AbortCommandException("You cannot supply both setInactive and setActive")

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

        if self.setActive:
            self.existingFlightPath.Active = True
        if self.setInactive:
            self.existingFlightPath.Active = False

        self.existingFlightPath.Update()
        print(f"Succesfully updated flight path : {self.existingFlightPath}")
        


class UpdateFlightPathCommandParser(CommandParser):
    def __init__(self):
        super().__init__(UpdateFlightPathCommand)


    def BuildCommandArgs(self, parser):
        parser.add_argument("-fp","--flightPathId", type=int, nargs=None, help="The Flight Path Id to update date for", required=True)
        parser.add_argument("-f","-from","--fromDestinationId", type=int, help="The Departure destination Id for the FlightPath")
        parser.add_argument("-fc","-fromCode","--fromDestinationAirportCode", type=str, help="The Departure destination Airport Code for the FlightPath")
        parser.add_argument("-t","-to","--toDestinationId", type=int, help="The Arrival Destination Id for the FlightPath")
        parser.add_argument("-tc","-to","--toDestinationAirportCode", type=str, help="The Arrival Destination Airport Code for the FlightPath")
        parser.add_argument("-d","-dist","--distanceKm", type=str, help="The Distance in Km between the two Destinations")
        parser.add_argument("-i","--setInactive", action='store_true', help="Sets the FlightPath to Inactive")
        parser.add_argument("-a","--setActive", action='store_true', help="Sets the FlightPath to Active")
        parser.set_defaults(command=self.run)
