from dataclasses import dataclass
from datetime import datetime
from FlightManagementSoftware.cli.CommandParser import CommandParser
from FlightManagementSoftware.cli.CommandHandler import CommandHandler
from FlightManagementSoftware.Entities.FlightPath import FlightPath
from FlightManagementSoftware.Entities.Flight import Flight
from FlightManagementSoftware.Entities.Airplane import Airplane
from FlightManagementSoftware.cli.UserInputHelpers import AbortCommandException
from FlightManagementSoftware.cli.InputValidator import AssertDateTimeString


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
            raise AbortCommandException(f"Flight path deleted")
        
        if self.airplaneId != None:
            self.existingAirplane : Airplane = Airplane.QueryById(self.airplaneId)

            if self.existingAirplane.DeletedDate != None:
                raise AbortCommandException("Airplane is deleted")


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
        parser.add_argument('-fp','--flightPathId', type=int, nargs=None, help="The FlightPath Id to create a flight for", required=True)
        
        parser.add_argument('-d','-dt','-departure','--departureTimeUTC', 
            type=lambda x: AssertDateTimeString(x), 
            nargs=None, help="The Departure time of the flight", 
            required=True)
        
        parser.add_argument('-p','-plane','--airplaneId', type=int, nargs=None,help="The AiirplaneId for this flight")
        parser.set_defaults(command=self.run)