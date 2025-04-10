from dataclasses import dataclass
from datetime import datetime
from FlightManagementSoftware.cli.InputValidator import (
    AssertDateTimeString,
    AssertDateAIsBeforeDateB
)
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
    flightPathId : int = None # requiring using a specific flight path Id
    airplaneId : int = None
    departureTimeUTC : datetime = None
    arrivalTimeUTC : datetime = None
    undoDeletion : bool = False

    def Validate(self):
        self.existingFlightRecord : Flight = Flight.QueryById(self.flightId)
        self.existingFlightPathRecord : FlightPath = None
        if self.flightPathId != None: 
            self.existingFlightPathRecord = FlightPath.QueryById(self.flightPathId)

            if self.existingFlightPathRecord == None:
                raise AbortCommandException(f"Unrecognized flightPathId : {self.flightPathId}")
            
            if self.existingFlightPathRecord.Active == False:
                raise AbortCommandException(f"Flight path with Id : {self.flightPathId} is currenlty inactive")

        if(self.existingFlightRecord == None):
            raise AbortCommandException(f"Could not find flight with Id : {self.flightId}")
        
        # Validate our flight times make sense
        endArrivalTime = self.existingFlightRecord.ArrivalTimeUTC if self.arrivalTimeUTC == None else self.arrivalTimeUTC
        endDepartureTime = self.existingFlightRecord.DepartureTimeUTC if self.departureTimeUTC == None else self.departureTimeUTC
        if endArrivalTime != None and (endDepartureTime < endArrivalTime):
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
        if self.flightPathId != None:
            self.existingFlightRecord.FlightPathId = self.flightPathId

        self.existingFlightRecord.Update()
        print(f"Successfully Update Flight : {self.existingFlightRecord}")


class UpdateFlightCommandParser(CommandParser):
    def __init__(self):
        super().__init__(UpdateFlightCommand)


    def BuildCommandArgs(self, parser):
        parser.add_argument('-f','--flightId', type=int, nargs=None, help="The flightId to update information for")
        parser.add_argument('-fp','--flightPathId', type=int, nargs=None, help="The flightPathId to set the flight for")
        parser.add_argument('-a','--airplaneId', type=int, nargs=None, help="The flightId to update information for")
        parser.add_argument('-ud', '--undoDeletion', action='store_true', help="Will reverse the deletion of a flight")
        
        parser.add_argument('-d','-dep','-departure','-departureTime','-from','--departureTimeUTC', nargs=None,
            type=lambda x: AssertDateTimeString(x),
            help="The departure time of the flight")
        
        parser.add_argument('-ar','-arrival','-arrivalTime','-to','--arrivalTimeUTC', nargs=None, 
            type=lambda x: AssertDateTimeString(x),
            help="The ArrivalTimeUTC of the flight")
        
        parser.set_defaults(command=self.run)
