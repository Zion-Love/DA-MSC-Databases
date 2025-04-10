from dataclasses import dataclass
from datetime import datetime
from FlightManagementSoftware.cli.CommandParser import CommandParser
from FlightManagementSoftware.cli.CommandHandler import CommandHandler
from FlightManagementSoftware.Entities.FlightPath import FlightPath
from FlightManagementSoftware.Entities.Flight import Flight
from FlightManagementSoftware.cli.UserInputHelpers import AbortCommandException


@dataclass
class CreateFlightCommand(CommandHandler):
    flightPathId : int
    departureTimeUTC : datetime
    airplaneId : int = None

    def Validate(self):
        self.existingFlightPath : FlightPath = FlightPath.QueryById(self.flightPathId)

        if self.existingFlightPath == None:
            raise AbortCommandException(f"Could not find flight path with Id {self.flightPathId}")
        
        if self.existingFlightPath.Active == False:
            raise AbortCommandException(f"Flight path with Id : {self.flightPathId} is not currently active")
        
        if self.existingFlightPath.DeletedDate != None:
            raise AbortCommandException(f"Flight path has been deleted")


    def Handle(self):
        flight : Flight = Flight(
            FlightPathId=self.flightPathId,
            AirplaneId=self.airplaneId,
            DepartureTimeUTC=self.departureTimeUTC,
            CreatedDate=datetime.now()
        )
        flight.Create()
        print(f"Flight successfully created.")


class CreateFlightCommandParser(CommandParser):
    def __init__(self):
        super().__init__(CreateFlightCommand)

    def BuildCommandArgs(self, parser):
        parser.set_defaults(command=self.run)