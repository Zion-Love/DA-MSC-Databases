from dataclasses import dataclass
from FlightManagementSoftware.cli.UserInputHelpers import ContinueYN, AbortCommandException
from FlightManagementSoftware.cli.CommandHandler import CommandHandler
from FlightManagementSoftware.cli.CommandParser import CommandParser
from FlightManagementSoftware.Entities.FlightPath import FlightPath
from FlightManagementSoftware.Entities.Flight import Flight
from FlightManagementSoftware.Entities.Destination import Destination


'''
    This Command will soft delete a Destination along with any FlightPaths and any Pending Flights
    associated with it
'''

@dataclass
class DeleteDestinationCommand(CommandHandler):
    destinationId : int = None
    airportCode : str = None

    def Validate(self):
        if self.destinationId == None and self.airportCode == None:
            raise AbortCommandException(f"You must supply either the destination Id or the airport code to delete it.")

        self.destination : Destination = (
            Destination.QueryById(self.destinationId) if self.destinationId != None else
            Destination.QueryByAirportCode(self.airportCode)
        )

        if self.destination == None:
            raise (
                AbortCommandException(f"Could not find destination with Id : {self.destinationId}") if self.destinationId != None else
                AbortCommandException(f"Could not find destination with AirportCode : {self.airportCode}")
            )
        
        associatedFlightPaths = FlightPath.QueryByDestinationId(self.destinationId)

        if associatedFlightPaths != None:
            associatedFlights = Flight.QueryByFlightPath([fp.Id for fp in associatedFlightPaths])
            ContinueYN(f"WARNING: Deleting this Destination will also Delete {len(associatedFlightPaths)} FlightPaths and {len(associatedFlights)} Flights, Continue? (y/n)")
            

    def Handle(self):
        self.destination.Delete()
        print("Successfully deleted Destination and accompanying Flights / FlightPaths")


class DeleteDestinationCommandParser(CommandParser):
    def __init__(self):
        super().__init__(DeleteDestinationCommand)

    def BuildCommandArgs(self, parser):
        parser.add_argument("-d","-dest","--destinationId", type=int, help="The Id of the Destination to delete")
        parser.add_argument("-c","-code","--airportCode", type=str, help="The Airport code of the Destination to delete")
        parser.set_defaults(command=self.run)