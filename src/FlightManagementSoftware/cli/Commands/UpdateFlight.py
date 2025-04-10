from dataclasses import dataclass
from datetime import datetime
from FlightManagementSoftware.cli.CommandParser import CommandParser
from FlightManagementSoftware.cli.CommandHandler import CommandHandler
from FlightManagementSoftware.Entities.Flight import Flight
from FlightManagementSoftware.Entities.FlightPath import FlightPath
from FlightManagementSoftware.cli.UserInputHelpers import AbortCommandException
from FlightManagementSoftware.cli.UserInputHelpers import ContinueYN

'''
    This command provides a way to update information about a specific flight

    Intentionally not allowing the editing of the CreatedDate column as this is representative
    of the isnertion time of record
'''
@dataclass
class UpdateFlightCommand(CommandHandler):
    flightId : int
    flightPathId : int = None
    airplaneId : int = None
    departureTimeUTC : datetime = None
    arrivalTimeUTC : datetime = None
    undoDeletion : bool = False

    def Validate(self):
        self.existingFlightRecord : Flight = Flight.QueryById(self.flightId)
        self.existingFlightPathRecord = None
        if self.FlightPathId != None: 
            self.existingFlightPathRecord = FlightPath.QueryById(self.flightPathId)

            if self.existingFlightPathRecord == None:
                raise AbortCommandException(f"Unrecognized flightPathId : {self.flightPathId}")

        if(self.existingFlightRecord == None):
            raise AbortCommandException(f"Could not find flight with Id : {self.flightId}")
        
        # Validate our flight times make sense
        endArrivalTime = self.existingFlightRecord.ArrivalTimeUTC if self.arrivalTimeUTC == None else self.arrivalTimeUTC
        endDepartureTime = self.existingFlightRecord.DepartureTimeUTC if self.departureTimeUTC == None else self.departureTimeUTC
        if(endDepartureTime < endArrivalTime):
            raise AbortCommandException(f"Cannot have a Departure : {endDepartureTime} time that is before an ArrivalTime : {endArrivalTime}")
        
        if self.existingFlightRecord.ArrivalTimeUTC != None:
            ContinueYN(f"WARNING: Flight already compeleted Arrival at : {self.existingFlightRecord.ArrivalTimeUTC} are you sure you want to update its information ? (y/n)")

        if self.existingFlightRecord.DeletedDate != None and not self.undoDeletion: 
            ContinueYN(f"WARNING: Attempting to update information for a deleted Flight, Continue? (y/n)")

        
    def Handle(self):
        if self.airplaneId != None:
            self.existingFlightRecord.AirplaneId = self.airplaneId
        if self.departureTimeUTC != None:
            self.existingFlightRecord.DepartureTimeUTC = self.departureTimeUTC
        if self.arrivalTimeUTC != None:
            self.existingFlightRecord.ArrivalTimeUTC = self.arrivalTimeUTC
        if self.undoDeletion == True:
            self.existingFlightRecord.DeletedDate = None

        self.existingFlightRecord.Update()
        print(f"Successfully Update Flight : {self.existingFlightRecord}")


class UpdateFlightCommandParser(CommandParser):
    def __init__(self):
        super().__init__(UpdateFlightCommand)


    def BuildCommandArgs(self, parser):
        parser.add_argument('--flightId', type=int, nargs=1, help="The flightId to update information for")
        parser.add_argument('--flightPathId', type=int, nargs=1, help="The flightPathId to set the flight for")
        parser.add_argument('--airplaneId', type=int, nargs=1, help="The flightId to update information for")
        parser.set_defaults(command=self.run)
